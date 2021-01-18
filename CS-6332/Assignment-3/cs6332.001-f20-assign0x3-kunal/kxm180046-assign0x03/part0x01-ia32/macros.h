//
// Created by Kangkook Jee on 10/15/20.
//

#ifndef CS6332_001_F20_ASSIGN0X3_MACROS_H
#define CS6332_001_F20_ASSIGN0X3_MACROS_H

#include <assert.h>
#include <stdint.h>

#define ASSERT              assert
#define NOT_REACHED()       assert(0)
#define NOT_IMPLEMENTED()   assert(0)
#define DPRINT              printf

#define BIT(_v, _b)         (((_v) >> (_b)) & 0x1)
#define BITS(_v, _l, _h)    (((uint32_t)(_v) << (31-(_h))) >> ((_l)+31-(_h)))

#endif //CS6332_001_F20_ASSIGN0X3_MACROS_H
