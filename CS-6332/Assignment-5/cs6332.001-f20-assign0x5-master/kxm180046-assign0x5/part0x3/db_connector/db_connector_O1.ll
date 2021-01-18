; ModuleID = 'db_connector_O1.bc'
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
@str = private unnamed_addr constant [24 x i8] c"Input error, exiting...\00"
@str1 = private unnamed_addr constant [24 x i8] c"Input error, exiting...\00"

; Function Attrs: nounwind
define i8* @redactPass(i8* nocapture readonly %pass) #0 {
entry:
  %call = tail call i32 @strlen(i8* %pass) #5
  %call1 = tail call i8* @strncpy(i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0), i8* %pass, i32 %call) #4
  %sub = add nsw i32 %call, -2
  %cmp5 = icmp sgt i32 %sub, 0
  br i1 %cmp5, label %for.cond.for.end_crit_edge, label %for.end

for.cond.for.end_crit_edge:                       ; preds = %entry
  %0 = add i32 %call, -2
  call void @llvm.memset.p0i8.i32(i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 1), i8 42, i32 %0, i32 1, i1 false)
  br label %for.end

for.end:                                          ; preds = %for.cond.for.end_crit_edge, %entry
  ret i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0)
}

; Function Attrs: nounwind readonly
declare i32 @strlen(i8* nocapture) #1

; Function Attrs: nounwind
declare i8* @strncpy(i8*, i8* nocapture readonly, i32) #0

; Function Attrs: nounwind
define i32 @main(i32 %argc, i8** nocapture readnone %argv) #0 {
entry:
  %cmd = alloca [80 x i8], align 1
  %user = alloca [16 x i8], align 1
  %pass = alloca [16 x i8], align 1
  call void bitcast (void (...)* @banner to void ()*)() #4
  %call = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([17 x i8]* @.str2, i32 0, i32 0)) #4
  %arraydecay = getelementptr inbounds [16 x i8]* %user, i32 0, i32 0
  %0 = load %struct._IO_FILE** @stdin, align 4
  %call1 = call i8* @fgets(i8* %arraydecay, i32 16, %struct._IO_FILE* %0) #4
  %cmp = icmp eq i8* %call1, null
  br i1 %cmp, label %if.else, label %if.then

if.then:                                          ; preds = %entry
  %call3 = call i32 @strlen(i8* %arraydecay) #5
  %sub = add i32 %call3, -1
  %arrayidx = getelementptr inbounds [16 x i8]* %user, i32 0, i32 %sub
  store i8 0, i8* %arrayidx, align 1
  %call5 = call i8* @getpass(i8* getelementptr inbounds ([10 x i8]* @.str4, i32 0, i32 0)) #4
  %cmp6 = icmp eq i8* %call5, null
  br i1 %cmp6, label %if.else14, label %if.then7

if.else:                                          ; preds = %entry
  %puts = call i32 @puts(i8* getelementptr inbounds ([24 x i8]* @str, i32 0, i32 0))
  call void @exit(i32 1) #6
  unreachable

if.then7:                                         ; preds = %if.then
  %arraydecay8 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 0
  %call9 = call i32 @strlen(i8* %arraydecay8) #5
  %sub10 = add i32 %call9, -1
  %arrayidx11 = getelementptr inbounds [16 x i8]* %pass, i32 0, i32 %sub10
  store i8 0, i8* %arrayidx11, align 1
  %call13 = call i8* @strncpy(i8* %arraydecay8, i8* %call5, i32 16) #4
  %call19 = call signext i8 @isValid(i8* %arraydecay, i8* %arraydecay8) #4
  %tobool = icmp eq i8 %call19, 0
  br i1 %tobool, label %if.then20, label %while.body.preheader

if.else14:                                        ; preds = %if.then
  %puts2 = call i32 @puts(i8* getelementptr inbounds ([24 x i8]* @str1, i32 0, i32 0))
  call void @exit(i32 1) #6
  unreachable

