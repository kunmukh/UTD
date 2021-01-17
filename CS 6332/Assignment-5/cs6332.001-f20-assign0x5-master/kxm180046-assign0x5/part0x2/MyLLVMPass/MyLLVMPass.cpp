//===- MyLLVMPass.cpp - Example code from "Writing an LLVM Pass" ---------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file implements two versions of the LLVM "Hello World" pass described
// in docs/WritingAnLLVMPass.html
//
//===----------------------------------------------------------------------===//

#define DEBUG_TYPE "hello"
#include "llvm/ADT/Statistic.h"
#include "llvm/IR/Function.h"
#include "llvm/Pass.h"
#include "llvm/Support/raw_ostream.h"

#include <llvm/Pass.h>
#include <llvm/PassManager.h>
#include <llvm/ADT/SmallVector.h>
#include <llvm/Analysis/Verifier.h>
#include <llvm/Assembly/PrintModulePass.h>
#include <llvm/IR/BasicBlock.h>
#include <llvm/IR/CallingConv.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/DerivedTypes.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/GlobalVariable.h>
#include <llvm/IR/InlineAsm.h>
#include <llvm/IR/Instructions.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/Support/FormattedStream.h>
#include <llvm/Support/MathExtras.h>
#include <algorithm>

#include "llvm/IR/IRBuilder.h"

// Kunal Function
#include <vector>
#include <string>
using namespace llvm; 


StringRef fname;

// Old LLVM PASS
//-------------------
namespace {
  // Hello - The first implementation, without getAnalysisUsage.
  struct MyLLVMPass : public ModulePass {
    static char ID; // Pass identification, replacement for typeid
      
    MyLLVMPass() : ModulePass(ID) {
    }
    
    virtual bool runOnModule(Module &M) {
        
        bool changed = false;
        errs() << "Hello, I am in MyLLVMPass Kunal \n";
	return changed;
    }
  };
}

char MyLLVMPass::ID = 0;
static RegisterPass<MyLLVMPass> X("MyLLVMPass", "MyLLVMPass");


// PART 1A LLVM PASS
//---------------------
namespace {
  // MyLLVMPass3 - The second implementation with getAnalysisUsage implemented.
  struct MyLLVMPass3 : public ModulePass {
    static char ID; // Pass identification, replacement for typeid
    
    MyLLVMPass3() : ModulePass(ID) {}

    bool runOnModule(Module &M){ 

        errs() << "Running on Module" << "\n";

        // print out the global variables
        errs() << "Constants in Module" << "\n\n";

        for (auto &G: M.getGlobalList()){

            if ( G.hasInitializer()){
                Type* t = G.getType();
        
                errs() << "Global Name: " << G.getName().str() << "\n";

                errs() << "Global Var Type: ";
                t->print(errs());
                errs()  <<"\n";
                
                errs() << "Global Initializer: " << G.getInitializer() << "\n\n";
            }
            else{
                errs() << G.getName().str() << "\n";
            }

        }
        errs() << "\n\n***";

        // print out the function and their prototype
        errs() << "Function in Module" << "\n";
        for (auto &F: M.getFunctionList()){
            
            errs() << F.getName() << "\n";

            Type* t = F.getType();
            errs() << "Function Prototype: ";
            t->print(errs());
            errs()  <<"\n\n";
        }
        errs() << "\n\n***";
        return false;
    }        

    // We don't modify the program, so we preserve all analyses.
    void getAnalysisUsage(AnalysisUsage &AU) const override {
      AU.setPreservesAll();
    }
  };
}

char MyLLVMPass3::ID = 0;
static RegisterPass<MyLLVMPass3>
Z("MyLLVMPass3", "MyLLVMPass3 Pass (with module analysis implemented)");


