#ifndef _RANDOMDGEN__XOSHIRO512_H_
#define _RANDOMDGEN__XOSHIRO512_H_

#include "../common/randomgen_config.h"

typedef struct XOSHIRO512_STATE_T
{
	uint64_t s[8];
	int has_uint32;
	uint32_t uinteger;
} xoshiro512_state_t;

static INLINE uint64_t rotl(const uint64_t x, int k)
{
	return (x << k) | (x >> (64 - k));
}

static INLINE uint64_t xoshiro512_next(uint64_t *s)
{
	const uint64_t result_starstar = rotl(s[1] * 5, 7) * 9;

	const uint64_t t = s[1] << 11;

	s[2] ^= s[0];
	s[5] ^= s[1];
	s[1] ^= s[2];
	s[7] ^= s[3];
	s[3] ^= s[4];
	s[4] ^= s[5];
	s[0] ^= s[6];
	s[6] ^= s[7];

	s[6] ^= t;

	s[7] = rotl(s[7], 21);

	return result_starstar;
}

static INLINE uint64_t
xoshiro512_next64(xoshiro512_state_t *state)
{
	return xoshiro512_next(&state->s[0]);
}

static INLINE uint32_t
xoshiro512_next32(xoshiro512_state_t *state)
{
	uint64_t next;
	if (state->has_uint32)
	{
		state->has_uint32 = 0;
		return state->uinteger;
	}
	next = xoshiro512_next(&state->s[0]);
	state->has_uint32 = 1;
	state->uinteger = (uint32_t)(next >> 32);
	return (uint32_t)(next & 0xffffffff);
}

void xoshiro512_jump(xoshiro512_state_t *state);

#endif
