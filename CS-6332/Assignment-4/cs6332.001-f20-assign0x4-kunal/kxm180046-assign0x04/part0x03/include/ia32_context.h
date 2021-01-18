//
// Created by Kangkook Jee on 10/15/20.
//

#ifndef CS6332_001_F20_ASSIGN0X3_IA32_CONTEXT_H
#define CS6332_001_F20_ASSIGN0X3_IA32_CONTEXT_H

/*********************************************************************
 *
 *  IA32Instr
 *
 *   Program registers saved on a callout. These must be restored
 *   when we return to the program.
 *
 *     pc - this is the return address of the callout
 *     retPC - this is only valid if the callout replaced a RET
 *             instruction. This will be the return PC the ret
 *             will jump to.
 *
 *********************************************************************/

typedef struct {
   uint32_t   eflags;
   uint32_t   edi;
   uint32_t   esi;
   uint32_t   ebp;
   uint32_t   esp;
   uint32_t   ebx;
   uint32_t   edx;
   uint32_t   ecx;
   uint32_t   eax;
   void      *pc;
   void      *retPC;
} SaveRegs;

#endif
