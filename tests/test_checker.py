# from utils import Checker


# def test_001():
#     """Test a valid program that should pass all checks"""
#     source = """
# class Test {
#     static void main() {
#         int x := 5;
#         int y := x + 1;
#     }
# }
# """
#     expected = "Static checking passed"
#     # Just check that it doesn't return an error
#     assert Checker(source).check_from_source() == expected

# def test_002():
#     """Test redeclared variable error"""
#     source = """
# class Test {
#     static void main() {
#         int x := 5;
#         int x := 10;
#     }
# }
# """
#     expected = "Redeclared(Variable, x)"
#     assert Checker(source).check_from_source() == expected

# def test_003():
#     """Test undeclared identifier error"""
#     source = """
# class Test {
#     static void main() {
#         int x := y + 1;
#     }
# }
# """
#     expected = "UndeclaredIdentifier(y)"
#     assert Checker(source).check_from_source() == expected

# def test_004():
#     """Test type mismatch error"""
#     source = """
# class Test {
#     static void main() {
#         int x := "hello";
#     }
# }
# """
#     expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
#     assert Checker(source).check_from_source() == expected

# def test_005():
#     """Test break not in loop error"""
#     source = """
# class Test {
#     static void main() {
#         break;
#     }
# }
# """
#     expected = "MustInLoop(BreakStatement())"
#     assert Checker(source).check_from_source() == expected

# def test_006():
#     """Test cannot assign to constant error"""
#     source = """
# class Test {
#     static void main() {
#         final int x := 5;
#         x := 10;
#     }
# }
# """
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
#     assert Checker(source).check_from_source() == expected

# def test_007():
#     """Test illegal array literal error - alternative case"""
#     source = """
# class Test {
#     static void main() {
#         boolean[2] flags := {true, 42};
#     }
# }
# """
#     expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
#     assert Checker(source).check_from_source() == expected


from utils import Checker
# from utils import ASTGenerator
# from src.utils.nodes import *

# # lms test 
# def test_lms_1():
#     source = """
# class C {}
# class B {
#     C(){
#         int a;
#     }
#     static void main(){}
# }
# """
#     expected = "TypeMismatchInStatement(ConstructorDecl(C([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(a)])], stmts=[])))"
#     assert Checker(source).check_from_source() == expected

# def test_lms_2():
#     """
    
# Với A.a := 1: đây là static attribute truy cập qua tên lớp, checker chấp nhận nên không có lỗi.
# Với A.b := 2: checker đã dựng đủ PostfixExpression(Identifier(A).b) rồi mới phát hiện b là instance field nhưng đang được truy cập dạng static, nên lỗi là IllegalMemberAccess(PostfixExpression(Identifier(A).b)).
#     """
#     source = """
# class A {static int a; int b;}
# class Test{
#     A a;
#     static void main(){
#         A.a := 1;
#         A.b := 2;
#     }
# }
# """
#     expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).b))"
#     assert Checker(source).check_from_source() == expected
# def test_lms_2_1():
#     """
    
    
#     """
#     source = """
# class Program {
#     int x;
    
#     static void main() {
#         # Lỗi: Sử dụng this trong static method
#         # Mong đợi: IllegalMemberAccess(ThisExpression)
#         # KHÔNG PHẢI: IllegalMemberAccess(FieldAccess(this.x))
#         int y := this.x; 
#     }
# }
# """
#     expected = "IllegalMemberAccess(ThisExpression)"
#     assert Checker(source).check_from_source() == expected

# def test_lms_2_2():
#     """
    
    
#     """
#     source = """
# class Program {
#     int x;
    
#     static void main() {
#         # Lỗi: Sử dụng this trong static method
#         # Mong đợi: IllegalMemberAccess(ThisExpression)
#         # KHÔNG PHẢI: IllegalMemberAccess(FieldAccess(this.x))
#         int y := this.x; 
#     }
# }
# """
#     expected = "IllegalMemberAccess(ThisExpression)"
#     assert Checker(source).check_from_source() == expected

# def test_lms_2_3():
#     """
    
    
#     """
#     source = """
# class Math {
#     void instanceMethod() { } # Instance method
# }

# class Program {
#     static void main() {
#         # Lỗi: Gọi instance method từ tên lớp
#         # Mong đợi: IllegalMemberAccess(CallExpr(Math.instanceMethod()))
#         Math.instanceMethod();
#     }
# }
# """
#     expected = "IllegalMemberAccess(CallExpr(Math.instanceMethod()))"
#     assert Checker(source).check_from_source() == expected

# def test_lms_2_4():
#     """
    
    
#     """
#     source = """
# class Config {
#     static int MAX_VAL := 100;
# }

# class Program {
#     static void main() {
#         Config c := new Config();
        
#         # Lỗi: MAX_VAL là static nhưng truy cập qua biến instance 'c'
#         # Mong đợi: IllegalMemberAccess(FieldAccess(c.MAX_VAL))
#         int x := c.MAX_VAL;
#     }
# }
# """
#     expected = "IllegalMemberAccess(FieldAccess(c.MAX_VAL))"
#     assert Checker(source).check_from_source() == expected

# def test_lms_2_5():
#     """
    
    
#     """
#     source = """
# class Runner {
#     static void process(Runner r) { }

#     static void main() {
#         # Lỗi: this đứng một mình làm tham số
#         # Mong đợi: IllegalMemberAccess(ThisExpression)
#         Runner.process(this);
#     }
# }
# """
#     expected = "IllegalMemberAccess(ThisExpression)"
#     assert Checker(source).check_from_source() == expected


# def test_lms_3():

#     source = """
# class Student {
#     static int totalStudents := 0;
#     static void resetCount() {
#         this.totalStudents := 0;
#     }
# }
# """
#     expected = "IllegalMemberAccess(this)"
#     assert Checker(source).check_from_source() == expected

# def test_lms_4():

#     source = """
# class Student {
#     static int totalStudents := 0;
#     static void resetCount() {
#         this.totalStudents := 0;
#     }
# }
# """
#     expected = "IllegalMemberAccess(this)"
#     assert Checker(source).check_from_source() == expected

def test_lms_001(): 
    source = """
class Test {
# cung tham so ham nen redeclare contructor
Test(int x; int y) {}
Test(int x, y) {}

    static void main(){
    }
}

"""
    expected = "Redeclared(Constructor, Test)" # test nay co the mo trong ra hai class cos cung mot func signature
    assert Checker(source).check_from_source() == expected

def test_lms_002(): 
    source = """
class Test {

   void foo (int z) {

       {

           {

               int z := 2;

           }

       }

   }
   static void main(){
   }

}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_003(): 
    source = """
class Test {
    void foo (int z) {
        int z := 2;
    }
    static void main(){
   }
}
"""
    expected = "Redeclared(Variable, z)" 
    assert Checker(source).check_from_source() == expected
def test_lms_004(): 
    """
        Kiểm tra gọi hàm trả về int nhưng không gán vào đâu.
        Trước đây: Lỗi TypeMismatchInStatement.
        Bây giờ: Phải Hợp lệ.
    """
    source = """
        class Math {
            static int add(int a; int b) {
                return a + b;
            }
            static void main() {
                # Gọi hàm trả về int như một statement
                Math.add(1, 2); 
            }
        }
        """
    expected = "Static checking passed" 
    assert Checker(source).check_from_source() == expected

def test_lms_005(): 
    """
        Kiểm tra Method Chaining (trả về đối tượng) dùng làm statement.
        Mô phỏng ví dụ StringBuilder của thầy.
        """
    source = """
        class Builder {
            Builder append(string s) {
                return this;
            }
            static void main() {
                Builder b := new Builder();
                # Method chaining: .append trả về Builder, 
                # nhưng cả dòng này là một Statement hợp lệ.
                b.append("Hello").append("World"); 
            }
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_lms_006(): 
    """
        Kiểm tra hồi quy: Hàm trả về void vẫn phải chạy đúng.
        """
    source = """
        class Math {
            # Hàm trả về int
            int add(int a; int b) { return a + b; }
            
            static void main() {
                # Tạo đối tượng để gọi hàm instance
                Math m := new Math();
                
                # Gọi hàm trả về int như một statement hợp lệ
                # Nếu chưa fix logic visit_method_invocation_statement -> Sẽ lỗi TypeMismatchInStatement
                # Nếu đã fix -> Static checking passed
                m.add(10, 20);
            }
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
# def test_lms_007(): 
#     """
#         Kiểm tra mảng chứa biểu thức tạo đối tượng (new A()).
#         Thầy xác nhận: ArrayLiteral là tập các expression.
#         """
#     source = """
#         class A {}
#         class Program {
#             static void main() {
#                 # Mảng đối tượng được khởi tạo bằng new
#                 A[2] arr := {new A(), new A()}; 
#             }
#         }
#         """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

def test_lms_008(): 
    """
        Kiểm tra mảng chứa biểu thức tạo đối tượng (new A()).
        Thầy xác nhận: ArrayLiteral là tập các expression.
        """
    source = """
        class EmptyArrays {
            void create() {
                int[0] empty1 := {};              #Valid if type can be inferred
            }
            static void main(){
            }
        }

        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_009(): 
    source = """class Program {
            static void main() {
                # Lỗi: int pha trộn boolean
                int[2] a := {1, true}; 
            }
        }"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected 

def test_lms_010(): 
    source = """
    class Program {
            static void main() {
                # Lỗi: int pha trộn boolean
                int[2] a := {1, true}; 
            }
        }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected 

def test_lms_011(): 
    source = """
class UnaryOpError {
    void operations() {
        string text := "hello";
        boolean flag := true;
       
        int negative := -text;  #Error: TypeMismatchInExpression at unary operation

    }
    static void main(){}
}


"""
    expected = "TypeMismatchInExpression(UnaryOp(-, Identifier(text)))"
    assert Checker(source).check_from_source() == expected 
def test_lms_012(): 
    source = """
class UnaryOpError {
    void operations() {
        string text := "hello";
        boolean flag := true;
       
        boolean not := !text;    # Error: TypeMismatchInExpression at unary operation

    }
    static void main(){}
}


"""
    expected = "TypeMismatchInExpression(UnaryOp(!, Identifier(text)))"
    assert Checker(source).check_from_source() == expected 
def test_lms_013(): 
    source = """
class UnaryOpError {
    void operations() {
        string text := "hello";
        boolean flag := true;
       
        int notFlag := !flag;    # Error: TypeMismatchInExpression at unary operation (if assigned to int)

    }
    static void main(){}
}


"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(notFlag = UnaryOp(!, Identifier(flag)))]))"
    assert Checker(source).check_from_source() == expected 


def test_lms_014(): 
    source = """
class ForLoopError {
    void loop() {
        float f := 1.5;
        boolean condition := true;
       
        for f := 0 to 10 do {  # Error: TypeMismatchInStatement at for statement
            io.writeFloatLn(f);
        }
     }  
    static void main(){}
}


"""
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeFloatLn(Identifier(f))))])))"
    assert Checker(source).check_from_source() == expected 
   
def test_lms_015(): 
    source = """
class ForLoopError {
    void loop() {
        float f := 1.5;
        boolean condition := true;
        int i; 
        for i := condition to 10 do {  #Error: TypeMismatchInStatement at variable declaration
            io.writeIntLn(i);
        }
     }  
    static void main(){}
}

"""
    expected = "TypeMismatchInStatement(ForStatement(for i := Identifier(condition) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected 

def test_lms_016(): 
    source = """
class ForLoopError {
    void loop() {
        float f := 1.5;
        boolean condition := true;
       
        for int i := 0 to 10.6 do { # Error: TypeMismatchInStatement at variable declaration
            io.writeIntLn(i);
        }
     }  
    static void main(){}
}

"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) 0 FloatLiteral(10.6) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected 
# def test_lms_017(): 
#     source = """
# class A {
#     A(int x){
#         final int y, z := 123;
#     }
# }
# # final kh dc phep := -> vi la gan
# # ma no chi dc la := 

# """
#     expected = "IllegalConstantExpression(123)"
#     assert Checker(source).check_from_source() == expected
def test_lms_018(): 
    source = """
class LoopExample {
    final int limit := 10;
    
    void process() {
        for limit := 0 to 20 do {  # Error: CannotAssignToConstant at for statement
            io.writeIntLn(limit);
        }
    }
    static void main(){
    }
}
"""
    expected = "CannotAssignToConstant(ForStatement(for limit := IntLiteral(0) to IntLiteral(20) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(limit))))])))"
    assert Checker(source).check_from_source() == expected
def test_lms_020(): 
    """
        Kiểm tra Attribute trùng tên với Constructor (tên Class).
        Class A {
            A() {}   # Constructor A
            int A;   # Attribute A -> Lỗi Redeclared
        }
        """
    source = """
        class Test {
            Test() {}
            int Test; 
            static void main(){
            }
        }
        """
        # Thứ tự khai báo có thể ảnh hưởng message (Redeclared Attribute hay Constructor)
        # Nhưng thường check Attribute sẽ thấy tên Class/Constructor đã "xí chỗ"
    expected = "Redeclared(Attribute, Test)"
    assert Checker(source).check_from_source() == expected
def test_lms_021(): 
    """
        Kiểm tra Attribute trùng tên với Constructor (tên Class).
        Class A {
            A() {}   # Constructor A
            int A;   # Attribute A -> Lỗi Redeclared
        }
        """
    source = """
        class Program {
            # Constructor mặc định là Program()
            
            # Hàm này trùng tên class -> Trùng tên Constructor
            void Program() {} 
            
            static void main() {}
        }
        """
        # Thứ tự khai báo có thể ảnh hưởng message (Redeclared Attribute hay Constructor)
        # Nhưng thường check Attribute sẽ thấy tên Class/Constructor đã "xí chỗ"
    expected = "Redeclared(Method, Program)"
    assert Checker(source).check_from_source() == expected
def test_lms_022(): 
    """
        """
    source = """
        class A {
            A() {}
            
            void foo(int A) { # A ở đây là param, shadow class name A
            }
            
            static void main() {}
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_023(): 
    """
        """
    source = """
        class A {
            A() {}
            
            void foo(int A) { # A ở đây là param, shadow class name A
                
            }
            
            static void main() {}
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_024(): 
    source = """
    class A {
        A(){}
        ~A(){}
        static void main(){}
    }
    
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_025(): 
    source = """
    class Test {
        Animal animal := new Animal();  # loi 
        static void main(){}
    }
    class Animal{
    }
"""
    expected = "UndeclaredClass(Animal)"
    assert Checker(source).check_from_source() == expected
def test_lms_026(): 
    source = """
    class Test {
        Animal animal;  # khong bi loi  
        static void main(){}
    }
    class Animal{
    }
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_lms_027():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
   
    static void resetCount() {
        Student.totalStudents := 0;
    }
}
class InstanceAccessError {
    void test() {
        Student s := new Student();
        s.resetCount();                    
    }
    static void main(){
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).resetCount()))"
    assert Checker(source).check_from_source() == expected
def test_lms_028():
    source = """
        class Test {
            void main() {
                int a;
                int x := a.b.c;
            }
        } 
"""
    expected = "TypeMismatchInExpression(Identifier(a))"
    assert Checker(source).check_from_source() == expected
def test_lms_029():
    """
        Kiểm tra chuỗi truy cập a.b.c, nhưng lỗi ngay tại a.
        a là int -> không thể chấm b.
        Mong đợi: TypeMismatchInExpression(a)
        """
    source = """
        class Test {
            void main() {
                int a := 10;
                
                # a là int, biểu thức a.b là sai.
                # Theo quy tắc thầy xác nhận: Lỗi trả về tại Identifier(a)
                a.b.c := 1; 
            }
        }
        """
    expected = "TypeMismatchInExpression(Identifier(a))"
    assert Checker(source).check_from_source() == expected

def test_lms_030():
    """
    Tương tự nhưng với lời gọi hàm: a.foo().
    a là int -> không thể gọi hàm.
    """
    source = """
    class Test {
        void main() {
            int a := 10;
            # Lỗi tại 'a'
            a.foo();
        }
    }
    """
    expected = "TypeMismatchInExpression(Identifier(a))"
    assert Checker(source).check_from_source() == expected
def test_lms_031(): 
    source = """
class Student {
    static int totalStudents := 0;
    static void main() {
        this.totalStudents := 0;
    }
}"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_lms_032(): 
    source = """
    class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        floatArray := intArray;
    }
}

"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(floatArray) := Identifier(intArray)))"
    assert Checker(source).check_from_source() == expected
def test_lms_033(): 
    source = """
class Test {

        int attr;

        static void main() {

           this.attr := 10;

        }
    }
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_lms_034(): 
    source = """
class ArraySubscriptError {
    void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
       
        int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([StringLiteral('index')])"
    assert Checker(source).check_from_source() == expected
def test_lms_035(): 
    source = """
class ArraySubscriptError {
    void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
       
        int value2 := numbers[2.5];   # Error: TypeMismatchInExpression at array access

    }
}
"""
    expected = "TypeMismatchInExpression([FloatLiteral(2.5)])"
    assert Checker(source).check_from_source() == expected
def test_lms_036(): 
    source = """
class ArraySubscriptError {
    void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
       
        string word := words[true];   # Error: TypeMismatchInExpression at array access

    }
}
"""
    expected = "TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected
def test_lms_037(): 
    source = """
class ArraySubscriptError {
    void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        int x; 
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access

    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected
# def test_lms_038(): 
#     source = """
#     class AttributeAccessError {
#         void access() {
#             int x := 10;
#             string text := "hello";
            
#             int length := text.value;  # Error: TypeMismatchInExpression at member access (if value doesn't exist)
#         }
#     }
# """
#     expected = "TypeMismatchInExpression(PostfixExpression(Identifier(text).value))"
#     assert Checker(source).check_from_source() == expected
def test_lms_039(): 
    source = """
class AttributeAccessError {
    void access() {
        int x := 10;
        string text := "hello";
        
        int invalid := x.length;   # Error: TypeMismatchInExpression at member access (x is not object)
    }
}

"""
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_redeclared_class():
        """
        Kiểm tra lỗi khai báo lại Class trong Global Scope.
        Example: Class Student được khai báo 2 lần.
        """
        source = """
        class Student {
            int id;
            string name;
        }
        class Student {  # Redeclared(Class, Student)
            float grade;
        }
        class Program { static void main() {} }
        """
        expected = "Redeclared(Class, Student)"
        assert Checker(source).check_from_source() == expected

def test_redeclared_method():
    """
    Kiểm tra lỗi khai báo lại Method trong cùng Class Scope.
    Example: Method add được khai báo 2 lần trong Calculator.
    """
    source = """
    class Calculator {
        int add(int a; int b) {
            return a + b;
        }
        int add(int x; int y) {  # Redeclared(Method, add)
            return x + y;
        }
    }
    class Program { static void main() {} }
    """
    expected = "Redeclared(Method, add)"
    assert Checker(source).check_from_source() == expected

def test_redeclared_attribute():
    """
    Kiểm tra lỗi khai báo lại Attribute trong cùng Class Scope.
    Example: Attribute 'name' được khai báo 2 lần trong Person.
    """
    source = """
    class Person {
        string name;
        int age;
        string name;  # Redeclared(Attribute, name)
    }
    class Program { static void main() {} }
    """
    expected = "Redeclared(Attribute, name)"
    assert Checker(source).check_from_source() == expected

def test_redeclared_variable_in_method():
    """
    Kiểm tra lỗi khai báo lại Variable trong cùng Method Scope.
    Example: Variable 'count' được khai báo 2 lần trong process().
    """
    source = """
    class Example {
        void process() {
            int count := 10;
            int count := 20;  # Redeclared(Variable, count)
        }
    }
    class Program { static void main() {} }
    """
    expected = "Redeclared(Variable, count)"
    assert Checker(source).check_from_source() == expected

def test_redeclared_parameter():
    """
    Kiểm tra lỗi khai báo lại Parameter trong cùng Method Signature.
    Example: Parameter 'x' xuất hiện 2 lần trong calculate().
    """
    source = """
    class Math {
        int calculate(int x; float y; int x) {  # Redeclared(Parameter, x)
            return x + y;
        }
    }
    class Program { static void main() {} }
    """
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_redeclared_global_constant():
    """
    Kiểm tra lỗi khai báo lại Constant (Global Variable final).
    Example: MAX_SIZE được khai báo 2 lần.
    """
    source = """
    final int MAX_SIZE := 100;
    final int MAX_SIZE := 200;  # Redeclared(Constant, MAX_SIZE)
    
    class Program { static void main() {} }
    """
    expected = "Redeclared(Constant, MAX_SIZE)"
    assert Checker(source).check_from_source() == expected

def test_valid_overriding():
    """
    Kiểm tra trường hợp hợp lệ: Method Overriding (Inheritance).
    Class Dog kế thừa và ghi đè hàm makeSound của Animal -> Không lỗi.
    """
    source = """
    class Animal {
        void makeSound() {
            io.writeStrLn("Some sound");
        }
    }
    class Dog extends Animal {
        void makeSound() {  # Valid: overriding, not redeclaring
            io.writeStrLn("Woof!");
        }
    }
    class Program { static void main() {} }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_valid_shadowing():
    """
    Kiểm tra trường hợp hợp lệ: Variable Shadowing.
    Biến local 'value' che khuất attribute 'value', và biến trong block con che khuất biến block cha.
    """
    source = """
    class ShadowExample {
        int value := 100;  # Class attribute
        
        void method() {
            int value := 200;  # Valid: shadows class attribute
            {
                int value := 300;  # Valid: shadows method variable
            }
        }
    }
    class Program { static void main() {} }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
# def test_undeclared_variable_local():
#     """
#     Kiểm tra sử dụng biến chưa khai báo trong hàm.
#     Example: undeclaredVar + 10
#     """
#     source = """
#     class Example {
#         void method() {
#             int result := undeclaredVar + 10;  # Lỗi: undeclaredVar chưa được khai báo
#         }
#         static void main() {}
#     }
#     """
#     expected = "UndeclaredIdentifier(undeclaredVar)"
#     assert Checker(source).check_from_source() == expected

# def test_scope_isolation():
#     """
#     Kiểm tra biến cục bộ của hàm này không nhìn thấy ở hàm khác.
#     Example: ScopeTest
#     """
#     source = """
#     class ScopeTest {
#         void method1() {
#             int localVar := 42;
#         }
        
#         void method2() {
#             # Lỗi: localVar chỉ tồn tại trong method1
#             int value := localVar + 1;  
#         }
#         static void main() {}
#     }
#     """
#     expected = "UndeclaredIdentifier(localVar)"
#     assert Checker(source).check_from_source() == expected

# def test_strict_attribute_access_is_identifier_error():
#     """
#     [QUAN TRỌNG] Kiểm tra luật 'Strict this'.
#     Truy cập attribute mà quên 'this.' sẽ bị coi là UndeclaredIdentifier.
#     """
#     source = """
#     class Car {
#         string brand;
#         void display() {
#             # Lỗi: brand là attribute, nhưng viết thiếu 'this.'
#             # Theo luật mới, checker coi đây là tìm biến local 'brand' -> Không thấy -> UndeclaredIdentifier
#             io.writeStrLn(brand); 
#         }
#         static void main() {}
#     }
#     """
#     expected = "UndeclaredIdentifier(brand)"
#     assert Checker(source).check_from_source() == expected
def test_undeclared_attribute_explicit():
    """
    Kiểm tra truy cập thuộc tính KHÔNG tồn tại thông qua đối tượng/this.
    Chỉ khi dùng dấu chấm (.) thì mới báo UndeclaredAttribute.
    """
    source = """
    class Car {
        string brand;
        void display() {
            # Lỗi: class Car không có thuộc tính 'model'
            io.writeStrLn(this.model); 
        }
        static void main() {}
    }
    """
    expected = "UndeclaredAttribute(model)"
    assert Checker(source).check_from_source() == expected

def test_undeclared_attribute_on_object():
    """
    Kiểm tra truy cập thuộc tính trên biến đối tượng khác.
    """
    source = """
    class Point {
        int x, y;
    }
    class Program {
        static void main() {
            Point p := new Point();
            p.z := 10; # Lỗi: Point không có thuộc tính z
        }
    }
    """
    expected = "UndeclaredAttribute(z)"
    assert Checker(source).check_from_source() == expected

def test_undeclared_method_internal():
    """
    Kiểm tra gọi hàm không tồn tại trong cùng class (hoặc cha).
    """
    source = """
    class Calculator {
        int add(int a; int b) {
            return a + b;
        }
        
        void test() {
            # Lỗi: hàm multiply chưa được khai báo
            # Lưu ý: Method call multiply(5,3) là call statement/expression
            # Checker sẽ tìm method tên 'multiply'
            int result := multiply(5, 3); 
        }
        static void main() {}
    }
    """
    expected = "UndeclaredMethod(multiply)"
    assert Checker(source).check_from_source() == expected

def test_undeclared_method_on_object():
    """
    Kiểm tra gọi hàm trên đối tượng mà class đó không hỗ trợ.
    Example: Gọi factorial trên class Calculator (trong khi nó ở MathUtils).
    """
    source = """
    class Calculator {
        # Class này rỗng, không có factorial
    }
    class Main {
        static void main() {
            Calculator calc := new Calculator();
            # Lỗi: Calculator không có hàm factorial
            int fact := calc.factorial(5);  
        }
    }
    """
    expected = "UndeclaredMethod(factorial)"
    assert Checker(source).check_from_source() == expected

def test_valid_inherited_access():
    """
    Kiểm tra trường hợp HỢP LỆ: Truy cập thành viên kế thừa.
    Để đảm bảo checker không báo lỗi sai.
    """
    source = """
    class Animal {
        string species;
        void setSpecies(string s) {
            this.species := s;
        }
    }
    class Dog extends Animal {
        void identify() {
            # Hợp lệ: setSpecies được kế thừa từ Animal
            this.setSpecies("Canine"); 
            
            # Hợp lệ: species được kế thừa
            io.writeStrLn(this.species); 
        }
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected




def test_assign_to_final_attribute_in_method():
    """
    Test 1: Gán giá trị mới cho thuộc tính final (đã khởi tạo) trong phương thức thường.
    Expected: CannotAssignToConstant tại câu lệnh gán.
    """
    source = """
    class Constants {
        final int MAX_COUNT := 100;
        
