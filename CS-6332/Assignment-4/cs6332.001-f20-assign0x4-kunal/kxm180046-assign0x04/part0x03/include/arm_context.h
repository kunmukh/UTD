//
// Created by Kangkook Jee on 10/15/20.
//

#ifndef CS6332_001_F20_ASSIGN0X3_ARM_CONTEXT_H
#define CS6332_001_F20_ASSIGN0X3_ARM_CONTEXT_H

#include <stdint.h>

typedef struct {
    uint32_t   CPSR;
    uint32_t   r[13];
    uint32_t   sp;
    uint32_t   lr;
    uint8_t    *retPC;
} SaveRegs;
#endif
