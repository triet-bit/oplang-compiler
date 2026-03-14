.source Main.java
.class public Main
.super java/lang/Object

.method public static <clinit>()V
Label0:
	return
Label1:
.limit stack 10
.limit locals 0
.end method

.method public <init>()V
.var 0 is this LMain; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 11
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is i [I from Label0 to Label1
	iconst_1
	newarray int
	dup
	pop
	astore_1
	iconst_0
	aload_1
	swap
	iconst_0
	swap
	iastore
Label4:
	aload_1
	iconst_0
	iaload
	iconst_5
	if_icmpgt Label3
	aload_1
	iconst_0
	iaload
	invokestatic io/writeInt(I)V
Label2:
	aload_1
	dup
	iconst_0
	iaload
	iconst_1
	iadd
	iconst_0
	swap
	iastore
	goto Label4
Label3:
	return
Label1:
.limit stack 14
.limit locals 2
.end method

.method public destructor()V
.var 0 is this LMain; from Label0 to Label1
Label0:
	return
Label1:
.limit stack 10
.limit locals 1
.end method
