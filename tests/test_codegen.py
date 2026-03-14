"""
Test cases for OPLang code generation.
This file contains test cases for the code generator.
Students should add more test cases here.
"""

from src.utils.nodes import *
from utils import CodeGenerator, ASTGenerator

def test_001():
    ast = """
class Main {
    static void main() {
        io.writeStrLn("Hello World");
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "Hello World"


# def test_002():
#     ast = """
# class Main {
#     static void main() {
#         io.writeIntLn(io.readInt());
#         io.writeInt(1);
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2025\n1"

# def test_003():
#     ast = """
# class Main {
#     static void main() {
#         io.writeFloatLn(io.readFloat());
#         io.writeFloat(1.0);
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2026.2025\n1.0"

# def test_004():
#     ast = """
# class Main {
#     static void main() {
#         io.writeFloatLn(io.readFloat());
#         io.writeFloat(1.0);
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2026.2025\n1.0"

# def test_005():
#     ast = """
# class Main {
#     static void main() {
#         io.writeBoolLn(io.readBool());
#         io.writeBool(false);
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "true\nfalse"

# def test_006():
#     ast = """
# class Main {
#     static void main() {
#         io.writeStrLn(io.readStr());
#         io.writeStr("bye");
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "VOTIEN-PPL-HK251\nbye"

def test_007():
    ast = """
class Main {
    static int foo() {return 1;}
    static void main() {
        io.writeInt(Main.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_008():
    ast = """