// PART 1B LLVM PASS
// -------------------
namespace {
  // MyLLVMPass2 - The second implementation with getAnalysisUsage implemented.
  struct MyLLVMPass2 : public FunctionPass {
    static char ID; // Pass identification, replacement for typeid
    std::map<std::string, int> opCounter;
    MyLLVMPass2() : FunctionPass(ID) {}

    bool runOnFunction(Function &F) override {
    	errs() << "Function " << F.getName() << '\n';

    	// print out the func
    	// print out parameters
    	Function::arg_iterator args = F.arg_begin();
    	Value*x = args;
    	errs() << "Function Argument: size: " << F.arg_size() <<" ";
    	while(args != F.arg_end()){
    		errs() << ": " << x->getName();
    		args++;
    		x = args;
    	}
    	errs() << "\n";
    	// print out the return type
    	Type* t = F.getReturnType();
    	
    	errs() << "Function Return Type: ";
    	t->print(errs());
    	errs()  <<"\n";
    	
    	// print the number of basic block
    	int numBB = 0;
    	for(BasicBlock &bb : F){
    		numBB++;
    	}
    	errs() << "Function Number of BB: "<< numBB <<"\n\n";


    	// print out basic block instrctions
    	int doneBB = 0;
        for(BasicBlock &bb : F){      
            for(Instruction &i: bb){
            	
                if(opCounter.find(i.getOpcodeName()) == opCounter.end()) {
                	opCounter[i.getOpcodeName()] = 1;
                } else {
                	opCounter[i.getOpcodeName()] += 1;
                }
            }
            errs() << "Function's BB done: " << doneBB << "\n";

            std::map <std::string, int>::iterator i = opCounter.begin();
        	std::map <std::string, int>::iterator e = opCounter.end();
        	while (i != e) {
        		errs() << "InstName: " << i->first << ", Operand #: " << i->second << "\n";
        		i++;
        	}
        	errs() << "\n";
        	opCounter.clear();

            doneBB++;
        }        
  		
  		errs() << "\n\n***";
        return false;
    }    

    // We don't modify the program, so we preserve all analyses.
    void getAnalysisUsage(AnalysisUsage &AU) const override {
      AU.setPreservesAll();
    }
  };
}

char MyLLVMPass2::ID = 0;
static RegisterPass<MyLLVMPass2>
Y("MyLLVMPass2", "MyLLVMPass2 Pass (with function analysis implemented)");


// PART 2 LLVM PASS
//--------------------
namespace {
  // MyLLVMPass4 - Dynamic analysis
  struct MyLLVMPass4 : public ModulePass {
    static char ID; // Pass identification, replacement for typeid
    MyLLVMPass4() : ModulePass(ID) {}

