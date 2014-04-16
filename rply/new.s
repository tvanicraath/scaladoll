; ModuleID = 'new.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"hello\0A\00", align 1
@.str1 = private unnamed_addr constant [8 x i8] c"hello2\0A\00", align 1
@.str2 = private unnamed_addr constant [3 x i8] c"%d\00", align 1

define i32 @main() nounwind uwtable {
  %x = alloca i32, align 4
  %y = alloca float, align 4
  %1 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0))
  %2 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([8 x i8]* @.str1, i32 0, i32 0))
  store i32 909090909, i32* %x, align 4
  %3 = load i32* %x, align 4
  %4 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([3 x i8]* @.str2, i32 0, i32 0), i32 %3)
  store float 0x4002C3C9E0000000, float* %y, align 4
  %5 = load float* %y, align 4
  %6 = fpext float %5 to double
  ret i32 0
}

declare i32 @printf(i8*, ...)
