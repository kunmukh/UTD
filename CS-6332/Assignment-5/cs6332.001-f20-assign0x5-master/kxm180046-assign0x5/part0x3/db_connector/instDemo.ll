; ModuleID = 'cs6332.001-f20-assign0x5-master/db_connector/instDB.ll'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-unknown-linux-gnu"

%struct.cred_t = type { i8*, i8* }
%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i32, i16, i8, [1 x i8], i8*, i64, i8*, i8*, i8*, i8*, i32, i32, [40 x i8] }
%struct._IO_marker = type { %struct._IO_marker*, %struct._IO_FILE*, i32 }

@.str = private unnamed_addr constant [7 x i8] c"cs6332\00", align 1
@.str1 = private unnamed_addr constant [15 x i8] c"mysecretpasswd\00", align 1
@cred_default = global %struct.cred_t { i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0), i8* getelementptr inbounds ([15 x i8]* @.str1, i32 0, i32 0) }, align 4
@pass_buf = common global [16 x i8] zeroinitializer, align 1
@.str2 = private unnamed_addr constant [17 x i8] c"Input username: \00", align 1
@stdin = external global %struct._IO_FILE*
@.str3 = private unnamed_addr constant [25 x i8] c"Input error, exiting...\0A\00", align 1
@.str4 = private unnamed_addr constant [10 x i8] c"Password:\00", align 1
@stderr = external global %struct._IO_FILE*
@.str5 = private unnamed_addr constant [42 x i8] c"Invalid credential input, using defaults\0A\00", align 1
@.str6 = private unnamed_addr constant [50 x i8] c"can we proceed with username %s and password %s? \00", align 1
@.str7 = private unnamed_addr constant [13 x i8] c"Exiting ...\0A\00", align 1
@.str8 = private unnamed_addr constant [31 x i8] c"PGPASSWORD=%s psql -h %s -U %s\00", align 1
@.str9 = private unnamed_addr constant [14 x i8] c"10.176.150.50\00", align 1
@.str10 = private unnamed_addr constant [41 x i8] c"=======================================\0A\00", align 1
@.str111 = private unnamed_addr constant [41 x i8] c"=            DB Connector             =\0A\00", align 1
@.str212 = private unnamed_addr constant [10 x i8] c"(y / N) :\00", align 1
@.str313 = private unnamed_addr constant [7 x i8] c"[%s] :\00", align 1
@.str414 = private unnamed_addr constant [6 x i8] c"\5C%02X\00", align 1
@.str515 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@xorKey = internal global i8 7, align 1

; Function Attrs: nounwind
define i8* @redactPass(i8* %pass) #0 {
entry:
  %pass.addr = alloca i8*, align 4
  %len = alloca i32, align 4
  %i = alloca i32, align 4
  store i8* %pass, i8** %pass.addr, align 4
  %0 = load i8** %pass.addr, align 4
  %call = call i32 @strlen(i8* %0) #4
  store i32 %call, i32* %len, align 4
  %1 = load i8** %pass.addr, align 4
  %2 = load i32* %len, align 4
  %call1 = call i8* @strncpy(i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0), i8* %1, i32 %2) #5
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %3 = load i32* %i, align 4
  %4 = load i32* %len, align 4
  %sub = sub nsw i32 %4, 2
  %cmp = icmp slt i32 %3, %sub
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %5 = load i32* %i, align 4
  %add = add nsw i32 %5, 1
  %arrayidx = getelementptr inbounds [16 x i8]* @pass_buf, i32 0, i32 %add
  store i8 42, i8* %arrayidx, align 1
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %6 = load i32* %i, align 4
  %inc = add nsw i32 %6, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  ret i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0)
}

; Function Attrs: nounwind readonly
declare i32 @strlen(i8*) #1

; Function Attrs: nounwind
declare i8* @strncpy(i8*, i8*, i32) #0

