//
// Created by Kangkook Jee on 10/15/20.
//
#ifndef CS6332_001_F20_ASSIGN0X4_ARM_DISASM_H
#define CS6332_001_F20_ASSIGN0X4_ARM_DISASM_H

#include <stdint.h>

#define ARM_BL      0xeb
#define ARM_B       0xea
#define ARM_BGT     0xca

typedef struct {
    uint16_t opcode;
    uint8_t len;
} ARMInstr;

// #define IS_ARM_CFLOW(_XX) (_XX == ARM_BL || _XX == ARM_B || _XX == ARM_BX || _XX == ARM_BGT)
#endif
