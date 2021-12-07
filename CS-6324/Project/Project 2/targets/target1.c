#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void foo(char * arg)
{
	char cmd[16];
	char par[16];
	char * p;

	strcpy(cmd, "ls --color -l ");
	strcpy(par, arg);

	printf("You can use \"%s %s\" to list the files in dir \"%s\"!\n",
														cmd, par, par);

	p = (char*)malloc(strlen(cmd) + strlen(par) + 2);
	strcpy(p, cmd);
	strcat(p, " ");
	strcat(p, par);
	system(p);
}	

int main(int argc, char ** argv)
{
	if (argc > 1)
		foo(argv[1]);
	else
		printf("usage: %s dir\n", argv[0]);
	return 0;
}