if.then20:                                        ; preds = %if.then7
  %1 = load %struct._IO_FILE** @stderr, align 4
  %2 = call i32 @fwrite(i8* getelementptr inbounds ([42 x i8]* @.str5, i32 0, i32 0), i32 41, i32 1, %struct._IO_FILE* %1) #7
  %3 = load i8** getelementptr inbounds (%struct.cred_t* @cred_default, i32 0, i32 0), align 4
  %call23 = call i8* @strncpy(i8* %arraydecay, i8* %3, i32 16) #4
  %4 = load i8** getelementptr inbounds (%struct.cred_t* @cred_default, i32 0, i32 1), align 4
  %call25 = call i8* @strncpy(i8* %arraydecay8, i8* %4, i32 16) #4
  br label %while.body.preheader

while.body.preheader:                             ; preds = %if.then20, %if.then7
  %call293 = call i8* @redactPass(i8* %arraydecay8)
  %call304 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([50 x i8]* @.str6, i32 0, i32 0), i8* %arraydecay, i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0)) #4
  %call315 = call signext i8 bitcast (i8 (...)* @askYesOrNo to i8 ()*)() #4
  %tobool326 = icmp eq i8 %call315, 0
  br i1 %tobool326, label %if.then33, label %if.end35.lr.ph

if.end35.lr.ph:                                   ; preds = %while.body.preheader
  %arraydecay36 = getelementptr inbounds [80 x i8]* %cmd, i32 0, i32 0
  br label %if.end35

if.then33:                                        ; preds = %if.end35, %while.body.preheader
  %5 = load %struct._IO_FILE** @stderr, align 4
  %6 = call i32 @fwrite(i8* getelementptr inbounds ([13 x i8]* @.str7, i32 0, i32 0), i32 12, i32 1, %struct._IO_FILE* %5) #7
  ret i32 0

if.end35:                                         ; preds = %if.end35, %if.end35.lr.ph
  %call39 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %arraydecay36, i32 80, i8* getelementptr inbounds ([31 x i8]* @.str8, i32 0, i32 0), i8* %arraydecay8, i8* getelementptr inbounds ([14 x i8]* @.str9, i32 0, i32 0), i8* %arraydecay) #4
  %call41 = call i32 @system(i8* %arraydecay36) #4
  %call29 = call i8* @redactPass(i8* %arraydecay8)
  %call30 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([50 x i8]* @.str6, i32 0, i32 0), i8* %arraydecay, i8* getelementptr inbounds ([16 x i8]* @pass_buf, i32 0, i32 0)) #4
  %call31 = call signext i8 bitcast (i8 (...)* @askYesOrNo to i8 ()*)() #4
  %tobool32 = icmp eq i8 %call31, 0
  br i1 %tobool32, label %if.then33, label %if.end35
}

declare void @banner(...) #2

; Function Attrs: nounwind
declare i32 @printf(i8* nocapture readonly, ...) #0

; Function Attrs: nounwind
declare i8* @fgets(i8*, i32, %struct._IO_FILE* nocapture) #0

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

declare i8* @getpass(i8*) #2

declare signext i8 @isValid(i8*, i8*) #2

declare signext i8 @askYesOrNo(...) #2

; Function Attrs: nounwind
declare i32 @snprintf(i8* nocapture, i32, i8* nocapture readonly, ...) #0

declare i32 @system(i8* nocapture readonly) #2

; Function Attrs: nounwind
declare i32 @puts(i8* nocapture readonly) #4

; Function Attrs: nounwind
declare i32 @fwrite(i8* nocapture, i32, i32, %struct._IO_FILE* nocapture) #4

; Function Attrs: nounwind
declare void @llvm.memset.p0i8.i32(i8* nocapture, i8, i32, i32, i1) #4

attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind }
attributes #5 = { nounwind readonly }
attributes #6 = { noreturn nounwind }
attributes #7 = { cold }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}
