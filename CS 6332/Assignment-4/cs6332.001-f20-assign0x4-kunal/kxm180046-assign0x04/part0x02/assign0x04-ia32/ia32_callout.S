
    .global jccCallout
jccCallout:
    pusha
    pushf
    call  handleJccCallout
    popf
    popa
    ret

    .global jmpCallout
jmpCallout:
    pusha
    pushf
    call  handleJmpCallout
    popf
    popa
    ret

    .global callCallout
callCallout:
    pusha
    pushf
    call  handleCallCallout
    popf
    popa            
    jmp   *callTarget

    .global retCallout
retCallout:
    pusha
    pushf
    call  handleRetCallout
    popf
    popa
    lea   4(%esp),%esp   # adds 4 to esp without modifying eflags
    ret
