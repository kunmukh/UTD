; ModuleID = 'cs6332.001-f20-assign0x5-master/db_connector/utils.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-unknown-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i32, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i32, i32, [40 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@.str = private unnamed_addr constant [41 x i8] c"=======================================\0A\00", align 1
@.str1 = private unnamed_addr constant [41 x i8] c"=            DB Connector             =\0A\00", align 1
@.str2 = private unnamed_addr constant [10 x i8] c"(y / N) :\00", align 1
@stdin = external global %struct._IO_FILE*
@.str3 = private unnamed_addr constant [7 x i8] c"[%s] :\00", align 1
@.str4 = private unnamed_addr constant [6 x i8] c"\5C%02X\00", align 1
@.str5 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@xorKey = internal global i8 7, align 1

; Function Attrs: nounwind
define void @banner() #0 {
entry:
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str, i32 0, i32 0))
  %call1 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str1, i32 0, i32 0))
  %call2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str, i32 0, i32 0))
  ret void
}

declare i32 @printf(i8*, ...) #1

; Function Attrs: nounwind
define signext i8 @askYesOrNo() #0 {
entry:
  %retval = alloca i8, align 1
  %buf = alloca [16 x i8], align 1
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([10 x i8]* @.str2, i32 0, i32 0))
  %arraydecay = getelementptr inbounds [16 x i8]* %buf, i32 0, i32 0
  %0 = load %struct._IO_FILE** @stdin, align 4
  %call1 = call i8* @fgets(i8* %arraydecay, i32 16, %struct._IO_FILE* %0)
  %arrayidx = getelementptr inbounds [16 x i8]* %buf, i32 0, i32 0
  %1 = load i8* %arrayidx, align 1
  %conv = sext i8 %1 to i32
  %cmp = icmp eq i32 %conv, 89
  br i1 %cmp, label %if.then, label %lor.lhs.false

lor.lhs.false:                                    ; preds = %entry
  %arrayidx3 = getelementptr inbounds [16 x i8]* %buf, i32 0, i32 0
  %2 = load i8* %arrayidx3, align 1
  %conv4 = sext i8 %2 to i32
  %cmp5 = icmp eq i32 %conv4, 121
  br i1 %cmp5, label %if.then, label %if.end

if.then:                                          ; preds = %lor.lhs.false, %entry
  store i8 1, i8* %retval
  br label %return

if.end:                                           ; preds = %lor.lhs.false
  store i8 0, i8* %retval
  br label %return

return:                                           ; preds = %if.end, %if.then
  %3 = load i8* %retval
  ret i8 %3
}

declare i8* @fgets(i8*, i32, %struct._IO_FILE*) #1

; Function Attrs: nounwind
define signext i8 @isValid(i8* %user, i8* %pass) #0 {
entry:
  %user.addr = alloca i8*, align 4
  %pass.addr = alloca i8*, align 4
  store i8* %user, i8** %user.addr, align 4
  store i8* %pass, i8** %pass.addr, align 4
  %0 = load i8** %user.addr, align 4
  %call = call i32 @strlen(i8* %0) #3
  %cmp = icmp ugt i32 %call, 4
  br i1 %cmp, label %land.rhs, label %land.end

land.rhs:                                         ; preds = %entry
  %1 = load i8** %pass.addr, align 4
  %call1 = call i32 @strlen(i8* %1) #3
  %cmp2 = icmp ugt i32 %call1, 4
  br label %land.end

land.end:                                         ; preds = %land.rhs, %entry
  %2 = phi i1 [ false, %entry ], [ %cmp2, %land.rhs ]
  %land.ext = zext i1 %2 to i32
  %conv = trunc i32 %land.ext to i8
  ret i8 %conv
}

; Function Attrs: nounwind readonly
declare i32 @strlen(i8*) #2

; Function Attrs: nounwind
define i32 @__xor_dbg(i8* %msg, i8* %in) #0 {
entry:
  %msg.addr = alloca i8*, align 4
  %in.addr = alloca i8*, align 4
  %len = alloca i32, align 4
  %i = alloca i32, align 4
  store i8* %msg, i8** %msg.addr, align 4
  store i8* %in, i8** %in.addr, align 4
  %0 = load i8** %msg.addr, align 4
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([7 x i8]* @.str3, i32 0, i32 0), i8* %0)
  %1 = load i8** %in.addr, align 4
  %call1 = call i32 @strlen(i8* %1) #3
  store i32 %call1, i32* %len, align 4
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %2 = load i32* %i, align 4
  %3 = load i32* %len, align 4
  %cmp = icmp slt i32 %2, %3
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %4 = load i32* %i, align 4
  %5 = load i8** %in.addr, align 4
  %arrayidx = getelementptr inbounds i8* %5, i32 %4
  %6 = load i8* %arrayidx, align 1
  %conv = sext i8 %6 to i32
  %call2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([6 x i8]* @.str4, i32 0, i32 0), i32 %conv)
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %7 = load i32* %i, align 4
  %inc = add nsw i32 %7, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %8 = load i32* %len, align 4
  %9 = load i8** %in.addr, align 4
  %arrayidx3 = getelementptr inbounds i8* %9, i32 %8
  %10 = load i8* %arrayidx3, align 1
  %conv4 = sext i8 %10 to i32
  %call5 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([6 x i8]* @.str4, i32 0, i32 0), i32 %conv4)
  %call6 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([2 x i8]* @.str5, i32 0, i32 0))
  %11 = load i32* %len, align 4
  ret i32 %11
}

; Function Attrs: nounwind
define i32 @xorCipher(i8* %dst, i8* %src) #0 {
entry:
  %dst.addr = alloca i8*, align 4
  %src.addr = alloca i8*, align 4
  %len = alloca i32, align 4
  %i = alloca i32, align 4
  store i8* %dst, i8** %dst.addr, align 4
  store i8* %src, i8** %src.addr, align 4
  %0 = load i8** %src.addr, align 4
  %call = call i32 @strlen(i8* %0) #3
  store i32 %call, i32* %len, align 4
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %1 = load i32* %i, align 4
  %2 = load i32* %len, align 4
  %cmp = icmp slt i32 %1, %2
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %3 = load i32* %i, align 4
  %4 = load i8** %src.addr, align 4
  %arrayidx = getelementptr inbounds i8* %4, i32 %3
  %5 = load i8* %arrayidx, align 1
  %conv = sext i8 %5 to i32
  %6 = load i8* @xorKey, align 1
  %conv1 = sext i8 %6 to i32
  %xor = xor i32 %conv, %conv1
  %conv2 = trunc i32 %xor to i8
  %7 = load i32* %i, align 4
  %8 = load i8** %dst.addr, align 4
  %arrayidx3 = getelementptr inbounds i8* %8, i32 %7
  store i8 %conv2, i8* %arrayidx3, align 1
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %9 = load i32* %i, align 4
  %inc = add nsw i32 %9, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %10 = load i32* %len, align 4
  %11 = load i8** %dst.addr, align 4
  %arrayidx4 = getelementptr inbounds i8* %11, i32 %10
  store i8 0, i8* %arrayidx4, align 1
  %12 = load i32* %len, align 4
  ret i32 %12
}

attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readonly }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}
