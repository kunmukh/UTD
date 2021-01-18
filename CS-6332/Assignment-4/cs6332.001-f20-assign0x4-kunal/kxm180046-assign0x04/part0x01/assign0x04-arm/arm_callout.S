    .global blCallout
blCallout:
    push    {sp,lr}
    push    {r0-r12}
    mrs     r0, cpsr    /* r0 is scratch, temporarily storing cspr */
    push    {r0}
    mov     r0, sp      /* setting the first arg (*SaveRegs) */

    bl handleBlCallout

    pop     {r0}
    msr     cpsr, r0
    pop     {r0-r12}
    add     sp, sp, #4  /* removing $sp from stack */
    pop     {lr}
    sub     lr, lr, #4  /* returning to the original instr, not next */
    mov     pc, lr


    .global bCallout
bCallout:
    push    {sp,lr}
    push    {r0-r12}
    mrs     r0, cpsr    /* r0 is scratch, temporarily storing cspr */
    push    {r0}
    mov     r0, sp      /* setting the first arg (*SaveRegs) */

    bl handleBCallout

    pop     {r0}
    msr     cpsr, r0
    pop     {r0-r12}
    add     sp, sp, #4  /* removing $sp from stack */
    pop     {lr}
    sub     lr, lr, #4  /* returning to the original instr, not next */
    mov     pc, lr


    .global bxCallout
bxCallout:
    push    {sp,lr}
    push    {r0-r12}
    mrs     r0, cpsr    /* r0 is scratch, temporarily storing cspr */
    push    {r0}
    mov     r0, sp      /* setting the first arg (*SaveRegs) */

    bl handleBxCallout

    pop     {r0}
    msr     cpsr, r0
    pop     {r0-r12}
    add     sp, sp, #4  /* removing $sp from stack */
    pop     {lr}
    sub     lr, lr, #4  /* returning to the original instr, not next */
    mov     pc, lr


    .global bgtCallout
bgtCallout:
    push    {sp,lr}
    push    {r0-r12}
    mrs     r0, cpsr    /* r0 is scratch, temporarily storing cspr */
    push    {r0}
    mov     r0, sp      /* setting the first arg (*SaveRegs) */

    bl handleBgtCallout

    pop     {r0}
    msr     cpsr, r0
    pop     {r0-r12}
    add     sp, sp, #4  /* removing $sp from stack */
    pop     {lr}
    sub     lr, lr, #4  /* returning to the original instr, not next */
    mov     pc, lr