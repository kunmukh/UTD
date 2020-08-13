Kunal Mukherjee
6/25/20
CS 6390
Dr. Ravi Prakash
Project 1 README

README:

A>---Running RIP----
0> transfer P1.zip from local directory to a dir in dcXX machines

1> ssh into 4 machines e.g. dc01, dc02, dc03, dc04

2> 'unzip P1.zip'

3> 'cd P1' on all 4 dcXX machines 


*** in dc01 ***
4> make clean

5> make rip

6> './rip'

7> 'b'

8> '8080'

9> go to dc02 to get its IP and PORT

*** in dc02 ***
10> './rip'

11> 'c'

12>  '8081'

13> go to dc03 to get its IP and PORT

*** in dc03 ***
14> './rip'

15> 'd'

16>  '8082'

17> go to dc04 to get its IP and PORT

*** in dc04 ***
18> './rip'

19> 'e'

20> '8083'

21> '1'

22> Enter dc03 IP and Port '10.176.69.34 8082'

23> go to dc03

*** in dc03 ***

24> '2'

25> Enter dc02 IP and Port '10.176.69.33 8081'

26> Enter dc04 IP and Port '10.176.69.35 8083'

27> go to dc02

*** in dc02 ***

28> '2'

29> Enter dc01 IP and Port '10.176.69.32 8080'

30> Enter dc03 IP and Port '10.176.69.34 8082'

31> go to dc01

*** in dc01 ***

32> '1'

33> Enter dc02 IP and Port '10.176.69.33 8081'

34> 'ANY KEY'

35> Wait for 30 sec for simulation to start. You will see dc01 update and subsequent 10 sec for dc02-04 updates

*** dc01-dc04 ***
Look at the Updated Routing vector in the TERMINAL of dc01-dc04 for all the rounds

dc01 output:

Thread: ***Current Updated Cost for RT Round:1***
Thread: NODE:a FROM c COST 3 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...

NOTE: Only node 'a' will be updated in each round. As that is the only connection where the link has gone down. e.g. 'Thread: NODE:a FROM c COST 3'


NOTE: By round 8, output in the terminal of dc01(node b) will be, showing that it took 8 rounds to propagate the messgae that route to A is down:

dc01 output:

Thread: ***Current Updated Cost for RT Round:8***
Thread: NODE:a FROM c COST 16 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...

B>---Running SPLIT HORIZON----


*** in dc01 ***
1> clear

2> make sh

3> './sh'

4> 'b'

5> '8080'

6> go to dc02 to get its IP and PORT

*** in dc02 ***
7> './sh'

8> 'c'

9>  '8081'

10> go to dc03 to get its IP and PORT

*** in dc03 ***
11> './sh'

12> 'd'

13>  '8082'

14> go to dc04 to get its IP and PORT

*** in dc04 ***
15> './sh'

16> 'e'

17> '8083'

18> '1'

19> Enter dc03 IP and Port '10.176.69.34 8082'

20> go to dc03

*** in dc03 ***

21> '2'

22> Enter dc02 IP and Port '10.176.69.33 8081'

23> Enter dc04 IP and Port '10.176.69.35 8083'

24> go to dc02

*** in dc02 ***

25> '2'

26> Enter dc01 IP and Port '10.176.69.32 8080'

27> Enter dc03 IP and Port '10.176.69.34 8082'

28> go to dc01

*** in dc01 ***

29> '1'

30> Enter dc02 IP and Port '10.176.69.33 8081'

31> 'ANY KEY'

32> Wait for 30 sec for simulation to start. You will see dc01 update and subsequent 10 sec for dc02-04 updates

*** dc01-dc04 ***
Look at the Updated Routing vector in the TERMINAL of dc01-dc04 for all the rounds

dc01 output:

Thread: ***Current Updated Cost for RT Round:1***
Thread: NODE:a FROM a COST 16 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...

NOTE: Only node 'a' will be updated in each round. As that is the only connection where the link has gone down. e.g, 'Thread: NODE:a FROM c COST 3'

NOTE: Whenever the server is sending an advertisement when the node is 1 hop away from the requesting router, e.g. router c sending update to router d containing RTE for e, will put 'x 20', a bogus value so that route is not utilized, mimicing if that route was not advertised. 

NOTE: By round 4, output in the terminal of dc01(node b) will be, showing that it took 8 rounds to propagate the messgae that route to A is down:

dc01 output:

Thread: ***Current Updated Cost for RT Round:8***
Thread: NODE:a FROM c COST 16 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...

B>---Running SPLIT HORIZON POISON REVERSE----


*** in dc01 ***
1> clear

2> make shpr

3> './shpr'

4> 'b'

5> '8080'

6> go to dc02 to get its IP and PORT

*** in dc02 ***
7> './shpr'

8> 'c'

9>  '8081'

10> go to dc03 to get its IP and PORT

*** in dc03 ***
11> './shpr'

12> 'd'

13>  '8082'

14> go to dc04 to get its IP and PORT

*** in dc04 ***
15> './shpr'

16> 'e'

17> '8083'

18> '1'

19> Enter dc03 IP and Port '10.176.69.34 8082'

20> go to dc03

*** in dc03 ***

21> '2'

22> Enter dc02 IP and Port '10.176.69.33 8081'

23> Enter dc04 IP and Port '10.176.69.35 8083'

24> go to dc02

*** in dc02 ***

25> '2'

26> Enter dc01 IP and Port '10.176.69.32 8080'

27> Enter dc03 IP and Port '10.176.69.34 8082'

28> go to dc01

*** in dc01 ***

29> '1'

30> Enter dc02 IP and Port '10.176.69.33 8081'

31> 'ANY KEY'

32> Wait for 30 sec for simulation to start. You will see dc01 update and subsequent 10 sec for dc02-04 updates

*** dc01-dc04 ***
Look at the Updated Routing vector in the TERMINAL of dc01-dc04 for all the rounds

dc01 output:

Thread: ***Current Updated Cost for RT Round:1***
Thread: NODE:a FROM a COST 16 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...

NOTE: Only node 'a' will be updated in each round. As that is the only connection where the link has gone down. e.g, 'Thread: NODE:a FROM c COST 3'

NOTE: Whenever the server is sending an advertisement when the node is 1 hop away from the requesting router, e.g. router c sending update to router d containing RTE for e, will put '16' or infinity. 

NOTE: By round 4, output in the terminal of dc01(node b) will be, showing that it took 4 rounds to propagate the messgae that route to A is down:

dc01 output:

Thread: ***Current Updated Cost for RT Round:8***
Thread: NODE:a FROM c COST 16 
Thread: NODE:b FROM b COST 0 
Thread: NODE:c FROM c COST 1 
Thread: NODE:d FROM c COST 2 
Thread: NODE:e FROM c COST 3 
Thread: ***Current Updated Cost for Routing Table***
Thread: Exiting...










