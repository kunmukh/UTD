Kunal Mukherjee
CS 6378
Project 1
Dr. Ravi Prakash

Step 1: Infrastructure Setup

Step 1a: open a terminal, terminal1

Step 1b: copy kxm180046_p1.zip to <netid>@dc01.utdallas.edu:/<some>/<dir>/

Step 1c: in terminal1, ssh onto <netid>@dc01.utdallas.edu

Step 1d: change directory to /<some>/<dir>/ in terminal1

Step 1e: unzip kxm180046_p1.zip

Step 1f: change directory to /<some>/<dir>/kxm180046_p1/

Step 1g: run command in terminal1: `make clean`

Step 1h: run command in terminal1: `make`

Step 1i: in terminal1, check the directory /<some>/<dir>/kxm180046_p1/ and it will show that `D1copy` DOESNOT EXISTS

Step 1j: in terminal1, check directory /<some>/<dir>/kxm180046_p1/D1/ to show that it contains two files `F1.txt` and `F2.txt` which will be used in this demonstration


Step 2a: open another terminal, terminal2, and ssh onto <netid>@dc02.utdallas.edu

Step 2b: change directory to /<some>/<dir>/kxm180046_p1/ in terminal2


Step 3: simulation's server client assignment [dc01: server, dc02: client]


Step 4: server setup

Step 4a: in terminal1, type `./driver`

Step 4b: in terminal1, type `a`

Step 4c: in terminal1, type `8080`


Step 5: client setup

Step 5a: in terminal2, type `./driver`

Step 5b: in terminal2, type `b`

Step 5c: in terminal2, type `8080`


Step 6: Simulation will start as soon as you enter server's IP and Port in terminal2

Step 6a: in terinal2, type `10.176.69.32 8080` (IP and PORT of server)

Step 6b: wait for client to finish working(about 30 sec).


Step 7: checking result

STEP 7a: in terminal2, check that how there EXISTS a directory `/<some>/<dir>/kxm180046_p1/D1copy` and it contains two files, `F1.txt` and `F2.txt`.

Step 7b: in terminal2 type `diff /<some>/<dir>/kxm180046_p1/D1 /<some>/<dir>/kxm180046_p1/D1copy` and you will see that there is NO OUTPUT, thus proving that `D1` and `D1copy` are the same directory and they contain the same contents