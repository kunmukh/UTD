##===- lib/Transforms/MyLLVMPass/Makefile -----------------------*- Makefile -*-===##
#
#                     The LLVM Compiler Infrastructure
#
# This file is distributed under the University of Illinois Open Source
# License. See LICENSE.TXT for details.
#
##===----------------------------------------------------------------------===##
# put it in ~/tools/llvm/src/lib/Transforms/MyLLVMPass/

LEVEL = ../../..
LIBRARYNAME = MyLLVMPass
LOADABLE_MODULE = 1
USEDLIBS =

# If we don't need RTTI or EH, there's no reason to export anything
# from the hello plugin.
ifneq ($(REQUIRES_RTTI), 1)
ifneq ($(REQUIRES_EH), 1)
EXPORTED_SYMBOL_FILE = $(PROJ_SRC_DIR)/MyLLVMPass.exports
endif
endif

include $(LEVEL)/Makefile.common

