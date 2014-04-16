; ModuleID = 'test.c'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"
define i32 @main() nounwind uwtable {
%"a@102" = alloca i32
store i32 1, i32* %"a@102"
%"t@@119" = alloca i32
%1 = load i32* %"a@102"
store i32 %1, i32* %"t@@119"
%"t@@120" = alloca i32
%2 = load i32* %"t@@119"
store i32 %2, i32* %"t@@120"
%"t@@121" = alloca i32
%3 = load i32* %"a@102"
store i32 %3, i32* %"t@@121"
%"t@@122" = alloca i32
%4 = load i32* %"t@@121"
store i32 %4, i32* %"t@@122"
%"t@@123" = alloca i1
%5 = load i32* %"t@@120"
%6 = load i32* %"t@@122"
%7 = icmp ne i32 %5, %6
store i1 %7, i1* %"t@@123"
%8 = load i1* %"t@@123"
br i1 %8, label %9, label %11
; <label>:9
	%"10" = alloca i32
; <label>:11
	store i1 %7, i1* %"t@@123"
ret i32 0
}
