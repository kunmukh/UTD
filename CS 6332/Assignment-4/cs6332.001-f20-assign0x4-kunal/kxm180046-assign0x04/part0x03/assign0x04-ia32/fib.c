//
// Created by Kangkook Jee on 10/15/20.
//

/*********************************************************************
 *
 *  fibonacci function.
 *
 *   This is the target program to be profiled.
 *
 *********************************************************************/

#include <stdio.h>

int user_prog(int i) __attribute__((alias("fib")));

int fib(int i) 
{
    if (i <= 1) {
        return 1;
    }

    return fib(i-1) + fib(i-2);
}

