#!python
"""
BitGenerator base class and SeedSequence used to seed the BitGenerators.

SeedSequence is derived from Melissa E. O'Neill's C++11 `std::seed_seq`
implementation, as it has a lot of nice properties that we want.

https://gist.github.com/imneme/540829265469e673d045
https://www.pcg-random.org/posts/developing-a-seed_seq-alternative.html

The MIT License (MIT)

Copyright (c) 2015 Melissa E. O'Neill
Copyright (c) 2019 NumPy Developers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import abc
from itertools import cycle
import re

try:
    from secrets import randbits
except ImportError:
    # secrets unavailable on python 3.5 and before
    from random import SystemRandom
    randbits = SystemRandom().getrandbits

import numpy as np

cimport numpy as np
from libc.stdint cimport uint32_t

__all__ = ["SeedSequence", "SeedlessSeedSequence", "ISeedSequence",
           "ISpawnableSeedSequence"]

np.import_array()

DECIMAL_RE = re.compile(r"[0-9]+")

cdef int DEFAULT_POOL_SIZE = 4  # Appears also in docstring for pool_size
cdef uint32_t INIT_A = 0x43b0d7e5
cdef uint32_t MULT_A = 0x931e8875
cdef uint32_t INIT_B = 0x8b51f9dd
cdef uint32_t MULT_B = 0x58f38ded
cdef uint32_t MIX_MULT_L = 0xca01f9dd
cdef uint32_t MIX_MULT_R = 0x4973f715
cdef uint32_t XSHIFT = np.dtype(np.uint32).itemsize * 8 // 2
cdef uint32_t MASK32 = 0xFFFFFFFF


def _int_to_uint32_array(n):
    arr = []
    if n < 0:
        raise ValueError("expected non-negative integer")
    if n == 0:
        arr.append(np.uint32(n))
    if isinstance(n, np.unsignedinteger):
        # Cannot do n & MASK32, convert to python int
        n = int(n)
    while n > 0:
        arr.append(np.uint32(n & MASK32))
        n //= (2**32)
    return np.array(arr, dtype=np.uint32)


def _coerce_to_uint32_array(x):
    """ Coerce an input to a uint32 array.

    If a `uint32` array, pass it through directly.
    If a non-negative integer, then break it up into `uint32` words, lowest
    bits first.
    If a string starting with "0x", then interpret as a hex integer, as above.
    If a string of decimal digits, interpret as a decimal integer, as above.
    If a sequence of ints or strings, interpret each element as above and
    concatenate.

    Note that the handling of `int64` or `uint64` arrays are not just
    straightforward views as `uint32` arrays. If an element is small enough to
    fit into a `uint32`, then it will only take up one `uint32` element in the
    output. This is to make sure that the interpretation of a sequence of
    integers is the same regardless of numpy's default integer type, which
    differs on different platforms.

    Parameters
    ----------
    x : int, str, sequence of int or str

    Returns
    -------
    seed_array : uint32 array

    Examples
    --------
    >>> import numpy as np
    >>> from randomgen.seed_sequence import _coerce_to_uint32_array
    >>> _coerce_to_uint32_array(12345)
    array([12345], dtype=uint32)
    >>> _coerce_to_uint32_array("12345")
    array([12345], dtype=uint32)
    >>> _coerce_to_uint32_array("0x12345")
    array([74565], dtype=uint32)
    >>> _coerce_to_uint32_array([12345, "67890"])
    array([12345, 67890], dtype=uint32)
    >>> _coerce_to_uint32_array(np.array([12345, 67890], dtype=np.uint32))
    array([12345, 67890], dtype=uint32)
    >>> _coerce_to_uint32_array(np.array([12345, 67890], dtype=np.int64))
    array([12345, 67890], dtype=uint32)
    >>> _coerce_to_uint32_array([12345, 0x10deadbeef, 67890, 0xdeadbeef])
    array([     12345, 3735928559,         16,      67890, 3735928559],
          dtype=uint32)
    >>> _coerce_to_uint32_array(1234567890123456789012345678901234567890)
    array([3460238034, 2898026390, 3235640248, 2697535605,          3],
          dtype=uint32)
    """
    if isinstance(x, np.ndarray) and x.dtype == np.dtype(np.uint32):
        return x.copy()
    elif isinstance(x, str):
        if x.startswith("0x"):
            x = int(x, base=16)
        elif DECIMAL_RE.match(x):
            x = int(x)
        else:
            raise ValueError("unrecognized seed string")
    if isinstance(x, (int, np.integer)):
        return _int_to_uint32_array(x)
    elif isinstance(x, (float, np.inexact)):
        raise TypeError("seed must be integer")
    else:
        if len(x) == 0:
            return np.array([], dtype=np.uint32)
        # Should be a sequence of interpretable-as-ints. Convert each one to
        # a uint32 array and concatenate.
        subseqs = [_coerce_to_uint32_array(v) for v in x]
        return np.concatenate(subseqs)


cdef uint32_t hashmix(uint32_t value, uint32_t *hash_const):
    # We are modifying the multiplier as we go along, so it is input-output
    value ^= hash_const[0]
    hash_const[0] *= MULT_A
    value *= hash_const[0]
    value ^= value >> XSHIFT
    return value

cdef uint32_t mix(uint32_t x, uint32_t y):
    cdef uint32_t result = (MIX_MULT_L * x - MIX_MULT_R * y)
    result ^= result >> XSHIFT
    return result


class ISeedSequence(metaclass=abc.ABCMeta):
    """
    Abstract base class for seed sequences.

    ``BitGenerator`` implementations should treat any object that adheres to
    this interface as a seed sequence.

    See Also
    --------
    SeedSequence, SeedlessSeedSequence
    """

    @abc.abstractmethod
    def generate_state(self, n_words, dtype=np.uint32):
        """
        generate_state(n_words, dtype=np.uint32)

        Return the requested number of words for PRNG seeding.

        A BitGenerator should call this method in its constructor with
        an appropriate `n_words` parameter to properly seed itself.

        Parameters
        ----------
        n_words : int
            Number of 32- or 64-bit words to generate.
        dtype : np.uint32 or np.uint64, optional
            The size of each word. This should only be either `uint32` or
            `uint64`. Strings (`"uint32"`, `"uint64"`) are fine. Note that
            requesting `uint64` will draw twice as many bits as `uint32` for
            the same `n_words`. This is a convenience for `BitGenerator`s that
            express their states as `uint64` arrays.

        Returns
        -------
        state : uint32 or uint64 array
            Array with shape (n_words,)
        """


class ISpawnableSeedSequence(ISeedSequence):
    """w
    Abstract base class for seed sequences that can spawn.
    """

    @abc.abstractmethod
    def spawn(self, n_children):
        """
        spawn(n_children)

        Spawn a number of child `SeedSequence` s by extending the
        `spawn_key`.

        Parameters
        ----------
        n_children : int

        Returns
        -------
        seqs : list of `SeedSequence` s
        """


cdef class SeedlessSeedSequence(object):
    """
    A seed sequence for BitGenerators with no need for seed state.

    See Also
    --------
    SeedSequence, ISeedSequence
    """

    def generate_state(self, n_words, dtype=np.uint32):
        raise NotImplementedError("seedless SeedSequences cannot generate state")

    def spawn(self, n_children):
        return [self] * n_children


cdef class SeedSequence(object):
    """
    SeedSequence(entropy=None, *, spawn_key=(), pool_size=4, n_children_spawned=0)

    SeedSequence mixes sources of entropy in a reproducible way to set the
    initial state for independent and very probably non-overlapping
    BitGenerators.

    Once the SeedSequence is instantiated, you can call the `generate_state`
    method to get an appropriately sized seed. Calling `spawn(n) <spawn>` will
    create ``n`` SeedSequences that can be used to seed independent
    BitGenerators, i.e. for different threads.

    Parameters
    ----------
    entropy : {None, int, sequence[int]}, optional
        The entropy for creating a `SeedSequence`.
    spawn_key : {(), sequence[int]}, optional
        A third source of entropy, used internally when calling
        `SeedSequence.spawn`
    pool_size : {int}, optional
        Size of the pooled entropy to store. Default is 4 to give a 128-bit
        entropy pool. 8 (for 256 bits) is another reasonable choice if working
        with larger PRNGs, but there is very little to be gained by selecting
        another value.
    n_children_spawned : {int}, optional
        The number of children already spawned. Only pass this if
        reconstructing a `SeedSequence` from a serialized form.

    Notes
    -----

    Best practice for achieving reproducible bit streams is to use
    the default ``None`` for the initial entropy, and then use
    `SeedSequence.entropy` to log/pickle the `entropy` for reproducibility:

    >>> sq1 = np.random.SeedSequence()
    >>> sq1.entropy
    243799254704924441050048792905230269161  # random
    >>> sq2 = np.random.SeedSequence(sq1.entropy)
    >>> np.all(sq1.generate_state(10) == sq2.generate_state(10))
    True
    """

    def __init__(self, entropy=None, *, spawn_key=(),
                 pool_size=DEFAULT_POOL_SIZE, n_children_spawned=0):
        if pool_size < DEFAULT_POOL_SIZE:
            raise ValueError("The size of the entropy pool should be at least "
                             "{0}".format(DEFAULT_POOL_SIZE))
        if entropy is None:
            entropy = randbits(pool_size * 32)
        elif not isinstance(entropy, (int, np.integer, list, tuple, range,
                                      np.ndarray, str)):
            raise TypeError("SeedSequence expects int or sequence of ints for "
                            "entropy not {}".format(entropy))
        self.entropy = entropy
        self.spawn_key = tuple(spawn_key)
        self.pool_size = pool_size
        self.n_children_spawned = n_children_spawned

        self.pool = np.zeros(pool_size, dtype=np.uint32)
        self.mix_entropy(self.pool, self.get_assembled_entropy())

    def __repr__(self):
        lines = [
            "{0}(".format(type(self).__name__),
            "    entropy={0},".format(self.entropy),
        ]
        # Omit some entries if they are left as the defaults in order to
        # simplify things.
        if self.spawn_key:
            lines.append("    spawn_key={0},".format(self.spawn_key))
        if self.pool_size != DEFAULT_POOL_SIZE:
            lines.append("    pool_size={0},".format(self.pool_size))
        if self.n_children_spawned != 0:
            n_child = self.n_children_spawned
            lines.append("    n_children_spawned={0},".format(n_child))
        lines.append(")")
        text = "\n".join(lines)
        return text

    @property
    def state(self):
        """Get the state of the SeedSequence"""
        return {k: getattr(self, k) for k in
                ["entropy", "spawn_key", "pool_size",
                 "n_children_spawned"]
                if getattr(self, k) is not None}

    cdef mix_entropy(self, np.ndarray[np.npy_uint32, ndim=1] mixer,
                     np.ndarray[np.npy_uint32, ndim=1] entropy_array):
        """
        Mix in the given entropy to mixer.

        Parameters
        ----------
        mixer : 1D uint32 array, modified in-place
        entropy_array : 1D uint32 array
        """
        cdef uint32_t hash_const[1]
        hash_const[0] = INIT_A

        # Add in the entropy up to the pool size.
        for i in range(len(mixer)):
            if i < len(entropy_array):
                mixer[i] = hashmix(entropy_array[i], hash_const)
            else:
                # Our pool size is bigger than our entropy, so just keep
                # running the hash out.
                mixer[i] = hashmix(0, hash_const)

        # Mix all bits together so late bits can affect earlier bits.
        for i_src in range(len(mixer)):
            for i_dst in range(len(mixer)):
                if i_src != i_dst:
                    mixer[i_dst] = mix(mixer[i_dst],
                                       hashmix(mixer[i_src], hash_const))

        # Add any remaining entropy, mixing each new entropy word with each
        # pool word.
        for i_src in range(len(mixer), len(entropy_array)):
            for i_dst in range(len(mixer)):
                mixer[i_dst] = mix(mixer[i_dst],
                                   hashmix(entropy_array[i_src], hash_const))

    cdef get_assembled_entropy(self):
        """
        Convert and assemble all entropy sources into a uniform uint32 array.

        Returns
        -------
        entropy_array : 1D uint32 array
        """
        # Convert run-entropy and the spawn key into uint32
        # arrays and concatenate them.

        # We MUST have at least some run-entropy. The others are optional.
        assert self.entropy is not None
        run_entropy = _coerce_to_uint32_array(self.entropy)
        spawn_entropy = _coerce_to_uint32_array(self.spawn_key)
        if len(spawn_entropy) > 0 and len(run_entropy) < self.pool_size:
            # Explicitly fill out the entropy with 0s to the pool size to avoid
            # conflict with spawn keys. We changed this in 1.19.0 to fix
            # gh-16539. In order to preserve stream-compatibility with
            # unspawned SeedSequences with small entropy inputs, we only do
            # this when a spawn_key is specified.
            diff = self.pool_size - len(run_entropy)
            run_entropy = np.concatenate(
                [run_entropy, np.zeros(diff, dtype=np.uint32)])
        entropy_array = np.concatenate([run_entropy, spawn_entropy])
        return entropy_array

    def generate_state(self, n_words, dtype=np.uint32):
        """
        generate_state(n_words, dtype=np.uint32)

        Return the requested number of words for PRNG seeding.

        A BitGenerator should call this method in its constructor with
        an appropriate `n_words` parameter to properly seed itself.

        Parameters
        ----------
        n_words : int
        dtype : np.uint32 or np.uint64, optional
            The size of each word. This should only be either `uint32` or
            `uint64`. Strings (`"uint32"`, `"uint64"`) are fine. Note that
            requesting `uint64` will draw twice as many bits as `uint32` for
            the same `n_words`. This is a convenience for `BitGenerator`s that
            express their states as `uint64` arrays.

        Returns
        -------
        state : {array_like[uint32], array_like[uint64]}, shape=(n_words,)
        """
        cdef uint32_t hash_const = INIT_B
        cdef uint32_t data_val
        with np.errstate(over="ignore"):
            out_dtype = np.dtype(dtype)
            if out_dtype == np.dtype(np.uint32):
                pass
            elif out_dtype == np.dtype(np.uint64):
                n_words *= 2
            else:
                raise ValueError("only support uint32 or uint64")
            state = np.zeros(n_words, dtype=np.uint32)
            src_cycle = cycle(self.pool)
            for i_dst in range(n_words):
                data_val = next(src_cycle)
                data_val ^= hash_const
                hash_const *= MULT_B
                data_val *= hash_const
                data_val ^= data_val >> XSHIFT
                state[i_dst] = data_val
            if out_dtype == np.dtype(np.uint64):
                # For consistency across different endiannesses, view first as
                # little-endian then convert the values to the native endianness.
                state = state.astype("<u4").view("<u8").astype(np.uint64)
        return state

    def spawn(self, n_children):
        """
        spawn(n_children)

        Spawn a number of child `SeedSequence` instances by extending the
        `spawn_key`.

        Parameters
        ----------
        n_children : int
            Number of child SeedSequences to create from the current instance

        Returns
        -------
        seqs :  list[SeedSequence]
            Child SeedSequences with incremented  ``spawn_key``
        """
        cdef int i

        seqs = []
        for i in range(self.n_children_spawned,
                       self.n_children_spawned + n_children):
            seqs.append(type(self)(
                self.entropy,
                spawn_key=self.spawn_key + (i,),
                pool_size=self.pool_size,
            ))
        self.n_children_spawned += n_children
        return seqs

# We cannot directly subclass a `cdef class` type from an `ABC` in Cython, so
# we must register it after the fact.
ISpawnableSeedSequence.register(SeedlessSeedSequence)
ISpawnableSeedSequence.register(SeedSequence)
