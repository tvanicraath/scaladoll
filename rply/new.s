; ModuleID = 'new.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [7 x i8] c"%f rac\00", align 1

define i32 @main() nounwind uwtable {
  %x = alloca float, align 4
  store float 2.000000e+00, float* %x, align 4
  %1 = load float* %x, align 4
  %2 = fpext float %1 to double
  %3 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([7 x i8]* @.str, i32 0, i32 0), double %2)
  ret i32 0
}

declare i32 @printf(i8*, ...)