    bool runOnModule(Module &M) override {
    
        // Loop through all of our functions in the module
        // This is where you could do something intersesting like only
        // modify a subset of the functions
        // The key is not to modify instrumenting functions!
        Module::FunctionListType &functions = M.getFunctionList();
        for(Module::FunctionListType::iterator FI = functions.begin(), FE = functions.end(); FI != FE; ++FI){
            // Ignore our instrumented function
            if(FI->getName()=="fib_logger"){
            	//errs() << "Inside fib_logger so ignore" << "\n\n";
                continue;
            }   

            for(BasicBlock &bb : *FI){      
	            for(Instruction &i: bb){	            	
	                //errs() << i.getOpcodeName() << "\n";
	                std::string _opName = i.getOpcodeName();

	                // refactor code
	                Function *F = FI;
		            // Build out the function type
	        		auto &Context = M.getContext();
		            // The start of our parameters
					Type* intTy = Type::getInt32Ty(Context);
					// push back all of the parameters
					std::vector<llvm::Type*> params;
					params.push_back(intTy);
					params.push_back(intTy);
					// Specify the return value, arguments, and if there are variable numbers of arguments.
					FunctionType* funcTy = FunctionType::get(intTy, params, false);


		            Constant* hook = M.getOrInsertFunction("fib_logger", funcTy);

	                if (_opName.compare("ret") == 0){
	                	
	                	errs() << "Inside opcode: " << i.getOpcodeName() << "\n";

	                	// args
	                	// In order to set the arguments of the instrumenting function, we are going to
				        // get all of our instrumenting functions arguments, and then modify them.
				        std::vector<Value*> args;
				        for(unsigned int i=0; i< funcTy->getNumParams(); ++i){
				            Type* t = funcTy->getParamType(i);			            
				            
				            Value *newValue;
				            if (i == 1){				            	
				            	newValue = ConstantInt::get(t,0x0);				            	
				            }else{
				            	newValue = F->arg_begin();
				            }            
				            
				            args.push_back(newValue);
				            
				        }

	                	auto *newInst = CallInst::Create(hook,args);
	                	bb.getInstList().insert(i, newInst);

	                } else if (isa<CallInst>(i)){
	                	
	                	StringRef name = cast<CallInst>(i).getCalledFunction()->getName();
	                	std::string _funcName = name;

	                	if (_funcName.compare("fib") == 0){
	                			                		
		                	errs() << "Inside opcode: " << i.getOpcodeName() <<" calling: " << _funcName << "\n";

		                	// args
		                	// In order to set the arguments of the instrumenting function, we are going to
					        // get all of our instrumenting functions arguments, and then modify them.
					        std::vector<Value*> args;
					        for(unsigned int ii=0; ii< funcTy->getNumParams(); ++ii){
					            Type* t = funcTy->getParamType(ii);		            
					            
					            Value *newValue;
					            if (ii == 1){				            	
					            	newValue = ConstantInt::get(t,0x1);				            	
					            }else{
					            	newValue = F->arg_begin();
					            }            
					            
					            args.push_back(newValue);
					            
					        }

		                	auto *newInst = CallInst::Create(hook,args);
		                	bb.getInstList().insert(i, newInst);
	                	}

	                }
	                  
	            }
        	}
        }
        return true;
    }

  };
}

char MyLLVMPass4::ID = 0;
static RegisterPass<MyLLVMPass4>
W("MyLLVMPass4", "Hello World Pass (Code injection)");


// PART 3 LLVM PASS
//---------------------
namespace {
  // MyLLVMPass5 - The second implementation with getAnalysisUsage implemented.
  struct MyLLVMPass5 : public ModulePass {
    static char ID; // Pass identification, replacement for typeid
    
    MyLLVMPass5() : ModulePass(ID) {}

