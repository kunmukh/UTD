Kunal Mukherjee
CS 6378
Project 1
Dr. Ravi Prakash

Step 1: Infrastructure Setup

Step 1a: open a terminal, terminal1

Step 1b: copy kxm180046_p2.zip to <netid>@dc01.utdallas.edu:/<some>/<dir>/

Step 1c: in terminal1, ssh onto <netid>@dc01.utdallas.edu

Step 1d: change directory to /<some>/<dir>/ in terminal1

Step 1e: unzip kxm180046_p2.zip

Step 1f: change directory to /<some>/<dir>/kxm180046_p2/

Step 1g: run command in terminal1: `make clean`

Step 1h: run command in terminal1: `make`

Step 1i: in terminal1, check the directory /<some>/<dir>/kxm180046_p2/ and it will show THREE dir: {0,1,2}


Step 3: simulation's server client assignment [dc01, dc02, dc03: server, dc04, dc05, dc06, dc07, dc08: client]


Step 4: server setup

Step 4a: open another terminal and ssh onto <netid>@dc0{1,2,3}.utdallas.edu

Step 4b: change directory to /<some>/<dir>/kxm180046_p2/ in terminal

Step 4c: in terminal, type `./server`

Step 4d: in terminal, type `0` [0: dc01, 1: dc02, 2: dc03]

Step 4d-note: Note the server IP displayed

Step 4e: in terminal, type `6060`

Step 4f: in terminal, neighbour_server_ip_1 neighbour_server_port_1

Step 4g: in terminal, neighbour_server_ip_2 neighbour_server_port_2

Step 4h: SERVER setup done


Step 5: client setup

Step 5a: open another terminal and ssh onto <netid>@dc0{4,5,6,7,8}.utdallas.edu

Step 5b: change directory to /<some>/<dir>/kxm180046_p2/ in terminal

Step 5c: in terminal, type `./client`

Step 5d: in terminal, type `6060`

Step 5e: in terminal, type `0` [0: dc04, 1: dc05, 2: dc06, 3: dc07, 4: dc08]

Step 5f: in terminal, neighbour_server_ip_1 neighbour_server_port_1

Step 5g: in terminal, neighbour_server_ip_2 neighbour_server_port_2

Step 5h: in terminal, neighbour_server_ip_3 neighbour_server_port_3

Step 5i: CLIENT setup done



Step 6: Simulation will start as soon as you enter `E` in client


Step 7: checking result

STEP 7a: in any of the client terminal, check that how there EXISTS THREE directory `/<some>/<dir>/kxm180046_p2/{0,1,2}` and it contains THREE files, `T1.txt` , `T2.txt`, and `T3.txt`.

Step 7b: in any of the client terminal type `diff /<some>/<dir>/kxm180046_p2/0 /<some>/<dir>/kxm180046_p2/1` and you will see that there is NO OUTPUT, thus proving that `0` and `1` are the same directory and they contain the same contents

Step 7c: in any of the client terminal type `diff /<some>/<dir>/kxm180046_p2/0 /<some>/<dir>/kxm180046_p2/2` and you will see that there is NO OUTPUT, thus proving that `0` and `2` are the same directory and they contain the same contents