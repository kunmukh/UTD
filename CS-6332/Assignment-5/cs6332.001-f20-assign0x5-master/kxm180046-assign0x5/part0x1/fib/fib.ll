; ModuleID = 'cs6332.001-f20-assign0x5-master/fib/fib.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i32, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i32, i32, [40 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@stderr = external global %struct._IO_FILE*
@.str = private unnamed_addr constant [19 x i8] c"usage: %s <value>\0A\00", align 1
@.str1 = private unnamed_addr constant [7 x i8] c"strtol\00", align 1
@.str2 = private unnamed_addr constant [29 x i8] c"error: %s is not an integer\0A\00", align 1
@.str3 = private unnamed_addr constant [37 x i8] c"error: junk at end of parameter: %s\0A\00", align 1
@.str4 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

; Function Attrs: nounwind
define i32 @fib(i32 %i) #0 {
entry:
  %retval = alloca i32, align 4
  %i.addr = alloca i32, align 4
  store i32 %i, i32* %i.addr, align 4
  %0 = load i32* %i.addr, align 4
  %cmp = icmp sle i32 %0, 1
  br i1 %cmp, label %if.then, label %if.end

if.then:                                          ; preds = %entry
  store i32 1, i32* %retval
  br label %return

if.end:                                           ; preds = %entry
  %1 = load i32* %i.addr, align 4
  %sub = sub nsw i32 %1, 1
  %call = call i32 @fib_logger(i32 %sub, i32 1)
  %2 = load i32* %i.addr, align 4
  %sub1 = sub nsw i32 %2, 1
  %call2 = call i32 @fib(i32 %sub1)
  %3 = load i32* %i.addr, align 4
  %sub3 = sub nsw i32 %3, 2
  %call4 = call i32 @fib(i32 %sub3)
  %add = add nsw i32 %call2, %call4
  store i32 %add, i32* %retval
  br label %return

return:                                           ; preds = %if.end, %if.then
  %4 = load i32* %retval
  ret i32 %4
}

declare i32 @fib_logger(i32, i32) #1

; Function Attrs: nounwind
define i32 @main(i32 %argc, i8** %argv) #0 {
entry:
  %retval = alloca i32, align 4
  %argc.addr = alloca i32, align 4
  %argv.addr = alloca i8**, align 4
  %value = alloca i32, align 4
  %end = alloca i8*, align 4
  store i32 0, i32* %retval
  store i32 %argc, i32* %argc.addr, align 4
  store i8** %argv, i8*** %argv.addr, align 4
  %0 = load i32* %argc.addr, align 4
  %cmp = icmp ne i32 %0, 2
  br i1 %cmp, label %if.then, label %if.end

if.then:                                          ; preds = %entry
  %1 = load %struct._IO_FILE** @stderr, align 4
  %2 = load i8*** %argv.addr, align 4
  %arrayidx = getelementptr inbounds i8** %2, i32 0
  %3 = load i8** %arrayidx, align 4
  %call = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %1, i8* getelementptr inbounds ([19 x i8]* @.str, i32 0, i32 0), i8* %3)
  call void @exit(i32 1) #4
  unreachable

if.end:                                           ; preds = %entry
  %4 = load i8*** %argv.addr, align 4
  %arrayidx1 = getelementptr inbounds i8** %4, i32 1
  %5 = load i8** %arrayidx1, align 4
  %call2 = call i32 @strtol(i8* %5, i8** %end, i32 10) #5
  store i32 %call2, i32* %value, align 4
  %call3 = call i32* @__errno_location() #6
  %6 = load i32* %call3, align 4
  %cmp4 = icmp eq i32 %6, 34
  br i1 %cmp4, label %land.lhs.true, label %lor.lhs.false7

land.lhs.true:                                    ; preds = %if.end
  %7 = load i32* %value, align 4
  %cmp5 = icmp eq i32 %7, 2147483647
  br i1 %cmp5, label %if.then12, label %lor.lhs.false

lor.lhs.false:                                    ; preds = %land.lhs.true
  %8 = load i32* %value, align 4
  %cmp6 = icmp eq i32 %8, -2147483648
  br i1 %cmp6, label %if.then12, label %lor.lhs.false7

lor.lhs.false7:                                   ; preds = %lor.lhs.false, %if.end
  %call8 = call i32* @__errno_location() #6
  %9 = load i32* %call8, align 4
  %cmp9 = icmp ne i32 %9, 0
  br i1 %cmp9, label %land.lhs.true10, label %if.end13

land.lhs.true10:                                  ; preds = %lor.lhs.false7
  %10 = load i32* %value, align 4
  %cmp11 = icmp eq i32 %10, 0
  br i1 %cmp11, label %if.then12, label %if.end13

if.then12:                                        ; preds = %land.lhs.true10, %lor.lhs.false, %land.lhs.true
  call void @perror(i8* getelementptr inbounds ([7 x i8]* @.str1, i32 0, i32 0))
  call void @exit(i32 1) #4
  unreachable

if.end13:                                         ; preds = %land.lhs.true10, %lor.lhs.false7
  %11 = load i8** %end, align 4
  %12 = load i8*** %argv.addr, align 4
  %arrayidx14 = getelementptr inbounds i8** %12, i32 1
  %13 = load i8** %arrayidx14, align 4
  %cmp15 = icmp eq i8* %11, %13
  br i1 %cmp15, label %if.then16, label %if.end19

if.then16:                                        ; preds = %if.end13
  %14 = load %struct._IO_FILE** @stderr, align 4
  %15 = load i8*** %argv.addr, align 4
  %arrayidx17 = getelementptr inbounds i8** %15, i32 1
  %16 = load i8** %arrayidx17, align 4
  %call18 = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %14, i8* getelementptr inbounds ([29 x i8]* @.str2, i32 0, i32 0), i8* %16)
  call void @exit(i32 1) #4
  unreachable

if.end19:                                         ; preds = %if.end13
  %17 = load i8** %end, align 4
  %18 = load i8* %17, align 1
  %conv = sext i8 %18 to i32
  %cmp20 = icmp ne i32 %conv, 0
  br i1 %cmp20, label %if.then22, label %if.end24

if.then22:                                        ; preds = %if.end19
  %19 = load %struct._IO_FILE** @stderr, align 4
  %20 = load i8** %end, align 4
  %call23 = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %19, i8* getelementptr inbounds ([37 x i8]* @.str3, i32 0, i32 0), i8* %20)
  call void @exit(i32 1) #4
  unreachable

if.end24:                                         ; preds = %if.end19
  %21 = load i32* %value, align 4
  %call25 = call i32 @fib(i32 %21)
  store i32 %call25, i32* %value, align 4
  %22 = load i32* %value, align 4
  %call26 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), i32 %22)
  call void @exit(i32 0) #4
  unreachable

return:                                           ; No predecessors!
  %23 = load i32* %retval
  ret i32 %23
}

declare i32 @fprintf(%struct._IO_FILE*, i8*, ...) #1

; Function Attrs: noreturn nounwind
declare void @exit(i32) #2

; Function Attrs: nounwind
declare i32 @strtol(i8*, i8**, i32) #0

; Function Attrs: nounwind readnone
declare i32* @__errno_location() #3

declare void @perror(i8*) #1

declare i32 @printf(i8*, ...) #1

attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readnone "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noreturn nounwind }
attributes #5 = { nounwind }
attributes #6 = { nounwind readnone }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}