    bool runOnModule(Module &M){ 

    	errs() << "Running on Module" << "\n";

    	/// print out the global variables
    	errs() << "Constants in Module" << "\n\n";

    	for (auto &G: M.getGlobalList()){

    		if (G.hasInitializer()){
    			Type* t = G.getType();
    	
    			errs() << "Global Name: " << G.getName().str() << "\n";

    			errs() << "Global Var Type: ";
    			t->print(errs());
    			errs()  <<"\n";

    			Value* newValue = G.getInitializer();    			
    			
    			errs() << "Global Initializer: " ;
    			newValue->print(errs());
    			errs() << "\n";

    			if(G.getName().str().find("str") != std::string::npos){

	    			ConstantDataArray* ds = cast<ConstantDataArray>(newValue);
	    			StringRef srf = ds->getAsCString();

	    			//  xor setting
	    			std::string src = srf.str();
	    			std::string dst = srf.str();

	    			char * _src = new char[src.length() + 1];
	    			std::strcpy(_src,src.c_str());

	    			char * _dst = new char[dst.length() + 1];
	    			std::strcpy(_dst,dst.c_str());

	    			xorCipher(_dst, _src);

	    			errs() <<"src: " << _src << " : dest: "<< _dst << "\n";

	    			//global var change
	    			Constant *const_array = ConstantDataArray::getString(M.getContext(), _dst, true);
	    			Type* t1 = const_array->getType();

	    			errs() << "New Global Var Type: ";
	    			t1->print(errs());
	    			errs()  <<"\n";

	    			//G.setInitializer(const_array);
	    			//errs() << "Initialization value changed\n";

	    			//newValue = G.getInitializer();    			
	    			
	    			//errs() << "New Global Initialization value: " ;
	    			//newValue->print(errs());

	    			errs() << "New Global Initialization value: "; 
	    			const_array->print(errs());
    			}
    			errs() << "\n\n";
    		}
    		else{
    			errs() << G.getName().str() << "\n";
    		}

    	}
    	errs() << "\n\n**\n\n";
    	
		Module::FunctionListType &functions = M.getFunctionList();

		std::vector<llvm::Value*> allGlobalVar;
		for(Module::global_iterator gi = M.global_begin(), gend = M.global_end(); gi != gend; ++gi){
    		for(Value::use_iterator i = gi->use_begin(), e = gi->use_end(); i!=e; ++i){
    			allGlobalVar.push_back(i->getOperand(0));
    		}
    	}
    	errs() << "\n\n";

        for(Module::FunctionListType::iterator FI = functions.begin(), FE = functions.end(); FI != FE; ++FI){
            for(BasicBlock &bb : *FI){  
	            for(Instruction &i: bb){
		            // The start of our parameters
	                if (isa<LoadInst>(i)){
	                		                	
	                	if (std::find(allGlobalVar.begin(), allGlobalVar.end(), i.getOperand(0)) != allGlobalVar.end()) {
	                		
	                		errs() << "Load Operand contain a global var: ";
	                		i.getOperand(0)->print(errs());
	                		errs() <<"\n";
	                	
	                	} else if (isa<GEPOperator>(i.getOperand(0))){

	                		GEPOperator *gepo = dyn_cast<GEPOperator>(i.getOperand(0));

	                		if (isa<GlobalVariable>(gepo->getPointerOperand())){
	                			//GlobalVariable *gv = dyn_cast<GlobalValue>(gepo->getPointerOperand());

	                			errs() << "GEPOperator == GlobalVariable" << "\n";
	                			
	                			LoadInst * li = dyn_cast<LoadInst>(&i);
		                		Value * v = li->getPointerOperand();

		                		errs() << "inside GEPOperator: ";
		                		v->print(errs());
		                		errs() << "\n";

		                		errs() << "XOR Called to decrypt" << "\n\n";
	                		}

    					}
	                } else if (isa<CallInst>(i)){
	                	if (isa<GEPOperator>(i.getOperand(0))){

	                		GEPOperator *gepo = dyn_cast<GEPOperator>(i.getOperand(0));

	                		if (isa<GlobalVariable>(gepo->getPointerOperand())){
	                			//GlobalVariable *gv = dyn_cast<GlobalValue>(gepo->getPointerOperand());

	                			errs() << "Call GEPOperator == GlobalVariable" << "\n";
	                			
	                			errs() << "inside GEPOperator: ";
		                		gepo->print(errs());
		                		errs() << "\n";

		                		errs() << "XOR Called to decrypt" << "\n\n";
	                		}

    					} 
	                }
	            }
	        }
	    }   	

    	return false;
    }

    char xorKey = 0x07;  // bell -- non-printable character.   

    int xorCipher(char *dst, char *src) {
	    int len = strlen(src);
	    for (int i = 0; i < len; i++) {
	        //  Not a good cipher.
	        dst[i] = src[i] ^ xorKey;
	    }
	    dst[len] = '\0';
	    return len;
	}

    // We don't modify the program, so we preserve all analyses.
    void getAnalysisUsage(AnalysisUsage &AU) const override {
      AU.setPreservesAll();
    }
  };
}

char MyLLVMPass5::ID = 0;
static RegisterPass<MyLLVMPass5>
U("MyLLVMPass5", "MyLLVMPass5 Pass (with module analysis implemented )");
