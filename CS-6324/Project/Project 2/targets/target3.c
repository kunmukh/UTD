#include <stdio.h>
#include <string.h>
#include <stdlib.h> 
#include <unistd.h>
#include <time.h>
#include <ctype.h>

char *signatures[] = {"sys_open_ports", "sys_module", "write_binaries"};

int is_virus(int argc, char ** argv)
{
        char traffic[64];
        int i, j, len;

        traffic[0] = 0;
        for (i = 1; i < argc; ++i)
                strcat(traffic, argv[i]);

        for (j = 0; j < 3; ++j) {
                len = strlen(signatures[j]);
                for (i = 0; i < (int)strlen(traffic); ++i)
                        if (strncmp(signatures[j], traffic+i, len) == 0)
                                return 1;
        }

        return 0;
}

int main(int argc, char ** argv)
{
        if (argc < 2) {
                system("echo 'usage: target3 network_traffic_packets'");
                exit(1);
        }

        if (is_virus(argc, argv))
                printf("Alarm! virus founded\n");
        else
                printf("safe.\n");

        return 0;
}