; Function Attrs: nounwind
define i32 @main(i32 %argc, i8** %argv) #0 {
entry:
  %retval = alloca i32, align 4
  %argc.addr = alloca i32, align 4
  %argv.addr = alloca i8**, align 4
  %cmd = alloca [80 x i8], align 1
  %user = alloca [16 x i8], align 1
  %pass = alloca [16 x i8], align 1
  %rc = alloca i8*, align 4
  %temp = alloca i8*, align 4
  store i32 0, i32* %retval
  store i32 %argc, i32* %argc.addr, align 4
  store i8** %argv, i8*** %argv.addr, align 4
  store i8* null, i8** %rc, align 4
  call void @banner()
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([17 x i8]* @.str2, i32 0, i32 0))
  %arraydecay = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %0 = load %struct._IO_FILE** @stdin, align 4
  %call1 = call i8* @fgets(i8* %arraydecay, i32 16, %struct._IO_FILE* %0)
  store i8* %call1, i8** %rc, align 4
  %1 = load i8** %rc, align 4
  %cmp = icmp ne i8* %1, null
  br i1 %cmp, label %if.then, label %if.else

if.then:                                          ; preds = %entry
  %arraydecay2 = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %call3 = call i32 @strlen(i8* %arraydecay2) #4
  %sub = sub i32 %call3, 1
  %arrayidx = getelementptr inbounds [16 x i8]* %user, i32 0, i32 %sub
  store i8 0, i8* %arrayidx, align 1
  br label %if.end

if.else:                                          ; preds = %entry
  %call4 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([25 x i8]* @.str3, i32 0, i32 0))
  call void @exit(i32 1) #6
  unreachable

if.end:                                           ; preds = %if.then
  %call5 = call i8* @getpass(i8* getelementptr inbounds ([10 x i8]* @.str4, i32 0, i32 0))
  store i8* %call5, i8** %temp, align 4
  %2 = load i8** %temp, align 4
  %cmp6 = icmp ne i8* %2, null
  br i1 %cmp6, label %if.then7, label %if.else14

if.then7:                                         ; preds = %if.end
  %arraydecay8 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %call9 = call i32 @strlen(i8* %arraydecay8) #4
  %sub10 = sub i32 %call9, 1
  %arrayidx11 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 %sub10
  store i8 0, i8* %arrayidx11, align 1
  %arraydecay12 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %3 = load i8** %temp, align 4
  %call13 = call i8* @strncpy(i8* %arraydecay12, i8* %3, i32 16) #5
  br label %if.end16

if.else14:                                        ; preds = %if.end
  %call15 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([25 x i8]* @.str3, i32 0, i32 0))
  call void @exit(i32 1) #6
  unreachable

if.end16:                                         ; preds = %if.then7
  %arraydecay17 = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %arraydecay18 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %call19 = call signext i8 @isValid(i8* %arraydecay17, i8* %arraydecay18)
  %tobool = icmp ne i8 %call19, 0
  br i1 %tobool, label %if.end26, label %if.then20

if.then20:                                        ; preds = %if.end16
  %4 = load %struct._IO_FILE** @stderr, align 4
  %call21 = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %4, i8* getelementptr inbounds ([42 x i8]* @.str5, i32 0, i32 0))
  %arraydecay22 = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %5 = load i8** getelementptr inbounds (%struct.cred_t* @cred_default, i32 0, i32 0), align 4
  %call23 = call i8* @strncpy(i8* %arraydecay22, i8* %5, i32 16) #5
  %arraydecay24 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %6 = load i8** getelementptr inbounds (%struct.cred_t* @cred_default, i32 0, i32 1), align 4
  %call25 = call i8* @strncpy(i8* %arraydecay24, i8* %6, i32 16) #5
  br label %if.end26

if.end26:                                         ; preds = %if.then20, %if.end16
  br label %while.body

while.body:                                       ; preds = %if.end35, %if.end26
  %arraydecay27 = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %arraydecay28 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %call29 = call i8* @redactPass(i8* %arraydecay28)
  %call30 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([50 x i8]* @.str6, i32 0, i32 0), i8* %arraydecay27, i8* %call29)
  %call31 = call signext i8 @askYesOrNo()
  %tobool32 = icmp ne i8 %call31, 0
  br i1 %tobool32, label %if.end35, label %if.then33