class Main {
    static int a := 1;
    static void main() {
        io.writeInt(Main.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_009():
    ast = """
class Main {
    static int a := 1;
    static void main() {
        io.writeInt(Main.b);
    }
    static int b := Main.a;
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_010():
    ast = """
class A {
    static int a := 1;
}
class X {
    static void main() {
        io.writeInt(A.a);        
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_011():
    ast = """
class A {
    static int foo(){return 1;}
}
class X {
    static void main() {
        io.writeInt(A.foo());        
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"


def test_012():
    ast = """
class A {
    static void main() {
        int a := 1;
        float b := 1.2;
        boolean c := true;
        string d := "votien";
        io.writeInt(a);    
        io.writeFloat(b); 
        io.writeBool(c);
        io.writeStr(d);       
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "11.2truevotien"

def test_013():
    ast = """
class X {
    static void main() {
        int a := 1;
        a := 2;
        io.writeInt(a);         
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_014():
    ast = """
class X {
    static void main() {
        int a;
        {
            a := 2;
        }
        io.writeInt(a);         
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_015():
    ast = """
class X {
    static void main() {
        int a := 1;
        {
            int a;
            a := 2;
            io.writeInt(a);  
        }
        io.writeInt(a);         
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "21"

def test_016():
    ast = """
class X {
    static void foo(int a){
        io.writeInt(a);
        a := 1;
        io.writeInt(a);
    }
    static void main() {
        int a := 2;
        X.foo(a);
        io.writeInt(a);      
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "212"

def test_017():
    ast = """
class X {
    static void main() {
        int a := 2, b := 3;
        io.writeInt(a);   
        io.writeInt(b);    
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "23"

def test_017():
    ast = """
class A {
    int a;
    A(){
        this.a := 5;
    }
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_018():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
}

class X {
    static void main() {
        A a := new A(2);
        io.writeInt(a.a);
        a.a := 4;
        io.writeInt(a.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "24"

def test_019():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
    int foo(){
        return this.a;
    }
}

class X {
    static void main() {
        A a := new A(5);
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_020():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
    int foo(){
        return this.coo();
    }
    int coo(){
        return this.a;
    }
}

class X {
    static void main() {
        A a := new A(5);
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_021():
    ast = """

class A {
    int a;
    A(int a){this.a := a;}
}

class B {
    A b;
    B(int a){this.b := new A(a);}
}
class X {
    static void main() {
        B b := new B(5);
        io.writeInt(b.b.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_022():
    ast = """

class A {
    int a;
    A(int a){this.a := a;}
}

class B {
    B(int a){this.b := new A(a);}
    A b;
}
class X {
    static void main() {
        B b := new B(5);
        io.writeInt(b.b.a);
        b.b.a := 2;
        io.writeInt(b.b.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "52"

def test_023():
    ast = """
class A {
    int a := 1;
    A(){}
    int foo(){return this.a;}
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_024():
    ast = """
class A {
    int a := 1;
    A(){this.a := 2;}
    int foo(){return this.a;}
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_025():
    ast = """
class A {
    int a := 1;
    A(int a){
        io.writeInt(this.a);
    }
}

class X {
    static void main() {
        A a := new A(2);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_026():
    ast = """
class X {
    static void main() {
        int a := 3;
        io.writeInt(a - 1 + 2);
        io.writeFloat(1.5 - 0.25 + 0.75);
        io.writeFloat(1.5 - 1);
        io.writeFloat(1 - 0.5);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "42.00.50.5"

def test_028():
    ast = """
class X {
    static void main() {
        int a := 5;
        io.writeInt(a % 2);
        io.writeInt(a \\ 2);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12"

def test_029():
    ast = """
class X {
    static boolean foo(){
        io.writeInt(3);
        return true;
    }

    static void main() {
        io.writeBool(true && X.foo());
        io.writeBool(false && X.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "3truefalse"

def test_030():
    ast = """
class X {
    static boolean foo(){
        io.writeInt(3);
        return true;
    }

    static void main() {
        io.writeBool(true || X.foo());
        io.writeBool(false || X.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "true3true"

def test_031():
    ast = """
class X {
    static void main() {
        io.writeBool(true == true);
        io.writeBool(false == true);
        io.writeBool(true != true);
        io.writeBool(false != true);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truefalsefalsetrue"

def test_032():
    ast = """
class X {
    static void main() {
        io.writeBool(1 == 1);
        io.writeBool(1 != 2);
        io.writeBool(1 != 1);
        io.writeBool(2 != 1);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truetruefalsetrue"


def test_033():
    ast = """
class X {
    static void main() {
        io.writeBool(1 > 1);
        io.writeBool(1 < 1.2);
        io.writeBool(2.3 >= 2);
        io.writeBool( 2 < 3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "falsetruetruetrue"

def test_034():
    ast = """
class X {
    static void main() {
        io.writeBool(1 > 1);
        io.writeBool(1 < 1.2);
        io.writeBool(2.3 >= 2);
        io.writeBool( 2 < 3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "falsetruetruetrue"

def test_035():
    ast = """
class X {
    static void main() {
        io.writeStr("vo" ^ "tien");
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "votien"


def test_035():
    ast = """
class X {
    static void main() {
        io.writeBool(!!!true);
        io.writeInt(---+3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "false-3"

def test_036():
    ast = """
class X {
    static void main() {
        int[5] numbers := {1, 2, 3, 4, 5};
        io.writeInt(numbers[2]);
        io.writeInt(numbers[0]);
        io.writeInt(numbers[4]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "315"

def test_037():
    ast = """
class X {
    static void main() {
        boolean[2] a := {true, false};
        float[2] b := {1.2, 2.2};
        string[2] c := {"a", "b"};

        io.writeBool(a[0]);
        io.writeBool(a[1*1]);
        io.writeFloat(b[0]);
        io.writeFloat(b[2 \\ 2]);
        io.writeStr(c[0]);
        io.writeStr(c[0+1]);   
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truefalse1.22.2ab"

def test_038():
    ast = """
class X {
    static void main() {
        int[2] a := {0,0};

        a[1] := 2;
        io.writeInt(a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_039():
    ast = """
class X {
    static void foo(int[2] a){
        a[1] := 2;
    }
    static void main() {
        int[2] a := {0,0};
        X.foo(a);
        io.writeInt(a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_040():
    ast = """
class X {
    static int[2] a := {0,0};
    static void main() {
        X.a[1] := 2;
        io.writeInt(X.a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_041():
    ast = """
class X {
    static int[2] a := {0,0};
    static void main() {
        io.writeInt(X.a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "0"

def test_042():
    ast = """
class X {
    static void main() {
        if (1 == 1) then {io.writeInt(1);}
        if (1 > 2) then {io.writeInt(2);}
        if (true) then {io.writeInt(3);} else {io.writeInt(4);}
        if (false) then {io.writeInt(5);} else {io.writeInt(6);}
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "136"

def test_043():
    ast = """
class X {
    static void main() {
        int a := 2, b := 1, c := 3;
        int max;

        if (a > b) then {
            if (a > c) then {
                max := a;
            } else {
                max := c;
            }
        } else {
            if (b > c) then {
                max := b;
            } else {
                max := c;
            }
        }

        io.writeInt(max);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "3"

def test_044():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
            io.writeInt(i);
        }
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12345"

def test_045():
    ast = """
class X {
    static void main() {
        int i;
        for i := 5 downto 1 do { 
            io.writeInt(i);
        }
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "54321"

def test_046():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
             if (i == 3) then {break;}
            io.writeInt(i);
        }
        io.writeInt(i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "123"

def test_047():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
            if (i == 3) then {continue;}
            io.writeInt(i);
        }
        io.writeInt(i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12456"

def test_048():
    ast = """
class Shape {
    Shape(){}
    float getArea(){
        return 1.0;
    }
}

class Rectangle extends Shape {
    Rectangle(){}
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeFloatLn(s.getArea());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1.0"

def test_049():
    ast = """
class Shape {
    int i := 0;
    Shape(){}
    int getArea(){
        return this.i;
    }
}

class Rectangle extends Shape {
    Rectangle(){this.i := 1;}
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeIntLn(s.getArea());
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n1"

def test_050():
    ast = """
class Shape {
    Shape(){}
    int getArea(){
        return 0;
    }
}

class Rectangle extends Shape {
    int i := 0;
    Rectangle(){this.i := 1;}
    int getArea(){
        return this.i;
    }
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeIntLn(s.getArea());
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n1"

def test_051():
    ast = """
class Shape {
    Shape(){}
    int getArea(){return 0; }
}

class Rectangle extends Shape {
    Rectangle(){}
    int getArea(){return 1;}
}

class Triangle extends Shape {
    Triangle(){}
    int getArea(){return 2;}
}

class X {
    static void main() {
        Shape s := new Rectangle();
        io.writeIntLn(s.getArea());
        s := new Triangle();
        io.writeIntLn(s.getArea());
        s := new Shape();
        io.writeIntLn(s.getArea());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n2\n0"

def test_052():
    ast = """
class Shape {
    int i := 0;
    Shape(int i){this.i:=i;}
    int getArea(){return this.i;} 
    Shape(){}
}

class Rectangle extends Shape {
    Rectangle(int i){}
    int getArea(){return this.i;}   
}


class X {
    static void main() {
        Shape s := new Rectangle(1);
        io.writeIntLn(s.i);
        s := new Shape();
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n0"

# def test_053():
#     ast = """
def test_014_():
    ast = """
class X {
    static void main() {
        int a;
        {
            a := 2;
        }
        io.writeInt(a);         
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_015_():
    ast = """
class X {
    static void main() {
        int a := 1;
        {
            int a;
            a := 2;
            io.writeInt(a);  
        }
        io.writeInt(a);         
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "21"

def test_016_():
    ast = """
class X {
    static void foo(int a){
        io.writeInt(a);
        a := 1;
        io.writeInt(a);
    }
    static void main() {
        int a := 2;
        X.foo(a);
        io.writeInt(a);      
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "212"

def test_017_():
    ast = """
class X {
    static void main() {
        int a := 2, b := 3;
        io.writeInt(a);   
        io.writeInt(b);    
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "23"

def test_017_cont():
    ast = """
class A {
    int a;
    A(){
        this.a := 5;
    }
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_018_():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
}

class X {
    static void main() {
        A a := new A(2);
        io.writeInt(a.a);
        a.a := 4;
        io.writeInt(a.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "24"

def test_019_():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
    int foo(){
        return this.a;
    }
}

class X {
    static void main() {
        A a := new A(5);
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_020_():
    ast = """
class A {
    int a;
    A(int a){
        this.a := a;
    }
    int foo(){
        return this.coo();
    }
    int coo(){
        return this.a;
    }
}

class X {
    static void main() {
        A a := new A(5);
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_021_():
    ast = """

class A {
    int a;
    A(int a){this.a := a;}
}

class B {
    A b;
    B(int a){this.b := new A(a);}
}
class X {
    static void main() {
        B b := new B(5);
        io.writeInt(b.b.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "5"

def test_022_():
    ast = """

class A {
    int a;
    A(int a){this.a := a;}
}

class B {
    B(int a){this.b := new A(a);}
    A b;
}
class X {
    static void main() {
        B b := new B(5);
        io.writeInt(b.b.a);
        b.b.a := 2;
        io.writeInt(b.b.a);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "52"

def test_023_():
    ast = """
class A {
    int a := 1;
    A(){}
    int foo(){return this.a;}
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_024_():
    ast = """
class A {
    int a := 1;
    A(){this.a := 2;}
    int foo(){return this.a;}
}

class X {
    static void main() {
        A a := new A();
        io.writeInt(a.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_025_():
    ast = """
class A {
    int a := 1;
    A(int a){
        io.writeInt(this.a);
    }
}

class X {
    static void main() {
        A a := new A(2);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1"

def test_026_():
    ast = """
class X {
    static void main() {
        int a := 3;
        io.writeInt(a - 1 + 2);
        io.writeFloat(1.5 - 0.25 + 0.75);
        io.writeFloat(1.5 - 1);
        io.writeFloat(1 - 0.5);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "42.00.50.5"

# def test_027_():
#     ast = """
# class X {
#     static void main() {
#         int a := 3;
#         io.writeInt(a * 2 / 3);
#         io.writeFloat(1.25 * 4.0);
#         io.writeFloat(4.4/2);
#         io.writeFloat(2 * 1.1);
#     }
# }
# """
#     assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "25.02.22.2"

def test_028_():
    ast = """
class X {
    static void main() {
        int a := 5;
        io.writeInt(a % 2);
        io.writeInt(a \\ 2);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12"

def test_029_():
    ast = """
class X {
    static boolean foo(){
        io.writeInt(3);
        return true;
    }

    static void main() {
        io.writeBool(true && X.foo());
        io.writeBool(false && X.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "3truefalse"

def test_030_():
    ast = """
class X {
    static boolean foo(){
        io.writeInt(3);
        return true;
    }

    static void main() {
        io.writeBool(true || X.foo());
        io.writeBool(false || X.foo());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "true3true"

def test_031_():
    ast = """
class X {
    static void main() {
        io.writeBool(true == true);
        io.writeBool(false == true);
        io.writeBool(true != true);
        io.writeBool(false != true);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truefalsefalsetrue"

def test_032_():
    ast = """
class X {
    static void main() {
        io.writeBool(1 == 1);
        io.writeBool(1 != 2);
        io.writeBool(1 != 1);
        io.writeBool(2 != 1);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truetruefalsetrue"


def test_033_():
    ast = """
class X {
    static void main() {
        io.writeBool(1 > 1);
        io.writeBool(1 < 1.2);
        io.writeBool(2.3 >= 2);
        io.writeBool( 2 < 3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "falsetruetruetrue"

def test_034_():
    ast = """
class X {
    static void main() {
        io.writeBool(1 > 1);
        io.writeBool(1 < 1.2);
        io.writeBool(2.3 >= 2);
        io.writeBool( 2 < 3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "falsetruetruetrue"

def test_035_():
    ast = """
class X {
    static void main() {
        io.writeStr("vo" ^ "tien");
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "votien"


def test_035_cont():
    ast = """
class X {
    static void main() {
        io.writeBool(!!!true);
        io.writeInt(---+3);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "false-3"

def test_036_():
    ast = """
class X {
    static void main() {
        int[5] numbers := {1, 2, 3, 4, 5};
        io.writeInt(numbers[2]);
        io.writeInt(numbers[0]);
        io.writeInt(numbers[4]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "315"

def test_037_():
    ast = """
class X {
    static void main() {
        boolean[2] a := {true, false};
        float[2] b := {1.2, 2.2};
        string[2] c := {"a", "b"};

        io.writeBool(a[0]);
        io.writeBool(a[1*1]);
        io.writeFloat(b[0]);
        io.writeFloat(b[2 \\ 2]);
        io.writeStr(c[0]);
        io.writeStr(c[0+1]);   
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "truefalse1.22.2ab"

def test_038_():
    ast = """
class X {
    static void main() {
        int[2] a := {0,0};

        a[1] := 2;
        io.writeInt(a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_039_():
    ast = """
class X {
    static void foo(int[2] a){
        a[1] := 2;
    }
    static void main() {
        int[2] a := {0,0};
        X.foo(a);
        io.writeInt(a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_040_():
    ast = """
class X {
    static int[2] a := {0,0};
    static void main() {
        X.a[1] := 2;
        io.writeInt(X.a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "2"

def test_041_():
    ast = """
class X {
    static int[2] a := {0,0};
    static void main() {
        io.writeInt(X.a[1]);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "0"

def test_042_():
    ast = """
class X {
    static void main() {
        if (1 == 1) then {io.writeInt(1);}
        if (1 > 2) then {io.writeInt(2);}
        if (true) then {io.writeInt(3);} else {io.writeInt(4);}
        if (false) then {io.writeInt(5);} else {io.writeInt(6);}
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "136"

def test_043_():
    ast = """
class X {
    static void main() {
        int a := 2, b := 1, c := 3;
        int max;

        if (a > b) then {
            if (a > c) then {
                max := a;
            } else {
                max := c;
            }
        } else {
            if (b > c) then {
                max := b;
            } else {
                max := c;
            }
        }

        io.writeInt(max);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "3"

def test_044_():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
            io.writeInt(i);
        }
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12345"

def test_045_():
    ast = """
class X {
    static void main() {
        int i;
        for i := 5 downto 1 do { 
            io.writeInt(i);
        }
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "54321"

def test_046_():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
             if (i == 3) then {break;}
            io.writeInt(i);
        }
        io.writeInt(i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "123"

def test_047_():
    ast = """
class X {
    static void main() {
        int i;
        for i := 1 to 5 do { 
            if (i == 3) then {continue;}
            io.writeInt(i);
        }
        io.writeInt(i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "12456"

def test_048_():
    ast = """
class Shape {
    Shape(){}
    float getArea(){
        return 1.0;
    }
}

class Rectangle extends Shape {
    Rectangle(){}
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeFloatLn(s.getArea());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1.0"

def test_049_():
    ast = """
class Shape {
    int i := 0;
    Shape(){}
    int getArea(){
        return this.i;
    }
}

class Rectangle extends Shape {
    Rectangle(){this.i := 1;}
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeIntLn(s.getArea());
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n1"

def test_050_():
    ast = """
class Shape {
    Shape(){}
    int getArea(){
        return 0;
    }
}

class Rectangle extends Shape {
    int i := 0;
    Rectangle(){this.i := 1;}
    int getArea(){
        return this.i;
    }
}

class X {
    static void main() {
        Rectangle s := new Rectangle();
        io.writeIntLn(s.getArea());
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n1"

def test_051_():
    ast = """
class Shape {
    Shape(){}
    int getArea(){return 0; }
}

class Rectangle extends Shape {
    Rectangle(){}
    int getArea(){return 1;}
}

class Triangle extends Shape {
    Triangle(){}
    int getArea(){return 2;}
}

class X {
    static void main() {
        Shape s := new Rectangle();
        io.writeIntLn(s.getArea());
        s := new Triangle();
        io.writeIntLn(s.getArea());
        s := new Shape();
        io.writeIntLn(s.getArea());
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n2\n0"

def test_052_():
    ast = """
class Shape {
    int i := 0;
    Shape(int i){this.i:=i;}
    int getArea(){return this.i;} 
    Shape(){}
}

class Rectangle extends Shape {
    Rectangle(int i){}
    int getArea(){return this.i;}   
}


class X {
    static void main() {
        Shape s := new Rectangle(1);
        io.writeIntLn(s.i);
        s := new Shape();
        io.writeIntLn(s.i);
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n0"

def test_053_():
    ast = """
class Shape {
    Shape(){}
    ~Shape(){io.writeIntLn(1);}
}

class Rectangle extends Shape {
    Rectangle(){}
    ~Rectangle(){io.writeIntLn(2);}
}

class Triangle extends Shape {
    Triangle(){}
    ~Triangle(){io.writeIntLn(3);}
}


class X {
    static void main() {
        Shape a := new Triangle();
        {
            Shape b := new Shape();
            Rectangle c := new Rectangle();
        }
    }
}
"""
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "1\n1\n2\n1\n3"



def test_003_adt():
    source = """
class Main{
    static void main(){
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_004_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        io.writeInt(x);
        io.writeInt(y);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "56"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_005_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z := x + y;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "11"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_006_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z := x - y;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_007_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z := x * y;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_008_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := x * y;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_009_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y - x;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := 2 * y + 4 * (x - 3);
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_011_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y % 4;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_012_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y \\ 4;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_013_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y \\ 4;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_014_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y \\ x;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_015_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := y % x;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_016_adt():
    source = """
class Main{

    static void main(){
        int x := 5;
        int y := 6;
        int z;
        z := - x;
        io.writeInt(z);
        z := -y;
        io.writeInt(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "-5-6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_017_adt():
    source = """
class Main{

    static void main(){
        float x := 5.0;
        float y := 6.0;
        float z;
        z := -(- x);
        io.writeFloatLn(z);
        z := -(-y);
        io.writeFloatLn(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "5.0\n6.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_018_adt():
    source = """
class Main{

    static void main(){
        float x := 5.0;
        float y := 6.0;
        float z;
        z := x + y;
        io.writeFloatLn(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "11.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_019_adt():
    source = """
class Main{

    static void main(){
        float x := 5.0;
        float y := 6.0;
        float z;
        z := x + 2;
        io.writeFloatLn(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "7.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_020_adt():
    source = """
class Main{

    static void main(){
        float x := 5.0;
        float y := 6.0;
        float z;
        z := (2 + y) / (x/2) ;
        io.writeFloatLn(z);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "3.2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_021_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        if (t) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_022_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        if (f) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_023_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        if (t && f) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_024_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        if (t || f) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_025_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        int a := 1, b := 3;

        if (a == b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_026_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        int a := 1, b := 3;

        if (a > b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        int a := 1, b := 3;

        if (a >= b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_028_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        int a := 1, b := 3;

        if (a <= b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_029_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        int a := 1, b := 3;

        if (a < b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_030_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0, b := 3.0;

        if (a < b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_031_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0, b := 3.0;

        if (a <= b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_032_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0; 
        int b := 3;

        if (a <= b) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_033_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0; 
        int b := 3;

        if ((a >= b) && t) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0; 
        int b := 3;

        if (!((a >= b) && t)) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_035_adt():
    source = """
class Main{

    static void main(){
        boolean t := true;
        boolean f := false;

        float a := 1.0; 
        int b := 3;

        if (!((a >= b) && t)) then {
            io.writeStrLn("It is True");
        }
        else {
            io.writeStrLn("It is False");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "It is True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036_adt():
    source = """
class Main{

    static void main(){
        int i;
        for i := 0 to 5 do {
            io.writeInt(i);
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "012345"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_037_adt():
    source = """
class Main{

    static void main(){
        int i;
        for i := 0 to 5 do {
            io.writeStr("M");
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "MMMMMM"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_038_adt():
    source = """
class Main{

    static void main(){
        int i;
        for i := 10 downto 5 do {
            io.writeInt(i + 1);
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "11109876"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_039():
    source = """
class Main{

    static void main(){
        int i;
        for i := 10 downto 5 do {
            io.writeInt(i * 2 + 4);
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "242220181614"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040_adt():
    source = """
class Main{

    static void main(){
        int i;
        for i := 0 to 20 do {
            
            if (i % 2 == 0) then {
                io.writeInt(i);
            }
            
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "02468101214161820"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_041_adt():
    source = """
class Main{

    static void main(){
        int i;
        for i := 0 to 20 do {
            
            if ((i % 2 == 0) && (i % 3 == 0)) then {
                io.writeInt(i);
            }
            
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "061218"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_042_adt():
    source = """
class Main{

    static void main(){
        int start := 0 * 187902;
        int end := 5 * 2 + 4;
        int i;
        for i := start to end do {
            
            if ((i % 2 == 0) && (i % 3 == 0)) then {
                io.writeInt(i);
            }
            
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "0612"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043_adt():
    source = """
class Main{

    static void main(){
        int start := 0 * 187902;
        int end := 5 * 2 + 4
        int i;
        for i := 0*187902 to (5*2 + 4) do {
            
            if ((i % 2 == 0) && (i % 3 == 0)) then {
                io.writeInt(i);
            }
            
        }

    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "0612"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044_adt():
    source = """
class Main{

    static void main(){ 
        A a := new A(5,7);
        io.writeInt(a.x);
        io.writeInt(a.y);
    }
}   

class A {
    int x;
    int y;
    A(int x, y) {
        this.x := x;
        this.y := y;
    }
}
"""
    ast = ASTGenerator(source).generate()
    expected = "57"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045_adt():
    source = """
class Main{

    static void main(){ 
        A a := new A(5,7);
        io.writeInt(a.cal());
    }
}   

class A {
    int x;
    int y;
    A(int x, y) {
        this.x := x;
        this.y := y;
    }

    int cal() {
        return this.x * this.y;
    }
}

"""
    ast = ASTGenerator(source).generate()
    expected = "35"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_046_adt():
    source = """
class Main{

    static void main(){ 
        A a := new A(5,7);
        io.writeInt(A.calA(a));
    }
}   

class A {
    int x;
    int y;
    A(int x, y) {
        this.x := x;
        this.y := y;
    }

    int cal() {
        return this.x * this.y;
    }

    static int calA(A a){
        return a.x + a.y;
    }
}

"""
    ast = ASTGenerator(source).generate()
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_047_adt():
    source = """
class Main{

    static void main(){ 
        A a1 := new A(5,7);
        A a2 := new A(2,2);
        io.writeInt(A.calA(a1));
        io.writeInt(A.calA(a2));
    }
}   

class A {
    int x;
    int y;
    A(int x, y) {
        this.x := x;
        this.y := y;
    }

    int cal() {
        return this.x * this.y;
    }

    static int calA(A a){
        return a.x + a.y;
    }
}

"""
    ast = ASTGenerator(source).generate()
    expected = "124"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_048_adt():
    source = """

class MathUtils {

    static int fac_recursive(int k) {
        if (k == 1) then {
            return k;
        }

        return k * MathUtils.fac_recursive(k-1);
    }
}

class Main{

    static void main(){ 
        
        int result := MathUtils.fac_recursive(5);

        io.writeInt(result);
    }
}   


"""
    ast = ASTGenerator(source).generate()
    expected = "120"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_049_adt():
    source = """

class Main{

    static void main(){ 
        int[5] arr := {4,3,2,1,0};
        int i;
        for i:= 0 to 4 do {
            io.writeInt(arr[i]);
        }
    }
}   


"""
    ast = ASTGenerator(source).generate()
    expected = "43210"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_050_adt():
    source = """

class Main{

    static void main(){ 
        int[5] arr := {4,3,2,1,0};
        int i;

        for i:= 0 to 4 do {
            io.writeInt(arr[i]);
        }


        /* Modify array*/

        arr[0] := 6;
        arr[4] := 9;

        for i := 0 to 4 do {
            io.writeInt(arr[i]);
        }

    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "4321063219"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_051_adt():
    source = """

class A {
    int x;
    int y;

    int calsum() {
        return this.x + this.y;
    }

    A(int x, y) {
        this.x := x;
        this.y := y;
    }
}

class Main{

    static void main(){ 
        
        A a1 := new A(1,2);
        A a2 := new A(2,2);
        A a3 := new A(0,6);
        
        A[3] arr_A := {a1, a2, a3};
        
        int i;

        for i:= 0 to 2 do {
            io.writeInt(arr_A[i].calsum());
        }
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "346"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_052_adt():
    source = """

class A {
    int x;
    int y;

    int calsum() {
        return this.x + this.y;
    }
}

class B extends A {
    B(int x, y) {
        this.x := x;
        this.y := y;
    }
}

class Main{

    static void main(){ 
        
        B b1 := new B(1,2), b2 := new B(2,2), b3 := new B(0,6);


        A[3] arr_A := {b1, b2, b3};
        
        int i;

        for i:= 0 to 2 do {
            io.writeInt(arr_A[i].calsum());
        }
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "346"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_053_adt():
    source = """

class Shape {
    int width;
    int height;

    int calS() {
        return -1;
    } 
}

class Rectangle extends Shape {
    Rectangle (int width, height) {
        this.width := width;
        this.height := height;
    }

    int calS() {
        return this.width * this.height;
    }
} 

class Triangle extends Shape {
    Triangle (int width, height) {
        this.width := width;
        this.height := height;
    }

    int calS() {
        return (this.width * this.height)\\2;
    }
} 


class Main{

    static void main(){ 

        Shape s0 := new Shape();    
        Shape s1 := new Rectangle(2,2);
        Shape s2 := new Triangle(2,2);

        io.writeStr(">>>Shape:");
        io.writeInt(s0.calS());

        io.writeStr(">>>Rectangle:");
        io.writeInt(s1.calS());

        io.writeStr(">>>Triangle:");
        io.writeInt(s2.calS());

    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = ">>>Shape:-1>>>Rectangle:4>>>Triangle:2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_054_adt():
    source = """

class LinkedList {
    int value;
    LinkedList next;

    LinkedList(int value) {
        this.value := value;
    }

    LinkedList addNode (LinkedList next) {
        this.next := next;
        return next;
    }

    void print() {
        io.writeInt(this.value);
        if (this.value != -1) then {
            this.next.print();
        }
    }
}

class Main{

    static void main(){ 
        LinkedList l1 := new LinkedList(1),
                   l2 := new LinkedList(2),
                   l3 := new LinkedList(3),
                   endl := new LinkedList(-1);

        l1.addNode(l2).addNode(l3).addNode(endl);

        l1.print();

    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "123-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_055_adt():
    source = """
class Main{

    static void main(){ 
        string str1 := "Hello", str2 := "World";
        string cstr := str1 ^ str2;
        io.writeStr(cstr);
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "HelloWorld"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_056_adt():
    source = """
class Main{

    static void main(){ 
        # Nested If
        if (true) then {
            if (true) then {
                if (true) then {
                    io.writeStr("TTT");
                }
            }
        }
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "TTT"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_057_adt():
    source = """

# Constructor Madness

class A {
    A() {
        io.writeStr("A");
    }
}

class B extends A {
    B() {
        io.writeStr("B");
    }
}

class Main{

    static void main(){
        A b := new B();
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "AB"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_058_adt():
    source = """

# Early init 

class K {
    int x := 5;
    int y := 12 - this.x;
}

class Main{

    static void main(){
        K k := new K();
        io.writeInt(k.x);
        io.writeInt(k.y);
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "57"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_059_adt():
    source = """

class CONSTANT {
    static final float PI := 3.14;
    static final float e := 2.17;
    static final float h := 6.62;
}

class Main{


    static void main(){     
        io.writeFloat(CONSTANT.PI);        
        io.writeStr(" ");
        io.writeFloat(CONSTANT.e);        
        io.writeStr(" ");
        io.writeFloat(CONSTANT.h);        
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "3.14 2.17 6.62"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_060_adt():
    source = """

class Story {
    static final string s1 := "You dont know how beautiful you are. You think no one would look at you without the kohl on your face, the gold in your hair, the corset cinched around your vanishing center. You thought coming here with a cloak on bent shoulders would make me see a crone, as if your unpainted skin held one single wrinkle. If you walked through the village instead of the wood, men would fight for the right to propose to you. Without any of the trappings and rituals you feel forced to maintain, you would still be the most beautiful thing any of them had ever seen."
}

class Main{

    static void main(){ 
        io.writeStr(Story.s1);
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "You dont know how beautiful you are. You think no one would look at you without the kohl on your face, the gold in your hair, the corset cinched around your vanishing center. You thought coming here with a cloak on bent shoulders would make me see a crone, as if your unpainted skin held one single wrinkle. If you walked through the village instead of the wood, men would fight for the right to propose to you. Without any of the trappings and rituals you feel forced to maintain, you would still be the most beautiful thing any of them had ever seen."
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_061_adt():
    source = """

class Main{


    static void main(){     

        int i,j;

        for i := 0 to 3 do {
            for j := 1 to 3 do {
                io.writeInt(i);
                io.writeInt(j);
                io.writeStr(" ");
            }
        }

    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "01 02 03 11 12 13 21 22 23 31 32 33"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_062_adt():
    source = """

class Main{


    static void main(){     

        int i, j := 5;

        for i := 0 to 10 do {
            io.writeInt(i);
            if (i == j) then {
                break;
            }
        }

        io.writeInt(i);

    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "0123455"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_063_adt():
    source = """

class Main{


    static void main(){     

        int i;

        for i := 0 to 10 do {
            if (i % 2 != 0) then {
                continue;
            }
            io.writeInt(i);
        }
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "0246810"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_064_adt():
    source = """
class MHelper {
    static string get_special() {
        return "I am special!";
    }
}

class Main{

    static void main(){     
        io.writeStr(MHelper.get_special());
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "I am special!"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_065_adt():
    source = """
class MHelper {
    static string get_special() {
        return "I am special!";
    }
}

class Main{

    static void main(){     
        io.writeStr(MHelper.get_special() ^ " <3");
    }
}   

"""
    ast = ASTGenerator(source).generate()
    expected = "I am special! <3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_066_adt():
    source = """
class AM {
    static void modify_arr(int[5] iarr) {
        iarr[0] := 4;
        iarr[1] := 5;
        iarr[2] := 6;
    }
}

class Main{

    static void main(){     
        int[5] arr := {0,0,0,0,0}
        int i;
        AM.modify_arr(arr);
        for i := 0 to 4 do {
            io.writeInt(arr[i]);
        } 
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "45600"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_067_adt():
    source = """
class Factory {

    string place;
    string color;

    static Factory makeFactory() {
        Factory f := new Factory();
        f.place := "London";
        f.color := "Red";

        return f;
    }

}

class Main{

    static void main(){     
        Factory fm := Factory.makeFactory();
        io.writeStr(fm.place);
        io.writeStr(" ");
        io.writeStr(fm.color);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "London Red"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_068_adt():
    source = """
# Nested Structure [].

class Point {
    float x, y;
} 

class Main{

    static void main(){     
        Point p1 := new Point(),
              p2 := new Point();

        Point[2] point_arr := {p1, p2};

        p1.x := 0.0; 
        p1.y := 6.2;

        p2.x := 5.3;
        p2.y := 4.4;

        io.writeFloat(point_arr[0].x);
        io.writeStr(" ");
        io.writeFloat(point_arr[1].x);
        io.writeStr(" ");
        io.writeFloat(point_arr[0].y);
        io.writeStr(" ");
        io.writeFloat(point_arr[1].y);
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "0.0 5.3 6.2 4.4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_069_adt():
    source = """
class Point {
    float x, y;

    static float get_distance_s2(Point p1, p2) {
        return p1.x * p2.x + p1.y * p2.y;
    }
} 

class Main{

    static void main(){     
        Point p1 := new Point(),
              p2 := new Point();

        p1.x := 2.2; p1.y := 4.6;
        p2.x := 1.1; p2.y := 8.2;

        io.writeFloat(
            Point.get_distance_s2(p1,p2)
        );
    }
}   
"""
    ast = ASTGenerator(source).generate()
    expected = "40.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_070_adt():
    source = """class Main { 
        static void main() { 
            float x := -3.3; 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    ast = ASTGenerator(source).generate()
    expected = "negative"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_071_adt():
    source = """class Main { 
        static void main() { 
            float x := 45.3; 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    ast = ASTGenerator(source).generate()
    expected = "positive"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_072_adt():
    source = """class Main { 
        static void main() { 
            int i := 0;
            int j := 0;
            for i := 1 to 10 do { 
                j := j + i; 
            }

            io.writeInt(j);
        }
    }"""
    ast = ASTGenerator(source).generate()
    expected = "55"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_073_adt():
    source = """
    class Main { 
        static void main() { 
            int[3] arr := {1, 2, 3};
            int first;
            int i;
            first := arr[0];
            arr[1] := 42;

            for i := 0 to 2 do {
                io.writeInt(arr[i]);
            }
            io.writeInt(first);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "14231"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_074_adt():
    source = """
    
    class Rectangle {
        float length, width;
        static int count;
        
        # Default constructor
        Rectangle() {
            this.length := 1.0;
            this.width := 1.0;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # Copy constructor
        Rectangle(Rectangle other) {
            this.length := other.length;
            this.width := other.width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        # User-defined constructor
        Rectangle(float length, width) {
            this.length := length;
            this.width := width;
            Rectangle.count := Rectangle.count + 1;
        }
        
        float getArea() {
            return this.length * this.width;
        }
        
        static int getCount() {
            return Rectangle.count;
        }
    }

    class Main {
        static void main() {
            # Using different constructors
            Rectangle r1 := new Rectangle();           # Default constructor
            Rectangle r2 := new Rectangle(5.0, 3.0);  # User-defined constructor
            Rectangle r3 := new Rectangle(r2);        # Copy constructor
            
            io.writeFloatLn(r1.getArea());  # 1.0
            io.writeFloatLn(r2.getArea());  # 15.0
            io.writeFloatLn(r3.getArea());  # 15.0
            io.writeIntLn(Rectangle.getCount());  # 3
            
        }
    }

    """
    ast = ASTGenerator(source).generate()
    expected = "1.0\n15.0\n15.0\n3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_075_adt():
    source = """
    class Patient {
        string name;
        float heartRate;
        float temperature;

        Patient(string n; float hr; float t) {
            this.name := n; this.heartRate := hr; this.temperature := t;
        }
    }

    class HealthMonitor {
        void check(Patient p) {
            if ((p.heartRate < 60) || (p.heartRate > 100)) then
                io.writeStrLn("ALERT: " ^ p.name ^ " abnormal heart rate");
            if (p.temperature > 37.5) then
                io.writeStrLn("ALERT: " ^ p.name ^ " fever detected");
        }

    }

    class Main {
        static void main() {
            Patient a := new Patient("Alice", 120.0, 36.5);
            HealthMonitor hm := new HealthMonitor();
            hm.check(a);
        }
    }
    
    """
    ast = ASTGenerator(source).generate()
    expected = "ALERT: Alice abnormal heart rate"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_076_adt():
    source = """
    class Patient {
        string name;
        float heartRate;
        float temperature;

        Patient(string n; float hr; float t) {
            this.name := n; this.heartRate := hr; this.temperature := t;
        }
    }

    class HealthMonitor {
        void check(Patient p) {
            if ((p.heartRate < 60) || (p.heartRate > 100)) then
                io.writeStrLn("ALERT: " ^ p.name ^ " abnormal heart rate");
            if (p.temperature > 37.5) then
                io.writeStrLn("ALERT: " ^ p.name ^ " fever detected");
        }

    }

    class Main {
        static void main() {
            Patient a := new Patient("Alice", 50, 36.5);
            HealthMonitor hm := new HealthMonitor();
            hm.check(a);
        }
    }
    
    """
    ast = ASTGenerator(source).generate()
    expected = "ALERT: Alice abnormal heart rate"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_077_adt():
    source = """
    class Patient {
        string name;
        float heartRate;
        float temperature;

        Patient(string n; float hr; float t) {
            this.name := n; this.heartRate := hr; this.temperature := t;
        }
    }

    class HealthMonitor {
        void check(Patient p) {
            if ((p.heartRate < 60) || (p.heartRate > 100)) then
                io.writeStrLn("ALERT: " ^ p.name ^ " abnormal heart rate");
            if (p.temperature > 37.5) then
                io.writeStrLn("ALERT: " ^ p.name ^ " fever detected");
        }

    }

    class Main {
        static void main() {
            Patient a := new Patient("Alice", 70, 39.0);
            HealthMonitor hm := new HealthMonitor();
            hm.check(a);
        }
    }
    
    """
    ast = ASTGenerator(source).generate()
    expected = "ALERT: Alice fever detected"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_078_adt():
    source = """
    class Patient {
        string name;
        float heartRate;
        float temperature;

        Patient(string n; float hr; float t) {
            this.name := n; this.heartRate := hr; this.temperature := t;
        }
    }

    class HealthMonitor {
        void check(Patient p) {
            if ((p.heartRate < 60) || (p.heartRate > 100)) then
                io.writeStrLn("ALERT: " ^ p.name ^ " abnormal heart rate");
            if (p.temperature > 37.5) then
                io.writeStrLn("ALERT: " ^ p.name ^ " fever detected");
        }

    }

    class Main {
        static void main() {
            Patient a := new Patient("Alice", 70, 37.0);
            HealthMonitor hm := new HealthMonitor();
            hm.check(a);
        }
    }
    
    """
    ast = ASTGenerator(source).generate()
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_079_adt():
    source = """
    class Counter {
        static int count := 0;
        Counter() { Counter.count := Counter.count + 1; }
        static int getCount() { return Counter.count; }
    }

    class Main {
        static void main() {
            Counter c1 := new Counter();
            Counter c2 := new Counter();
            io.writeIntLn(Counter.getCount());   # 2
        }
    }

    """
    ast = ASTGenerator(source).generate()
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_080_adt():
    source = """
    class ArrayOps {
        static int sum(int[5] arr) {
            int s := 0;
            int i;
            for i := 0 to 4 do s := s + arr[i];
            return s;
        }
    }

    class Main {
        static void main () {
            int[5] a := {1, 2, 3, 4, 5};
            io.writeIntLn(ArrayOps.sum(a));   # 15
        }
    }

    """
    ast = ASTGenerator(source).generate()
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_081_adt():
    source = """
    class QuickSort {
        void swap(int[10] arr; int i, j) {
            int temp := arr[i];
            arr[i] := arr[j];
            arr[j] := temp;
        }

        int partition(int[10] arr; int low, high) {
            int pivot := arr[high];
            int i := low - 1;
            int j;
            for j := low to high - 1 do {
                if arr[j] < pivot then {
                    i := i + 1;
                    this.swap(arr, i, j);
                }
            }
            this.swap(arr, i + 1, high);
            return i + 1;
        }

        void sort(int[10] arr; int low, high) {
            if low < high then {
                int pi := this.partition(arr, low, high);
                this.sort(arr, low, pi - 1);
                this.sort(arr, pi + 1, high);
            }
        }

    }

    class Main {
        static void main() {
            int[10] arr := {10, 7, 8, 9, 1, 5, 3, 2, 6, 4};
            int i;
            QuickSort q := new QuickSort();
            q.sort(arr, 0, 9);
            for i := 0 to 9 do io.writeInt(arr[i]);
        }
    }

    """
    ast = ASTGenerator(source).generate()
    expected = "12345678910"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_082_adt():
    source = """
    class VendingMachine {
        int state := 0;   # 0=no coin, 1=has coin

        void insertCoin() {
            if this.state == 0 then {
                this.state := 1;
                io.writeStrLn("Coin inserted");
            } else io.writeStrLn("Already has coin");
        }

        void selectItem() {
            if this.state == 1 then {
                io.writeStrLn("Item dispensed");
                this.state := 0;
            } else io.writeStrLn("Insert coin first");
        }
    }

    class Main {
        static void main () {
            VendingMachine v := new VendingMachine();
            v.selectItem();
            v.insertCoin();
            v.selectItem();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Insert coin first\nCoin inserted\nItem dispensed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_083_adt():
    source = """
    class Vector {
        int[3] values := {0,0,0};

        Vector(int x, y, z) {
            this.values[0] := x;
            this.values[1] := y;
            this.values[2] := z;
        }

        int dot(Vector other) {
            return this.values[0]*other.values[0] + 
                   this.values[1]*other.values[1] +
                   this.values[2]*other.values[2];
        }

        Vector add(Vector other) {
            return new Vector(
                this.values[0]+other.values[0],
                this.values[1]+other.values[1],
                this.values[2]+other.values[2]
            );
        }

        void print() {
            int i;
            io.writeStr("(");
            for i := 0 to 2 do io.writeInt(this.values[i]);
            io.writeStr(")");
        }

    }

    class Main {
        static void main() {
            Vector v1 := new Vector(1,2,3);
            Vector v2 := new Vector(4,5,6);
            Vector v3 := v1.add(v2);
            v3.print();                   # (5,7,9)
            io.writeStr(" ");
            io.writeInt(v1.dot(v2));    # 32
        }
    }

    """
    ast = ASTGenerator(source).generate()
    expected = "(579) 32"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084_adt():
    source = """
    class Main {
        static void main() {
            io.writeStr("Hello");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_085_adt():
    source = """
    class SubsetSum {
        boolean solve(int[5] arr; int n; int target) {
            if target == 0 then return true;
            if n == 0 then return false;
            return this.solve(arr, n-1, target) || 
                   this.solve(arr, n-1, target-arr[n-1]);
        }
    }

    class Main {
        static void main () {
            int[5] arr := {3, 34, 4, 12, 5};
            int target := 9;
            if (new SubsetSum()).solve(arr, 5, target) then
                io.writeStrLn("Subset exists");
            else
                io.writeStrLn("No subset");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Subset exists"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_086_adt():
    source = """
    class BinaryStrings {

        string toBinaryRecursive(int n) {
            if (n == 0) then {
                return "0";
            }
            return this.toBinaryHelper(n);
        }

        string toBinaryHelper(int n) {
            
            string bin;

            if (n == 0) then {
                return "";
            }

            if (n % 2 == 0) then { bin := "0"; } else { bin := "1"; }

            return this.toBinaryHelper(n \\ 2) ^ bin;
        }
    }

    class Main {
        static void main () {
            io.writeStr(
                (new BinaryStrings()).toBinaryRecursive(3)
            );
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "11"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_087_adt():
    source = """
    class MathLib {
        static int add(int a, b) { return a + b; }
        static int mul(int a, b) { return a * b; }
        static int pow(int base, exp) {
            int res := 1;
            int i;
            for i := 1 to exp do res := res * base;
            return res;
        }
    }

    class Main {
        static void main () {
            io.writeIntLn(MathLib.add(3,4));
            io.writeIntLn(MathLib.mul(5,6));
            io.writeIntLn(MathLib.pow(2,10));
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "7\n30\n1024"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_088_adt():
    source = """
    class Individual {
        string name;
        int fitness;

        void print() {
            io.writeStr(this.name ^ ":");
            io.writeInt(this.fitness);
            io.writeStr(" ");
        }

        Individual(string name; int fitness) {
            this.name := name;
            this.fitness := fitness;
        }
    }

    class Main {
        static void main() {
            Individual id1 := new Individual("Alice", 102);
            Individual id2 := new Individual("Bob", 155);
            Individual id3 := new Individual("Kandy", 92);
            Individual id4 := new Individual("Julia", 88);
            Individual[4] idns := {id1, id2, id3, id4};
            int i;

            for i := 0  to 3 do
                idns[i].print();
        }
    }
"""
    ast = ASTGenerator(source).generate()
    expected = "Alice:102 Bob:155 Kandy:92 Julia:88"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_089_adt():
    source = """
    class Snake {
        int length := 1;

        void eat() {
            this.length := this.length + 1;
        }
    }

    class Main {
        static void main() {
            Snake s := new Snake();
            s.eat();
            s.eat();
            io.writeInt(s.length);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_090_adt():
    source = """
    class Main {
        static void main() {
            boolean b1 := (true || false) && (false && false);
            io.writeBool(b1);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_091_adt():
    source = """
    class VectorProduct {
        static float dot(float[3] v1, v2) {
            return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]* v2[2];
        }
    }

    class Main {
        static void main() {
            float[3] v1 := {1.1, 2.0, 3.5};
            float[3] v2 := {0.0, 5.0, 6.2};

            io.writeFloat(VectorProduct.dot(v1,v2));

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "31.699999"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_092_adt():
    source = """
    class VectorProduct {
        static float dot(float[3] v1, v2; int length) {
            int i;
            float sum := 0.0;
            for i := 0 to length - 1 do {
                sum := sum + v1[i] * v2[i];
            }  

            return sum;
        }
    }

    class Main {
        static void main() {
            float[3] v1 := {1.1, 2.0, 3.5};
            float[3] v2 := {0.0, 5.0, 6.2};

            io.writeFloat(VectorProduct.dot(v1, v2, 3));

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "31.699999"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_093_adt():
    source = """
    class VectorProduct {
        static float dot(float[3] v1, v2; int length) {
            if (length == 1) then return v1[0]*v2[0];

            return v1[length-1] * v2[length-1] + VectorProduct.dot(v1,v2,length - 1); 
        }
    }

    class Main {
        static void main() {
            float[3] v1 := {1.1, 2.0, 3.5};
            float[3] v2 := {0.0, 5.0, 6.2};

            io.writeFloat(VectorProduct.dot(v1, v2, 3));

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "31.699999"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_094_adt():
    source = """

    class Utils {
        static void slice(int[6] arr; int[3] result) {
            result := {arr[0], arr[1], arr[2]};
        }
    }

    class Main {
        static void main() { 
            int[6] arr := {1,2,3,4,5,6};
            int[3] sarr := {0,0,0};
            int i;
            
            Utils.slice(arr,sarr);

            for i := 0 to 2 do {
                io.writeInt(sarr[i]);
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "000"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_095_adt():
    source = """

    class Array {
        int[3] array;

        Array(int[3] array) {
            this.array := array;
        }

        int get(int i) {
            return this.array[i];
        }

    }

    class Utils {
        static Array initArray(int init) {
            int[3] init_arr := {0,0,0};
            int i;
            
            for i:= 0 to 2 do {
                init_arr[i] := init;
            }

            return new Array(init_arr);

        }
    }

    class Main {
        static void main() { 
            Array arr := Utils.initArray(9);
            int i;

            for i := 0 to 2 do {
                io.writeInt(arr.get(i));
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "999"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_096_adt():
    source = """

    class Main {
        static void main() { 
            float k := 12.0 / 6.0;

            if (k <= 2 + 0e-5) && (k >= 2 - 0e-5) then {
                io.writeInt(2);
            } else {
                io.writeInt(-1);
            }

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_097_adt():
    source = """

    class Main {
        static void main() { 
            float e := 2.71;
            float phi := 1.61;

            if (e >= phi) then {
                io.writeStr("e >= phi");
            }
            else {
                io.writeStr("HUM??");
            }

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "e >= phi"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_098_adt():
    source = """

    class Main {
        static void main() { 

            if (2.1369 >= 0.2225) then {
                io.writeStr("Expected");
            }
            else {
                io.writeStr("HUM??");
            }

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Expected"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_099_adt():
    source = """

    class MathUtils {
        static float power(float num; int p) {
            int i;
            float product := 1.0;
            
            if (p == 0) then return 1.0;

            for i := 1 to p do {
                product := product * num;
            }
            return product;
        }
    }

    class Main {
        static void main() { 

            if ( MathUtils.power(2.32, 3) >= 13) then {
                io.writeStr("NO");
            }
            else {
                io.writeStr("LessThan");
            }

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "LessThan"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_100_adt():
    source = """

    class DVector {
        int[2] vec;

        DVector(int[2] vec) {
            this.vec := vec;
        }

        int get(int i) {
            return this.vec[i];
        }
    }

    class TwoSum {
        static DVector twoSum(int[5] nums; int length; int target) {
            int i,j;
            for i := 0 to length - 1 do {
                for j:= 0 to length - 1 do {
                    if (nums[i] + nums[j] == target) then {
                        int[2] result := {nums[i], nums[j]};
                        return new DVector(result);
                    }
                }
            }

            return new DVector({0,0});
        }
    }

    class Main {
        static void main() { 
            int[5] arr := {1,2,2,6,7};
            DVector result := TwoSum.twoSum(arr,5,8);
            io.writeInt(result.get(0));
            io.writeInt(result.get(1));

        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "17"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_001_self():
    source = """
class Tester {
    # Hàm này in ra giá trị n và trả về true
    # Dùng để kiểm tra xem hàm có được gọi hay không
    static boolean check(int n) {
        io.writeInt(n);
        return true;
    }

    static void main() {
        # Test 1: OR Short-circuit
        # true || ... -> Vế phải KHÔNG được chạy -> Không in số 1
        if (true || Tester.check(1)) then 
            io.writeStr("pass1");
        else 
            io.writeStr("fail1");

        # Test 2: AND Short-circuit
        # false && ... -> Vế phải KHÔNG được chạy -> Không in số 2
        if (false && Tester.check(2)) then 
            io.writeStr("fail2");
        else 
            io.writeStr("pass2");

        # Test 3: Normal OR (No short-circuit)
        # false || ... -> Vế phải PHẢI chạy -> In số 3, trả về true -> In pass3
        if (false || Tester.check(3)) then 
            io.writeStr("pass3");
        else 
            io.writeStr("fail3");

        # Test 4: Normal AND (No short-circuit)
        # true && ... -> Vế phải PHẢI chạy -> In số 4, trả về true -> In pass4
        if (true && Tester.check(4)) then 
            io.writeStr("pass4");
        else 
            io.writeStr("fail4");
    }
}
"""
    ast = ASTGenerator(source).generate()
    expected = "pass1pass23pass34pass4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_var_decl_default_values():
    source = """
    class DefaultValues {
        int i;          # Default: 0
        float f;        # Default: 0.0
        boolean b;      # Default: false
        string s;       # Default: "" or null (tùy implement, thường là null/nil)
        
        void check() {
            io.writeInt(this.i);
            io.writeFloat(this.f);
            io.writeBool(this.b);
            # String chưa init là null, in ra có thể gây lỗi hoặc in "null"
            # Ta check 3 cái primitive trước
        }
    }
    
    class Main {
        static void main() {
            DefaultValues d := new DefaultValues();
            d.check();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Mong đợi: 0, 0.0, false
    expected = "00.0false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_var_decl_multiple():
    source = """
    class Main {
        static void main() {
            # a không init, b init = 10, c không init
            # Lưu ý: Local variable phải init trước khi dùng trong JVM chuẩn.
            # Ở đây ta test việc gán giá trị cho biến đã khai báo cùng dòng.
            int a := 1, b := 2, c := 3; 
            
            io.writeInt(a);
            io.writeInt(b);
            io.writeInt(c);
            
            a := b + c;
            io.writeInt(a);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "1235"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_var_assignment_coercion():
    source = """
    class Main {
        static void main() {
            float f1 := 10;      # Assign int literal to float variable
            int i := 5;
            float f2 := i;       # Assign int variable to float variable
            
            io.writeFloat(f1);
            io.writeFloat(f2);
            
            # Kiểm tra biểu thức hỗn hợp
            float f3 := i + 2;   # (int + int) -> int -> float
            io.writeFloat(f3);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "10.05.07.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_var_scope_shadowing():
    source = """
    class Shadow {
        int x := 100; # Class attribute
        
        void test() {
            io.writeInt(this.x); # 100
            
            int x := 200;        # Local var hides attribute
            io.writeInt(x);      # 200
            
            {
                int x := 300;    # Block var hides local var
                io.writeInt(x);  # 300
                
                x := 301;
                io.writeInt(x);  # 301
            }
            
            io.writeInt(x);      # 200 (Back to local scope)
            io.writeInt(this.x); # 100 (Attribute unaffected)
        }
    }
    
    class Main {
        static void main() {
            new Shadow().test();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "100200300301200100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_static_vs_instance_vars():
    source = """
    class Counter {
        static int globalCount := 0;
        int localCount := 0;
        
        void inc() {
            Counter.globalCount := Counter.globalCount + 1;
            this.localCount := this.localCount + 1;
        }
        
        void print() {
            io.writeInt(Counter.globalCount);
            io.writeInt(this.localCount);
        }
    }
    
    class Main {
        static void main() {
            Counter c1 := new Counter();
            Counter c2 := new Counter();
            
            c1.inc(); 
            c1.print(); # global=1, local=1
            
            c2.inc();
            c2.print(); # global=2, local=1 (local của c2 riêng biệt)
            
            c1.print(); # global=2, local=1 (check lại c1)
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "112121"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_assignment_inheritance():
    source = """
    class Parent {
        int getValue() { return 1; }
    }
    
    class Child extends Parent {
        int getValue() { return 2; }
    }
    
    class Main {
        static void main() {
            Parent p;
            Child c := new Child();
            
            p := new Parent();
            io.writeInt(p.getValue()); # 1
            
            p := c; # Assign Child to Parent variable
            io.writeInt(p.getValue()); # 2 (Polymorphism check)
            
            # Gán lại bằng new Child trực tiếp
            p := new Child();
            io.writeInt(p.getValue()); # 2
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "122"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_array_assignment():
    source = """
    class Main {
        static void main() {
            int[3] arr := {1, 2, 3};
            
            # Read
            io.writeInt(arr[0]);
            
            # Modify
            arr[1] := 20;
            io.writeInt(arr[1]);
            
            # Expression in index and value
            int i := 2;
            arr[i] := arr[0] + arr[1]; # 1 + 20 = 21
            io.writeInt(arr[2]);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "12021"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_arithmetic():
    source = """
    class Main {
        static void main() {
            # Integer arithmetic
            io.writeInt(10 + 5);    # 15
            io.writeInt(10 - 20);   # -10
            io.writeInt(3 * 7);     # 21
            io.writeInt(10 % 3);    # 1 (Modulo)
            
            # Float arithmetic
            io.writeFloat(1.5 + 2.5); # 4.0
            io.writeFloat(5.5 - 1.5); # 4.0
            io.writeFloat(2.0 * 1.5); # 3.0
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Lưu ý: float in ra thường có .0 hoặc định dạng số thực tùy implementation của io.writeFloat
    # Giả sử format là chuẩn.
    expected = "15-102114.04.03.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
# def test_binary_division_types():
#     source = """
#     class Main {
#         static void main() {
#             # Operator / always returns float
#             io.writeFloat(5 / 2);     # 2.5 (int / int -> float)
#             io.writeFloat(5.0 / 2.0); # 2.5
            
#             # Operator \ is integer division
#             io.writeInt(5 \\ 2);      # 2
#             io.writeInt(10 \\ 3);     # 3
#         }
#     }
#     """
#     ast = ASTGenerator(source).generate()
#     expected = "2.52.523"
#     result = CodeGenerator().generate_and_run(ast)
#     assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_mixed_type_arithmetic():
    source = """
    class Main {
        static void main() {
            # Int op Float -> Float
            io.writeFloat(2 + 3.5);   # 5.5
            io.writeFloat(5.5 - 2);   # 3.5
            io.writeFloat(2 * 1.5);   # 3.0
            
            # Phép so sánh hỗn hợp
            if (2 < 2.5) then io.writeStr("True"); else io.writeStr("False");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "5.53.53.0True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_relational():
    source = """
    class Main {
        static void main() {
            # Comparison
            io.writeBool(10 > 5);       # true
            io.writeBool(10 < 5);       # false
            io.writeBool(5 >= 5);       # true
            io.writeBool(5 <= 4);       # false
            
            # Equality
            io.writeBool(5 == 5);       # true
            io.writeBool(5 != 5);       # false
            io.writeBool(true == true); # true
            io.writeBool(true != false);# true
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "truefalsetruefalsetruefalsetruetrue"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_logical_short_circuit():
    source = """
    class Utils {
        static boolean check(int n) {
            io.writeInt(n); # Side effect
            return true;
        }
    }
    class Main {
        static void main() {
            # OR Short-circuit: true || ... (vế phải KHÔNG chạy)
            if (true || Utils.check(1)) then io.writeStr("A");
            
            # AND Short-circuit: false && ... (vế phải KHÔNG chạy)
            if (false && Utils.check(2)) then io.writeStr("B"); else io.writeStr("C");
            
            # Normal eval: false || ... (vế phải PHẢI chạy -> in 3)
            if (false || Utils.check(3)) then io.writeStr("D");
            
            # Normal eval: true && ... (vế phải PHẢI chạy -> in 4)
            if (true && Utils.check(4)) then io.writeStr("E");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Mong đợi:
    # 1. true || ... -> "A" (không in 1)
    # 2. false && ... -> else -> "C" (không in 2)
    # 3. false || check(3) -> in "3", trả về true -> "D"
    # 4. true && check(4) -> in "4", trả về true -> "E"
    expected = "AC3D4E"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_string_concat():
    source = """
    class Main {
        static void main() {
            string s1 := "Hello";
            string s2 := "World";
            io.writeStr(s1 ^ " " ^ s2 ^ "!");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Hello World!"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_binary_operator_precedence():
    source = """
    class Main {
        static void main() {
            # 2 + (3 * 4) = 14, not (2+3)*4 = 20
            io.writeInt(2 + 3 * 4); 
            
            # (10 / 2) + 1 = 6.0
            io.writeFloat(10.0 / 2.0 + 1.0);
            
            # 5 > 3 && 2 < 4 -> true && true -> true
            # (Precedence: > < before &&)
            io.writeBool((5 > 3) && (2 < 4));
            
            # !true || true -> false || true -> true
            # (Precedence: ! before ||)
            io.writeBool(!true || true);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "146.0truetrue"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_unary_operations():
    source = """
    class Main {
        static void main() {
            int i := 10;
            float f := 2.5;
            boolean b := false;

            # 1. Integer Unary
            io.writeInt(-i);        # -10
            io.writeInt(+i);        # 10
            io.writeInt(-(-5));     # 5 (Nested unary)

            # 2. Float Unary
            io.writeFloat(-f);      # -2.5
            io.writeFloat(+f);      # 2.5
            
            # 3. Boolean Unary
            io.writeBool(!b);       # true
            io.writeBool(!true);    # false
            io.writeBool(!!b);      # false (Double negation)

            # 4. Precedence Check
            # !false || false -> true || false -> true
            if (!b || false) then io.writeStr("Pass"); else io.writeStr("Fail");
            
            # -(3) * 2 -> -6
            io.writeInt(-3 * 2);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Expected output logic:
    # -10
    # 10
    # 5
    # -2.5
    # 2.5
    # true
    # false
    # false
    # Pass
    # -6
    expected = "-10105-2.52.5truefalsefalsePass-6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_if():
    source = """
    class Main {
        static void main() {
            # 1. Simple If (True)
            if (true) then io.writeInt(1);
            
            # 2. Simple If (False) - Should not print
            if (false) then io.writeInt(2);
            
            # 3. If-Else (True)
            if (10 > 5) then io.writeInt(3); else io.writeInt(4);
            
            # 4. If-Else (False)
            if (10 < 5) then io.writeInt(5); else io.writeInt(6);
            
            # 5. Nested If
            if (true) then {
                if (false) then io.writeInt(7);
                else io.writeInt(8);
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Expected: 1, 3, 6, 8
    expected = "1368"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_for_basic():
    source = """
    class Main {
        static void main() {
            int i;
            
            # 1. Loop 'to' (1 to 3) -> 1, 2, 3
            for i := 1 to 3 do io.writeInt(i);
            
            # 2. Loop 'downto' (3 downto 1) -> 3, 2, 1
            for i := 3 downto 1 do io.writeInt(i);
            
            # 3. No execution (start > end with 'to')
            for i := 5 to 1 do io.writeStr("Fail");
            
            # 4. No execution (start < end with 'downto')
            for i := 1 downto 5 do io.writeStr("Fail");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "123321"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_nested_for():
    source = """
    class Main {
        static void main() {
            int i, j;
            # Outer: 1..2, Inner: 1..2
            # 1-1, 1-2, 2-1, 2-2
            for i := 1 to 2 do {
                for j := 1 to 2 do {
                    io.writeInt(i);
                    io.writeInt(j);
                }
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "11122122"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_break():
    source = """
    class Main {
        static void main() {
            int i;
            # Loop 1..5, but break at 3
            # Should print: 1, 2
            for i := 1 to 5 do {
                if (i == 3) then break;
                io.writeInt(i);
            }
            io.writeStr("End");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "12End"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_continue():
    source = """
    class Main {
        static void main() {
            int i;
            # Loop 1..5, continue if even
            # Should print: 1, 3, 5
            for i := 1 to 5 do {
                if (i % 2 == 0) then continue;
                io.writeInt(i);
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "135"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_control_flow_complex():
    source = """
    class Main {
        static void main() {
            int i, j;
            # i: 1..3
            for i := 1 to 3 do {
                if (i == 2) then continue; # Skip i=2 -> i=3
                
                # j: 1..3
                for j := 1 to 3 do {
                    if (j == 2) then break; # Stop inner loop at j=2
                    io.writeInt(i);
                    io.writeInt(j);
                }
            }
            # Expected logic:
            # i=1:
            #   j=1 -> print 11
            #   j=2 -> break inner (j loop ends)
            # i=2: continue outer (skip j loop)
            # i=3:
            #   j=1 -> print 31
            #   j=2 -> break inner
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "1131"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_return_types_basic():
    source = """
    class ReturnTypes {
        static int getInt() { return 10; }
        static float getFloat() { return 10.5; }
        static boolean getBool() { return true; }
        static string getStr() { return "Hello"; }
    }
    
    class Main {
        static void main() {
            io.writeIntLn(ReturnTypes.getInt());
            io.writeFloatLn(ReturnTypes.getFloat());
            io.writeBoolLn(ReturnTypes.getBool());
            io.writeStrLn(ReturnTypes.getStr());
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "10\n10.5\ntrue\nHello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
def test_return_objects_arrays():
    source = """
    class Container {
        int val;
        Container(int v) { this.val := v; }
    }
    
    class Factory {
        static Container createContainer(int v) {
            return new Container(v);
        }
        
        static int[3] createArray() {
            return {1, 2, 3};
        }
    }
    
    class Main {
        static void main() {
            Container c := Factory.createContainer(99);
            io.writeIntLn(c.val);
            
            int[3] arr := Factory.createArray();
            io.writeIntLn(arr[2]);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "99\n3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
def test_return_control_flow():
    source = """
    class Utils {
        # Test return inside if
        static int abs(int n) {
            if (n < 0) then return -n;
            return n;
        }
        
        # Test return inside loop
        static int find(int[5] arr; int target) {
            int i;
            for i := 0 to 4 do {
                if (arr[i] == target) then return i;
            }
            return -1;
        }
    }
    
    class Main {
        static void main() {
            io.writeIntLn(Utils.abs(-5));
            io.writeIntLn(Utils.abs(10));
            
            int[5] data := {10, 20, 30, 40, 50};
            io.writeIntLn(Utils.find(data, 30)); # Index 2
            io.writeIntLn(Utils.find(data, 99)); # Not found -1
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "5\n10\n2\n-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
def test_return_recursion():
    source = """
    class Math {
        static int fib(int n) {
            if (n <= 1) then return n;
            return Math.fib(n-1) + Math.fib(n-2);
        }
    }
    
    class Main {
        static void main() {
            # Fib(6) = 8
            io.writeInt(Math.fib(6));
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_return_coercion_int_to_float():
    source = """
    class Calculator {
        # Function declared to return float
        static float getPi() {
            return 3; # Returning int '3'
        }
        
        static float add(float a; float b) {
            return 10; # Returning int literal
        }
    }
    
    class Main {
        static void main() {
            float f := Calculator.getPi();
            io.writeFloatLn(f); # Should print 3.0
            
            io.writeFloatLn(Calculator.add(1.0, 2.0)); # Should print 10.0
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "3.0\n10.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
def test_method_call_basic():
    source = """
    class Calculator {
        int val;
        
        # Instance method
        void setVal(int v) {
            this.val := v;
        }
        
        int getVal() {
            return this.val;
        }
        
        # Static method
        static int add(int a, b) {
            return a + b;
        }
    }
    
    class Main {
        static void main() {
            # Test Static Call
            io.writeIntLn(Calculator.add(10, 20));
            
            # Test Instance Call
            Calculator c := new Calculator();
            c.setVal(100);
            io.writeIntLn(c.getVal());
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "30\n100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_static_via_instance():
    source = """
    class Utils {
        static void greet() {
            io.writeStrLn("Hello Static");
        }
    }
    
    class Main {
        static void main() {
            Utils u := new Utils();
            
            # Gọi hàm static thông qua biến instance
            # Codegen sẽ sinh lệnh 'pop' để loại bỏ 'u' khỏi stack, sau đó gọi invokestatic
            u.greet();
            
            # Gọi thông qua object creation tạm thời
            (new Utils()).greet();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Hello Static\nHello Static"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_coercion():
    source = """
    class Converter {
        # Tham số là float
        static void printFloat(float v) {
            io.writeFloatLn(v);
        }
        
        static float sum(float a; float b) {
            return a + b;
        }
    }
    
    class Main {
        static void main() {
            # Truyền int literals
            Converter.printFloat(10); 
            
            int x := 5;
            # Truyền biến int
            Converter.printFloat(x);
            
            # Hỗn hợp
            io.writeFloatLn(Converter.sum(1, 2.5));
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "10.0\n5.0\n3.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_chaining():
    source = """
    class Counter {
        int count := 0;
        
        # Trả về this để chain
        Counter inc() {
            this.count := this.count + 1;
            return this;
        }
        
        void print() {
            io.writeIntLn(this.count);
        }
    }
    
    class Main {
        static void main() {
            Counter c := new Counter();
            
            # Chaining calls
            c.inc().inc().inc().print();
            
            # Chain với new
            (new Counter()).inc().print();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "3\n1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_arg_order():
    source = """
    class Test {
        static int trace(int v) {
            io.writeInt(v);
            return v;
        }
        
        static void run(int a, b, c) {
            io.writeStr("Done");
        }
    }
    
    class Main {
        static void main() {
            # Các hàm trace phải được gọi theo thứ tự 1 -> 2 -> 3
            Test.run(Test.trace(1), Test.trace(2), Test.trace(3));
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "123Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_recursion():
    source = """
    class Math {
        static int fact(int n) {
            if (n <= 1) then return 1;
            return n * Math.fact(n - 1);
        }
        
        int fib(int n) {
            if (n <= 1) then return n;
            return this.fib(n-1) + this.fib(n-2);
        }
    }
    
    class Main {
        static void main() {
            io.writeIntLn(Math.fact(5)); # 120
            
            Math m := new Math();
            io.writeIntLn(m.fib(6));     # 8
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "120\n8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_method_call_this():
    source = """
    class Greeter {
        void hello() {
            io.writeStr("Hello ");
        }
        
        void world() {
            io.writeStr("World");
        }
        
        void greet() {
            this.hello();
            this.world();
        }
    }
    
    class Main {
        static void main() {
            Greeter g := new Greeter();
            g.greet();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_member_access_basic():
    source = """
    class Point {
        int x, y;
        
        Point(int x, y) {
            this.x := x;
            this.y := y;
        }
    }
    
    class Main {
        static void main() {
            # Object Creation
            Point p := new Point(10, 20);
            
            # Member Access (Read)
            io.writeInt(p.x);
            io.writeInt(p.y);
            
            # Member Access (Write)
            p.x := 100;
            io.writeInt(p.x);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "1020100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_this_method_chaining():
    source = """
    class Counter {
        int val := 0;
        
        Counter add(int n) {
            this.val := this.val + n;
            return this; # Return 'this' for chaining
        }
        
        Counter sub(int n) {
            this.val := this.val - n;
            return this;
        }
        
        void print() {
            io.writeInt(this.val);
        }
    }
    
    class Main {
        static void main() {
            # Create object and chain methods
            new Counter().add(10).sub(2).add(5).print(); # 0+10-2+5 = 13
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_array_access_complex():
    source = """
    class Main {
        static void main() {
            int[5] arr := {10, 20, 30, 40, 50};
            int i := 2;
            
            # Basic access
            io.writeInt(arr[0]); # 10
            
            # Expression index
            io.writeInt(arr[i * 2 - 1]); # arr[3] -> 40
            
            # Nested index (arr[arr[0]...]) - Logic: arr[0]=10, quá lớn so với size 5
            # Ta dùng logic khác:
            int[3] idx := {0, 1, 2};
            # arr[idx[1]] -> arr[1] -> 20
            io.writeInt(arr[idx[1]]); 
            
            # Modification
            arr[idx[2]] := 99; # arr[2] = 99
            io.writeInt(arr[2]);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "10402099"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_nested_member_access():
    source = """
    class Box {
        int value;
        Box(int v) { this.value := v; }
    }
    
    class Container {
        Box b;
        Container(Box b) { this.b := b; }
        
        Box getBox() { return this.b; }
    }
    
    class Main {
        static void main() {
            Box b := new Box(123);
            Container c := new Container(b);
            
            # Access nested field: c.b.value
            io.writeInt(c.b.value);
            
            # Access via method call: c.getBox().value
            io.writeInt(c.getBox().value);
            
            # Modify nested
            c.b.value := 456;
            io.writeInt(c.getBox().value);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "123123456"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_pass_this_as_argument():
    source = """
    class Visitor {
        void visit(Node n) {
            io.writeStr("Visited Node ");
            io.writeInt(n.id);
        }
    }
    
    class Node {
        int id;
        Node(int id) { this.id := id; }
        
        void accept(Visitor v) {
            # Pass 'this' (current Node) to visitor
            v.visit(this);
        }
    }
    
    class Main {
        static void main() {
            Visitor v := new Visitor();
            Node n := new Node(1);
            n.accept(v);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Visited Node 1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_array_of_objects():
    source = """
    class Player {
        int score;
        Player(int s) { this.score := s; }
    }
    
    class Main {
        static void main() {
            Player p1 := new Player(10);
            Player p2 := new Player(20);
            
            # Array initialization with objects
            Player[2] players := {p1, p2};
            
            # Access object field via array index
            io.writeInt(players[0].score); # 10
            io.writeInt(players[1].score); # 20
            
            # Modify object via array
            players[0].score := 99;
            io.writeInt(p1.score); # Should reflect 99 (reference type)
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "102099"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_this_shadowing():
    source = """
    class Shadow {
        int x := 10;
        
        void test(int x) {
            io.writeInt(x);      # Tham số (argument)
            io.writeInt(this.x); # Thuộc tính (field)
            
            this.x := x;         # Gán tham số vào thuộc tính
            io.writeInt(this.x);
        }
    }
    
    class Main {
        static void main() {
            Shadow s := new Shadow();
            s.test(5);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "5105"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_constructor_destructor_basic():
    source = """
    class Counter {
        int val;
        
        Counter(int v) {
            this.val := v;
            io.writeStr("Init ");
        }
        
        ~Counter() {
                io.writeStr("Done");
            }
    }
    
    class Main {
        static void main() {
            Counter c := new Counter(10);
            io.writeInt(c.val);
            io.writeStr(" ");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Flow: 
    # 1. new Counter(10) -> Print "Init "
    # 2. writeInt(10) -> Print "10"
    # 3. writeStr(" ") -> Print " "
    # 4. End of main -> Call c.destructor() -> Print "Done"
    expected = "Init 10 Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_constructor_overloading():
    source = """
    class Box {
        int area;
        
        # Constructor 1 tham số
        Box(int side) {
            this.area := side * side;
        }
        
        # Constructor 2 tham số
        Box(int l, w) {
            this.area := l * w;
        }
    }
    
    class Main {
        static void main() {
            Box b1 := new Box(5);
            Box b2 := new Box(4, 6);
            
            io.writeInt(b1.area); # 25
            io.writeInt(b2.area); # 24
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "2524"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_constructor_destructor_inheritance():
    source = """
    class Parent {
        Parent() { io.writeStr("P_Ctor "); }
        ~Parent() { io.writeStr("P_Dtor "); }
    }
    
    class Child extends Parent {
        Child() { io.writeStr("C_Ctor "); }
        ~Child() { io.writeStr("C_Dtor "); }
    }
    
    class Main {
        static void main() {
            Child c := new Child();
            io.writeStr("| ");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Logic hiện tại của bạn:
    # Ctor: Child gọi super() -> P_Ctor -> C_Ctor
    # Dtor: Child gọi super() -> P_Dtor -> C_Dtor
    expected = "P_Ctor C_Ctor | P_Dtor C_Dtor"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_destructor_scope():
    source = """
    class A {
        int id;
        A(int i) { this.id := i; }
        ~A() { io.writeInt(this.id); }
    }
    
    class Main {
        static void main() {
            io.writeStr("Start ");
            
            # Block 1
            {
                A a1 := new A(1);
                io.writeStr("InBlock ");
            } # a1 chết ở đây -> in 1
            
            io.writeStr("Mid ");
            
            # Block 2
            if (true) then {
                A a2 := new A(2);
            } # a2 chết ở đây -> in 2
            
            io.writeStr("End");
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "Start InBlock 1Mid 2End"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_default_ctor_dtor_generation():
    source = """
    class Empty {
        int x := 99;
        # Không có constructor -> dùng default
        # Không có destructor -> codegen tự sinh default
    }
    
    class Main {
        static void main() {
            Empty e := new Empty();
            io.writeInt(e.x);
            # Cuối hàm main, e.destructor() được gọi. 
            # Nếu codegen không tự sinh method này, JVM sẽ báo lỗi NoSuchMethodError.
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_destructor_multiple_vars():
    source = """
    class Item {
        int id;
        Item(int i) { this.id := i; }
        ~Item() { io.writeInt(this.id); }
    }
    
    class Main {
        static void main() {
            {
                Item i1 := new Item(1);
                Item i2 := new Item(2);
                Item i3 := new Item(3);
            }
            # Logic codegen hiện tại duyệt xuôi: hủy i1 -> i2 -> i3
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_inheritance_method_override():
    source = """
    class Animal {
        void speak() { io.writeStr("Animal"); }
    }
    
    class Dog extends Animal {
        void speak() { io.writeStr("Woof"); }
    }
    
    class Cat extends Animal {
        void speak() { io.writeStr("Meow"); }
    }
    
    class Main {
        static void main() {
            Animal a;
            
            a := new Animal();
            a.speak(); # Animal
            
            a := new Dog();
            a.speak(); # Woof (Polymorphism)
            
            a := new Cat();
            a.speak(); # Meow (Polymorphism)
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "AnimalWoofMeow"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_inheritance_chain():
    source = """
    class A {
        void foo() { io.writeStr("A_foo "); }
        void bar() { io.writeStr("A_bar "); }
    }
    
    class B extends A {
        # B inherits foo from A
        # B overrides bar
        void bar() { io.writeStr("B_bar "); }
    }
    
    class C extends B {
        # C overrides foo
        void foo() { io.writeStr("C_foo "); }
        # C inherits bar from B
    }
    
    class Main {
        static void main() {
            A obj := new C();
            
            # C override foo của A -> gọi C.foo
            obj.foo(); 
            
            # C kế thừa bar của B (B override A) -> gọi B.bar
            obj.bar();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "C_foo B_bar"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_inheritance_field_shadowing():
    source = """
    class Parent {
        int val := 10;
        int getVal() { return this.val; }
    }
    
    class Child extends Parent {
        int val := 20; # Shadowing parent's field
        int getVal() { return this.val; }
    }
    
    class Main {
        static void main() {
            Parent p := new Child();
            
            # Access field directly -> Static binding (Type of p is Parent)
            # Mong đợi: lấy val của Parent (10)
            io.writeInt(p.val);
            
            io.writeStr(" ");
            
            # Access via method -> Dynamic binding (Instance is Child)
            # Mong đợi: gọi getVal() của Child, trả về val của Child (20)
            io.writeInt(p.getVal());
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "10 20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_polymorphism_arguments():
    source = """
    class Shape {
        void draw() { io.writeStr("Shape"); }
    }
    
    class Circle extends Shape {
        void draw() { io.writeStr("Circle"); }
    }
    
    class Square extends Shape {
        void draw() { io.writeStr("Square"); }
    }
    
    class Printer {
        # Tham số là Shape, nhưng có thể nhận Circle/Square
        static void print(Shape s) {
            s.draw();
        }
    }
    
    class Main {
        static void main() {
            Printer.print(new Shape());
            Printer.print(new Circle());
            Printer.print(new Square());
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "ShapeCircleSquare"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_polymorphism_array():
    source = """
    class Worker {
        int salary() { return 100; }
    }
    
    class Manager extends Worker {
        int salary() { return 200; }
    }
    
    class CEO extends Manager {
        int salary() { return 500; }
    }
    
    class Main {
        static void main() {
            Worker w := new Worker();
            Manager m := new Manager();
            CEO c := new CEO();
            
            # Array type is Worker, but holds subclass instances
            Worker[3] staff := {w, m, c};
            
            int i;
            int total := 0;
            
            for i := 0 to 2 do {
                total := total + staff[i].salary();
            }
            
            io.writeInt(total); # 100 + 200 + 500 = 800
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "800"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_call_overridden_from_constructor():
    source = """
    class Base {
        Base() {
            this.init();
        }
        
        void init() {
            io.writeStr("Base ");
        }
    }
    
    class Derived extends Base {
        Derived() { }
        
        # Override init
        void init() {
            io.writeStr("Derived ");
        }
    }
    
    class Main {
        static void main() {
            # new Derived() -> Base() -> this.init() (Virtual call) -> Derived.init()
        Derived d := new Derived();        }
    }
    """
    ast = ASTGenerator(source).generate()
    # Expected: "Derived " vì phương thức được dispatch động
    expected = "Derived"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
def test_reference_swap_and_alias():
    """
    Test case kiểm tra tính năng Reference Type (int &):
    1. Truyền tham chiếu vào hàm (SwapUtils.swap) để thay đổi giá trị biến gốc.
    2. Khai báo biến tham chiếu cục bộ (Aliasing) và sửa đổi giá trị qua tham chiếu đó.
    """
    ast = """
    class SwapUtils {
        # Hàm nhận tham chiếu, thay đổi giá trị gốc
        static void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }

    class ReferenceTest {
        static void main() {
            int x := 10;
            int y := 20;
            
            # 1. Kiểm tra giá trị ban đầu
            io.writeStr("Before swap: x=");
            io.writeInt(x);
            io.writeStr(", y=");
            io.writeIntLn(y);
            
            # 2. Gọi hàm swap (Pass-by-Reference)
            SwapUtils.swap(x, y);
            
            io.writeStr("After swap: x=");
            io.writeInt(x);
            io.writeStr(", y=");
            io.writeIntLn(y);
            
            # 3. Test Alias (Biến tham chiếu cục bộ)
            int & ref := x;
            ref := 100;
            io.writeStr("After ref:=100, x=");
            io.writeIntLn(x); # x phải là 100 vì ref trỏ tới x
        }
    }
    """
    
    # Kết quả mong đợi (Lưu ý: writeIntLn sẽ thêm ký tự xuống dòng \n)
    expected_output = (
        "Before swap: x=10, y=20\n"
        "After swap: x=20, y=10\n"
        "After ref:=100, x=100"
    )
    
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == expected_output

def test_object_default_init():
    ast = """
    class A {
        int x := 10;
    }
    class Main {
        static void main() {
            # Khai báo nhưng không khởi tạo -> mặc định là null
            A a; 
            
            # Nếu a chưa được init (null), chương trình vẫn chạy qua dòng này
            io.writeStr("Declared");
            
            # Lưu ý: Nếu truy cập a.x sẽ gây NullPointerException (Runtime Error hợp lệ),
            # nhưng quan trọng là không được bị VerifyError lúc compile.
            
            # Gán giá trị sau đó
            a := new A();
            io.writeInt(a.x);
        }
    }
    """
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "Declared10"

def test_copy_constructor_resolution():
    ast = """
    class A {
        int val;
        
        # Constructor thường
        A(int v) {
            this.val := v;
            io.writeStr("Int Const ");
        }
        
        # Copy Constructor
        A(A other) {
            this.val := other.val;
            io.writeStr("Copy Const ");
        }
    }
    
    class Main {
        static void main() {
            A a1 := new A(10);      # Phải gọi A(int)
            A a2 := new A(a1);      # Phải gọi A(A)
            
            io.writeInt(a2.val);
        }
    }
    """
    # Expected: "Int Const Copy Const 10"
    assert CodeGenerator().generate_and_run(ASTGenerator(ast).generate()) == "Int Const Copy Const 10"



# # TODO: Add more test cases here
# # Students should implement at least 100 test cases covering:
# # - All literal types (int, float, boolean, string, array, nil)
# # - Variable declarations and assignments
# # - Binary operations (+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||)
# # - Unary operations (-, +, !)
# # - Control flow (if, for, break, continue)
# # - Return statements
# # - Method calls (static and instance)
# # - Member access
# # - Array access
# # - Object creation
# # - This expression
# # - Constructors and destructors
# # - Inheritance and polymorphism


# # class Shape {
# #     Shape(){}
# #     ~Shape(){io.writeIntLn(1);}
# # }

# # class Rectangle extends Shape {
# #     Rectangle(){}
# #     ~Rectangle(){io.writeIntLn(2);}
# # }

# # class Triangle extends Shape {
# #     Triangle(){}
# #     ~Triangle(){io.writeIntLn(3);}
# # }


# # class X {
# #     static void main() {
# #         Shape a := new Triangle();
# #         {
# #             Shape b := new Shape();
# #             Rectangle c := new Rectangle();
# #         }
# #     }
# # }
# # """
# #     assert CodeGenerator().generate_and_run(ast) == "1\n1\n2\n1\n3"




# # # TODO: Add more test cases here
# # # Students should implement at least 100 test cases covering:
# # # - All literal types (int, float, boolean, string, array, nil)
# # # - Variable declarations and assignments
# # # - Binary operations (+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||)
# # # - Unary operations (-, +, !)
# # # - Control flow (if, for, break, continue)
# # # - Return statements
# # # - Method calls (static and instance)
# # # - Member access
# # # - Array access
# # # - Object creation
# # # - This expression
# # # - Constructors and destructors
# # # - Inheritance and polymorphism

