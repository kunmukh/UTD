//
// Created by Kangkook Jee on 10/15/20.
//
#ifndef CS6332_001_F20_ASSIGN0X4_ARM_DISASM_H
#define CS6332_001_F20_ASSIGN0X4_ARM_DISASM_H

#include <stdint.h>

#define ARM_BL      0xeb
#define ARM_B       0xea
#define ARM_BGT     0xca
//Kunal
#define ARM_BX_1_BYTE     0xe1
#define ARM_BX_INST 0xe12fff1e


// ARM conditional prefix, just necessary parts.
// ....
#define ARM_COND_GT 0xc
#define ARM_COND_LE 0xd
#define ARM_COND_AL 0xe


// [NEED_TO_IMPLEMENT]: IS_ARM_B, IS_ARM_BL, IS_ARM_BX
// we only need to look into 30th, 29th bytes of each instruction.
#define IS_ARM_B(_XX) (_XX==ARM_B) // 1010 b
#define IS_ARM_BL(_XX) (_XX==ARM_BL)  // 1011 b // FIX
#define IS_ARM_BGT(_XX) (_XX==ARM_BGT)  // 0000 b
#define IS_ARM_BX(_XX) (_XX==ARM_BX_1_BYTE)  // 0000 b

typedef struct {
    uint8_t     cond;
    uint16_t     opcode; // a single byte is enough to indentify opcode.
    uint8_t     len;
} ARMInstr;

// [NEED_TO_IMPLEMENT]: IS_ARM_CFLOW
#define IS_ARM_CFLOW(_XX)  ((IS_ARM_B(_XX) ) || (IS_ARM_BL(_XX)) || (IS_ARM_BGT(_XX)))


#endif   // CS6332_001_F20_ASSIGN0X4_ARM_DISASM_H