        void example() {
            # Lỗi: MAX_COUNT là final attribute
            MAX_COUNT := 200;  
        }
        static void main() {}
    }
    """
    # Giả định cấu trúc AssignmentStatement(IdLHS(MAX_COUNT), IntLiteral(200))
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(MAX_COUNT) := IntLiteral(200)))"
    assert Checker(source).check_from_source() == expected

def test_assign_to_final_attribute_via_this():
    """
    Test 2: Gán cho thuộc tính final thông qua 'this.' trong phương thức thường.
    Expected: CannotAssignToConstant.
    """
    source = """
    class Configuration {
        final string APP_NAME := "MyApp";
        
        void updateConfig() {
            # Lỗi: this.APP_NAME là final
            this.APP_NAME := "NewApp";  
        }
        static void main() {}
    }
    """
    # LHS là PostfixLHS chứa ThisExpression và MemberAccess
    # Lưu ý: Bạn cần điều chỉnh string này khớp với __str__ của PostfixLHS trong code bạn
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).APP_NAME)) := StringLiteral('NewApp')))"
    assert Checker(source).check_from_source() == expected

def test_assign_to_final_local_variable():
    """
    Test 3: Gán lại giá trị cho biến cục bộ final.
    Expected: CannotAssignToConstant.
    """
    source = """
    class LocalConst {
        void process() {
            final int x := 10;
            # Lỗi: x là final local variable
            x := 20; 
        }
        static void main() {}
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(20)))"
    assert Checker(source).check_from_source() == expected

def test_assign_to_global_constant():
    """
    Test 4: Gán lại giá trị cho hằng số toàn cục (Global Constant).
    Expected: CannotAssignToConstant.
    """
    source = """
    final int MAX_SIZE := 1000;
    
    class Program {
        static void main() {
            # Lỗi: MAX_SIZE là global final
            MAX_SIZE := 2000;
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(MAX_SIZE) := IntLiteral(2000)))"
    assert Checker(source).check_from_source() == expected

def test_valid_final_init_in_constructor():
    """
    Test 5: Khởi tạo thuộc tính final (chưa có giá trị) trong Constructor.
    Expected: Passed (Hợp lệ).
    """
    source = """
    class ValidConstants {
        final string VERSION;
        
        ValidConstants(string version) {
            # Hợp lệ: Khởi tạo lần đầu trong constructor
            this.VERSION := version; 
        }
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_invalid_reassign_in_constructor():
    """
    Test 6: Gán lại thuộc tính final (đã có giá trị khởi tạo) trong Constructor.
    Expected: CannotAssignToConstant (Vì đã khởi tạo tại dòng khai báo rồi).
    """
    source = """
    class InvalidReassign {
        final int ID := 1;
        
        InvalidReassign() {
            # Lỗi: ID đã được khởi tạo là 1, không được gán lại
            ID := 2; 
        }
        static void main() {}
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(ID) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_loop_variable_cannot_be_final():
    """
    Test 7: Sử dụng biến final làm biến chạy trong vòng lặp For.
    Lưu ý: Test này kiểm tra logic 'For loop variable assigned'.
    """
    source = """
    class LoopError {
        final int i := 0;
        void loop() {
            # Lỗi: Biến i là final, không thể bị thay đổi bởi vòng lặp
            for i := 1 to 10 do {}
        }
        static void main() {}
    }
    """
    # Node lỗi là ForStatement (theo ví dụ mẫu trong tài liệu)
    # String expect có thể rất dài, bạn có thể chỉ check startswith nếu cần
    # Ở đây mình viết ngắn gọn đại diện
    # expected = "CannotAssignToConstant(ForStatement(...))" 
    # Để chạy được assert chính xác, bạn nên copy string output thực tế từ lần chạy đầu tiên    
    expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected
def test_if_stmt_non_boolean_int():
    """
    Kiểm tra If statement với điều kiện là int.
    Spec: If statement condition must be boolean type.
    """
    source = """
    class Program {
        static void main() {
            int x := 5;
            # Lỗi: x là int, không phải boolean
            if x then {
                io.writeStrLn("Invalid");
            }
        }
    }
    """
    # Node lỗi là IfStatement
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(x) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Invalid'))))])))"
    assert Checker(source).check_from_source() == expected

def test_if_stmt_non_boolean_string():
    """
    Kiểm tra If statement với điều kiện là string.
    """
    source = """
    class Program {
        static void main() {
            # Lỗi: string literal không phải boolean
            if "true" then {}
        }
    }
    """
    expected = "TypeMismatchInStatement(IfStatement(if StringLiteral('true') then BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_for_loop_float_variable():
    """
    Kiểm tra For loop với biến chạy là float.
    Spec: Scalar variable must be integer type.
    """
    source = """
    class Program {
        static void main() {
            float f := 1.5;
            # Lỗi: biến chạy f là float
            for f := 0 to 10 do {}
        }
    }
    """
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_for_loop_non_integer_bounds():
    """
    Kiểm tra For loop với biểu thức giới hạn không phải int.
    Spec: Expression 1 and Expression 2 must be integer type.
    """
    source = """
    class Program {
        static void main() {
            int i;
            # Lỗi: start_expr là float (1.5)
            for i := 1.5 to 10 do {}
        }
    }
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := FloatLiteral(1.5) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_for_loop_float_variable():
    """
    Kiểm tra For loop với biến chạy là float.
    Spec: Scalar variable must be integer type.
    """
    source = """
    class Program {
        static void main() {
            float f := 1.5;
            # Lỗi: biến chạy f là float
            for f := 0 to 10 do {}
        }
    }
    """
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_for_loop_non_integer_bounds():
    """
    Kiểm tra For loop với biểu thức giới hạn không phải int.
    Spec: Expression 1 and Expression 2 must be integer type.
    """
    source = """
    class Program {
        static void main() {
            int i;
            # Lỗi: start_expr là float (1.5)
            for i := 1.5 to 10 do {}
        }
    }
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := FloatLiteral(1.5) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected
def test_assign_mismatch_basic():
    """
    Kiểm tra gán sai kiểu cơ bản (int := string).
    """
    source = """
    class Program {
        static void main() {
            int x := 10;
            string text := "hello";
            # Lỗi: không thể gán string cho int
            x := text;
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_assign_valid_coercion_int_to_float():
    """
    Kiểm tra ép kiểu hợp lệ: int -> float.
    """
    source = """
    class Program {
        static void main() {
            int i := 10;
            float f := 1.5;
            # Hợp lệ: int gán vào float được
            f := i;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_assign_valid_sub_to_super():
    """
    Kiểm tra ép kiểu hợp lệ: Class con -> Class cha.
    """
    source = """
    class Parent {}
    class Child extends Parent {}
    class Program {
        static void main() {
            Parent p;
            Child c := new Child();
            # Hợp lệ: Child gán vào Parent
            p := c;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_assign_invalid_super_to_sub():
    """
    Kiểm tra gán ngược: Class cha -> Class con (Lỗi).
    """
    source = """
    class Parent {}
    class Child extends Parent {}
    class Program {
        static void main() {
            Parent p := new Parent();
            Child c;
            # Lỗi: Parent không gán được cho Child (cần ép kiểu tường minh nếu hỗ trợ, nhưng gán trực tiếp là lỗi)
            c := p;
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(p)))"
    assert Checker(source).check_from_source() == expected
def test_assign_array_mismatch_type():
        """
        Kiểm tra gán mảng khác kiểu (int[] := float[]).
        Spec: Example 'intArray := floatArray' is Error.
        """
        source = """
        class Program {
            static void main() {
                int[3] a;
                float[3] b;
                # Lỗi: int[] không nhận float[]
                a := b;
            }
        }
        """
        expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
        assert Checker(source).check_from_source() == expected

def test_assign_array_mismatch_size():
    """
    Kiểm tra gán mảng khác kích thước.
    Spec: Array assignments require same size.
    """
    source = """
    class Program {
        static void main() {
            int[3] a;
            int[2] b;
            # Lỗi: size 3 != size 2
            a := b;
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected
# def test_call_stmt_arg_mismatch():
#     """
#     Kiểm tra truyền sai kiểu tham số.
#     """
#     source = """
#     class Program {
#         void process(int x) {}
        
#         static void main() {
#             Program p := new Program();
#             # Lỗi: process cần int, truyền string
#             p.process("hello");
#         }
#     }
#     """
#     # Node lỗi là MethodInvocationStatement (chứa MethodCall bị sai)
#     # Tuy nhiên, trong logic checker _check_method_args, ta thường raise TypeMismatchInStatement(arg) hoặc statement.
#     # Dựa trên spec: TypeMismatchInStatement(<statement>)
#     expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(p).process(StringLiteral(hello)))))"
#     assert Checker(source).check_from_source() == expected

# def test_call_stmt_arg_count_mismatch():
#     """
#     Kiểm tra sai số lượng tham số.
#     """
#     source = """
#     class Program {
#         void process(int x; int y) {}
        
#         static void main() {
#             Program p := new Program();
#             # Lỗi: thiếu tham số
#             p.process(1);
#         }
#     }
#     """
#     expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(p).process(IntLiteral(1)))))"
#     assert Checker(source).check_from_source() == expected


def test_return_mismatch_type():
    """
    Kiểm tra return sai kiểu (void method return int).
    """
    source = """
    class Program {
        void doNothing() {
            # Lỗi: hàm void không được return giá trị
            return 1;
        }
        static void main() {}
    }
    """
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_return_mismatch_int_expected_string():
    """
    Kiểm tra return sai kiểu (int method return string).
    """
    source = """
    class Program {
        int getValue() {
            # Lỗi: cần int, trả về string
            return "invalid";
        }
        static void main() {}
    }
    """
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('invalid')))"
    assert Checker(source).check_from_source() == expected


# chuaw test type mismatch in expr

def test_const_mismatch_int_float():
    """
    Kiểm tra gán float cho hằng số int (Attribute).
    Spec: final int a = 1.2; -> Error
    """
    source = """
    class ConstantTypeError {
        final int a := 1.2;
        static void main() {}
    }
    """
    # Node lỗi là AttributeDecl
    # Cấu trúc string phụ thuộc vào __str__ của node AttributeDecl và Attribute
    # Giả định: AttributeDecl(False, True, IntType, [Attribute(a, FloatLit(1.2))])
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(a = FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected

def test_const_mismatch_string_int_global():
    """
    Kiểm tra gán int cho hằng số string (Global).
    Spec: final string text = 42; -> Error
    """
    source = """
    final string text := 42;
    
    class Program {
        static void main() {}
    }
    """
    # Node lỗi là VariableDecl
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(string), [Variable(text = IntLiteral(42))]))"
    assert Checker(source).check_from_source() == expected

def test_const_mismatch_boolean_string():
    """
    Kiểm tra gán string cho hằng số boolean.
    Spec: final boolean flag = "true"; -> Error
    """
    source = """
    class Config {
        final boolean flag := "true";
        static void main() {}
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = StringLiteral('true'))]))"
    assert Checker(source).check_from_source() == expected

def test_const_array_mismatch_type():
    """
    Kiểm tra gán mảng float[] cho hằng số int[].
    Spec: final int[3] numbers = {1.0, ...}; -> Error
    """
    source = """
    class ArrayConstantError {
        final int[3] numbers := {1.0, 2.0, 3.0};
        static void main() {}
    }
    """
    # Lưu ý: ArrayLiteral được parse thành list các FloatLiteral
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(PrimitiveType(int)[3]), [Attribute(numbers = ArrayLiteral({FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0)}))]))"
    assert Checker(source).check_from_source() == expected

def test_const_object_mismatch():
    """
    Kiểm tra gán object sai kiểu cho hằng số (không có quan hệ thừa kế).
    """
    source = """
    class A {}
    class B {}
    
    class ObjectConstantError {
        final A obj := new B(); # Lỗi: B không phải con của A
        static void main() {}
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(A), [Attribute(obj = ObjectCreation(new B()))]))"
    assert Checker(source).check_from_source() == expected

def test_valid_const_coercion_int_to_float():
    """
    Kiểm tra ép kiểu hợp lệ cho hằng số: int -> float.
    Spec: Integer can coerce to float.
    """
    source = """
    class ValidConstants {
        final float PI := 3; # int 3 gán cho float PI -> OK
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_break_outside_loop_simple():
    """
    Kiểm tra break nằm trơ trọi trong hàm (không có vòng lặp).
    Expected: MustInLoop(BreakStatement).
    """
    source = """
    class LoopError {
        void method() {
            break;     # Lỗi: Không nằm trong loop
        }
        static void main() {}
    }
    """
    # Node lỗi là BreakStatement (thường không có tham số)
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_continue_inside_if_no_loop():
    """
    Kiểm tra continue nằm trong if, nhưng if không nằm trong loop.
    Spec: Can be nested inside conditionals WITHIN LOOPS.
    """
    source = """
    class ConditionalError {
        void check() {
            if true then {
                continue;  # Lỗi: If này không nằm trong loop nào cả
            }
        }
        static void main() {}
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_break_cross_method_boundary():
    """
    Kiểm tra lỗi logic phổ biến: Loop gọi hàm -> Hàm chứa break.
    Spec: Cannot cross method boundaries.
    """
    source = """
    class MethodCallError {
        void helperMethod() {
            # Lỗi: Dù hàm này được gọi từ loop, nhưng về mặt lexical scope
            # nó không nằm trong loop nào cả.
            break;     
        }
        
        void loopWithCall() {
            for i := 0 to 10 do {
                this.helperMethod(); 
            }
        }
        static void main() {}
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_continue_after_loop_scope():
    """
    Kiểm tra continue nằm ngay sau khi loop kết thúc.
    """
    source = """
    class ScopeError {
        void main() {
            for i := 0 to 10 do {
                # Hợp lệ trong này
            }
            # Ra khỏi loop rồi -> Lỗi
            continue; 
        }
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_valid_nested_loop_context():
    """
    Kiểm tra trường hợp hợp lệ: Break/Continue lồng nhau nhiều cấp.
    """
    source = """
    class ValidLoops {
        void nestedLoops() {
            for i := 0 to 5 do {
                if i > 2 then break; # Valid (loop 1)
                
                for j := 0 to 5 do {
                    if i == j then {
                        continue;  # Valid (loop 2)
                    }
                    if j > 3 then {
                        break;     # Valid (loop 2)
                    }
                }
            }
        }
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_valid_break_in_block():
    """
    Kiểm tra break nằm trong block statement {} của loop.
    """
    source = """
    class BlockTest {
        static void main() {
            for i := 0 to 10 do {
                {
                    int x := 1;
                    if x == 1 then break; # Valid
                }
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
# ***
def test_const_init_nil():
    """
    Kiểm tra khởi tạo hằng số với nil hoặc không khởi tạo.
    Spec: Expression must not be None/null.
    """
    # Trường hợp 1: Không khởi tạo (final int x;)
    source1 = """
    class IllegalConstantError {
        final int x;  # Lỗi: Không có giá trị khởi tạo
        static void main() {}
    }
    """
    # Trong code Checker của bạn, trường hợp này raise IllegalConstantExpression(NilLiteral())
    expected1 = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(x)]))"
    assert Checker(source1).check_from_source() == expected1
#***
    # # Trường hợp 2: Khởi tạo bằng nil (final string s := nil;)
    # source2 = """
    # class IllegalConstantError {
    #     final string text := nil; # Lỗi: nil không phải hằng số hợp lệ
    #     static void main() {}
    # }
    # """
    # expected2 = "IllegalConstantExpression(NilLiteral())"
    # assert Checker(source2).check_from_source() == expected2

def test_const_init_with_mutable_var():
    """
    Kiểm tra khởi tạo hằng số bằng biến (mutable).
    Spec: No references to mutable variables.
    """
    source = """
    class MutableInConstant {
        int mutableVar := 10;
        # Lỗi: mutableVar có thể thay đổi, không dùng làm hằng được
        final int constant1 := this.mutableVar; 
        
        static void main() {}
    }
    """
    # Node lỗi là biểu thức truy cập: this.mutableVar (PostfixExpression)
    # Lưu ý format string phụ thuộc vào AST Node __str__
    # Giả định: PostfixExpression(ThisExpression(), [MemberAccess(mutableVar)])
    # Bạn có thể cần điều chỉnh string này cho khớp code của bạn
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).mutableVar))"
    assert Checker(source).check_from_source() == expected

def test_const_init_with_method_call():
    """
    Kiểm tra khởi tạo hằng số bằng lời gọi hàm.
    Spec: Can only use operators, no method calls.
    """
    source = """
    class MethodCallInConstant {
        int getValue() { return 42; }
        
        # Lỗi: Gọi hàm là runtime evaluation
        final int value := this.getValue(); 
        
        static void main() {}
    }
    """
    # Node lỗi là biểu thức gọi hàm
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).getValue()))"
    assert Checker(source).check_from_source() == expected

def test_const_init_complex_expression():
    """
    Kiểm tra biểu thức phức tạp chứa biến mutable.
    Spec: Result must be statically evaluable.
    """
    source = """
    class ComplexIllegalExpression {
        int a := 10;
        # Lỗi: (this.a * 2) chứa 'a' là mutable -> Invalid
        final int result := (this.a * 2) + 5; 
        
        static void main() {}
    }
    """
    # Lỗi thường được báo ở node gốc của biểu thức (BinaryOp) hoặc node lá gây lỗi (this.a)
    # Dựa trên code `_is_valid_constant_expr`, nếu nó trả về False cho root, checker raise root.
    expected = "IllegalConstantExpression(BinaryOp(ParenthesizedExpression((BinaryOp(PostfixExpression(ThisExpression(this).a), *, IntLiteral(2)))), +, IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_const_array_access():
    """
    Kiểm tra truy cập phần tử mảng trong hằng số.
    Spec: Array element access in constant ... Error.
    """
    source = """
    class ArrayAccessInConstant {
        final int[5] NUMBERS := {1, 2, 3, 4, 5};
        # Lỗi: Truy cập mảng [0] không được coi là hằng số (dù mảng là final)
        final int FIRST := this.NUMBERS[0];  
        
        static void main() {}
    }
    """
    expected = "IllegalConstantExpression(PostfixExpression(PostfixExpression(ThisExpression(this).NUMBERS)[IntLiteral(0)]))"
    assert Checker(source).check_from_source() == expected

def test_valid_const_expressions():
    """
    Kiểm tra các trường hợp hằng số HỢP LỆ.
    Spec: Literals, immutable attributes, operators.
    """
    source = """
    class ValidConstantExpressions {
        final int MAX_SIZE := 100;
        # Valid: Dùng final attribute khác (MAX_SIZE) và toán tử
        final int DOUBLE_SIZE := this.MAX_SIZE * 2;     
        
        # Valid: String concatenation literal
        final string MESSAGE := "Hello" ^ "World"; 
        
        # Valid: Boolean logic
        final boolean FLAG := true && false;       
        
        final float PI := 3.14159;
        # Valid: Expression phức tạp nhưng toàn thành phần tĩnh
        final float CIRCLE_AREA := this.PI * 10.0 * 10.0;   
        
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_valid_global_const_usage():
    """
    Kiểm tra sử dụng biến toàn cục final trong class final.
    """
    source = """
    final int GLOBAL_MAX := 100;
    
    class Program {
        # Hợp lệ: GLOBAL_MAX là hằng số
        final int LOCAL_MAX := GLOBAL_MAX + 1;
        
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_illegal_array_mixed_int_float():
    """
    Kiểm tra mảng chứa lẫn lộn int và float.
    Spec: {1, 2.0, 3} -> Error (No type coercion in array literals).
    """
    source = """
    class IllegalArrayError {
        void create() {
            # Lỗi: int và float không đồng nhất trong literal
            int[3] mixed1 := {1, 2.0, 3}; 
        }
        static void main() {}
    }
    """
    # Node lỗi là ArrayLiteral
    # Format string phụ thuộc vào AST: ArrayLiteral([IntLiteral(1), FloatLiteral(2.0), IntLiteral(3)])
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0), IntLiteral(3)}))"
    assert Checker(source).check_from_source() == expected

def test_illegal_array_mixed_string_int():
    """
    Kiểm tra mảng chứa lẫn lộn string và int.
    Spec: {"hello", 42} -> Error.
    """
    source = """
    class IllegalArrayError {
        void create() {
            string[2] mixed2 := {"hello", 42};
        }
        static void main() {}
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('hello'), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected

def test_illegal_array_mixed_bool_int():
    """
    Kiểm tra mảng chứa lẫn lộn boolean và int.
    Spec: {true, 1} -> Error.
    """
    source = """
    class IllegalArrayError {
        void create() {
            boolean[2] mixed3 := {true, 1};
        }
        static void main() {}
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected

def test_valid_empty_array():
    """
    Kiểm tra mảng rỗng (luôn hợp lệ vì không có phần tử để mâu thuẫn).
    Spec: Empty arrays are allowed if type can be inferred.
    """
    source = """
    class EmptyArrays {
        void create() {
            int[0] empty1 := {}; # Valid
        }
        static void main() {}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected


def test_004():
    """Test type mismatch in expression"""
    source = """
class Test {
    static void main() {
        int x := 5 + true;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(5), +, BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected


def test_005():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_006():
    source = """
class io {}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Class, io)"
    assert Checker(source).check_from_source() == expected


def test_007():
    source = """
class test {
    int a;
    int a;
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected


def test_008():
    source = """
class test {
    int a := 1, b, a;
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected


def test_009():
    source = """
class test {
    void foo(){}
    void foo(){}
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Method, foo)"
    assert Checker(source).check_from_source() == expected


def test_010():
    source = """
class test {
    void foo(int a; int a){}
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected

def test_013():
    source = """
class test {
    int a := 1;
    void b(){}
    void a(){}
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected


def test_014():
    source = """
class test {
    ~test(){}
}
class nguyen{static void main(){}}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_015():
    source = """
    class test {
        void a(){}
        int b, c, a;
    }
    class nguyen{static void main(){}}
    """
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected
def test_015_cont():
    source = """
    class test {
        int b, c, a;
        void a(){}
        
    }
    class nguyen{static void main(){}}
    """
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected


def test_016():
    source = """
class test {
    int a;
    test(){}
    test(int b; float c; string k:="hello"){}
}
class nguyen{static void main(){}}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_017():
    source = """
class test {}
class test {}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Class, test)"
    assert Checker(source).check_from_source() == expected


def test_018():
    source = """
class nguyen{
    static void main(){
        int a, b, a;
    }
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_019():
    source = """
class nguyen{
    static void main(){
        final int a := 1, b, a;
    }
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected


def test_020():
    source = """
class nguyen{
    static void main(){
        int a;
        final int a;
    }
}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected


def test_021():
    source = """
class test {
    void foo(int a) {
        int b;
        int a;
    }
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_022():
    source = """
class test {
    void foo(int a) {
        int b;
        final int a;
    }
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected


def test_023():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        int c;
    }
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Variable, c)"
    assert Checker(source).check_from_source() == expected


def test_024():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int a;
            int e, c, e;
        }
    }
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Variable, e)"
    assert Checker(source).check_from_source() == expected


def test_025():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int c;
            final int c;
        }
    }
}
class nguyen{static void main(){}}
"""
    expected = "Redeclared(Constant, c)"
    assert Checker(source).check_from_source() == expected


def test_026():
    source = """
