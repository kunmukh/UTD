; ModuleID = 'cs6332.001-f20-assign0x5-master/fib/utils.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i32, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i32, i32, [40 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@.str = private unnamed_addr constant [11 x i8] c"FIB_LOGGER\00", align 1
@.str1 = private unnamed_addr constant [14 x i8] c"call fib(%d)\0A\00", align 1
@.str2 = private unnamed_addr constant [18 x i8] c"fib() returns %d\0A\00", align 1
@stderr = external global %struct._IO_FILE*

; Function Attrs: nounwind
define i32 @fib_logger(i32 %val, i32 %isCall) #0 {
entry:
  %retval = alloca i32, align 4
  %val.addr = alloca i32, align 4
  %isCall.addr = alloca i32, align 4
  %fmt = alloca i8*, align 4
  store i32 %val, i32* %val.addr, align 4
  store i32 %isCall, i32* %isCall.addr, align 4
  %call = call i8* @getenv(i8* getelementptr inbounds ([11 x i8]* @.str, i32 0, i32 0)) #3
  %call1 = call i32 @atoi(i8* %call) #4
  %tobool = icmp ne i32 %call1, 0
  br i1 %tobool, label %if.end, label %if.then

if.then:                                          ; preds = %entry
  store i32 -1, i32* %retval
  br label %return

if.end:                                           ; preds = %entry
  %0 = load i32* %isCall.addr, align 4
  %tobool2 = icmp ne i32 %0, 0
  br i1 %tobool2, label %if.then3, label %if.else

if.then3:                                         ; preds = %if.end
  store i8* getelementptr inbounds ([14 x i8]* @.str1, i32 0, i32 0), i8** %fmt, align 4
  br label %if.end4

if.else:                                          ; preds = %if.end
  store i8* getelementptr inbounds ([18 x i8]* @.str2, i32 0, i32 0), i8** %fmt, align 4
  br label %if.end4

if.end4:                                          ; preds = %if.else, %if.then3
  %1 = load %struct._IO_FILE** @stderr, align 4
  %2 = load i8** %fmt, align 4
  %3 = load i32* %val.addr, align 4
  %call5 = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %1, i8* %2, i32 %3)
  %4 = load i32* %val.addr, align 4
  store i32 %4, i32* %retval
  br label %return

return:                                           ; preds = %if.end4, %if.then
  %5 = load i32* %retval
  ret i32 %5
}

; Function Attrs: nounwind readonly
declare i32 @atoi(i8*) #1

; Function Attrs: nounwind
declare i8* @getenv(i8*) #0

declare i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }
attributes #4 = { nounwind readonly }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}