if.then33:                                        ; preds = %while.body
  %7 = load %struct._IO_FILE** @stderr, align 4
  %call34 = call i32 (%struct._IO_FILE*, i8*, ...)* @fprintf(%struct._IO_FILE* %7, i8* getelementptr inbounds ([13 x i8]* @.str7, i32 0, i32 0))
  br label %RET

if.end35:                                         ; preds = %while.body
  %arraydecay36 = getelementptr inbounds [80 x i8]* %cmd, i32 0, i32 0
  %arraydecay37 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %arraydecay38 = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %call39 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %arraydecay36, i32 80, i8* getelementptr inbounds ([31 x i8]* @.str8, i32 0, i32 0), i8* %arraydecay37, i8* getelementptr inbounds ([14 x i8]* @.str9, i32 0, i32 0), i8* %arraydecay38) #5
  %arraydecay40 = getelementptr inbounds [80 x i8]* %cmd, i32 0, i32 0
  %call41 = call i32 @system(i8* %arraydecay40)
  br label %while.body

RET:                                              ; preds = %if.then33
  ret i32 0
}

declare i32 @printf(i8*, ...) #2

declare i8* @fgets(i8*, i32, %struct._IO_FILE*) #2

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

declare i8* @getpass(i8*) #2

declare i32 @fprintf(%struct._IO_FILE*, i8*, ...) #2

; Function Attrs: nounwind
declare i32 @snprintf(i8*, i32, i8*, ...) #0

declare i32 @system(i8*) #2

; Function Attrs: nounwind
define void @banner() #0 {
entry:
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str10, i32 0, i32 0))
  %call1 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str111, i32 0, i32 0))
  %call2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([41 x i8]* @.str10, i32 0, i32 0))
  ret void
}

; Function Attrs: nounwind
define signext i8 @askYesOrNo() #0 {
entry:
  %retval = alloca i8, align 1
  %buf = alloca [16 x i8], align 1
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([10 x i8]* @.str212, i32 0, i32 0))
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

; Function Attrs: nounwind
define signext i8 @isValid(i8* %user, i8* %pass) #0 {
entry:
  %user.addr = alloca i8*, align 4
  %pass.addr = alloca i8*, align 4
  store i8* %user, i8** %user.addr, align 4
  store i8* %pass, i8** %pass.addr, align 4
  %0 = load i8** %user.addr, align 4
  %call = call i32 @strlen(i8* %0) #4
  %cmp = icmp ugt i32 %call, 4
  br i1 %cmp, label %land.rhs, label %land.end

land.rhs:                                         ; preds = %entry
  %1 = load i8** %pass.addr, align 4
  %call1 = call i32 @strlen(i8* %1) #4
  %cmp2 = icmp ugt i32 %call1, 4
  br label %land.end

land.end:                                         ; preds = %land.rhs, %entry
  %2 = phi i1 [ false, %entry ], [ %cmp2, %land.rhs ]
  %land.ext = zext i1 %2 to i32
  %conv = trunc i32 %land.ext to i8
  ret i8 %conv
}

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
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([7 x i8]* @.str313, i32 0, i32 0), i8* %0)
  %1 = load i8** %in.addr, align 4
  %call1 = call i32 @strlen(i8* %1) #4
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
  %call2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([6 x i8]* @.str414, i32 0, i32 0), i32 %conv)
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
  %call5 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([6 x i8]* @.str414, i32 0, i32 0), i32 %conv4)
  %call6 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([2 x i8]* @.str515, i32 0, i32 0))
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
  %call = call i32 @strlen(i8* %0) #4
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
attributes #1 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind readonly }
attributes #5 = { nounwind }
attributes #6 = { noreturn nounwind }

!llvm.ident = !{!0, !0}

!0 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}