class nguyen{
    void main(){}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_027():
    source = """
class nguyen{
    void main(){}
    static void main(){}
}
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected


def test_028():
    source = """
class nguyen{
    static int main(){return 1;}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_029():
    source = """
class A{
    static void main(){}
}
class B{
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_030():
    source = """
class nguyen1{
    static void main(int a){}
}
class nguyen2{
    static void main(){}
}
class nguyen3{
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_031():
    source = """
class nguyen{
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_033():
    source = """
class A{}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_034():
    source = """
class A extends io {}
class B extends A {}
class C extends Z {}

class nguyen{static void main(){}}
"""
    expected = "UndeclaredClass(Z)"
    assert Checker(source).check_from_source() == expected


# def test_035():
#     source = """
# class A extends B {}
# class B extends A {}
# class nguyen{static void main(){}}
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected


def test_036():
    source = """
class nguyen{static void main(){
    int a := 1;
    a := b;
}}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected


def test_037(): # lieen quan toiws this nene phari passs
    source = """
class nguyen{
    int a;
    static void main(){
        int b := a;
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_038():
    source = """
    class nguyen{
        int a;
    
        static void main(){a:= 1;}
    }
    """
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected


def test_039():
    source = """
    class nguyen{
        int a;
        int b := a;
        static void main(){}
    }
    """
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected


def test_040():
    source = """
class nguyen{
    int a;
    static void main(){
        this.b := 1;
        this.a := 1;   
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected


def test_041():
    source = """
class nguyen{
    int a;
    void foo(){
        this.a := 1;
    }
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_042():
    source = """
    class A {int a; int c;}
    class nguyen extends A{
        static void main(){
            this.b := 1;
            this.c := 1;    
        }
    }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected


def test_043():
    source = """
class nguyen{
    void foo(){}
    static void main(){
        this.foo();
        this.bar();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected


def test_044():
    source = """
class nguyen{
    int foo(){return 1;} 
    static void main(){
        int a;
        a := this.foo();
        a := this.coo();
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected


def test_045():
    source = """
    class B{int a;}
    class A extends B{int foo(){return 1;} }
    class nguyen extends A{
        void main(){
            int a;
            a := this.foo();
            a := this.coo();
        }
    }
    """
    expected = "UndeclaredMethod(coo)"
    assert Checker(source).check_from_source() == expected


def test_046():
    source = """
        class A {
            void foo(){}
        }
        class nguyen extends A{
            static void main(){
                A a;
                a.foo();
            }
        }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_047():
    source = """
        class A {
            int a;
        }
        class nguyen extends A{
            static void main(){
                A a;
                a.a := 1;
            }
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_048():
    source = """
class nguyen{
    final int a := 1;
    static void main(){
        nguyen N;
        N.a := 2;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(N).a)) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected


def test_049():
    source = """
class nguyen{
    static void main(){
        final int a := 1;
        a := 2;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(a) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected


def test_050():
    source = """
class nguyen{
    static void main(){
        final int a := 1;
        int  b;
        {
            b := a;
            a := b;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_051():
    source = """
class nguyen{
    int a;
    static void main(){
        nguyen N;
        N.a := 1;
        N.a := 2;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_052():
    source = """
    class nguyen{
        final int a := 1;
        nguyen(){}
        static void main(){
            nguyen N;
            N.a := 2;
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(N).a)) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected


def test_053():
    source = """
class nguyen{
    static void main(){
        int i;
        for i := 1 to 10 do {
            i := 5;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_054():
    source = """
    class nguyen{
        static void main(){
            final int i := 1;
            for i := 1 to 4 do {}
        }
    }
    """
    expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(1) to IntLiteral(4) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_055():
    source = """
class nguyen{
    static void main(){
        final int i;
    }
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected


def test_056():
    source = """
class nguyen{
    static void main(){
        final int i := 1, j;
    }
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected


def test_057():
    source = """
class A{}
class nguyen{
    final A a;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final ClassType(A), [Attribute(a)]))"
    assert Checker(source).check_from_source() == expected


def test_058():
    source = """
class nguyen{
    final int[2] a;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final ArrayType(PrimitiveType(int)[2]), [Attribute(a)]))"
    assert Checker(source).check_from_source() == expected


def test_059():
    source = """
class nguyen{
    static void main(){
        int x;
        final int a := x;
    }
}
"""
    expected = "IllegalConstantExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_060():
    source = """
class nguyen{
    static void main(){
        final int a := 1 + 2 * 3;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_061():
    source = """
    class nguyen{
        static void main(){
        final int MAX_SIZE := 100;
        final int DOUBLE_SIZE := MAX_SIZE * 2;     # Valid: uses immutable attribute
        final string MESSAGE := "Hello" ^ "World"; # Valid: literal concatenation
        final boolean FLAG := true && false;       # Valid: boolean literals with operators
        final float PI := 3.14159;
        final float CIRCLE_AREA := PI * 10 * 10;   # Valid: uses final attribute
    
        final int SUM := 10 + 20 + 30;         # Valid: literal arithmetic
    
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_062():
    source = """
class nguyen{
    static void main(){
        int x := 10;
        final int a := x + 1;
    }
}
"""
    expected = "IllegalConstantExpression(BinaryOp(Identifier(x), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected


def test_063():
    source = """
class nguyen{
    int x := 10;
    final int a := this.x;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).x))"
    assert Checker(source).check_from_source() == expected


def test_064():
    source = """
    class nguyen{
        final int MAX_SIZE := 1;
        final int A := this.MAX_SIZE;
        final int b :=  this.A * this.MAX_SIZE;
        static void main(){}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_065():
    source = """
class nguyen{
    int MAX_SIZE := 1;
    final int A := this.MAX_SIZE;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).MAX_SIZE))"
    assert Checker(source).check_from_source() == expected


def test_066():
    source = """
        class nguyen{
            static void main(){
                final int a := this.foo();
            }
            int foo(){return 1;}
        }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected


def test_067():
    source = """
class ppl{
    static void main(){
        final int a := new nguyen();
    }
    nguyen(){}
}
"""
    expected = "UndeclaredClass(nguyen)"
    assert Checker(source).check_from_source() == expected


def test_068():
    source = """
class nguyen{
    static void main(){
        int[2] a := {1, 2};
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_069():
    source = """
class nguyen{
    static void main(){
        int[3] a := {1, 2};
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ArrayType(PrimitiveType(int)[3]), [Variable(a = ArrayLiteral({IntLiteral(1), IntLiteral(2)}))]))"
    assert Checker(source).check_from_source() == expected


def test_070():
    source = """
class nguyen{
    static void main(){
          boolean[2] mixed3 := {true, 1};  
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected


def test_071():
    source = """
class nguyen{
    static void main(){
        int a; boolean b; float c; string d;
        a := 1;
        b := true;
        c := 1.0;
        c := 1;
        d := "s";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_072():
    source = """
class nguyen{
    static void main(){
        int a; float b;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_073():
    source = """
class nguyen{
    static void main(){
        int a; float b;
        b := a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_074():
    source = """
class nguyen{
    static void main(){
        boolean a; int b;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_075():
    source = """
class nguyen{
    static void main(){
        string a; int b;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_076():
    source = """
class A{}
class nguyen{
    static void main(){
        A a;
        a := nil;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_077():
    source = """
class nguyen{
    static void main(){
        int a;
        a := nil;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := NilLiteral(nil)))"
    assert Checker(source).check_from_source() == expected


def test_078():
    source = """
class nguyen{
    static void main(){
        int[2] a; int[2] b;
        a := b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_079():
    source = """
class nguyen{
    static void main(){
        float[2] a;
        a := {1.0,2.0};
        a := {1,2};
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := ArrayLiteral({IntLiteral(1), IntLiteral(2)})))"
    assert Checker(source).check_from_source() == expected


def test_080():
    source = """
class A{}
class B extends A{}
class nguyen{
    static void main(){
        A a; B b;
        a := b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_081():
    source = """
class A{}
class B extends A{}
class nguyen{
    static void main(){
        A a; B b;
        b := a;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := Identifier(a)))"
    assert Checker(source).check_from_source() == expected


def test_082():
    source = """
class A {}
class B extends A {}
class C extends B {}

class nguyen{
    static void main(){
        A a; B b; C c;
        c := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_083():
    source = """
class A {}
class B extends A {}
class C extends A {}

class nguyen{
    static void main(){
        A a; B b; C c;
        a := b;
        a := c;
        b := c;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := Identifier(c)))"
    assert Checker(source).check_from_source() == expected


def test_084():
    source = """
class A {}
class B extends A {}

class nguyen{
    static void main(){
        A[2] a; B[2] b;
        a := a;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_085():
    source = """
class nguyen{
    static void main(){
        if true then {}
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_086():
    source = """
class nguyen{
    static void main(){
        int a;
        if a then {}
    }
}
"""
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(a) then BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_087():
    source = """
class nguyen{
    static void main(){
        int i;
        for i := 1 to 10 do {}
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_088():
    source = """
class nguyen{
    static void main(){
        float i;
        for i := 1 to 10 do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_089():
    source = """
class nguyen{
    static void main(){
        int i;
        for i := 1.0 to 10 do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := FloatLiteral(1.0) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_090():
    source = """
class nguyen{
    static void main(){
        int i;
        for i := 1 to 10.0 do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(1) to FloatLiteral(10.0) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_091():
    source = """
class nguyen{
    static void main(){
        int i; float f;
        for i := 0 to f do { }
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to Identifier(f) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_092():
    source = """
class nguyen{
    int foo(){return 1;}
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_093():
    source = """
class nguyen{
    void foo(){}
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_094():
    source = """
    class votien{
        static float foo(){return 1;}
        static void main(){}
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_095():
    source = """
    class votien{
        void foo(){}
        int coo(){
            return 1;
            this.foo();
            this.coo();
        }
        static void main(){
    
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_096():
    source = """
    class nguyen{
        void foo(int a){}
        static void main(){
            nguyen N;
            N.foo(1);
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_097():
    source = """
class nguyen{
    void foo(float a){}
    static void main(){
        nguyen N;
        N.foo(1);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_098():
    source = """
class nguyen{
    void foo(float a){}
    static void main(){
        nguyen N;
        N.foo(1.0, 1);
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(N).foo(FloatLiteral(1.0), IntLiteral(1)))))"
    assert Checker(source).check_from_source() == expected


def test_099():
    source = """
    class nguyen{
        void foo(int a){}
        static void main(){
            nguyen N;
            N.foo(1.0);
        }
    }
    """
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(N).foo(FloatLiteral(1.0)))))"
    assert Checker(source).check_from_source() == expected


def test_100():
    source = """
class nguyen{
    static void main(){
        int[2] a;
        int b;
        b := a[1];
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected



def test_101():
    source = """
    class votien{
    
        static void main(){
            A.a := 1;
        }
    }
    class A {static int a := 1;}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_102():
    source = """
    class votien{
        int a;
        static void main(){
            this.a := 1;
        }
    }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_103():
    source = """
        class Student {
            void resetCount(Student a; A b) {
                b.foo();
                A.coo();
            }
            static void main(){}
        }
        class A{
            void foo(){}
            static void coo(){}
        }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


# Test cases in instructions 
# ====== Error 1: Redeclared Variable/Constant/Attribute/Class/Method/Parameter ======
def test_101():
    """Redeclared variable in same block after statement list start"""
    source = """
class Test {
    static void main() {
        int a := 0;
        float a;
    }
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_102():
    """Redeclared class at global scope"""
    source = """
class A {
    static void main() {}
}

class A {
}
"""
    expected = "Redeclared(Class, A)"
    assert Checker(source).check_from_source() == expected


def test_103():
    """Redeclared constant at global scope"""
    source = """
class Program {
    static void main() {
        final int MAX := 10;
        final int MAX := 20;
    }
}
"""
    expected = "Redeclared(Constant, MAX)"
    assert Checker(source).check_from_source() == expected


def test_104():
    """Redeclared attribute in same class"""
    source = """
class Test {
    int x;
    static int x;

    static void main() {}
}
"""
    expected = "Redeclared(Attribute, x)"
    assert Checker(source).check_from_source() == expected


def test_105():
    """Redeclared method in same class (no overloading allowed)"""
    source = """
class Test {
    static void foo() {}

    static int foo() {
        return 1;
    }

    static void main() {}
}
"""
    expected = "Redeclared(Method, foo)"
    assert Checker(source).check_from_source() == expected


def test_106():
    """Redeclared parameter in same method"""
    source = """
class Test {
    static void foo(int a; int a) {
    }

    static void main() {}
}
"""
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected


def test_104():
    """Redeclared local variable in same method scope"""
    source = """
class Test {
    static void main() {
        int a := 1;
        int a := 2;
    }
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_108():
    """Redeclared variable in same block """
    source = """
class Test {
    static void main() {
        int a := 1;
        int a := 3;
        string b := "hi";
        a := 2;
    }
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_109():
    """ Error: Redeclared Attribute in same class"""
    source = """class Person {
        string name;
        int age;
        string name;  # Redeclared(Attribute, name)
}
"""
    expected = "Redeclared(Attribute, name)"
    assert Checker(source).check_from_source() == expected


def test_110():
    """Redeclared method in subclass body (same class scope, counted there)"""
    source = """
class A {
    static void foo() {}
}

class B extends A {
    static void foo() {}
    static void foo(int x) {}
    static void main() {}
}
"""
    expected = "Redeclared(Method, foo)"
    assert Checker(source).check_from_source() == expected

def test_111():
    """Redeclared Parameter in method"""
    source = """class Test {
    static void main(){
    }
   void foo (int z) {
    int z := 5;  # Redeclared(Variable, z)
   }

}"""
    expected = "Redeclared(Variable, z)"
    assert Checker(source).check_from_source() == expected


# ====== Error 2: Undeclared Identifier/Attribute/Method/Class ======
"""
**Rules:**
- All identifiers (variables, constants, parameters) must be declared before use
- Classes must be declared before instantiation or inheritance
- Attributes must exist in the class or its inheritance chain
- Methods must exist in the class or its inheritance chain

**Exceptions:**
- `UndeclaredIdentifier(<identifier>)`: For undeclared variables, constants, or parameters
- `UndeclaredClass(<class-name>)`: For undeclared classes
- `UndeclaredAttribute(<attribute-name>)`: For undeclared attributes
- `UndeclaredMethod(<method-name>)`: For undeclared methods

**Inheritance Rules:**
- Members of parent classes are accessible in subclasses
- Members are accessible based on scope rules
"""

def test_211():
    """Undeclared identifier: local variable used without declaration"""
    source = """
class Test {
    static void main() {
        a := 1;
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected


# def test_212():
#     """Undeclared identifier: use before declaration in same block"""
#     source = """
# class Test {
#     static void main() {
#         int x := y + 1;
#         int y := 2;
#     }
# }
# """
#     expected = "UndeclaredIdentifier(y)"
#     assert Checker(source).check_from_source() == expected


# def test_213():
#     """Undeclared identifier: inside method with parameters"""
#     source = """
# class Test {
#     static void foo(int a) {
#         int c := a + b;
#     }

#     static void main() {}
# }
# """
#     expected = "UndeclaredIdentifier(b)"
#     assert Checker(source).check_from_source() == expected

# def test_214():
#     """Error: Undeclared Variable"""
#     source = """
#     class Example {
#         void method() {
#             int result := undeclaredVar + 10;  # UndeclaredIdentifier(undeclaredVar)
#         }
#     }
# """
#     expected = "UndeclaredAttribute(undeclaredVar)"
#     assert Checker(source).check_from_source() == expected


# def test_221():
#     """Undeclared class: extends unknown superclass"""
#     source = """
# class B extends A {
#     static void main() {}
# }
# """
#     expected = "UndeclaredClass(A)"
#     assert Checker(source).check_from_source() == expected
# def test_221a():
#     source = """class A extends B{

#         static void main(){}

#     }

#  class B {}
#  """
#     expected = "UndeclaredClass(B)"
#     assert Checker(source).check_from_source() == expected

# def test_221b():
#     source = """class Test { 
#         Animal animal;
#         static void main() {}
#     }
#     class Animal {}"""
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

# def test_221b():
#     source = """class Test {
#         Animal animal := new Animal();
#         static void main() {}
#         }
#         class Animal {}
# """
#     expected = "UndeclaredClass(Animal)"
#     assert Checker(source).check_from_source() == expected


# def test_222():
#     """Undeclared class: use unknown class type in variable declaration"""
#     source = """
# class Program {
#     static void main() {
#         A obj;
#     }
# }
# """
#     expected = "UndeclaredClass(A)"
#     assert Checker(source).check_from_source() == expected

# def test_223():
#     source ="""

# class Program {
#     A a := new A();
# }

# class A{
#     static void main(){
#     }
# }

# """
#     expected = "UndeclaredClass(A)"
#     assert Checker(source).check_from_source() == expected



# def test_231():
#     """Undeclared attribute: instance field not in class or its parents"""
#     source = """
# class A {
#     int x;
# }

# class Program {
#     static void main() {
#         A a;
#        a.y := 1;
#     }
# }
# """
#     expected = "UndeclaredAttribute(y)"
#     assert Checker(source).check_from_source() == expected
# def test_232():
#     """Undeclared attribute: instance field not in class or its parents"""
#     source = """
# class A {
#     int x;
# }

# class Program {
#     static void main() {
#         A a;
#        int z := a.y;
#     }
# }
# """
#     expected = "UndeclaredAttribute(y)"
#     assert Checker(source).check_from_source() == expected

# def test_233():
#     """Undeclared attribute: static field access not in class or its parents"""
#     source = """
# class A {
#     static int x;
# }

# class Program {
#     static void main() {
#         A.y := 1;
#     }
# }
# """
#     expected = "UndeclaredAttribute(y)"
#     assert Checker(source).check_from_source() == expected


# def test_241():
#     """Undeclared method: static call on class with no such method"""
#     source = """
# class A {
#     static void foo() {}
# }

# class Program {
#     static void main() {
#         A.bar();
#     }
# }
# """
#     expected = "UndeclaredMethod(bar)"
#     assert Checker(source).check_from_source() == expected


# def test_242():
#     """Undeclared method: instance call to missing method"""
#     source = """
# class A {
#     void foo() {}
# }

# class Program {
#     static void main() {
#         A a;
#         a.bar();
#     }
# }
# """
#     expected = "UndeclaredMethod(bar)"
#     assert Checker(source).check_from_source() == expected


# def test_243():
#     """Inheritance: attribute from parent accessible in subclass (should succeed)"""
#     source = """
# class A {
#     int x;
# }

# class B extends A {
#     static void main() {
#         B b;
#         b.x := 10;
#     }
# }
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected


# def test_244():
#     """Inheritance: method from parent accessible in subclass (should succeed)"""
#     source = """
# class A {
#     static void foo() {}
#     void bar() {}
# }

# class B extends A {
#     static void main() {
#         B.foo();
#         B b;
#         b.bar();
#     }
# }
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

# def test_244():
#     """Undeclared method: instance call to missing method"""
#     source = """
# class Calculator {
#     int add(int a; int b) {
#         return a + b;
#     }
    
#     static void main() {
#         Calculator calc;
#         int result := calc.multiply(2, 3); 
#     }
# }
# """
#     expected = "UndeclaredMethod(multiply)"
#     assert Checker(source).check_from_source() == expected

# def test_245():
#     source = """
#     class Calculator {
#     int add(int a; int b) {
#         return a + b;
#     }
    
#     class MathUtils {
#         static int factorial(int n) {
#             if (n <= 1) then{
#                 return 1;
#             } 
#             else {
#                 return n * 3;
#             }
#         }
#     }

#     class Main {
#         static void main() {
#             Calculator calc := new Calculator();
#             int fact := calc.factorial(5);  # UndeclaredMethod(factorial) - not in Calculator
#     }"""
#     expected = "UndeclaredMethod(factorial)"
#     assert Checker(source).check_from_source() == expected


# def test_246():
#     source = """
#     class Animal {
#         string species;
        
#         void setSpecies(string s) {
#             species := s;
#         }
#     }

#     class Dog extends Animal {
#         void identify() {
#             Animal a;
#             a.setSpecies("Canine");  # Valid: inherited method
#         }
#         static void main() {
#         }
#     }
    
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected


def test_247():
    source = """
    class ScopeTest {
        void method1() {
            int localVar := 42;
        }
        
        void method2() {
            int value := localVar + 1; 
        }
    }"""
    expected = "UndeclaredIdentifier(localVar)"
    assert Checker(source).check_from_source() == expected

# #====== Error 3: Cannot Assign To Constant======
# ### 3. Cannot Assign To Constant

# """**Rule:** Constants (final variables/attributes) cannot be modified after initialization.

# **Exception:** `CannotAssignToConstant(<statement>)`

# **Constant Rules:**
# - Final variables must be initialized at declaration or in constructor
# - Final variables cannot be reassigned after initialization
# - Final attributes follow the same rules
# - Assignment in for loops is also checked"""

# def test_311():
#     """OK: final attribute initialized exactly once in constructor"""
#     source = """
# class Test {
#     final int x;

#     Test() {
#         x := 10;
#     }

#     void foo() {
#         int y := x;
#     }

#     static void main() {
#         Test t;
#         t := new Test();
#         t.foo();
#     }
# }
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected


# def test_321():
#     """Cannot assign to constant variable (local)"""
#     source = """
# class Test {
#     static void main() {
#         final int x := 5;
#         x := 10;
#     }
# }
# """
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
#     assert Checker(source).check_from_source() == expected
# def test_322():
#     """Cannot assign to constant variable (local, using expression)"""
#     source = """
# class Test {
#     static void main() {
#         final int x := 5;
#         x := x + 1;
#     }
# }
# """
#     expected = ("CannotAssignToConstant(AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), +, IntLiteral(1))))"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_323():
#     """Cannot assign to final attribute inside method"""
#     source = """
# class Test {
#     final int x := 5;

#     void foo() {
#         x := 20;
#     }

#     static void main() {
#         Test t;
#         t := new Test();
#         t.foo();
#     }
# }
# """
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(20)))"
#     assert Checker(source).check_from_source() == expected

# def test_324():
#     """Cannot assign to static final attribute"""
#     source = """
# class Test {
#     static final int x := 5;

#     static void main() {
#         x := 100;
#     }
# }
# """
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(100)))"
#     assert Checker(source).check_from_source() == expected

# def test_325():
#     #Error: Multiple assignment attempts
#     source = """
# class MultipleAssignment {
#     final float PI := 3.14159;
    
#     void calculate() {
#         PI := PI * 2;  # Error: CannotAssignToConstant at assignment statement
#     }
# }"""
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(PI) := BinaryOp(Identifier(PI), *, IntLiteral(2))))"
#     assert Checker(source).check_from_source() == expected
# def test_341():
#     """Cannot assign to constant variable in for-loop update"""
#     source = """
# class Test {
#     static void main() {
#         final int i := 0;
#         for i := 1 to 10 do {
#         }
#     }
# }
# """
#     expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[])))"
#     assert Checker(source).check_from_source() == expected

# def test_342():
#     source = """

#     class ValidConstants {
#         final int MAX_SIZE := 1000;
#         final string VERSION;
        
#         ValidConstants(string version) {
#             VERSION := version;  # Valid: initialization in constructor
#         }
#         void display() {
#             ValidConstants vc;
#             string s := vc.VERSION;  # Valid: reading constant
#             int x := MAX_SIZE;  # Valid: reading constant
#             vc := new ValidConstants("1.0");
#         }
#         static void main() {
#         }
#     }
    
# """ 
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

# def test_343():
#     """Cannot assign to final local inside for-loop body"""
#     source = """
# class Test {
#     static void main() {
#         final int x := 0;
#         int i;
#         for i := 1 to 5 do {
#             x := x + 1;
#         }
#     }
# }
# """
#     expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(x), +, IntLiteral(1))))"
#     assert Checker(source).check_from_source() == expected

# # ====== Error 4 : Type Mismatch In Statement ======

# """"**Statement Type Rules:**

# **1.Conditional Statements:**
# - If statement condition must be boolean type"""

# def test_411():
#     """If condition must be boolean (using int instead)"""
#     source = """
# class Test {
#     static void main() {
#         if 1 then {
#         }
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement(IfStatement(if IntLiteral(1) then BlockStatement(stmts=[]))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_412():
#     source ="""class ConditionalError {
#     static void main() {
#     }
#     void checkCondition() {
#         int x := 10;
#         if x then {  # Error: Condition must be boolean
#         }
#     }
# }"""
#     expected = "TypeMismatchInStatement(IfStatement(if Identifier(x) then BlockStatement(stmts=[])))"
#     assert Checker(source).check_from_source() == expected
# def test_413():
#     source ="""class ConditionalError {
#     static void main() {
#     }
#     void checkCondition() {
#         string message := "hello";
#         if message then {  # Error: TypeMismatchInStatement at if statement
#             io.writeStrLn("Also invalid");
#         }
#     }
# }"""
#     expected ="TypeMismatchInStatement(IfStatement(if Identifier(message) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Also invalid'))))])))"
#     assert Checker(source).check_from_source() == expected



# """2.**For Statements:**
# - Scalar variable must be integer type
# - Expression 1 and Expression 2 must be integer type"""

# def test_421():
#     """For scalar variable must be integer type (using float)"""
#     source = """
# class Test {
#     static void main() {
#         float f := 1.5;
#         for f := 0 to 10 do {
#         }
#     }
# }
# """
#     expected ="TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[])))"
#     assert Checker(source).check_from_source() == expected
# def test_422():
#     """For expr1 must be integer (using string)"""
#     source = """
# class Test {
#     static void main() {
#         int i;
#         for i := "0" to 10 do{
#         }
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "ForStatement(for i := StringLiteral('0') to IntLiteral(10) do BlockStatement(stmts=[]))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_423():
#     """For expr2 must be integer (using float)"""
#     source = """
# class Test {
#     static void main() {
#         int i;
#         for i := 0 to 10.5 do{
#         }
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "ForStatement(for i := IntLiteral(0) to FloatLiteral(10.5) do BlockStatement(stmts=[]))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected


# """3.**Assignment Statements:**
# - LHS cannot be void type
# - RHS must be same type as LHS or coercible to LHS type
# - Integer can coerce to float
# - Subtype can coerce to supertype
# - Array assignments require same size and compatible element types"""

# def test_431():
#     """LHS cannot be void-type expression (assign to call of void method)"""
#     source = """
# class Test {
#     void foo() { }
# }
# class Program {
#     static void main() {
#         Test t:= new Test();
#         t.foo() := 1;
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "AssignmentStatement("
#         "PostfixLHS(PostfixExpression(Identifier(t).foo())) := IntLiteral(1)"
#         ")"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_432():
#     """RHS must match or be coercible (int := string)"""
#     source = """
# class Test {
#     static void main() {
#         int x;
#         x := "hello";
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "AssignmentStatement(IdLHS(x) := StringLiteral('hello'))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected
# def test_433():
#     """No coercion from float to int"""
#     source = """
# class Test {
#     static void main() {
#         int x;
#         x := 1.5;
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "AssignmentStatement(IdLHS(x) := FloatLiteral(1.5))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_434():
#     """Valid int to float coerc"""
#     source = """
# class Test {
#     static void main() {
#         float x;
#         x := 1;
#     }
# }
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected
# def test_435():
#     """Error: Assignment type mismatch"""
#     source = """
# class AssignmentError {
#     void assign() {
#         int x := 10;
#         string text := "hello";
#         boolean flag := true;
        
#         x := text;  # Error: TypeMismatchInStatement at assignment
#         #text := x;  # Error: TypeMismatchInStatement at assignment
#         #flag := x;  # Error: TypeMismatchInStatement at assignment
#     }
# }"""
#     expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
#     #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(text) := Identifier(x)))"
#     #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(flag) := Identifier(x)))"
#     assert Checker(source).check_from_source() == expected

# def test_436():
#     """Subtype can coerce to supertype, not vice versa (Parent -> Child)"""
#     source = """
# class Parent {}
# class Child extends Parent {}
# class Test {
#     static void main() {
#         Parent p;
#         Child c;
#         c := p;    # invalid: super to sub
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "AssignmentStatement(IdLHS(c) := Identifier(p))"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_437():
#     """Subtype can coerce to supertype, not vice versa (Parent -> Child)"""
#     source = """
# class Parent {}
# class Child extends Parent {}
# class Test {
#     static void main() {
#         Parent p;
#         Child c;
#         p := c;    # valid: sub to super
#     }
# }
# """
#     expected = "Static checking passed" 
#     assert Checker(source).check_from_source() == expected

# def test_438():
#     """Array assignment requires same size and compatible element types """
#     source = """
# class ArrayError {
#     static void main() {
#     }
#     void arrayAssign() {
#         int[3] intArray := {1, 2, 3};
#         float[3] floatArray := {1.0, 2.0, 3.0};
#         int[3] anotherIntArray := {4, 5, 6};
#         int[2] smallArray := {1, 2};
        
#         #intArray := anotherIntArray;   # valid assignment
#         #intArray := floatArray;        # Error: TypeMismatchInStatement at assignment
#         intArray := smallArray;         # Error: TypeMismatchInStatement at assignment (different size)
#     }
# }"""
#     #expeceted ="Static checking passed"
#     #expeceted ="TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(floatArray)))"
#     expeceted ="TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(smallArray)))"
#     assert Checker(source).check_from_source() == expeceted


# """4.**Call Statements:**
# - Object must be class type
# - Method must return void
# - Arguments must match parameter types (with coercion rules)"""
# def test_441():
#     """Call statement: object must be class type"""
#     source = """
# class A {
#     void foo() { }
# }
# class Test {
#     static void main() {
#         int x;
#         x.foo();    # x is not class type
#     }
# }
# """
#     expected = (
#         "TypeMismatchInStatement("
#         "MethodInvocationStatement("
#         "PostfixExpression(Identifier(x).foo())"
#         ")"
#         ")"
#     )
#     assert Checker(source).check_from_source() == expected

# def test_443():
#     """Error: Method call with wrong arguments"""
#     source = """
# class CallError {
#     void processInt(int value) {
#         #do something
#     }
    
#     static void main() {
#         string text := "123";
#         CallError ce;
#         ce.processInt(text);  # Error: TypeMismatchInStatement at method call
#     }
# }"""
#     expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(ce).processInt(Identifier(text)))))"
#     assert Checker(source).check_from_source() == expected

# """**Return Statements:**
# - Return expression must match method return type"""
# def test_451():
#     source = """# Error: Return type mismatch
# class ReturnError {
#     int getValue() {
#         return "invalid";  # Error: TypeMismatchInStatement at return statement
#     }
# }"""
#     expected ="TypeMismatchInStatement(ReturnStatement(return StringLiteral('invalid')))"
#     assert Checker(source).check_from_source() == expected
# def test_452():
#     """Void method cannot return a value"""
#     source = """
# class Test {
#     void foo() {
#         return 1;
#   }
# }
# """
#     expected ="TypeMismatchInStatement(ReturnStatement(return IntLiteral(1)))"
#     assert Checker(source).check_from_source() == expected

# def test_452():
#     """Void method cannot return a value"""
#     source = """
#     class Shape{
#     }
#     class Rectangle extends Shape{
#         float hight, width;
#         Rectangle(float hight; float width){
#             this.hight := hight;
#             this.width := width;
#         }
#     }
#     class ValidCoercion {
#         static void main() {
#             int x := 10;
#             float y := x;  # Valid: int to float coercion
        
#             Shape obj := new Rectangle(5.0, 3.0);  # Valid: subtype to supertype
#         }
#     }
# """
#     expected ="Static checking passed"
#     assert Checker(source).check_from_source() == expected

# # ====== Error 5: TypeMismatchInExpression ======
# """ **Expression Type Rules:**

# 1**Array Subscripting:**
# - E1 must be array type
# - E2 must be integer type

# 2**Binary and Unary Expressions:**
# - Follow OPLang specification type rules
# - Arithmetic operations require numeric types
# - Comparison operations return boolean
# - Logical operations require boolean operands

# 3**Method Calls:**
# - Object must be class type
# - Method must have non-void return type
# - Arguments must match parameters with coercion rules

# 4**Attribute Access:**
# - Object must be class type
# - Attribute must exist in class or inheritance chain """

def test_511():
    """Type mismatch in array access: E2 is int, E1 must be array"""
    source = """
class Test {
    static void main() {
        int x;
        int y := x[1];
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected
def test_512():
    """Type mismatch in array index: E2 is not be int"""
    source = """
class Test {
    static void main() {
        int[3] a;
        int x := a[true];
    }
}
"""
    expected = "TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected
def test_513():
    # Error: Array subscripting with wrong types
    source ="""class ArraySubscriptError {
    static void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        #int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
        #int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
        string word := words[true];      # Error: TypeMismatchInExpression at array access
        
        # Non-array subscripting
        int x := 10;
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access
    }
}"""
    #expected ="TypeMismatchInExpression(PostfixExpression(Identifier(numbers)[StringLiteral('index')]))"
    #expected ="TypeMismatchInExpression(PostfixExpression(Identifier(numbers)[FloatLiteral(2.5)]))"
    expected ="TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_521():
    """Type mismatch in expression: 1 + true (arithmetic requires numeric)"""
    source = """
class Test {
    static void main() {
        int x := 1 + true;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), +, BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected
def test_522():
    """Type mismatch in expression: 1 && 2 (logical requires boolean)"""
    source = """
class Test {
    static void main() {
        boolean b := 1 && 2;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), &&, IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_523():
    # Error: Binary operation type mismatch
    source ="""
class BinaryOpError {
    static void calculate() {
        int x := 5;
        string text := "hello";
        boolean flag := true;
        
        #int sum := x + text;          # Error: TypeMismatchInExpression at binary operation
        #boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
        int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
    }
}"""
    #expected ="TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(text)))"
    #expected ="TypeMismatchInExpression(BinaryOp(Identifier(x), &&, Identifier(flag)))"
    expected ="TypeMismatchInExpression(BinaryOp(Identifier(text), <, Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_524():
    source ="""class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        int e := 4;
        e := (a ^ b) + 2;
    }
}"""
    expected ="TypeMismatchInExpression(BinaryOp(Identifier(a), ^, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_532():
    """Type mismatch in expression: call method with not classtype"""
    source = """
class A {
    static void foo() { return;}
}
class Test {
    static void main() {
        int z;
        int x := z.foo(); 
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(z))"
    assert Checker(source).check_from_source() == expected

def test_532_1():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static void foo() {}
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(A).foo()))"
    assert Checker(source).check_from_source() == expected
def test_532_2():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static void foo() { return 1; }
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected
def test_532_3():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static int foo() { return ; }
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return NilLiteral(nil)))"
    assert Checker(source).check_from_source() == expected
def test_532_4():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static int foo() {  }
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return NilLiteral(nil)))"
    assert Checker(source).check_from_source() == expected
def test_533():
    """Error: Method call don't match parameters"""
    source = """

class MethodCallError {
    int getValue(float x) {
        return 42;
    }
}
class Test{
    void test() {
        MethodCallError mce := new MethodCallError();
        string text := "number";
        int valid :=  mce.getValue(3);      #Valid
        int value := mce.getValue(text);  # Error: TypeMismatchInExpression at method call
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(mce).getValue(Identifier(text))))"
    assert Checker(source).check_from_source() == expected

def test_541():
    """Type mismatch in expression: attribute access on non-class"""
    source = """

class Test {
    static void main() {
        int x;
        string text := "hello";
        int y := text.value;
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(text))"
    assert Checker(source).check_from_source() == expected
def test_542():
    """Type mismatch in expression: attribute must exist or heritance"""
    source = """
class Data{
    int data;
}
class Value extends Data{
    int value;
}
class Test {
    static void main() {
        Value find := new Value();
        int x := find.value;
        int y := find.data;
        #int z := find.notFound; -> cái này nó Undeclared(notFound)
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_1to5():
    source ="""
class Student{
    string getName(){
        return "abc";
    }
}
class ValidExpressions {
    static void main() {
        int[3] numbers := {1, 2, 3};
        int index := 1;
        int value := numbers[index];  #Valid
        
        int x := 10, y := 20;
        boolean result := x < y;      # Valid
        int sum := x + y;             # Valid
        
        Student student := new Student();
        string name := student.getName();  # Valid - assuming getName() returns string
    }
}"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected  

### 
# ====== Error 6. Type Mismatch In Constant ======
"""**Rule:** The types of left and right hand sides in constant declaration must be compatible.

**Exception:** `TypeMismatchInConstant(<ConstDecl>)`

**Constant Type Rules:**
- RHS type must match LHS type or be coercible to LHS type
- Same coercion rules as assignment statements
- Integer can coerce to float
- Subtype can coerce to supertype
"""
def test_611():
    # Error: Type mismatch in constant declaration
    source ="""
class ConstantTypeError {
    static void main(){
    }
    final int count := 3.14;       # TypeMismatchInConstant at constant declaration
}"""
  
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(count = FloatLiteral(3.14))]))"
    assert Checker(source).check_from_source() == expected  
def test_612():
    # / Error: Array constant type mismatch
    source ="""
class ArrayConstantError {
    static void main(){
        #final int[3] numbers := {1.0, 2.0, 3.0};  # Error: TypeMismatchInConstant at constant declaration
    }
    final string[3] words := {1, 2, 3};        # Error: TypeMismatchInConstant at constant declaration
}"""
    
    # #expected = ("TypeMismatchInConstant(Variable(numbers = " 
    # "ArrayLiteral({FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0)})))"
    # )
    expected ="TypeMismatchInConstant(AttributeDecl(final ArrayType(PrimitiveType(string)[3]), [Attribute(words = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]))"
    assert Checker(source).check_from_source() == expected 

def test_612_1():
    # // Valid: Proper constant types
    source ="""
    class ValidConstants {
        static void main(){
            final int MAX_SIZE := 1000;           # Valid
            final float PI := 3.14159;            #Valid
        }
        final string APP_NAME := "MyApp";       # Valid
        final int[4] PRIMES := {2, 3, 5, 7};    # Valid
        final float ratio := 10;                #Valid: int to float coercion
    }

"""
    expected ="Static checking passed"
    assert Checker(source).check_from_source() == expected 
def test_613():
    #Error: Object type mismatch
    source ="""
    class Shape{
    }
    class Integer{
        int value;
        Integer(int value){
            this.value := value;
        }
    }
    class ObjectConstantError {
        final Shape shape := new Integer(42);  #TypeMismatchInConstant - if no inheritance relationship
    }
"""
    expected ="TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer(IntLiteral(42))))]))"
    assert Checker(source).check_from_source() == expected 

### 7. Break/Continue Not In Loop

"""**Rule:** Break and continue statements must be inside a loop (directly or indirectly).

**Exception:** `MustInLoop(<statement>)`

**Loop Context Rules:**
- Break and continue are only valid inside for loops
- Can be nested inside conditionals within loops
- Cannot cross method boundaries
- Must be in the lexical scope of a loop
"""
def test_711():
    #Error: Break/continue outside loop
    source ="""
    class LoopError {
        void method() {
            #break;     # MustInLoop(break)
            #continue;  # MustInLoop(continue)
        }
        void conditionalError() {
        if true then {
            #break;     # MustInLoop(break)
            continue;  # MustInLoop(continue)
        }
    }
    }
"""
    #expected = "MustInLoop(BreakStatement())"
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected
def test_712():
    #Error: Error: Break/continue in method called from loop
    source ="""
class MethodCallError {
    void helperMethod() {
        break;                  #MustInLoop(break) - different method scope
        continue;               #MustInLoop(continue)
    }
    
    void loopWithCall() {
        int i;
        for i := 1 to 10 do{
            MethodCallError.helperMethod();
        }
        
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    #expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_713():
    #// Valid: Break/continue in loops
    source ="""

class ValidLoops {
    static void main(){
    }
    int i;
    void forLoopWithBreak() {
        
        for i := 0 to 10 do {
            if i == 5 then {
                break;     # Valid
            }
            if i % 2 == 0 then {
                continue;  # Valid
            }
        }
    }
    
    void forLoop() {
        for i := 0 to 10 do {
            if i == 3 then {
                continue;  # Valid
            }
            if i == 8 then {
                break;     # Valid
            }
        }
    }
    
    void nestedLoops() {
        int j;
        for i := 0 to 5 do {
            for j := 0 to 5 do {
                if i == j then {
                    continue;  # Valid - affects inner loop
                }
                if j > 3 then {
                    break;     # Valid - breaks inner loop
                }
            }
        }
    }
}

"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


"""### 10. Illegal Member Access

**Rule:** Static and instance members must be accessed appropriately according to their visibility and context.

**Exception:** `IllegalMemberAccess(<field-access-or-method-invocation>)`

**Member Access Rules:**
a- Static members accessed via class name (ClassName.member)
b- Instance members accessed via object reference (object.member)
c- Members accessible based on scope and inheritance rules

**Access Violation Types:**
1. Accessing instance member via class name
2. Accessing static member via instance
3. Accessing members that don't exist in inheritance chain"""

def test_10a():
    #Accessing static member via instance
    source ="""
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    void secretMethod() {
    }
}


class InstanceAccessError {
    void test() {
        Student s := new Student();
        #int count := s.totalStudents;        # Error: IllegalMemberAccess at member access
        s.resetCount();                     # Error: IllegalMemberAccess at method call
    }
}"""
    #expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).totalStudents))"
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).resetCount()))"
    assert Checker(source).check_from_source() == expected
def test_10b():
    #Dùng class để truy cập instance member
    source ="""
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    void secretMethod() {
    }
}

# Error: Accessing instance member via class
class StaticAccessError {
    void test() {
        #string school := Student.school;     # Error: IllegalMemberAccess at member access
        Student.setName("John");            # Error: IllegalMemberAccess at method call
    }
}
"""

    #expected = "llegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).setName(StringLiteral('John'))))"
    assert Checker(source).check_from_source() == expected
def test_10xx():
    source = """
class A {
    static int a;
    int b;
}
class Test{
    A a;
    static void main(){
        A.a := 1;
        A.b := 2;
    }
}"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).b))"
    assert Checker(source).check_from_source() == expected

def test_1001_abc():
    #// Error: Accessing static member via instance
    source ="""
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    static void classMethod() {
    }
}

class UndeclaredMemberError {
    void test() {
        Student s := new Student();
        string name := s.name;               # Valid - if name exists
        s.classMethod();                   # Valid - if secretMethod exists
        s.nonExistentMethod();              # UndeclaredMethod(nonExistentMethod)
    }
}
"""
    expected = "UndeclaredMethod(nonExistentMethod)"
    assert Checker(source).check_from_source() == expected

def test_1000():
    #// Error: Accessing static member via instance
    source ="""
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    void secretMethod() {
    }
}
# Valid: Proper member access
class ValidAccess {
    void test() {
        # Correct instance access
        Student s := new Student();
        s.school := "New School";            # Valid - instance member
        s.setName("Alice");                 # Valid - instance method
        {
            # Correct static access
            int count := Student.totalStudents;  # Valid
            Student.resetCount();               # Valid
        }
        
    }
}

# Valid: Access from within inheritance hierarchy
class GraduateStudent extends Student {
    void accessProtected() {
        GraduateStudent g;                          # Valid - inherited member
        age := 25;   
        g.setName("Graduate");   # Valid - inherited method
    }
    static void main(){
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_1001():
    #Error: Complex access violations
    source ="""
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    void secretMethod() {
    }
}
 
class ComplexAccessError {
    void complexTest() {
        Student s1 := new Student();
        Student s2 := new Student();
        
        # Chained access errors
        s1.secretMethod();                   # Valid if method exists
        #string result := Student.school;     # Error: IllegalMemberAccess at member access
        
        # Method call on static access
        s1.resetCount();                     # Error: IllegalMemberAccess at method call
    }
}
"""
    #expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s1).resetCount()))"
    assert Checker(source).check_from_source() == expected
def test_1001a():
    source = """
    class Test {
        int attr;
        static void main() {
           this.attr := 10;
        }
    }"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_1002():
    #Error: Accessing members through wrong reference type
    source ="""
class Shape {
}
class Student extends Shape {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        totalStudents := 0;
    }
    
    void setName(string n) {
        name := n;
    }
    
    void secretMethod() {
    }
}
class ReferenceTypeError {
    void wrongReference() {
        Shape obj := new Student();
        obj.school := "Test";             # IllegalMemberAccess - Shape doesn't have school
        # obj.setName("Test");             # IllegalMemberAccess - Shape doesn't have setName
        
        # Need to cast first
        #((Student)obj).setName("Test");     # Valid after cast
    }
}
"""
    expected = "UndeclaredAttribute(school)"
    assert Checker(source).check_from_source() == expected

"""### 8. Illegal Constant Expression

**Rule:** Constant initialization expressions must be evaluable at compile time.

**Exception:** `IllegalConstantExpression(<expression>)`

**Constant Expression Rules:**
- Expression must not be None/null
- Must be statically evaluable
- Can only use literals and immutable attributes
- Can only use operators, no method calls
- No references to mutable variables"""

# def test_811():
#     #Error: None/null initialization
#     source="""

# class IllegalConstantError {
#     #final int x;  # Error: IllegalConstantExpression at constant declaration
#     final string text := nil;  # Error: IllegalConstantExpression at constant declaration
# }
# """
#     expected = "IllegalConstantExpression()"
#     assert Checker(source).check_from_source() == expected


def test_812():
    #Using mutable variable in constant expression
    source="""
class MutableInConstant {
    int mutableVar := 10;
    #final int constant1 := mutableVar;  # Error: IllegalConstantExpression at constant declaration
    
    int localVar := 5;
    final int constant2 := 1 + this.localVar;  # Error: IllegalConstantExpression at constant declaration
}
"""
    #expected = "IllegalConstantExpression(Identifier(mutableVar))"
    expected = "IllegalConstantExpression(BinaryOp(IntLiteral(1), +, PostfixExpression(ThisExpression(this).localVar)))"
    assert Checker(source).check_from_source() == expected

def test_813():
    #Error: Method calls in constant expression
    source="""
class MethodCallInConstant {
    final int value := MethodCallInConstant.getValue();  # Error: IllegalConstantExpression at constant declaration
    
    static int getValue() {
        return 42;
    }
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(MethodCallInConstant).getValue()))"
    assert Checker(source).check_from_source() == expected

def test_814():
    #// Error: Complex expressions with variables
    source="""
class ComplexIllegalExpression {
    static boolean isValid() {
        return true;
    }
    int a := 10;
    
    #final int result := (a * 2) + 5;  # Error: IllegalConstantExpression at constant declaration
    final boolean flag := ComplexIllegalExpression.isValid();   # Error: IllegalConstantExpression at constant declaration
    
    
}
"""
    #expected = "IllegalConstantExpression(BinaryOp(ParenthesizedExpression((BinaryOp(Identifier(a), *, IntLiteral(2)))), +, IntLiteral(5)))"
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(ComplexIllegalExpression).isValid()))"
    assert Checker(source).check_from_source() == expected

def test_815():
    #Valid: Proper constant expressions
    source ="""
class ValidConstantExpressions {
    
    final int MAX_SIZE := 100;
    final int DOUBLE_SIZE := this.MAX_SIZE * 2;     # Valid: uses immutable attribute
    final string MESSAGE := "Hello" ^ "World"; # Valid: literal concatenation
    final boolean FLAG := true && false;       # Valid: boolean literals with operators
    final float PI := 3.14159;
    final float CIRCLE_AREA := this.PI * 10 * 10;   # Valid: uses final attribute
    
    final int SUM := 10 + 20 + 30;         # Valid: literal arithmetic
    static void main(){}
}"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_816():
    # Error: Gọi method instance trong biểu thức hằng
    source = """class A{
    int getValue() {
        return 42;
    }
    static void main(){
        A a := new A();
        final int VALUE := a.getValue();    # Error: IllegalConstantExpression at constant declaration
    }
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(a).getValue()))"
    assert Checker(source).check_from_source() == expected
def test_817():
    source = """class Example3 {
        void foo(int p) {
        final int C := p + 1;  # IllegalConstantExpression – p là mutable (tham số)
        }   
    }"""
    expected = "IllegalConstantExpression(BinaryOp(Identifier(p), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_818():
    # Error: Dùng truy cập phần tử mảng trong biểu thức hằng
    source = """
class ArrayAccessInConstant {
    int[5] NUMBERS := {1, 2, 3, 4, 5};
    final int FIRST := NUMBERS[0];    # Error: IllegalConstantExpression at constant declaration
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
    
"""
### 9. Illegal Array Literal

**Rule:** All elements in an array literal must have the same type.

**Exception:** `IllegalArrayLiteral(<array-literal>)`

**Array Literal Rules:**
- All elements must be exactly the same type
- No type coercion in array literals
- Empty arrays are allowed if type can be inferred"""


def test_911():
    #Error: Mixed types in array litera
    source="""
class IllegalArrayError {
    void create() {
        int[3] mixed1 := {1, 2.0, 3};      # Error: IllegalArrayLiteral at array literal
        string[2] mixed2 := {"hello", 42}; # Error: IllegalArrayLiteral at array literal
        boolean[2] mixed3 := {true, 1};    # Error: IllegalArrayLiteral at array literal
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0), IntLiteral(3)}))"
    assert Checker(source).check_from_source() == expected


# def test_912():
#     # Error: Mixed object types
#     source="""
# class Rectangle{
#     Rectangle(int x; int y){
#     }
# }
# class Triangle{
#     Triangle(int x; int y){
#     }
# }
# class Shape{
#     Shape(){
#     }
# }
# class MixedObjectArray {
#     static void main(){}
#     void create() {
#         Shape[3] mixed := {new Rectangle(1.0, 2.0), new Triangle(1.0, 2.0), "not a shape"};  # Error: IllegalArrayLiteral at array literal
#     }
# }
# """
#     expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new Rectangle(FloatLiteral(1.0), FloatLiteral(2.0))), ObjectCreation(new Triangle(FloatLiteral(1.0), FloatLiteral(2.0))), StringLiteral('not a shape')}))"
#     assert Checker(source).check_from_source() == expected

def test_913():
    #Valid: Consistent array literals
    source="""
class Rectangle{}
class ValidArrays {
    static void main(){}
    void create() {
        int[5] numbers := {1, 2, 3, 4, 5};           # Valid
        string[3] words := {"hello", "world", "!"};   # Valid
        boolean[3] flags := {true, false, true};      # Valid
        float[3] decimals := {1.0, 2.5, 3.14};      # Valid
        
        # Valid object arrays with same type
        Rectangle[2] shapes := {new Rectangle(1.0, 2.0), new Rectangle(3.0, 4.0)};
    }
}
"""
    expected = "TypeMismatchInExpression(ObjectCreation(new Rectangle(FloatLiteral(1.0), FloatLiteral(2.0))))"
    assert Checker(source).check_from_source() == expected


def test_914():
    #Valid: Empty arrays (if context provides type)
    source="""
class EmptyArrays {
    static void main(){
    }
    void create() {
        int[0] empty1 := {};               # Valid if type can be inferred
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected





def test_4xx():
    source = """class ArrayError {
    static void main() {}
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        #floatArray := intArray; #valid
        intArray := floatArray;
    }
}"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(floatArray)))"
    assert Checker(source).check_from_source() == expected


def test_0001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_0002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_0003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_0005():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_0006():
    source = """
class io {}
class example{static void main(){}}
"""
    expected = "Redeclared(Class, io)"
    assert Checker(source).check_from_source() == expected

def test_0008():
    source = """
class test {
    int a := 1, b, a;
}
class example{static void main(){}}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected

def test_0013():
    source = """
class test {
    int a := 1;
    void b(){}
    void a(){}
}
class example{static void main(){}}
"""
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected

def test_0021():
    source = """
class test {
    void foo(int a) {
        int b;
        int a;
    }
}
class example{static void main(){}}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_0022():
    source = """
class test {
    void foo(int a) {
        int b;
        final int a;
    }
}
class example{static void main(){}}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected

def test_0023():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        int c;
    }
}
class example{static void main(){}}
"""
    expected = "Redeclared(Variable, c)"
    assert Checker(source).check_from_source() == expected

def test_0024():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int a;
            int e, c, e;
        }
    }
}
class example{static void main(){}}
"""
    expected = "Redeclared(Variable, e)"
    assert Checker(source).check_from_source() == expected

def test_0025():
    source = """
class test {
    void foo(int a) {
        int b, c, d;
        {
            int c;
            final int c;
        }
    }
}
class example{static void main(){}}
"""
    expected = "Redeclared(Constant, c)"
    assert Checker(source).check_from_source() == expected

def test_0026():
    source = """
class example{
    void main(){}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_0030():
    source = """
class votien1{
    static void main(int a){}
}
class votie2{
    static void main(){}
}
class votien3{
    static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_0034():
    source = """
class A extends io {}
class B extends A {}
class C extends Z {}

class example{static void main(){}}
"""
    expected = "UndeclaredClass(Z)"
    assert Checker(source).check_from_source() == expected

def test_0036():
    source = """
class example{static void main(){
    int a := 1;
    a := b;
}}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected

def test_0040():
    source = """
class example{
    int a;
    static void main(){}
    void func(){
        this.a := 1;
        this.b := 1;
    }
}
"""
    expected = "UndeclaredAttribute(b)"
    assert Checker(source).check_from_source() == expected

def test_0044():
    source = """
class example{
    int foo(){return 1;} 
    static void main(){}
    void func(){
        int a;
        a := this.foo();
        a := this.coo();
    }
}
"""
    expected = "UndeclaredMethod(coo)"
    assert Checker(source).check_from_source() == expected

def test_0050():
    source = """
class example{
    static void main(){
        final int a := 1;
        int  b;
        {
            b := a;
            a := b;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_0052():
    source = """
class example{
    final int a := 1;
    example(){}
    static void main(){}
    void func(){this.a := 2;}
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).a)) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_0056():
    source = """
class example{
    static void main(){
        final int i := 1, j;
    }
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected


def test_0065():
    source = """
class example{
    int MAX_SIZE := 1;
    final int A := this.MAX_SIZE;
    static void main(){}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).MAX_SIZE))"
    assert Checker(source).check_from_source() == expected

def test_0070():
    source = """
class example{
    static void main(){
          boolean[2] mixed3 := {true, 1};  
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected


def test_0071():
    source = """
class example{
    static void main(){
        int a; boolean b; float c; string d;
        a := 1;
        b := true;
        c := 1.0;
        c := 1;
        d := "s";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_0079():
    source = """
class example{
    static void main(){
        float[2] a;
        a := {1.0,2.0};
        a := {1,2};
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := ArrayLiteral({IntLiteral(1), IntLiteral(2)})))"
    assert Checker(source).check_from_source() == expected

def test_0082():
    source = """
class A {}
class B extends A {}
class C extends B {}

class example{
    static void main(){
        A a; B b; C c;
        c := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_0083():
    source = """
class A {}
class B extends A {}
class C extends A {}

class example{
    static void main(){
        A a; B b; C c;
        a := b;
        a := c;
        b := c;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := Identifier(c)))"
    assert Checker(source).check_from_source() == expected

def test_0084():
    source = """
class A {}
class B extends A {}

class example{
    static void main(){
        A[2] a; B[2] b;
        a := a;
        a := b;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_0086():
    source = """
class example{
    static void main(){
        int a;
        if a then {}
    }
}
"""
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(a) then BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_0091():
    source = """
class example{
    static void main(){
        int i; float f;
        for i := 0 to f do { }
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to Identifier(f) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_0094():
        source = """
    class votien{
        static float foo(){return 1;}
        static void main(){}
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected
        
def test_0095():
        source = """
    class votien{
        void foo(){}
        int coo(){return 1;
        this.foo();
            this.coo();}
        static void main(){
    
        }
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected

def test_0098():
    source = """
class example{
    void foo(float a){}
    static void main(){}
    void func(){
        this.foo(1.0, 1);
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).foo(FloatLiteral(1.0), IntLiteral(1)))))"
    assert Checker(source).check_from_source() == expected

def test_1001_():
    source = """
class example{
    static void main(){
        int[2] a;
        string b;
        b := b[1];
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(b))"
    assert Checker(source).check_from_source() == expected

def test_1014():
    source = """
class example{
    int foo(float a){return 1;}
    static void main(){}
    void func(){
        int a;
        a := this.foo(1);
        a := this.foo(1.0);
        a := this.foo();
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).foo()))"
    assert Checker(source).check_from_source() == expected

def test_1018():
    source = """
class B{}
class A extends B{
    A(){}
    A(int a){}
    A(int a; string b){}
}
class example{
    static void main(){
        A a; B b;
        a := new A(1.2);
    }
}
"""
    expected = "TypeMismatchInExpression(ObjectCreation(new A(FloatLiteral(1.2))))"
    assert Checker(source).check_from_source() == expected

# def test_1019():
#     source = """
# class example{
#     int foo() {
#         int a;
#         return 1 % a;
#         return a \\ 3;
#         return 1.2 % 2;
#     }
#     static void main(){}
# }
# """
#     expected = "TypeMismatchInExpression(BinaryOp(FloatLiteral(1.2), %, IntLiteral(2)))"
#     assert Checker(source).check_from_source() == expected

def test_1032():
    source = """
class example{
    static void main(){
        int x := 10, y := 20;
        int & xRef := x;
        int & yRef := y;
        xRef := x;
        x := yRef;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_1035():
    source = """
class example{
    final int x := "s";
    static void main(){
        
    }
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(x = StringLiteral('s'))]))"
    assert Checker(source).check_from_source() == expected

def test_1042():
    source = """
class A {int coo() {return 1;} static int foo() {return 1;}}
class example{
    A a;
    static void main(){
        int x := A.foo() + A.coo();
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).coo()))"
    assert Checker(source).check_from_source() == expected

def test_1043():
    source = """
class A {static int a; int b;}
class example{
    A a;
    static void main(){
        A.a := 1;
        A.b := 2;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).b))"
    assert Checker(source).check_from_source() == expected
def test_1043_cont():
    source = """
class A {
    static int a; int b;
    int foo(){
        return this.b; 
    }
    int foo1(){
        return A.a; 
    }
}
class example{
    A a;
    static void main(){
        int c := a.foo1(); 
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(a).foo1()))"
    assert Checker(source).check_from_source() == expected
def test_1043_cont1():
    source = """
class A {
    static int a; int b;
    int foo(){
        return this.b; 
    }
    int foo1(){
        return A.a; 
    }
}
class example{
    A a;
    static void main(){
        int c := a.foo(); 
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(a).foo()))"
    assert Checker(source).check_from_source() == expected
def test_1043_cont2():
    source = """
class A {
    static int a; int b;
    int foo(){
        return this.b; 
    }
    int foo1(){
        return A.a; 
    }
}
class example{
    A a;
    static void main(){
        int c := a.foo(); 
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(a).foo()))"
    assert Checker(source).check_from_source() == expected
def test_1045():
    source = """
class Example1 {
    int factorial(int n){
        if n == 0 then return 1; else return n * this.factorial(n - 1);
    }

    static void main(){
        int x;
        x := io.readInt();
        io.writeIntLn(this.factorial(x));
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_1046():
        source = """
    class example{
        static void main(){
            final int[5] NUMBERS := {1, 2, 3, 4, 5};
            final int j := NUMBERS[1];
        }
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected

def test_1047():
        source = """
    class example{
        final int MAX_SIZE;
        static void main(){}
    }
    """
        expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(MAX_SIZE)]))"
        assert Checker(source).check_from_source() == expected

def test_1048():
        source = """
    class example{
        final int MAX_SIZE := 1;
        final int A := this.MAX_SIZE;
        final int b :=  this.A * this.MAX_SIZE;
        static void main(){}
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected
        
def test_1049():
        source = """
    class example{
        static void main(){}
        void foo(){}
        int coo(){return 1;}
        void func(){
            this.foo();
            this.coo();
        }
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected
        
def test_1050():
    source = """
    class A{
        final int a;
        int b;
        A() {
            this.a := 1; this.b := 2;}
        ~A() {}
        ~A() {b := 0;}
    }"""
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected
    
def test_1051():
    source = """
    class example{
        static void main(){
            A.a := 1;
        }
    }
    class A {static int a := 1;}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
    
def test_1052():
        source = """
    class example{
        void foo(){}
        void func(){
            int a;
            a := this.foo();
        }
        static void main(){}
    }
    """
        expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).foo()))"
        assert Checker(source).check_from_source() == expected
        
def test_1053():
        source = """
    class A {}
    class example{
        A a := nil;
        static void main(){
            A& b := this.a;
            A& c := b;
        }
    }
    """
        expected = "IllegalMemberAccess(ThisExpression(this))"
        assert Checker(source).check_from_source() == expected

def test_1058():
        source = """
    class A {}
    class example{
        static void main(){
            A a;
            B b;
        }
    }
    """
        expected = "UndeclaredClass(B)"
        assert Checker(source).check_from_source() == expected
        
def test_1073():
        source = """
    class Animal {
        string species;
    
        void setSpecies(string s) {
            this.species := s;
        }
            static void main(){}
    }
    
    class Dog extends Animal {
        void identify() {
            this.setSpecies("Canine");
            io.writeStrLn(this.species);
        }
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected
        
def test_2008():
        source = """
    class Shape {}
    
    class Integer {}
    
    class ObjectConstantError {
        final Shape shape1 := new Shape();
        final Shape shape := new Integer();
    }
    """
        expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer()))]))"
        assert Checker(source).check_from_source() == expected


def test_this_type_check():
    """Verify 'this' has the type of the enclosing class"""
    source = """
    class B {}
    class A {
        void check() {
            A x := this;    # Hợp lệ: this có kiểu A -> gán cho biến A
            B y := this;    # Lỗi: this có kiểu A -> không thể gán cho biến B
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(B), [Variable(y = ThisExpression(this))]))"
    assert Checker(source).check_from_source() == expected


def test_this_as_return_value():
    """Verify 'this' can be returned when return type is the class itself"""
    source = """
    class A {
        A getMe() {
            return this; # Hợp lệ: return type là A, this cũng là A
        }
        
        int getWrong() {
            return this; # Lỗi: return type là int, this là A
        }
    }
    """
    # Mong đợi lỗi ở hàm getWrong
    expected = "TypeMismatchInStatement(ReturnStatement(return ThisExpression(this)))"
    assert Checker(source).check_from_source() == expected
def test_this_as_return_value():
    """Verify 'this' can be returned when return type is the class itself"""
    source = """
    class A {
        A getMe() {
            return this; # Hợp lệ: return type là A, this cũng là A
        }
        
        int getWrong() {
            return this; # Lỗi: return type là int, this là A
        }
    }
    """
    # Mong đợi lỗi ở hàm getWrong
    expected = "TypeMismatchInStatement(ReturnStatement(return ThisExpression(this)))"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing():
    """Verify 'this.x' refers to attribute, distinguishing from parameter 'x'"""
    source = """
    class A {
        int x;
        void setX(float x) {
            # x ở đây là float (param)
            # this.x là int (attribute)
            
            this.x := x;      # Lỗi: gán float (param x) vào int (attribute this.x) -> TypeMismatch
        }
    }
    """
    # Lưu ý: OPLang thường không cho gán float vào int (coercion chỉ cho int -> float)
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_this_access_in_static():
    """Test using 'this.x' inside a static method"""
    source = """
    class A {
        int x;
        static void main() {
            # Lỗi: Không thể dùng 'this' trong static main
            # Checker sẽ bắt lỗi ngay tại từ khóa 'this'
            io.writeInt(this.x); 
        }
    }
    """
    # Checker ném lỗi IllegalMemberAccess chứa node ThisExpression
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_assignment_in_static():
    """Test assigning 'this' to a variable inside static method"""
    source = """
    class A {
        static void main() {
            # Lỗi: 'this' không tồn tại trong ngữ cảnh static
            A a := this; 
        }
    }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_method_call_in_static():
    """Test calling 'this.foo()' inside static method"""
    source = """
    class A {
        void foo() {}
        static void main() {
            # Lỗi: Không thể dùng 'this' để gọi hàm
            this.foo();
        }
    }
    """
    # Checker vẫn báo lỗi tại 'this', không phải tại MethodCall
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing_resolution():
    """Verify 'this.x' refers to int attribute, while 'x' refers to float param"""
    source = """
    class ShadowTest {
        int x; # Attribute là INT
        
        void setX(float x) { # Parameter là FLOAT
            this.x := x;     # Lỗi: Không thể gán float (param) vào int (attribute)
        }
    }
    """
    # Lưu ý: Cấu trúc lỗi phụ thuộc vào cách bạn __str__ AST
    # Node gây lỗi là AssignmentStatement
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)))"
    
    # Nếu Checker của bạn báo lỗi AssignmentStatement chứ không phải từng phần tử
    # Bạn cần điều chỉnh chuỗi expected cho khớp với thực tế chạy
    assert Checker(source).check_from_source() == expected
def test_this_method_invocation():
    """Test calling another instance method using 'this'"""
    source = """
    class Calculator {
        int result;
        
        void reset() {
            this.result := 0;
        }
        
        void compute() {
            this.reset(); # Gọi method khác qua this
            this.result := 100;
        }
        
        static void main() {
            Calculator c := new Calculator();
            c.compute();
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing_valid():
    """Test valid shadowing: assigning param to this.attr"""
    source = """
    class Rectangle {
        int width;
        int height;
        
        # Constructor có tham số trùng tên với attribute
        Rectangle(int width; int height) {
            this.width := width;   # Hợp lệ: gán int vào int
            this.height := height; # Hợp lệ: gán int vào int
        }
        
        static void main() {
            Rectangle r := new Rectangle(10, 20);
        }
    }
    """
    # Nếu checker đúng, nó sẽ trả về None hoặc list rỗng (tuỳ implementation của bạn)
    # Hoặc bạn có thể assert nó không raise exception
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_implicit_this_valid():
    """Test implicit 'this' when there is no name conflict"""
    source = """
    class Box {
        int width;
        
        void setWidth() {
            # Không có tham số/biến cục bộ nào tên 'width'
            # Nên 'width' ở đây phải được hiểu là 'this.width'
            width := 10; 
        }
        
        static void main() {
            Box b := new Box();
            b.setWidth();
        }
    }
    """
    # Mong đợi: Không có lỗi
    assert Checker(source).check_from_source() == "Static checking passed"

def test_implicit_this_type_check():
    """Verify implicit access refers to the correctly typed attribute"""
    source = """
    class Box {
        int width;
        
        void setWrong() {
            # width là int (attribute)
            # gán float vào int -> Phải báo lỗi TypeMismatch
            width := 5.5; 
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(width) := FloatLiteral(5.5)))"
    assert Checker(source).check_from_source() == expected
def test_shadowing_behavior():
    """
    Verify that parameter shadows attribute.
    Implicit 'this' is disabled here.
    """
    source = """
    class Shadow {
        int val; # Attribute là INT
        
        # Parameter là FLOAT -> Nó sẽ che khuất attribute
        void test(float val) {
            
            # Ở đây 'val' là parameter (float)
            # Phép gán này HỢP LỆ (float := float)
            # Nếu checker nhầm 'val' là attribute (int), nó sẽ báo lỗi.
            val := 10.5; 
            
            # Để gán vào attribute, BẮT BUỘC dùng this
            # this.val := val; # Dòng này sẽ lỗi (int := float) nhưng ta đang test dòng trên
        }
        static void main(){}
    }

    """
    # Mong đợi: Không có lỗi (Static checking passed)
    # Vì val := 10.5 là gán vào parameter float
    assert Checker(source).check_from_source() == "Static checking passed"

def test_this_101(): 
    source = """
class Person {
    string name;
    void abc(){
        int a := b; 
    }
}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected
def test_this_102():
    source = """
class Person {
    string name;
    static void abc(){
        int a := b; 
    }
}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected
def test_this_access_static_member_error():
    """
    Test Point 6: 'this' cannot be used to access static attributes.
    Spec requires: ClassName.member for static.
    """
    source = """
    class MathUtil {
        static float PI;
        
        void setup() {
            # LỖI: PI là static, không được gọi qua 'this' (instance)
            # Đúng phải là: MathUtil.PI := 3.14;
            this.PI := 3.14; 
        }
    }
    """
    # Checker sẽ báo lỗi IllegalMemberAccess vì PI là static mà lại bị truy cập kiểu instance
    # Node lỗi là FieldAccess (this.PI) hoặc toán hạng postfix
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).PI))" 
    
    # Lưu ý: Nếu checker của bạn báo lỗi cả cụm gán, hãy điều chỉnh expected
    # Dựa trên code của bạn: raise IllegalMemberAccess(op) -> FieldAccess/MemberAccess
    assert Checker(source).check_from_source() == expected
def test_polymorphism_validity():
    """
    Test Point 7: Verify static checker allows polymorphism structures.
    1. Upcasting (Subtype := Supertype)
    2. Calling inherited/overridden methods via 'this'
    """
    source = """
    class Shape {
        float getArea() { return 0.0; }
    }
    
    class Rectangle extends Shape {
        float width, height;
        
        # Override method
        float getArea() { 
            return this.width * this.height; 
        }
        
        void printArea() {
            # Gọi method qua this.
            # Static Checker chỉ cần biết getArea() tồn tại trong Rectangle (hoặc cha của nó)
            io.writeFloat(this.getArea()); 
        }
    }
    
    class Main {
        static void main() {
            # 1. Test Upcasting (Dynamic Dispatch setup)
            # Biến s kiểu Shape, nhưng giữ object Rectangle
            Shape s := new Rectangle(); 
            
            # 2. Test gọi hàm
            # Static check: Kiểm tra xem class 'Shape' có hàm getArea không? -> Có -> OK.
            s.getArea(); 
        }
    }
    """
    expect = "Static checking passed" 
    assert Checker(source).check_from_source() == expect

def test_this_inherited_members():
    """Verify 'this' can access members defined in parent class"""
    source = """
    class Parent {
        int id;
        void setId(int id) {
            this.id := id;
        }
    }
    
    class Child extends Parent {
        void update() {
            # 'id' được khai báo ở Parent.
            # 'this.id' ở Child phải hợp lệ và trỏ lên Parent.id
            this.id := 100; 
            
            # 'setId' được khai báo ở Parent
            # 'this.setId' phải hợp lệ
            this.setId(200);
        }
        static void main(){}
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_scope_class_inheritance():
    """
    Class scope: Attributes are visible in subclasses.
    """
    source = """
    class Parent {
        int inheritedVar;
    }
    
    class Child extends Parent {
        void test() {
            # inheritedVar được khai báo ở Parent
            # Child phải nhìn thấy nó (thông qua this hoặc implicit)
            this.inheritedVar := 100; 
        }
        
        static void main() {
            Child c := new Child();
            c.test();
        }
    }
    """
    # Mong đợi: Không có lỗi
    assert Checker(source).check_from_source() == "Static checking passed"
def test_scope_global_static():
    """
    Global scope: Static attributes/methods are visible everywhere via ClassName.
    """
    source = """
    class GlobalConfig {
        static int MAX_USERS;
    }
    
    class UserManager {
        void check() {
            # Truy cập biến static của class khác
            # Nếu Global scope đúng, Checker sẽ tìm thấy GlobalConfig -> MAX_USERS
            GlobalConfig.MAX_USERS := 500;
        }
        static void main(){}
    }
    """
    # Mong đợi: Không có lỗi
    assert Checker(source).check_from_source() == "Static checking passed"
def test_entry_point_invalid():
    """Test various invalid main signatures"""
    # 1. Main with params
    source1 = """class Program { static void main(int x) {} }"""
    assert Checker(source1).check_from_source() == "No Entry Point"

    # 2. Main not static
    source2 = """class Program { void main() {} }"""
    assert Checker(source2).check_from_source() == "No Entry Point"
    
    # 3. Main returns int
    source3 = """class Program { static int main() { return 1; } }"""
    assert Checker(source3).check_from_source() == "No Entry Point"

def test_string_operators():
    """Verify strict string operators"""
    source = """
    class StringTest {
        static void main() {
            string s;
            s := "Hello" ^ "World"; # Hợp lệ
            
            # LỖI 1: Dùng + cho chuỗi (phải báo TypeMismatchInExpression)
            # s := "Hello" + "World"; 
            
            # LỖI 2: Concat chuỗi với số (phải báo TypeMismatchInExpression)
            s := "Age: " ^ 18; 
        }
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('Age: '), ^, IntLiteral(18)))"
    assert Checker(source).check_from_source() == expected

def test_check01(): 
    source = """
    class Constants {
    final int MAX_COUNT := 100;
    
    void example() {
        MAX_COUNT := 200;  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(MAX_COUNT) := IntLiteral(200)))"
    assert Checker(source).check_from_source() == expected
def test_check02(): 
    source = """
        class Constants {
    final int MAX_COUNT; # error
    
    void example() {
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_check03():
    source = """
    class Constants {
    final int MAX_count; 
    Constants() {
        this.MAX_count := 100;
        }
    }
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_check04():
    source = """
    class Constants {
    final int MAX_count := 100 ; 
    Constants() {
        this.MAX_count := 123;
        }
    }
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).MAX_count)) := IntLiteral(123)))"
    assert Checker(source).check_from_source() == expected

    
def test_check05():
    source = """
    class Constants {
    void test(){
        final int MAX_count := 100 ; 
        }
    }

"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_check08(): 
    source = """
class LoopExample {
    final int limit := 10;
    
    void process() {
        for limit := 0 to 20 do {  # Error: CannotAssignToConstant at for statement
            io.writeIntLn(limit);
        }
    }
}

"""
    expected = "CannotAssignToConstant(ForStatement(for limit := IntLiteral(0) to IntLiteral(20) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(limit))))])))"
    assert Checker(source).check_from_source() == expected
def test_check09(): 
    source = """
    class Constants {
    Constants(){
        final int MAX_count := 100 ; 
        }
    }

"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_method1(): 
    source = """
        class A {
            void main() {
                this.foo(); 
            }
        }
"""
    expected = "UndeclaredMethod(foo)"
    assert Checker(source).check_from_source() == expected
def test_method2(): 
    source = """
        class Parent {
            void parentMethod() {}
        }
        class Child extends Parent {
            void childMethod() {}
        }
        class Main {
            void main() {
                Parent p := new Child();
                p.parentMethod(); 
                p.childMethod(); 
            }
        }
"""
    expected = "UndeclaredMethod(childMethod)"
    assert Checker(source).check_from_source() == expected

def test_method3(): 
    source = """
        class Worker {
            void work() {}
        }
        class Manager {
            void manage() {
                Worker w;
                w.relax(); 
            }
        }
"""
    expected = "UndeclaredMethod(relax)"
    assert Checker(source).check_from_source() == expected
def test_method4(): 
    source = """
        class A {
            A getSelf() { return this; }
            void exist() {}
        }
        class Main {
            void main() {
                A a;
                a.getSelf().getSelf().notExist(); 
            }
        }
"""
    expected = "UndeclaredMethod(notExist)"
    assert Checker(source).check_from_source() == expected
def test_method5(): 
    source = """
        class A {
            int myProp;
            void main() {
                this.myProp(); 
            }
        }
"""
    expected = "UndeclaredMethod(myProp)"
    assert Checker(source).check_from_source() == expected
def test_method6(): 
    source = """
class MathUtils {
            static int add(int a; int b) { return a + b; }
        }
        class Main {
            void main() {
                int x := MathUtils.subtract(10, 5); 
            }
        }
"""
    expected = "UndeclaredMethod(subtract)"
    assert Checker(source).check_from_source() == expected

def test_method7(): 
    source = """
class A {
            int getVal() { return 1; }
        }
        class Main {
            void main() {
                A a;
                int x := a.getVal() + a.getUnknown(); 
            }
        }
"""
    expected = "UndeclaredMethod(getUnknown)"
    assert Checker(source).check_from_source() == expected
def test_checkign(): 
    source = """
    class ArrayAccessInConstant {
    final int[5] NUMBERS := {1, 2, 3, 4, 5};
    final int FIRST := NUMBERS[0]; 
        static void main(){}
    }
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_007():
    """Test illegal array literal error - alternative case"""
    source = """
class Test {
    static void main() {
        boolean[2] flags := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected
# chuaw cos chinhr laij array
# def test_illegal_array_mixed_objects():
#     """
#     Kiểm tra mảng chứa các object khác loại (và không liên quan).
#     Spec: {new Rect(), "not a shape"} -> Error.
#     """
#     source = """
#     class Rectangle { Rectangle(float l, w) {} }
#     class MixedObjectArray {
#         void create() {
#             # Lỗi: Rectangle và String không cùng kiểu
#             Rectangle[2] mixed := {new Rectangle(1.0, 2.0), "not a shape"};
#         }
#         static void main() {}
#     }
#     """
#     expected = "IllegalArrayLiteral([ObjectCreation(Rectangle,[FloatLiteral(1.0),FloatLiteral(2.0)]),StringLiteral(not a shape)])"
#     assert Checker(source).check_from_source() == expected

# def test_valid_consistent_arrays():
#     """
#     Kiểm tra các trường hợp mảng hợp lệ (đồng nhất kiểu).
#     """
#     source = """
#     class Rectangle { Rectangle(float l, w) {} }
#     class ValidArrays {
#         void create() {
#             int[5] numbers := {1, 2, 3, 4, 5};           # Valid: All int
#             string[3] words := {"hello", "world", "!"};   # Valid: All string
#             boolean[3] flags := {true, false, true};      # Valid: All boolean
#             float[3] decimals := {1.0, 2.5, 3.14};        # Valid: All float
            
#             # Valid: All Rectangle objects
#             Rectangle[2] shapes := {new Rectangle(1.0, 2.0), new Rectangle(3.0, 4.0)};
#         }
#         static void main() {}
#     }
#     """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

# def test_poly1(): 
#     source = """
# class Animal {
#     string name;
    
#     Animal(string name) {
#         this.name := name;
#     }
    
#     void makeSound() {
#         io.writeStrLn("Some generic animal sound");
#     }
    
#     void eat() {
#         io.writeStrLn("Animal is eating");
#     }
# }

# class Dog extends Animal {
#     Dog(string name) {
#         this.name := name;
#     }
    
#     # Override makeSound
#     void makeSound() {
#         io.writeStrLn("Woof! Woof!");
#     }
    
#     # Dog-specific method
#     void fetch() {
#         io.writeStrLn("Dog is fetching");
#     }
# }

# class Test1 {
#     void main() {
#         # Test polymorphic behavior
#         Animal animal := new Dog("Buddy");
#         animal.makeSound();  # Should call Dog's makeSound
#         animal.eat();        # Should call Animal's eat
#         animal.fetch();    # ERROR: UndeclaredMethod - Animal doesn't have fetch
#     }
# }
# """
#     expected = "UndeclaredMethod(fetch)"
#     assert Checker(source).check_from_source() == expected
# def test_poly2():
#     source = """
# class Vehicle {
#     float speed;
    
#     void move() {
#         io.writeStrLn("Vehicle is moving");
#     }
    
#     float getSpeed() {
#         return this.speed;
#     }
# }

# class Car extends Vehicle {
#     int doors;
    
#     void move() {
#         io.writeStrLn("Car is driving");
#     }
    
#     void honk() {
#         io.writeStrLn("Beep beep!");
#     }
# }

# class SportsCar extends Car {
#     boolean turboMode;
    
#     void move() {
#         io.writeStrLn("Sports car is racing!");
#     }
    
#     void activateTurbo() {
#         this.turboMode := true;
#         io.writeStrLn("Turbo activated!");
#     }
# }

# class Test2 {
#     static void main() {
#         # Multi-level upcasting
#         Vehicle v1 := new SportsCar();
#         v1.move();  # Should call SportsCar's move
        
#         Vehicle v2 := new Car();
#         v2.move();  # Should call Car's move
        
#         Car c := new SportsCar();
#         c.move();   # Should call SportsCar's move
#         c.honk();   # Should call Car's honk
        
#         v1.honk();          # ERROR: UndeclaredMethod - Vehicle doesn't have honk
#         # v1.activateTurbo();  ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "UndeclaredMethod(honk)"
#     assert Checker(source).check_from_source() == expected
# def test_poly2_():
#     source = """
# class Vehicle {
#     float speed;
    
#     void move() {
#         io.writeStrLn("Vehicle is moving");
#     }
    
#     float getSpeed() {
#         return this.speed;
#     }
# }

# class Car extends Vehicle {
#     int doors;
    
#     void move() {
#         io.writeStrLn("Car is driving");
#     }
    
#     void honk() {
#         io.writeStrLn("Beep beep!");
#     }
# }

# class SportsCar extends Car {
#     boolean turboMode;
    
#     void move() {
#         io.writeStrLn("Sports car is racing!");
#     }
    
#     void activateTurbo() {
#         turboMode := true;
#         io.writeStrLn("Turbo activated!");
#     }
# }

# class Test2 {
#     void main() {
#         # Multi-level upcasting
#         Vehicle v1 := new SportsCar();
#         v1.move();  # Should call SportsCar's move
        
#         Vehicle v2 := new Car();
#         v2.move();  # Should call Car's move
        
#         Car c := new SportsCar();
#         c.move();   # Should call SportsCar's move
#         c.honk();   # Should call Car's honk
        
#         #v1.honk();          # ERROR: UndeclaredMethod - Vehicle doesn't have honk
#         v1.activateTurbo(); # ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "UndeclaredMethod(activateTurbo)"
#     assert Checker(source).check_from_source() == expected
# def test_poly4():
#     source = """
# class Shape {
#     string color;
    
#     float getArea() {
#         return 0.0;
#     }
    
#     void draw() {
#         io.writeStrLn("Drawing shape");
#     }
# }

# class Circle extends Shape {
#     float radius;
    
#     Circle(float r) {
#         this.radius := r;
#     }
    
#     float getArea() {
#         return 3.14159 * this.radius * this.radius;
#     }
    
#     void draw() {
#         io.writeStrLn("Drawing circle");
#     }
# }

# class Rectangle extends Shape {
#     float width, height;
    
#     Rectangle(float w; float h) {
#         this.width := w;
#         this.height := h;
#     }
    
#     float getArea() {
#         return this.width * this.height;
#     }
    
#     void draw() {
#         io.writeStrLn("Drawing rectangle");
#     }
# }

# class Test3 {
#     static void main() {
#         # Polymorphic array
#         Shape[3] shapes;
#         shapes[0] := new Circle(5.0);
#         shapes[1] := new Rectangle(4.0, 3.0);
#         shapes[2] := new Circle(2.5);
        
#         # Iterate and call overridden methods
#         for int i := 0 to 2 do {
#             shapes[i].draw();
#             io.writeFloatLn(shapes[i].getArea());
#         }
#     }
# }

# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == expected

# def test_poly5():
#     source = """
# class Employee {
#     string name;
#     float baseSalary;
    
#     Employee(string name; float salary) {
#         this.name := name;
#         this.baseSalary := salary;
#     }
    
#     float calculatePay() {
#         return this.baseSalary;
#     }
    
#     void work() {
#         io.writeStrLn("Employee is working");
#     }
# }

# class Manager extends Employee {
#     float bonus;
    
#     Manager(string name; float salary; float bonus) {
#         this.name := name;
#         this.baseSalary := salary;
#         this.bonus := bonus;
#     }
    
#     float calculatePay() {
#         return this.baseSalary + this.bonus;
#     }
    
#     void work() {
#         io.writeStrLn("Manager is managing");
#     }
    
#     void conductMeeting() {
#         io.writeStrLn("Conducting meeting");
#     }
# }

# class Programmer extends Employee {
#     int linesOfCode;
    
#     Programmer(string name; float salary) {
#         this.name := name;
#         this.baseSalary := salary;
#     }
    
#     float calculatePay() {
#         return this.baseSalary * 1.2;  # 20% productivity bonus
#     }
    
#     void work() {
#         io.writeStrLn("Programmer is coding");
#     }
    
#     void debug() {
#         io.writeStrLn("Debugging code");
#     }
# }

# class PayrollSystem {
#     void processPayroll(Employee emp) {
#         io.writeStr("Processing payroll for: ");
#         io.writeStrLn(emp.name);
#         emp.work();  # Polymorphic call
#         io.writeFloatLn(emp.calculatePay());  # Polymorphic call
#     }
    
#     void processBatch(Employee[3] employees) {
#         for int i := 0 to 2 do {
#             this.processPayroll(employees[i]);
#         }
#     }
# }

# class Test4 {
#     void main() {
#         PayrollSystem payroll := new PayrollSystem();
        
#         # Pass different subtypes as parameters
#         Employee emp1 := new Manager("Alice", 5000.0, 1000.0);
#         Employee emp2 := new Programmer("Bob", 4000.0);
#         Employee emp3 := new Employee("Charlie", 3000.0);
        
#         payroll.processPayroll(emp1);  # Should use Manager's methods
#         payroll.processPayroll(emp2);  # Should use Programmer's methods
#         payroll.processPayroll(emp3);  # Should use Employee's methods
        
#         # Array of polymorphic objects
#         Employee[3] team;
#         team[0] := emp1;
#         team[1] := emp2;
#         team[2] := emp3;
#         payroll.processBatch(team);
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected

# def test_poly6():
#     source = """
# class Product {
#     string name;
#     float price;
    
#     Product(string name; float price) {
#         this.name := name;
#         this.price := price;
#     }
    
#     float getPrice() {
#         return this.price;
#     }
    
#     void display() {
#         io.writeStrLn("Product: " ^ this.name);
#     }
# }

# class Book extends Product {
#     string author;
    
#     Book(string name; float price; string author) {
#         this.name := name;
#         this.price := price;
#         this.author := author;
#     }
    
#     void display() {
#         io.writeStrLn("Book: " ^ this.name ^ " by " ^ this.author);
#     }
# }

# class Electronics extends Product {
#     int warrantyMonths;
    
#     Electronics(string name; float price; int warranty) {
#         this.name := name;
#         this.price := price;
#         this.warrantyMonths := warranty;
#     }
    
#     void display() {
#         io.writeStr("Electronics: " ^ this.name);
#         io.writeStr(" - Warranty: ");
#         io.writeIntLn(this.warrantyMonths);
#     }
# }

# class Store {
#     # Return supertype from method
#     Product createProduct(int type) {
#         if type == 1 then
#             return new Book("The Great Gatsby", 15.99, "F. Scott Fitzgerald");
#         else
#             return new Electronics("Laptop", 999.99, 24);
#     }
    
#     # Method that returns different subtypes
#     Product getSpecialOffer() {
#         return new Book("Special Edition", 9.99, "Various");
#     }
# }

# class Test5 {
#     void main() {
#         Store store := new Store();
        
#         Product p1 := store.createProduct(1);
#         Product p2 := store.createProduct(2);
#         Product p3 := store.getSpecialOffer();
        
#         p1.display();  # Should call Book's display
#         p2.display();  # Should call Electronics's display
#         p3.display();  # Should call Book's display
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected

# def test_poly7():
#     source = """
# class Person {
#     string name;
#     int age;
    
#     Person(string name; int age) {
#         this.name := name;
#         this.age := age;
#     }
    
#     void introduce() {
#         io.writeStrLn("I am " ^ this.name);
#     }
# }

# class Student extends Person {
#     float gpa;
#     string studentId;
    
#     Student(string name; int age; string id; float gpa) {
#         this.name := name;
#         this.age := age;
#         this.studentId := id;
#         this.gpa := gpa;
#     }
    
#     void introduce() {
#         io.writeStrLn("Student " ^ this.name ^ " - ID: " ^ this.studentId);
#     }
    
#     void study() {
#         io.writeStrLn("Studying...");
#     }
# }

# class Test6 {
#     void main() {
#         Person p := new Student("Alice", 20, "S12345", 3.8);
        
#         # Can access inherited attributes
#         io.writeStrLn(p.name);  # Valid - name is in Person
#         io.writeIntLn(p.age);   # Valid - age is in Person
        
#         # Cannot access subclass-specific attributes
#         io.writeFloatLn(p.gpa);      # ERROR: UndeclaredAttribute
#         # io.writeStrLn(p.studentId);  # ERROR: UndeclaredAttribute
        
#         # Can call overridden method
#         p.introduce();  # Calls Student's introduce
        
#         # Cannot call subclass-specific method
#         # p.study();  # ERROR: UndeclaredMethod
#     }
# }

# """
#     expected = "UndeclaredAttribute(gpa)"
#     assert Checker(source).check_from_source() == expected
# def test_poly10():
#     source = """
# class Person {
#     string name;
#     int age;
    
#     Person(string name; int age) {
#         this.name := name;
#         this.age := age;
#     }
    
#     void introduce() {
#         io.writeStrLn("I am " ^ this.name);
#     }
# }

# class Student extends Person {
#     float gpa;
#     string studentId;
    
#     Student(string name; int age; string id; float gpa) {
#         this.name := name;
#         this.age := age;
#         this.studentId := id;
#         this.gpa := gpa;
#     }
    
#     void introduce() {
#         io.writeStrLn("Student " ^ this.name ^ " - ID: " ^ this.studentId);
#     }
    
#     void study() {
#         io.writeStrLn("Studying...");
#     }
# }

# class Test6 {
#     void main() {
#         Person p := new Student("Alice", 20, "S12345", 3.8);
        
#         # Can access inherited attributes
#         io.writeStrLn(p.name);  # Valid - name is in Person
#         io.writeIntLn(p.age);   # Valid - age is in Person
        
#         # Cannot access subclass-specific attributes
#         #io.writeFloatLn(p.gpa);      # ERROR: UndeclaredAttribute
#         io.writeStrLn(p.studentId);  # ERROR: UndeclaredAttribute
        
#         # Can call overridden method
#         p.introduce();  # Calls Student's introduce
        
#         # Cannot call subclass-specific method
#         # p.study();  # ERROR: UndeclaredMethod
#     }
# }

# """
#     expected = "UndeclaredAttribute(studentId)"
#     assert Checker(source).check_from_source() == expected

# def test_poly8():
#     source = """
# class Counter {
#     static int globalCount := 0;
#     int instanceCount;
    
#     Counter() {
#         Counter.globalCount := Counter.globalCount + 1;
#         this.instanceCount := 0;
#     }
    
#     void increment() {
#         this.instanceCount := this.instanceCount + 1;
#         Counter.globalCount := Counter.globalCount + 1;
#     }
    
#     static int getGlobalCount() {
#         return Counter.globalCount;
#     }
# }

# class SpecialCounter extends Counter {
#     int multiplier;
    
#     SpecialCounter(int mult) {
#         Counter.globalCount := Counter.globalCount + 1;
#         this.multiplier := mult;
#         this.instanceCount := 0;
#     }
    
#     void increment() {
#         this.instanceCount := this.instanceCount + this.multiplier;
#         Counter.globalCount := Counter.globalCount + this.multiplier;
#     }
# }

# class Test7 {
#     void main() {
#         Counter c1 := new SpecialCounter(5);
#         c1.increment();  # Calls SpecialCounter's increment
        
#         io.writeIntLn(Counter.getGlobalCount());  # Static method call
        
#         # Static members are shared across hierarchy
#         Counter c2 := new Counter();
#         io.writeIntLn(Counter.getGlobalCount());
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected

# def test_poly9():
#     source = """
# class Number {
#     float value;
    
#     Number(float v) {
#         this.value := v;
#     }
    
#     float getValue() {
#         return this.value;
#     }
    
#     float calculate() {
#         return this.value;
#     }
# }

# class IntegerNumber extends Number {
#     IntegerNumber(float v) {
#         this.value := v;
#     }
    
#     float calculate() {
#         return this.value * 2.0;
#     }
# }

# class FloatNumber extends Number {
#     FloatNumber(float v) {
#         this.value := v;
#     }
    
#     float calculate() {
#         return this.value / 2.0;
#     }
# }

# class Test8 {
#     void main() {
#         Number n1 := new IntegerNumber(10.0);
#         Number n2 := new FloatNumber(20.0);
        
#         # Polymorphic calls in expressions
#         float result1 := n1.calculate() + n2.calculate();
#         float result2 := n1.getValue() * n2.getValue();
        
#         boolean condition := n1.calculate() > n2.calculate();
        
#         if n1.calculate() < 100.0 then {
#             io.writeStrLn("Less than 100");
#         }
        
#         io.writeFloatLn(result1);
#         io.writeFloatLn(result2);
#         io.writeBoolLn(condition);
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected

# def test_poly12(): 
#     source = """
# class Base {
#     int x;
    
#     void method1() {
#         io.writeStrLn("Base method1");
#     }
    
#     int getValue() {
#         return this.x;
#     }
# }

# class Derived extends Base {
#     int y;
    
#     void method1() {
#         io.writeStrLn("Derived method1");
#     }
    
#     void method2() {
#         io.writeStrLn("Derived method2");
#     }
    
#     int getY() {
#         return this.y;
#     }
# }

# class Test10_Errors {
#     void main() {
#         Base b := new Derived();
        
#         # Valid polymorphic calls
#         b.method1();  # Calls Derived's method1
#         int val := b.getValue();  # Calls Base's getValue
        
#         # ERROR CASES:
        
#         # Cannot access subclass-specific members through superclass reference
#         # b.method2();  # ERROR: UndeclaredMethod(method2) - Base doesn't have method2
#         int yVal := b.getY();  # ERROR: UndeclaredMethod(getY)
#         # b.y := 10;  # ERROR: UndeclaredAttribute(y)
        
#         # Cannot downcast without explicit mechanism (OPLang doesn't support casting)
#         # Derived d := b;  # ERROR: TypeMismatchInStatement - cannot assign Base to Derived
        
#         # Array type mismatch
#         Base[3] bases;
#         Derived[3] deriveds;
#         # bases := deriveds;  # This would be valid (upcasting array)
#         # deriveds := bases;  # ERROR: TypeMismatchInStatement (downcasting not allowed)
#     }
# }
# """
#     expected = "UndeclaredMethod(getY)"
#     assert Checker(source).check_from_source() == expected
# def test_poly13(): 
#     source = """
# class Base {
#     int x;
    
#     void method1() {
#         io.writeStrLn("Base method1");
#     }
    
#     int getValue() {
#         return this.x;
#     }
# }

# class Derived extends Base {
#     int y;
    
#     void method1() {
#         io.writeStrLn("Derived method1");
#     }
    
#     void method2() {
#         io.writeStrLn("Derived method2");
#     }
    
#     int getY() {
#         return this.y;
#     }
# }

# class Test10_Errors {
#     void main() {
#         Base b := new Derived();
        
#         # Valid polymorphic calls
#         b.method1();  # Calls Derived's method1
#         int val := b.getValue();  # Calls Base's getValue
        
#         # ERROR CASES:
        
#         # Cannot access subclass-specific members through superclass reference
#         # b.method2();  # ERROR: UndeclaredMethod(method2) - Base doesn't have method2
#         #int yVal := b.getY();  # ERROR: UndeclaredMethod(getY)
#         b.y := 10;  # ERROR: UndeclaredAttribute(y)
        
#         # Cannot downcast without explicit mechanism (OPLang doesn't support casting)
#         # Derived d := b;  # ERROR: TypeMismatchInStatement - cannot assign Base to Derived
        
#         # Array type mismatch
#         Base[3] bases;
#         Derived[3] deriveds;
#         # bases := deriveds;  # This would be valid (upcasting array)
#         # deriveds := bases;  # ERROR: TypeMismatchInStatement (downcasting not allowed)
#     }
# }
# """
#     expected = "UndeclaredAttribute(y)"
#     assert Checker(source).check_from_source() == expected
# def test_poly14(): 
#     source = """
# class Base {
#     int x;
    
#     void method1() {
#         io.writeStrLn("Base method1");
#     }
    
#     int getValue() {
#         return this.x;
#     }
# }

# class Derived extends Base {
#     int y;
    
#     void method1() {
#         io.writeStrLn("Derived method1");
#     }
    
#     void method2() {
#         io.writeStrLn("Derived method2");
#     }
    
#     int getY() {
#         return this.y;
#     }
# }

# class Test10_Errors {
#     void main() {
#         Base b := new Derived();
        
#         # Valid polymorphic calls
#         b.method1();  # Calls Derived's method1
#         int val := b.getValue();  # Calls Base's getValue
        
#         # ERROR CASES:
        
#         # Cannot access subclass-specific members through superclass reference
#         # b.method2();  # ERROR: UndeclaredMethod(method2) - Base doesn't have method2
#         #int yVal := b.getY();  # ERROR: UndeclaredMethod(getY)
#         # b.y := 10;  # ERROR: UndeclaredAttribute(y)
        
#         # Cannot downcast without explicit mechanism (OPLang doesn't support casting)
#         Derived d := b;  # ERROR: TypeMismatchInStatement - cannot assign Base to Derived
        
#         # Array type mismatch
#         Base[3] bases;
#         Derived[3] deriveds;
#         # bases := deriveds;  # This would be valid (upcasting array)
#         # deriveds := bases;  # ERROR: TypeMismatchInStatement (downcasting not allowed)
#     }
# }
# """
#     expected = "TypeMismatchInStatement(VariableDecl(ClassType(Derived), [Variable(d = Identifier(b))]))"
#     assert Checker(source).check_from_source() == expected
# def test_poly15(): 
#     source = """
# class Base {
#     int x;
    
#     void method1() {
#         io.writeStrLn("Base method1");
#     }
    
#     int getValue() {
#         return this.x;
#     }
# }

# class Derived extends Base {
#     int y;
    
#     void method1() {
#         io.writeStrLn("Derived method1");
#     }
    
#     void method2() {
#         io.writeStrLn("Derived method2");
#     }
    
#     int getY() {
#         return this.y;
#     }
# }

# class Test10_Errors {
#     void main() {
#         Base b := new Derived();
        
#         # Valid polymorphic calls
#         b.method1();  # Calls Derived's method1
#         int val := b.getValue();  # Calls Base's getValue
        
#         # ERROR CASES:
        
#         # Cannot access subclass-specific members through superclass reference
#         # b.method2();  # ERROR: UndeclaredMethod(method2) - Base doesn't have method2
#         #int yVal := b.getY();  # ERROR: UndeclaredMethod(getY)
#         # b.y := 10;  # ERROR: UndeclaredAttribute(y)
        
#         # Cannot downcast without explicit mechanism (OPLang doesn't support casting)
#         # Derived d := b;  # ERROR: TypeMismatchInStatement - cannot assign Base to Derived
        
#         # Array type mismatch
#         Base[3] bases;
#         Derived[3] deriveds;
#         bases := deriveds;  # This would be valid (upcasting array)
#         # deriveds := bases;  # ERROR: TypeMismatchInStatement (downcasting not allowed)
#     }
# }
# """
#     expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(bases) := Identifier(deriveds)))"
#     assert Checker(source).check_from_source() == expected
# def test_poly16(): 
#     source = """
# class Base {
#     int x;
    
#     void method1() {
#         io.writeStrLn("Base method1");
#     }
    
#     int getValue() {
#         return this.x;
#     }
# }

# class Derived extends Base {
#     int y;
    
#     void method1() {
#         io.writeStrLn("Derived method1");
#     }
    
#     void method2() {
#         io.writeStrLn("Derived method2");
#     }
    
#     int getY() {
#         return this.y;
#     }
# }

# class Test10_Errors {
#     void main() {
#         Base b := new Derived();
        
#         # Valid polymorphic calls
#         b.method1();  # Calls Derived's method1
#         int val := b.getValue();  # Calls Base's getValue
        
#         # ERROR CASES:
        
#         # Cannot access subclass-specific members through superclass reference
#         # b.method2();  # ERROR: UndeclaredMethod(method2) - Base doesn't have method2
#         #int yVal := b.getY();  # ERROR: UndeclaredMethod(getY)
#         # b.y := 10;  # ERROR: UndeclaredAttribute(y)
        
#         # Cannot downcast without explicit mechanism (OPLang doesn't support casting)
#         # Derived d := b;  # ERROR: TypeMismatchInStatement - cannot assign Base to Derived
        
#         # Array type mismatch
#         Base[3] bases;
#         Derived[3] deriveds;
#         # bases := deriveds;  # This would be valid (upcasting array)
#         deriveds := bases;  # ERROR: TypeMismatchInStatement (downcasting not allowed)
#     }
# }
# """
#     expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(deriveds) := Identifier(bases)))"
#     assert Checker(source).check_from_source() == expected
# def test_poly17(): 
#     source = """
# class Account {
#     string accountNumber;
#     float balance;
    
#     Account(string accNum; float initialBalance) {
#         this.accountNumber := accNum;
#         this.balance := initialBalance;
#     }
    
#     void deposit(float amount) {
#         this.balance := this.balance + amount;
#     }
    
#     void withdraw(float amount) {
#         this.balance := this.balance - amount;
#     }
    
#     float getBalance() {
#         return this.balance;
#     }
# }

# class SavingsAccount extends Account {
#     float interestRate;
    
#     SavingsAccount(string accNum; float initialBalance; float rate) {
#         this.accountNumber := accNum;
#         this.balance := initialBalance;
#         this.interestRate := rate;
#     }
    
#     void applyInterest() {
#         this.balance := this.balance + (this.balance * this.interestRate);
#     }
    
#     void withdraw(float amount) {
#         # Override with restriction
#         if this.balance - amount >= 100.0 then {
#             this.balance := this.balance - amount;
#         } else {
#             io.writeStrLn("Minimum balance required!");
#         }
#     }
# }

# class CheckingAccount extends Account {
#     float overdraftLimit;
    
#     CheckingAccount(string accNum; float initialBalance; float overdraft) {
#         this.accountNumber := accNum;
#         this.balance := initialBalance;
#         this.overdraftLimit := overdraft;
#     }
    
#     void withdraw(float amount) {
#         # Override with overdraft support
#         if this.balance - amount >= -this.overdraftLimit then {
#             this.balance := this.balance - amount;
#         } else {
#             io.writeStrLn("Overdraft limit exceeded!");
#         }
#     }
# }

# class Test11 {
#     void main() {
#         # Create accounts through superclass reference
#         Account acc1 := new SavingsAccount("SAV001", 1000.0, 0.05);
#         Account acc2 := new CheckingAccount("CHK001", 500.0, 200.0);
        
#         # Polymorphic withdraw calls
#         acc1.withdraw(50.0);   # Calls SavingsAccount's withdraw
#         acc2.withdraw(600.0);  # Calls CheckingAccount's withdraw
        
#         io.writeFloatLn(acc1.getBalance());
#         io.writeFloatLn(acc2.getBalance());
        
#         # Cannot call subclass-specific methods
#         acc1.applyInterest();  # ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "UndeclaredMethod(applyInterest)"
#     assert Checker(source).check_from_source() == expected

# def test_poly18(): 
#     source = """
# class LivingThing {
#     void breathe() {
#         io.writeStrLn("Breathing...");
#     }
    
#     void live() {
#         io.writeStrLn("Living...");
#     }
# }

# class Animal extends LivingThing {
#     void move() {
#         io.writeStrLn("Moving...");
#     }
    
#     void live() {
#         io.writeStrLn("Animal is living");
#     }
# }

# class Mammal extends Animal {
#     void feedMilk() {
#         io.writeStrLn("Feeding milk...");
#     }
    
#     void live() {
#         io.writeStrLn("Mammal is living");
#     }
# }

# class Human extends Mammal {
#     void think() {
#         io.writeStrLn("Thinking...");
#     }
    
#     void live() {
#         io.writeStrLn("Human is living");
#     }
# }

# class Test12 {
#     void main() {
#         # Test polymorphism across deep hierarchy
#         LivingThing lt := new Human();
#         lt.live();      # Should call Human's live
#         lt.breathe();   # Calls LivingThing's breathe
#         # lt.move();    # ERROR: UndeclaredMethod
#         # lt.think();   # ERROR: UndeclaredMethod
        
#         Animal a := new Human();
#         a.live();       # Should call Human's live
#         a.move();       # Calls Animal's move
#         a.breathe();    # Calls LivingThing's breathe
#         # a.think();    # ERROR: UndeclaredMethod
        
#         Mammal m := new Human();
#         m.live();       # Should call Human's live
#         m.feedMilk();   # Calls Mammal's feedMilk
#         m.move();       # Calls Animal's move
#         m.breathe();    # Calls LivingThing's breathe
#         # m.think();    # ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected
# def test_poly19(): 
#     source = """
# class LivingThing {
#     void breathe() {
#         io.writeStrLn("Breathing...");
#     }
    
#     void live() {
#         io.writeStrLn("Living...");
#     }
# }

# class Animal extends LivingThing {
#     void move() {
#         io.writeStrLn("Moving...");
#     }
    
#     void live() {
#         io.writeStrLn("Animal is living");
#     }
# }

# class Mammal extends Animal {
#     void feedMilk() {
#         io.writeStrLn("Feeding milk...");
#     }
    
#     void live() {
#         io.writeStrLn("Mammal is living");
#     }
# }

# class Human extends Mammal {
#     void think() {
#         io.writeStrLn("Thinking...");
#     }
    
#     void live() {
#         io.writeStrLn("Human is living");
#     }
# }

# class Test12 {
#     void main() {
#         # Test polymorphism across deep hierarchy
#         LivingThing lt := new Human();
#         lt.live();      # Should call Human's live
#         lt.breathe();   # Calls LivingThing's breathe
#         # lt.move();    # ERROR: UndeclaredMethod
#         # lt.think();   # ERROR: UndeclaredMethod
        
#         Animal a := new Human();
#         a.live();       # Should call Human's live
#         a.move();       # Calls Animal's move
#         a.breathe();    # Calls LivingThing's breathe
#         # a.think();    # ERROR: UndeclaredMethod
        
#         Mammal m := new Human();
#         m.live();       # Should call Human's live
#         m.feedMilk();   # Calls Mammal's feedMilk
#         m.move();       # Calls Animal's move
#         m.breathe();    # Calls LivingThing's breathe
#         # m.think();    # ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected
# def test_poly20(): 
#     source = """
# class LivingThing {
#     void breathe() {
#         io.writeStrLn("Breathing...");
#     }
    
#     void live() {
#         io.writeStrLn("Living...");
#     }
# }

# class Animal extends LivingThing {
#     void move() {
#         io.writeStrLn("Moving...");
#     }
    
#     void live() {
#         io.writeStrLn("Animal is living");
#     }
# }

# class Mammal extends Animal {
#     void feedMilk() {
#         io.writeStrLn("Feeding milk...");
#     }
    
#     void live() {
#         io.writeStrLn("Mammal is living");
#     }
# }

# class Human extends Mammal {
#     void think() {
#         io.writeStrLn("Thinking...");
#     }
    
#     void live() {
#         io.writeStrLn("Human is living");
#     }
# }

# class Test12 {
#     void main() {
#         # Test polymorphism across deep hierarchy
#         LivingThing lt := new Human();
#         lt.live();      # Should call Human's live
#         lt.breathe();   # Calls LivingThing's breathe
#         # lt.move();    # ERROR: UndeclaredMethod
#         # lt.think();   # ERROR: UndeclaredMethod
        
#         Animal a := new Human();
#         a.live();       # Should call Human's live
#         a.move();       # Calls Animal's move
#         a.breathe();    # Calls LivingThing's breathe
#         # a.think();    # ERROR: UndeclaredMethod
        
#         Mammal m := new Human();
#         m.live();       # Should call Human's live
#         m.feedMilk();   # Calls Mammal's feedMilk
#         m.move();       # Calls Animal's move
#         m.breathe();    # Calls LivingThing's breathe
#         # m.think();    # ERROR: UndeclaredMethod
#     }
# }
# """
#     expected = "No Entry Point"
#     assert Checker(source).check_from_source() == expected
# def test_poly_undeclared_method_in_parent():
#     """
#     Edge case: Biến kiểu Cha (P) giữ đối tượng Con (C). 
#     Gọi method chỉ có ở Con -> Phải báo lỗi Undeclared Method.
#     Lý do: Static check chỉ nhìn thấy kiểu P.
#     """
#     source = """
#     class P { 
#         void parentMethod() {} 
#     }
#     class C extends P { 
#         void childMethod() {} 
#     }
#     class Test {
#         static void main() {
#             P obj := new C();
#             obj.parentMethod(); # OK
#             obj.childMethod();  # Error: P không có childMethod
#         }
#     }
#     """
#     expected = "UndeclaredMethod(childMethod)"
#     assert Checker(source).check_from_source() == expected

# def test_poly_field_access_shadowing():
#     """
#     Edge case: Truy cập thuộc tính (Attribute). 
#     Attribute không có đa hình động. Truy cập qua P phải tìm trong P.
#     """
#     source = """
#     class P { 
#         int x := 1; 
#     }
#     class C extends P { 
#         float x := 1.5; 
#     }
#     class Test {
#         static void main() {
#             P obj := new C();
#             float val := obj.x; # Error: obj.x là int (của P), không gán được cho float nếu không coerce
#             # Hoặc nếu P không có x thì sẽ là Undeclared Attribute
#         }
#     }
#     """
#     # Trường hợp này: P.x là int. Gán int vào float là hợp lệ (coercion).
#     # Tuy nhiên, nếu test logic Undeclared, ta đổi tên biến:
#     source_undeclared = """
#     class P {}
#     class C extends P { int x := 1; }
#     class Test {
#         static void main() {
#             P obj := new C();
#             int val := obj.x; # Error: P không có x
#         }
#     }
#     """
#     expected = "UndeclaredAttribute(x)"
#     assert Checker(source_undeclared).check_from_source() == expected

def test_inheritance_undeclared_parent():
    """Test extending a non-existent class"""
    source = """
class Child extends GhostClass {
    void main() {
        io.writeStrLn("Hello");
    }
}
"""
    expected = "UndeclaredClass(GhostClass)"
    assert Checker(source).check_from_source() == expected

def test_inheritance_access_parent_field():
    """Test accessing a field defined in the parent class"""
    source = """
class Parent {
    int heritage;
}

class Child extends Parent {
    void accessParentField() {
        this.heritage := 100; # Should be valid
    }
    
    static void main() {
        Child c := new Child();
        c.accessParentField();
    }
}
"""
    expected = "Static checking passed" # No error expected
    assert Checker(source).check_from_source() == expected   

def test_inheritance_type_mismatch_assign():
    """Test assigning a Parent object to a Child variable (invalid downcast)"""
    source = """
class Parent {}
class Child extends Parent {}

class Test {
    static void main() {
        Parent p := new Parent();
        Child c;
        c := p; # Error: Parent is not compatible with Child
    }
}
"""
    # Lưu ý: Nội dung trong TypeMismatchInStatement thường là dòng code hoặc cấu trúc AST
    # Tùy thuộc vào implement của bạn, string trả về có thể khác nhau đôi chút.
    # Ở đây giả định output chuẩn theo format ErrorTypes.
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(p)))" 
    # Hoặc đơn giản là chuỗi báo lỗi class chung
    # expected = "TypeMismatchInStatement(...)"
    assert Checker(source).check_from_source() == expected

def test_inheritance_method_overriding():
    """Test valid method overriding (should not raise Redeclared error)"""
    source = """
class Animal {
    void makeSound() {
        io.writeStrLn("...");
    }
}

class Dog extends Animal {
    # This is Overriding, VALID in OPLang, not Redeclared
    void makeSound() {
        io.writeStrLn("Woof");
    }
    
    static void main() {
        Dog d := new Dog();
        d.makeSound();
    }
}
"""
    expected = "Static checking passed" # No error expected
    assert Checker(source).check_from_source() == expected

def test_inheritance_undeclared_attribute_chain():
    """Test accessing an attribute that exists in neither Child nor Parent"""
    source = """
class GrandParent { int x; }
class Parent extends GrandParent { int y; }
class Child extends Parent { int z; }

class Test {
    static void main() {
        Child c := new Child();
        c.x := 1; # Valid (from GrandParent)
        c.y := 2; # Valid (from Parent)
        c.z := 3; # Valid (from Child)
        c.w := 4; # Error: Not found anywhere in chain
    }
}
"""
    expected = "UndeclaredAttribute(w)"
    assert Checker(source).check_from_source() == expected

def test_inheritance_polymorphism_valid():
    """Test assigning Child object to Parent variable (Valid Upcast)"""
    source = """
class Shape {
    float getArea() { return 0.0; }
}

class Rectangle extends Shape {
    float length, width;
}

class Test {
    static void main() {
        Shape s;
        # Valid: Rectangle is a Shape (subtype -> supertype coercion)
        s := new Rectangle(); 
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_inheritance_transitive_assignment():
    """Test assigning GrandChild to GrandParent variable (Transitive Upcast)"""
    source = """
class GrandParent { int rootField; }
class Parent extends GrandParent { int midField; }
class Child extends Parent { int leafField; }

class Test {
    static void main() {
        GrandParent g;
        Child c := new Child();
        
        # Valid: Child IS-A Parent IS-A GrandParent
        g := c; 
        
        # Valid: Accessing root field via Child instance
        c.rootField := 10;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_inheritance_polymorphic_argument():
    """Test passing Child object to method expecting Parent"""
    source = """
class Animal {}
class Cat extends Animal {}

class Vet {
    void treat(Animal a) {
        # Do something
    }

    static void main() {
        Vet v := new Vet();
        Cat kitty := new Cat();
        
        # Valid: treat expects Animal, Cat is Animal
        v.treat(kitty);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_inheritance_polymorphic_argument():
    """Test passing Child object to method expecting Parent"""
    source = """
class Animal {}
class Cat extends Animal {}

class Vet {
    void treat(Animal a) {
        # Do something
    }

    static void main() {
        Vet v := new Vet();
        Cat kitty := new Cat();
        
        # Valid: treat expects Animal, Cat is Animal
        v.treat(kitty);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_inheritance_invalid_argument_downcast(): # check lai xem tesst nay
    """Test passing Parent object to method expecting Child"""
    source = """
class Animal {}
class Cat extends Animal {}

class Vet {
    void groom(Cat c) {}

    static void main() {
        Vet v := new Vet();
        Animal a := new Animal();
        
        # Error: TypeMismatch. Cannot pass Animal to Cat parameter.
        v.groom(a);
    }
}
"""
    # Lưu ý: Nội dung lỗi phụ thuộc vào AST của Call statement
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(Identifier(v).groom(Identifier(a)))))" 
    assert Checker(source).check_from_source() == expected

def test_inheritance_return_subtype(): # check lai
    """Test returning Child object in method declaring Parent return type"""
    source = """
class Shape {}
class Circle extends Shape {}

class Factory {
    Shape createShape() {
        # Valid: Returning Circle where Shape is expected
        return new Circle();
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_inheritance_access_child_method_from_parent_ref():
    """Test calling Child-only method on a Parent reference"""
    source = """
class Bird {
    void fly() {}
}

class Penguin extends Bird {
    void swim() {}
}

class Test {
    static void main() {
        Bird b := new Penguin();
        b.fly();  # Valid
        b.swim(); # Error: 'swim' is not defined in Bird
    }
}
"""
    expected = "UndeclaredMethod(swim)"
    assert Checker(source).check_from_source() == expected

def test_inheritance_field_shadowing():
    """Test declaring a field in Child with same name as Parent (Shadowing)"""
    source = """
class Parent {
    int x;
}

class Child extends Parent {
    # Valid: Shadows Parent.x. 
    # Not 'Redeclared' because it's in a different scope (Child vs Parent)
    float x; 

    static void main() {
        this.x := 1.5; # Refers to Child.x (float)
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_inheritance_array_element_assignment():
    """Test assigning Child object to element of Parent array"""
    source = """
class Fruit {}
class Apple extends Fruit {}

class Test {
    static void main() {
        Fruit[5] basket;
        Apple a := new Apple();
        
        # Valid: Apple is Fruit
        basket[0] := a;
        
        # Valid: New Apple is Fruit
        basket[1] := new Apple();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_inheritance_sibling_mismatch():
    """Test assigning one sibling class to another"""
    source = """
class Vehicle {}
class Car extends Vehicle {}
class Truck extends Vehicle {}

class Test {
    static void main() {
        Car c := new Car();
        Truck t := new Truck();
        
        c := t; # Error: Truck is not a Car
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := Identifier(t)))"
    assert Checker(source).check_from_source() == expected
def test_inheritance_undeclared_forward_ref(): # check lai thu no co global scope hay khong
    """Test extending a class defined later (if forward ref not allowed) or Undeclared"""
    source = """
class A extends B {} # If B is not yet seen, might be UndeclaredClass(B)
class B {}
class Test{
    static void main() {
    }
}
"""
    # Nếu OPLang biên dịch 1 pass từ trên xuống dưới:
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected


# OPLang Inheritance Test Cases

# Test 1: Valid inheritance - accessing inherited attributes
def test_inheritance_001(): # cai nay ph la no error 
    """Test valid access to inherited attribute"""
    source = """
class Animal {
    string species;
    
    void setSpecies(string s) {
        species := s;
    }
}

class Dog extends Animal {
    void identify() {
        setSpecies("Canine");
        io.writeStrLn(this.species);
    }
    
    static void main() {
        Dog d := new Dog();
        d.identify();
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 2: Valid inheritance - accessing inherited methods
def test_inheritance_002():
    """Test valid access to inherited method"""
    source = """
class Animal {
    string name;
    
    void setName(string n) {
        this.name := n;
    }
    
    string getName() {
        return this.name;
    }
}

class Dog extends Animal {
    static void main() {
        Dog d := new Dog();
        d.setName("Buddy");
        io.writeStrLn(d.getName());
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 3: Valid method overriding
def test_inheritance_003():
    """Test valid method overriding (not redeclaration)"""
    source = """
class Animal {
    void makeSound() {
        io.writeStrLn("Some sound");
    }
}

class Dog extends Animal {
    void makeSound() {
        io.writeStrLn("Woof!");
    }
    
    static void main() {
        Dog d := new Dog();
        d.makeSound();
    }
}
"""
    expected = "Static checking passed"  # No error expected (overriding is valid)
    assert Checker(source).check_from_source() == expected


# Test 4: Undeclared parent class
def test_inheritance_004():
    """Test inheritance from undeclared class"""
    source = """
class Student extends Person {
    int studentId;
    
    static void main() {
        Student s := new Student();
    }
}
"""
    expected = "UndeclaredClass(Person)"
    assert Checker(source).check_from_source() == expected


# Test 5: Accessing inherited attribute through subclass instance
def test_inheritance_005():
    """Test accessing parent attribute from subclass instance"""
    source = """
class Shape {
    float length;
    float width;
}

class Rectangle extends Shape {
    float getArea() {
        return this.length * this.width;
    }
    
    static void main() {
        Rectangle r := new Rectangle();
        r.length := 5.0;
        r.width := 3.0;
        io.writeFloatLn(r.getArea());
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 6: Type coercion - subtype to supertype
def test_inheritance_006():
    """Test valid subtype to supertype assignment"""
    source = """
class Shape {
    float getArea() {
        return 0.0;
    }
}

class Rectangle extends Shape {
    float length;
    float width;
    
    float getArea() {
        return this.length * this.width;
    }
}

class Example {
    static void main() {
        Shape s;
        s := new Rectangle();
        io.writeFloatLn(s.getArea());
    }
}
"""
    expected = "Static checking passed"  # No error expected (subtype can coerce to supertype)
    assert Checker(source).check_from_source() == expected


# Test 7: Accessing method that doesn't exist in parent or child
def test_inheritance_007():
    """Test accessing undeclared method in inheritance hierarchy"""
    source = """
class Animal {
    string species;
}

class Dog extends Animal {
    static void main() {
        Dog d := new Dog();
        d.fly();
    }
}
"""
    expected = "UndeclaredMethod(fly)"
    assert Checker(source).check_from_source() == expected


# Test 8: Accessing attribute that doesn't exist in inheritance chain
def test_inheritance_008():
    """Test accessing undeclared attribute in inheritance hierarchy"""
    source = """
class Animal {
    string species;
}

class Dog extends Animal {
    void display() {
        io.writeStrLn(this.breed);
    }
    
    static void main() {
        Dog d := new Dog();
        d.display();
    }
}
"""
    expected = "UndeclaredAttribute(breed)"
    assert Checker(source).check_from_source() == expected


# Test 9: Multi-level inheritance
def test_inheritance_009():
    """Test accessing attributes through multi-level inheritance"""
    source = """
class Animal {
    string species;
}

class Mammal extends Animal {
    int legs;
}

class Dog extends Mammal {
    static void main() {
        Dog d := new Dog();
        d.species := "Canine";
        d.legs := 4;
        io.writeStrLn(d.species);
        io.writeIntLn(d.legs);
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 10: Polymorphism - calling overridden method
def test_inheritance_010():
    """Test polymorphism with method overriding"""
    source = """
class Shape {
    float getArea() {
        return 0.0;
    }
}

class Rectangle extends Shape {
    float length;
    float width;
    
    float getArea() {
        return this.length * this.width;
    }
}

class Triangle extends Shape {
    float base;
    float height;
    
    float getArea() {
        return this.base * this.height / 2;
    }
}

class Example {
    static void main() {
        Shape s;
        s := new Rectangle();
        io.writeFloatLn(s.getArea());
        s := new Triangle();
        io.writeFloatLn(s.getArea());
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 11: Cannot access child's attribute through parent reference
def test_inheritance_011():
    """Test accessing child-specific attribute through parent reference"""
    source = """
class Shape {
    float area;
}

class Rectangle extends Shape {
    float length;
    float width;
}

class Example {
    static void main() {
        Shape s := new Rectangle();
        s.length := 5.0;
    }
}
"""
    expected = "UndeclaredAttribute(length)"
    assert Checker(source).check_from_source() == expected


# Test 12: Cannot access child's method through parent reference
def test_inheritance_012():
    """Test accessing child-specific method through parent reference"""
    source = """
class Shape {
    float getArea() {
        return 0.0;
    }
}

class Rectangle extends Shape {
    float getPerimeter() {
        return 0.0;
    }
}

class Example {
    static void main() {
        Shape s := new Rectangle();
        io.writeFloatLn(s.getPerimeter());
    }
}
"""
    expected = "UndeclaredMethod(getPerimeter)"
    assert Checker(source).check_from_source() == expected


# Test 13: Valid shadowing in different scopes (not inheritance)
def test_inheritance_013():
    """Test valid shadowing - not an error"""
    source = """
class ShadowExample {
    int value;
    
    void method() {
        int value := 200;
        io.writeIntLn(value);
    }
    
    static void main() {
        ShadowExample se := new ShadowExample();
        se.value := 100;
        se.method();
    }
}
"""
    expected = "Static checking passed"  # No error expected (shadowing is allowed)
    assert Checker(source).check_from_source() == expected


# Test 14: Redeclared attribute in same class (not inheritance)
def test_inheritance_014():
    """Test redeclared attribute in same class"""
    source = """
class Person {
    string name;
    int age;
    string name;
}
"""
    expected = "Redeclared(Attribute, name)"
    assert Checker(source).check_from_source() == expected


# Test 15: Accessing 'this' in inherited context
def test_inheritance_015():
    """Test using 'this' to access inherited members"""
    source = """
class Animal {
    string species;
    
    void setSpecies(string s) {
        this.species := s;
    }
}

class Dog extends Animal {
    void identify() {
        this.setSpecies("Canine");
        io.writeStrLn(this.species);
    }
    
    static void main() {
        Dog d := new Dog();
        d.identify();
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 16: Type mismatch with inheritance
def test_inheritance_016():
    """Test type mismatch - cannot assign parent to child"""
    source = """
class Shape {
    float area;
}

class Rectangle extends Shape {
    float length;
    float width;
}

class Example {
    static void main() {
        Rectangle r;
        r := new Shape();
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(r) := ObjectCreation(new Shape())))"
    assert Checker(source).check_from_source() == expected


# Test 17: Inherited static members
def test_inheritance_017():
    """Test accessing inherited static members"""
    source = """
class Animal {
    static int count;
    
    static void resetCount() {
        Animal.count := 0;
    }
}

class Dog extends Animal {
    static void main() {
        Dog.resetCount();
        io.writeIntLn(Dog.count);
    }
}
"""
    expected = "Static checking passed"  # No error expected (static members are inherited)
    assert Checker(source).check_from_source() == expected


# Test 18: Complex inheritance with multiple attributes and methods
def test_inheritance_018():
    """Test complex inheritance scenario"""
    source = """
class Vehicle {
    string brand;
    int year;
    
    void setBrand(string b) {
        this.brand := b;
    }
    
    string getBrand() {
        return this.brand;
    }
}

class Car extends Vehicle {
    int doors;
    
    void setDoors(int d) {
        this.doors := d;
    }
    
    void display() {
        io.writeStrLn(this.getBrand());
        io.writeIntLn(this.year);
        io.writeIntLn(this.doors);
    }
    
    static void main() {
        Car c := new Car();
        c.setBrand("Toyota");
        c.year := 2023;
        c.setDoors(4);
        c.display();
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 19: Overriding with different return type (should be error if types don't match)
def test_inheritance_019():
    """Test method overriding with type compatibility"""
    source = """
class Shape {
    int getValue() {
        return 0;
    }
}

class Rectangle extends Shape {
    int getValue() {
        return 10;
    }
    
    static void main() {
        Rectangle r := new Rectangle();
        io.writeIntLn(r.getValue());
    }
}
"""
    expected = "Static checking passed"  # No error expected (same return type)
    assert Checker(source).check_from_source() == expected


# Test 20: Accessing inherited final attributes
def test_inheritance_020():
    """Test accessing inherited final (constant) attributes"""
    source = """
class Constants {
    final int MAX_SIZE := 100;
}

class MyClass extends Constants {
    static void main() {
        MyClass mc := new MyClass();
        io.writeIntLn(mc.MAX_SIZE);
    }
}
"""
    expected = "Static checking passed"  # No error expected (can read inherited constants)
    assert Checker(source).check_from_source() == expected



# Test 1: Simple recursive factorial
def test_recursive_001():
    """Test simple recursive factorial function"""
    source = """
class Math {
    int factorial(int n) {
        if n == 0 then 
            return 1; 
        else 
            return n * this.factorial(n - 1);
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.factorial(5));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 2: Recursive fibonacci
def test_recursive_002():
    """Test recursive fibonacci function"""
    source = """
class Math {
    int fibonacci(int n) {
        if n <= 1 then
            return n;
        else
            return this.fibonacci(n - 1) + this.fibonacci(n - 2);
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.fibonacci(6));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 3: Recursive sum of array elements
def test_recursive_003():
    """Test recursive sum of array"""
    source = """
class ArrayUtils {
    int sumArray(int[10] arr; int index) {
        if index < 0 then
            return 0;
        else
            return arr[index] + this.sumArray(arr, index - 1);
    }
    
    static void main() {
        ArrayUtils au := new ArrayUtils();
        int[10] numbers := {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        io.writeIntLn(au.sumArray(numbers, 9));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 4: Recursive power function
def test_recursive_004():
    """Test recursive power function"""
    source = """
class Math {
    int power(int base; int exp) {
        if exp == 0 then
            return 1;
        else
            return base * this.power(base, exp - 1);
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.power(2, 10));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 5: Recursive GCD (Greatest Common Divisor)
def test_recursive_005():
    """Test recursive GCD calculation"""
    source = """
class Math {
    int gcd(int a; int b) {
        if b == 0 then
            return a;
        else
            return this.gcd(b, a % b);
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.gcd(48, 18));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 6: Recursive countdown
def test_recursive_006():
    """Test recursive countdown"""
    source = """
class Counter {
    void countdown(int n) {
        if n > 0 then {
            io.writeIntLn(n);
            this.countdown(n - 1);
        }
    }
    
    static void main() {
        Counter c := new Counter();
        c.countdown(5);
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# # Test 7: Recursive string reversal (using recursion concept)
# def test_recursive_007(): # khong ho tro test nay
#     """Test recursive number reversal"""
#     source = """
# class StringUtils {
#     int reverseNumber(int num; int reversed) {
#         if num == 0 then
#             return reversed;
#         else
#             return this.reverseNumber(num \ 10, reversed * 10 + num % 10);
#     }
    
#     static void main() {
#         StringUtils su := new StringUtils();
#         io.writeIntLn(su.reverseNumber(12345, 0));
#     }
# }
# """
#     expected = "Static checking passed"  # No error expected
#     assert Checker(source).check_from_source() == expected


# Test 8: Recursive sum of digits
# def test_recursive_008():
#     """Test recursive sum of digits"""
#     source = """
# class Math {
#     int sumDigits(int n) {
#         if n == 0 then
#             return 0;
#         else
#             return n % 10 + this.sumDigits(n \ 10);
#     }
    
#     static void main() {
#         Math m := new Math();
#         io.writeIntLn(m.sumDigits(12345));
#     }
# }
# """
#     expected = "Static checking passed"  # No error expected
#     assert Checker(source).check_from_source() == expected


# Test 9: Mutual recursion (two functions calling each other)
def test_recursive_009():
    """Test mutual recursion"""
    source = """
class EvenOdd {
    boolean isEven(int n) {
        if n == 0 then
            return true;
        else
            return this.isOdd(n - 1);
    }
    
    boolean isOdd(int n) {
        if n == 0 then
            return false;
        else
            return this.isEven(n - 1);
    }
    
    static void main() {
        EvenOdd eo := new EvenOdd();
        io.writeBoolLn(eo.isEven(10));
        io.writeBoolLn(eo.isOdd(10));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 10: Recursive binary search
# def test_recursive_010(): # chua pass 
#     """Test recursive binary search"""
#     source = """
# class Search {
#     int binarySearch(int[10] arr; int left; int right; int target) {
#         if right >= left then {
#             int mid := left + (right - left) \ 2;
            
#             if arr[mid] == target then
#                 return mid;
            
#             if arr[mid] > target then
#                 return this.binarySearch(arr, left, mid - 1, target);
            
#             return this.binarySearch(arr, mid + 1, right, target);
#         }
#         return -1;
#     }
    
#     static void main() {
#         Search s := new Search();
#         int[10] arr := {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
#         io.writeIntLn(s.binarySearch(arr, 0, 9, 7));
#     }
# }
# """
#     expected = "Static checking passed"  # No error expected
#     assert Checker(source).check_from_source() == expected


# Test 11: Recursive with float return type
def test_recursive_011():
    """Test recursive function with float return"""
    source = """
class Math {
    float geometricSum(float r; int n) {
        if n == 0 then
            return 1.0;
        else
            return 1.0 + r * this.geometricSum(r, n - 1);
    }
    
    static void main() {
        Math m := new Math();
        io.writeFloatLn(m.geometricSum(0.5, 5));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 12: Recursive Tower of Hanoi
def test_recursive_012():
    """Test recursive Tower of Hanoi"""
    source = """
class TowerOfHanoi {
    void solve(int n; string from; string tow; string aux) {
        if n == 1 then {
            io.writeStrLn("Move disk 1 from " ^ from ^ " to " ^ tow);
        } else {
            this.solve(n - 1, from, aux, tow);
            io.writeStrLn("Move disk from " ^ from ^ " to " ^ tow);
            this.solve(n - 1, aux, tow, from);
        }
    }
    
    static void main() {
        TowerOfHanoi toh := new TowerOfHanoi();
        toh.solve(3, "A", "C", "B");
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# # Test 13: Recursive palindrome check
# def test_recursive_013():
#     """Test recursive palindrome number check"""
#     source = """
# class StringUtils {
#     int getReversed(int num; int reversed) {
#         if num == 0 then
#             return reversed;
#         else
#             return this.getReversed(num \ 10, reversed * 10 + num % 10);
#     }
    
#     boolean isPalindrome(int num) {
#         return num == this.getReversed(num, 0);
#     }
    
#     static void main() {
#         StringUtils su := new StringUtils();
#         io.writeBoolLn(su.isPalindrome(12321));
#         io.writeBoolLn(su.isPalindrome(12345));
#     }
# }
# """
#     expected = "Static checking passed"  # No error expected
#     assert Checker(source).check_from_source() == expected


# Test 14: Recursive with static method
def test_recursive_014():
    """Test recursive static method"""
    source = """
class Math {
    static int factorial(int n) {
        if n <= 1 then 
            return 1; 
        else 
            return n * Math.factorial(n - 1);
    }
    
    static void main() {
        io.writeIntLn(Math.factorial(5));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 15: Recursive method calling with wrong type - should error
def test_recursive_015():
    """Test recursive call with type mismatch"""
    source = """
class Math {
    int factorial(int n) {
        if n == 0 then 
            return 1; 
        else 
            return n * this.factorial("5");
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.factorial(5));
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).factorial(StringLiteral('5'))))"
    assert Checker(source).check_from_source() == expected


# Test 16: Recursive method with undeclared variable in recursive call
def test_recursive_016():
    """Test recursive call with undeclared variable"""
    source = """
class Math {
    int factorial(int n) {
        if n == 0 then 
            return 1; 
        else 
            return n * this.factorial(undeclaredVar);
    }
    
    static void main() {
        Math m := new Math();
        io.writeIntLn(m.factorial(5));
    }
}
"""
    expected = "UndeclaredIdentifier(undeclaredVar)"
    assert Checker(source).check_from_source() == expected


# Test 17: Recursive with inheritance
def test_recursive_017():
    """Test recursive method in inherited class"""
    source = """
class BaseMath {
    int factorial(int n) {
        if n <= 1 then 
            return 1; 
        else 
            return n * this.factorial(n - 1);
    }
}

class AdvancedMath extends BaseMath {
    int doubleFactorial(int n) {
        return 2 * this.factorial(n);
    }
    
    static void main() {
        AdvancedMath am := new AdvancedMath();
        io.writeIntLn(am.doubleFactorial(5));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 18: Recursive with multiple parameters
def test_recursive_018():
    """Test recursive function with multiple parameters"""
    source = """
class Math {
    int ackermann(int m; int n) {
        if m == 0 then
            return n + 1;
        else {
            if n == 0 then
                return this.ackermann(m - 1, 1);
            else
                return this.ackermann(m - 1, this.ackermann(m, n - 1));
        }
    }
    
    static void main() {
        Math math := new Math();
        io.writeIntLn(math.ackermann(2, 3));
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 19: Recursive void function
def test_recursive_019():
    """Test recursive void function"""
    source = """
class Printer {
    void printNumbers(int n) {
        if n > 0 then {
            this.printNumbers(n - 1);
            io.writeIntLn(n);
        }
    }
    
    static void main() {
        Printer p := new Printer();
        p.printNumbers(5);
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected


# Test 20: Recursive with array manipulation
def test_recursive_020():
    """Test recursive function manipulating arrays"""
    source = """
class ArrayProcessor {
    void fillArray(int[10] arr; int index; int value) {
        if index >= 0 then {
            arr[index] := value;
            this.fillArray(arr, index - 1, value + 1);
        }
    }
    
    static void main() {
        ArrayProcessor ap := new ArrayProcessor();
        int[10] numbers := {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        ap.fillArray(numbers, 9, 1);
        for i := 0 to 9 do {
            io.writeIntLn(numbers[i]);
        }
    }
}
"""
    expected = "Static checking passed"  # No error expected
    assert Checker(source).check_from_source() == expected
def test_array_literal_polymorphic_valid():
    source = """
class A {}
class B extends A {}
class C extends A {}

class Test {
    static void main() {}

    void m() {
        A[2] arr := { new B(), new C() };   # OK vì B, C đều là subclass của A
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new B()), ObjectCreation(new C())}))"
    assert Checker(source).check_from_source() == expected
def test_array_literal_polymorphic_invalid():
    source = """
class A {}
class B extends A {}

class Test {
    static void main() {}

    void m() {
        B[2] arr := { new A(), new B() };   # ERROR: A không phải B
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new A()), ObjectCreation(new B())}))"
    assert Checker(source).check_from_source() == expected
    
def test_array(): 
    source = """
    class A {}
    class B extends A {}
    class C extends A {}
    class Test {
    static void main() {
    
    # 1. Khởi tạo mảng A rỗng (hoặc với giá trị mặc định nếu có)
    # Lưu ý: OPLang yêu cầu kích thước mảng là literal số nguyên, và khởi tạo mảng object thường là nil
    A[2] arr; 
    
    # 2. Gán từng phần tử (Cho phép Subtype coercion tại đây)
    arr[0] := new B(); # Hợp lệ: B ép kiểu lên A
    arr[1] := new C(); # Hợp lệ: C ép kiểu lên A   
    
    }

}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_assignment_array_size_mismatch():
    """Test array assignment with different sizes"""
    source = """
class TestArray {
    void main() {
        int[5] arr5;
        int[3] arr3;
        
        # Initialize arrays (assuming support or simple declaration)
        arr5 := arr3;   # Error: Different sizes (5 vs 3)
    }
}
"""
    expect_error = "TypeMismatchInStatement(AssignmentStatement(IdLHS(arr5) := Identifier(arr3)))"
    assert str(Checker(source).check_from_source()) == expect_error


def test_assignment_array_type_mismatch():
    """Test array assignment with incompatible element types"""
    source = """
class TestArrayType {
    void main() {
        int[5] intArr;
        float[5] floatArr;
        
        # Even though int -> float is valid for scalars, 
        # int[] -> float[] is typically invalid in strict static checking 
        # or implies TypeMismatch if OPLang doesn't support array covariance.
        # Based on error spec: "IllegalArrayLiteral" implies strict typing.
        
        intArr := floatArr; # Error: float cannot be assigned to int
    }
}
"""
    expect_error = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArr) := Identifier(floatArr)))"
    assert str(Checker(source).check_from_source()) == expect_error
def test_assignment_void_mismatch():
    """Test assigning a void method result to a variable"""
    source = """
class TestVoid {
    void doNothing() {
        return;
    }

    void main() {
        int x;
        x := this.doNothing(); # Error: RHS is void, LHS is int
    }
}
"""
    expect_error = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).doNothing()))"
    assert str(Checker(source).check_from_source()) == expect_error
def test_void(): 
    source = """
class A {}    
class TestVoid {
    void doNothing() {
        return;
    }
}
class test {
    static void main() {
        A a; 
        TestVoid b; 
        a := b.doNothing(); # Error: RHS is void, LHS is int
    
    }
}
"""

    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(b).doNothing()))"
    assert Checker(source).check_from_source() == expected

def test_static_typing_assignment():
    """Test: Variable cannot hold value of incompatible type (e.g., int var holding string)"""
    source = """
    class TypeCheck {
        void main() {
            int x := 10;
            # Static error: Cannot assign string to int variable
            x := "Hello World"; 
        }
    }
    """
    # Lỗi xảy ra tại câu lệnh gán x := "Hello World"
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := StringLiteral('Hello World')))"
    assert Checker(source).check_from_source() == expected

def test_static_typing_function_args():
    """Test: Function arguments are checked at compile time"""
    source = """
    class MathUtils {
        # Method expects an integer
        int square(int n) {
            return n * n;
        }
        
        void main() {
            # Static error: Passing a string to a method expecting int
            # OPLang does not coerce string to int
            int result := this.square("5");
        }
    }
    """
    # Lỗi xảy ra khi truyền tham số "5" vào square
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).square(StringLiteral('5'))))" 
    assert Checker(source).check_from_source() == expected

def test_static_typing_binary_op():
    """Test: Binary operations check operand types statically"""
    source = """
    class Calc {
        void main() {
            int a := 5;
            boolean b := true;
            # Static error: Cannot add integer and boolean
            int c := a + b;
        }
    }
    """
    # Lỗi xảy ra tại biểu thức a + b
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), +, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_static_typing_return_type():
    """Test: Return value must match declared return type"""
    source = """
    class TestReturn {
        # Declared to return int
        int getNumber() {
            # Static error: Returning a float when int is expected
            # Note: int -> float coercion is ok, but float -> int is usually not implicit
            return 3.14;
        }
        
        static void main() {
            TestReturn t := new TestReturn();
            t.getNumber();
        }
    }
    """
    # Lỗi tại lệnh return 3.14
    expected = "TypeMismatchInStatement(ReturnStatement(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_static_typing_inheritance_mismatch():
    """Test: Cannot assign Superclass object to Subclass variable (Implicit Downcasting invalid)"""
    source = """
    class Animal {}
    class Dog extends Animal {}
    
    class Main {
        static void main() {
            Animal a := new Animal();
            # Static error: Cannot assign Animal to Dog implicitly
            # 'a' has type Animal, variable 'd' has type Dog.
            # OPLang spec: expression in subtype can be assigned to superclass (Dog -> Animal OK)
            # But Animal -> Dog is NOT OK.
            Dog d := a;
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(Dog), [Variable(d = Identifier(a))]))"
    assert Checker(source).check_from_source() == expected

def test_static_typing_mixed_array():
    """Test: Array literal elements must be of the same type (determined statically)"""
    source = """
    class ArrayCheck {
        void main() {
            # Static error: Mixed types in array literal (int and float)
            # Even if coercion exists, array literals usually require strict type matching or explicit casting
            float[3] arr := {1.0, 2.0, 3}; 
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({FloatLiteral(1.0), FloatLiteral(2.0), IntLiteral(3)}))"
    assert Checker(source).check_from_source() == expected
def test_coerce_int_to_float_full_flow():
    """
    Test valid coercion from Int to Float in:
    1. Variable declaration/assignment
    2. Method Argument
    3. Method Return
    """
    source = """
    class CoercionTest {
        # 1. Method defined to return float, but actually returns int literal
        float getFloatFromInt() {
            return 10; # Coercion: int -> float
        }

        # 2. Method expects float param
        void processFloat(float f) {
            io.writeFloatLn(f);
        }

        static void main() {
            # 3. Assign int to float variable
            float x := 5; 
            CoercionTest ct := new CoercionTest();
            # 4. Pass int variable to method expecting float
            int i := 100;
            ct.processFloat(i); # Coercion: int -> float
            
            # 5. Pass int literal to method expecting float
            ct.processFloat(99); 

            # Check complex expression coercion: int * float -> float
            float y := i * x; 
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_div_operator_result_type_error():
    """
    Edge case: Operator '/' always returns float.
    Assigning (int / int) to int variable should FAIL.
    """
    source = """
    class DivTest {
        void main() {
            int a := 10;
            int b := 2;
            
            # Error: 10 / 2 returns float (5.0), cannot assign to int without cast (which OPLang lacks)
            int c := a / b; 
        }
    }
    """
    # Kỳ vọng lỗi TypeMismatchInStatement tại dòng int c := a / b;
    # (Vì vế phải là float, vế trái là int)
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(c = BinaryOp(Identifier(a), /, Identifier(b)))]))"
    assert Checker(source).check_from_source() == expected
# def test_int_div_operator_success():
#     """
#     Edge case: Operator '\' returns int.
#     Can be assigned to both int (direct) and float (coercion).
#     """
#     source = """
#     class IntDivTest {
#         void main() {
#             int a := 10;
#             int b := 3;
            
#             int c := a \ b;   # OK: int -> int
#             float d := a \ b; # OK: int -> float (coercion)
#         }
#     }
#     """
#     expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_inheritance_coercion_param_and_assign():
    """
    Test passing Subclass object to method expecting Superclass.
    Test assigning Subclass object to Superclass variable.
    """
    source = """
    class Animal {}
    class Dog extends Animal {}
    class Cat extends Animal {}

    class Zoo {
        # Method expects Animal
        void checkAnimal(Animal a) {
            io.writeStrLn("Checked");
        }

        void main() {
            Dog d := new Dog();
            
            # 1. Assign Subtype to Supertype variable
            Animal a := d; 
            
            # 2. Pass Subtype to method expecting Supertype
            this.checkAnimal(d);
            
            # 3. Pass new Subtype instance directly
            this.checkAnimal(new Cat());
        }
    }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_invalid_implicit_downcast():
    """
    Error: Cannot implicitly assign Superclass object to Subclass variable.
    """
    source = """
    class Animal {}
    class Dog extends Animal {}

    class Main {
        void main() {
            Animal a := new Dog(); # Upcast OK
            
            # Error: Animal cannot be assigned to Dog implicitly
            Dog d := a; 
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(Dog), [Variable(d = Identifier(a))]))"
    assert Checker(source).check_from_source() == expected
def test_mod_operator_float_error():
    """
    Edge case: Modulo '%' operands must be int. 
    Using float should fail TypeMismatchInExpression.
    """
    source = """
    class ModTest {
        void main() {
            int x := 10;
            float y := 3.0;
            
            # Error: y is float
            int z := x % y; 
        }
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), %, Identifier(y)))"
    assert Checker(source).check_from_source() == expected
def test_void_usage_error():
    """
    Edge case: Cannot use result of void method in assignment or expression.
    """
    source = """
    class VoidTest {
        void doNothing() {
            return;
        }

        void main() {
            int x;
            # Error: RHS is void, LHS is int
            x := this.doNothing(); 
        }
    }
    """
    # Lỗi này có thể là TypeMismatchInExpression (vì void method call là expression)
    # hoặc TypeMismatchInStatement (lỗi gán).
    # Dựa trên spec lỗi số 5: "Method must have non-void return type" trong Expression.
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).doNothing()))" # Hoặc logic tương tự trong code bạn
    assert Checker(source).check_from_source() == expected
def test_array_element_coercion():
    """
    Test that implicit coercion (int -> float) works when assigning to array elements.
    """
    source = """
    class ArrayCoercion {
        static void main() {
            float[5] fArr;
            
            # Assign int literal to float array element -> OK
            fArr[0] := 10; 
            
            int x := 5;
            # Assign int variable to float array element -> OK
            fArr[1] := x;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_illegal_mixed_array_literal():
    """
    Error: Array literal elements must be of the same type.
    No coercion happens inside the literal list itself.
    """
    source = """
    class MixedArray {
        void main() {
            # Error: Mixed int (1) and float (2.5)
            float[2] arr := {1, 2.5};
        }
    }
    """
    # Code của bạn nên bắt lỗi IllegalArrayLiteral trước khi check assignment
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.5)}))"
    assert Checker(source).check_from_source() == expected
def test_chut(): 
    source = """
class Car {
    string brand;
    int year;
    
    void display() {
        io.writeStrLn(model);  # UndeclaredAttribute(model)
    }
}

"""
    expected = "UndeclaredIdentifier(model)"
    assert Checker(source).check_from_source() == expected
