Kunal Mukherjee
7/26/20
CS 6390
Dr. Ravi Prakash
Project 2 README

A>---Running PROJECT 2----<

    0> transfer P2.zip from local directory to a dir in dcXX machines

    1> ssh into 7 machines e.g. dc01, dc02, dc03, dc04, dc05, dc06, dc07
    `ssh kxm180046@dc01.utdallas.edu`

    2> 'unzip P2.zip'

    3> 'cd P2' on all 7 dcXX machines

B>---Understanding the connection we will form---<

    1> VM assignment
    dc01 -> RP
    dc02 -> dc01 (source 1)
    dc03 -> dc01 (source 2)
    dc04 -> dc01 (random router in group)
    dc05 -> dc01 (router in group)
    dc06 -> dc05 (destination 1)
    dc07 -> dc05 (destination 2)


    2-A> Topology- Simulation Part A
     dc03   dc03
        \   /   
        dc01     dc06
        /  \    /
     dc04   dc05
                \ 
                 dc07

    2-B> Topology- Simulation Part B
       dc03 dc02--------
        \  /      |    |
        dc01     dc06  | 
        /  \    /      |
     dc04   dc05       |
                \      |
                 dc07--

    3> IP:PORT MAPPING for easy understanding
    dc01 - 10.176.69.32:6060
    dc02 - 10.176.69.33:8080
    dc03 - 10.176.69.34:8081
    dc04 - 10.176.69.35:8082
    dc05 - 10.176.69.36:8083
    dc06 - 10.176.69.37:7071
    dc07 - 10.176.69.38:7072

C>---General Notes---<
    - There will be 2 executable that can be created

    - `make` will create executable named "routerRP" that will emulate the RP router
    - "routerRP" when executed ('./routerRP') will show  server's log messages for different requests it receives and actions it takes, e.g. updating routing table, broadcasting messages, receiving messages

    - `make router` will create executable named "router" that will emulate the normal router
    - "router" executable when executed ('./router') will ask for which PORT its server will listen to
    - "router" will output a line in the terminal "Thread : The output file is $FILENAME", where $FILENAME will be a filename of the format "[num1][num2]uterServer.txt".This file will contains the output of the "router" server log messages
    - you would want to look into it to see how different requests (broadcast messages, joining RP group messages) are processed (on a DIFFERENT terminal `tail -f $FILENAME`)
    - So, to view the working of the "router", you should have two terminals open.
        - 1st terminal, where you will run the `./router`, and do client related stuff, e.g. 'Connect RP','Connect Router(RP Group)','Send Message', 'Connect Router'. 
        - 2nd terminal `tail -f $FILENAME`, you will just look at it to see your router server's log messages for different requests it receives   

D>---Connection Setup---<

    1> in dc01
    - `make`
    - `./routerRP`
    - `$PORT` for example $PORT=6060 that you want to listen to
    - NOTE: his terminal will show log requests as routerRP process request and broadcasts messages


    2-1> in dc02-dc05
    - 'make router'
    - `./router`
    - `$PORT` ENTER $PORT=808x that you want to listen to
    - `1`
    - `10.176.69.32 6060` {IP:PORT-dc01: RP Router}
    - NOTE: Find the line in terminal "Thread : The output file is $FILENAME", for example $FILENAME = 60uterServer.txt
    - open a new terminal and go to the P2 dir
    - `tail -f $FILENAME`
    - now in this terminal you see messages as it process requests

    2-2> in dc06-dc07
    - 'make router'
    - `./router`
    - `$PORT` ENTER $PORT=707x that you want to listen to
    - `2`
    - `10.176.69.36 8083` {IP:PORT-dc05: Router that is connected to RP(dc01)}
    - NOTE: Find the line in terminal "Thread : The output file is $FILENAME", for example $FILENAME = 60uterServer.txt
    - open a new terminal and go to the P2 dir
    - `tail -f $FILENAME`
    - now in this terminal you see log messages from your router as it process requests


    3> In the 'router' first terminal you can do actions and the other terminal you can see messages as your router's server process requests

    4> You can do whatever from now on. But, to show that required simulation of P2 follow the additional steps below.

E>---SIMULATION---

    1> PART A- simulation
    -in dc02-03
    `3`
    Enter your message that you want to send to RP to be broadcasted
    `1`
    - NOTE: look at the 2nd terminal of dc06-dc07, where their server log file $FILENAME should be open to verify the broadcasted message

    2> PART B- simulation
    -in dc03
    `3`
    Enter your message that you want to send to RP to be broadcasted
    `1`
    - NOTE: look at the 2nd terminal of dc06-dc07, where their server log file $FILENAME should be open to verify the broadcasted message

    -in dc07-07
    `4`
    `10.176.69.33 8080` {IP:PORT-dc02}

    -in dc02
    `3`
    Enter your message that will be broadcasted to the connected neighbors {dc06-dc07}
    `3`
    - note: look at the 2nd terminal of dc06-dc07, where their server log file $FILENAME should be open to verify the broadcasted message





