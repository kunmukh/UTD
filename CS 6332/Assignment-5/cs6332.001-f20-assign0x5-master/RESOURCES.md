# CS6332-001: LLVM Resources

## LLVM installation / configuration

* Please refer to [the set-up documentation][llvm-3.4-quick-guide].

### Build LLVM from IDEs

[CMake] build framework provides an easy and convenient IDE integration to accelerate development process. Please try `cmake -G` command from the source directory and check out the supported IDEs.


```bash!
llvm-3.4/llvm git:(master*) $ cmake -G
CMake Error: No generator specified for -G

Generators
* Unix Makefiles               = Generates standard UNIX makefiles.
  Ninja                        = Generates build.ninja files.
  Ninja Multi-Config           = Generates build-<Config>.ninja files.
  Xcode                        = Generate Xcode project files.
  CodeBlocks - Ninja           = Generates CodeBlocks project files.
  CodeBlocks - Unix Makefiles  = Generates CodeBlocks project files.
  CodeLite - Ninja             = Generates CodeLite project files.
  CodeLite - Unix Makefiles    = Generates CodeLite project files.
  Sublime Text 2 - Ninja       = Generates Sublime Text 2 project files.
  Sublime Text 2 - Unix Makefiles
                               = Generates Sublime Text 2 project files.
  Kate - Ninja                 = Generates Kate project files.
  Kate - Unix Makefiles        = Generates Kate project files.
  Eclipse CDT4 - Ninja         = Generates Eclipse CDT 4.0 project files.
  Eclipse CDT4 - Unix Makefiles= Generates Eclipse CDT 4.0 project files.
```

## LLVM-IR

### Key readings

* [Introducing LLVM Intermediate Representation | Packt Hub]

* [LLVM Language Reference Manual — LLVM 12 documentation]

* [The Often Misunderstood GEP Instruction — LLVM 12 documentation]

### Additional readings

* [syntax - Understanding the simplest LLVM IR - Stack Overflow]

* [IR is better than assembly — Idea of the day]

* [LLVM's getelementptr, by example]

[LLVM's getelementptr, by example]:https://blog.yossarian.net/2020/09/19/LLVMs-getelementptr-by-example
[Introducing LLVM Intermediate Representation | Packt Hub]:https://hub.packtpub.com/introducing-llvm-intermediate-representation/

[LLVM's getelementptr, by example]:https://blog.yossarian.net/2020/09/19/LLVMs-getelementptr-by-example

[syntax - Understanding the simplest LLVM IR - Stack Overflow]:https://stackoverflow.com/questions/27447865/understanding-the-simplest-llvm-ir

[LLVM Language Reference Manual — LLVM 12 documentation]:http://llvm.org/docs/LangRef.html

[The Often Misunderstood GEP Instruction — LLVM 12 documentation]:https://llvm.org/docs/GetElementPtr.html

[IR is better than assembly — Idea of the day]:https://idea.popcount.org/2013-07-24-ir-is-better-than-assembly/


## Writing LLVM Pass

* [GitHub - banach-space/llvm-tutor: A collection of out-of-tree LLVM passes for teaching and learning]

## LLVM resources

* [LLVM Mailing List][LLVM Development - Google Groups]

* [LLVM Coding Standards LLVM 12 documentation]

* [About LLVM 12 documentation]


###### tags: `llvm`,`cs6332`


[About LLVM 12 documentation]:https://llvm.org/docs/index.html#

[LLVM Coding Standards LLVM 12 documentation]:https://llvm.org/docs/CodingStandards.html

[LLVM Development - Google Groups]:https://groups.google.com/g/llvm-dev

[cmake]:todo

[llvm-3.4-quick-guide]:todo

[llvm-3.4-doxygen]:todo

[GitHub - banach-space/llvm-tutor: A collection of out-of-tree LLVM passes for teaching and learning]:https://github.com/banach-space/llvm-tutor
