        .global retCallout
retCallout:
        pusha
        pushf
        call    handleRetCallout
        popf
        popa
        lea     4(%esp),%esp      # adds 4 to esp without modifying eflags
        ret
