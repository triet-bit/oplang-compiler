grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: decllist EOF; // write for program rule here using vardecl and funcdecl
//////////////////////////////////////////////////////////
// PARSER RULES
//////////////////////////////////////////////////////////
decllist: decl decllist | ; 
decl: classdecl | vardecl ; //here
////////////////////
// CLASS DECLARATION
////////////////////
classdecl: CLASS ID (EXTENDS ID)? memberdecl; 
memberdecl: L_CURL memberlist R_CURL; 
memberlist: member memberlist| ; 
member: attributedecl | methoddecl | constructordecl | destructordecl; 
////////////////////
// ATTRIBUTE
////////////////////
attributedecl: static_atom final_atom decl_type2 attributelist SEMI
            | final_atom static_atom decl_type2 attributelist SEMI;
static_atom: STATIC |; 
final_atom: FINAL |;  
ampersand_atom: AMPERSAND |; 
attributelist: attributeprime COMMA attributelist | attributeprime; 
attributeprime:  ID | ID ASSIGN expr; 
////////////////////
// METHOD
////////////////////
methoddecl: static_atom return_type_method ID paramdecl blockstmt_method;    
return_type_method : return_type ampersand_atom; 

////////////////////
// VARIABLE DECLARATION, this is using for blockstmt
////////////////////
vardecllist: vardecl vardecllist|;
vardecl: (FINAL)? decl_type ampersand_atom varlist SEMI;
// sua cho nay
////////////////////
// PARAMETERS
////////////////////
paramdecl: L_PAREN paramlist R_PAREN; 
paramlist: paramprime |; 
paramprime: param SEMI paramprime| param; 
param: decl_type2 ampersand_atom idlist; 
////////////////////
// CONSTRUCTOR & DESTRUCTOR
////////////////////
constructordecl: default_contructor | copy_contructor | userdef_contructor; 
default_contructor: ID L_PAREN R_PAREN blockstmt;  
copy_contructor: ID L_PAREN ID ID R_PAREN blockstmt; 
userdef_contructor: ID paramdecl blockstmt; 
destructordecl: destructor; 
destructor: TILDE ID L_PAREN R_PAREN blockstmt; 
////////////////////
// BLOCK STATEMENT
////////////////////
blockstmt: L_CURL vardecllist stmtlist R_CURL; 
blockstmt_method: L_CURL vardecllist stmtlist R_CURL; 


//vardeclstmt:  decl_type2 idlist SEMI
//             | decl_type2 idlist ASSIGN expr SEMI
//             | decl_type2 assignlist SEMI; 
vardeclstmt: decl_type2 varlist SEMI;
varlist: varitem COMMA varlist | varitem;
varitem: ID | ID ASSIGN expr;
assignlist: ID ASSIGN expr COMMA assignlist| ID ASSIGN expr; 
////////////////////
// STATEMENTS
////////////////////
stmtlist: stmt stmtlist |; 
stmt
    : blockstmt                      // { ... }
    | ifstmt                         // if ... then ... (else ...)
    | forstmt                        // nested for
    | breakstmt                      // break;
    | continuestmt
    | assignstmt               // ID := ... ;
    | vardeclstmt
    | ID L_PAREN expr R_PAREN SEMI
    | returnstmt
    | expr SEMI                      // expression statement, ví dụ function call ;
    | SEMI                           // empty statement allowed
    ;
//funct_call
funct_call: ID L_PAREN exprlist R_PAREN SEMI; 
functparam: functprime |; 
functprime: literal COLON functprime | literal; 

//if statement
ifstmt: IF expr THEN stmt (ELSE stmt)?; 

//for statement
forstmt: FOR ID ASSIGN expr (TO | DOWNTO) expr DO stmt;

//break continue return stmt
breakstmt: BREAK SEMI; 
continuestmt: CONTINUE SEMI; 
returnstmt: RETURN ID SEMI | RETURN SEMI | RETURN expr SEMI; 
////////////////////
// ASSIGNMENT
////////////////////
assigndecl: assignstmt assigndecl | assignstmt; 
assignstmt: lhs ASSIGN expr SEMI; 
lhs: ID                              // biến thường
   | expr                  // arr[0], obj.field[2], ...
   | THIS DOT ID;                    // this.x
////////////////////
// EXPRESSIONS
////////////////////
expr : relexpr; 
relexpr: equalexpr (GREATER|GREATER_EQ|LESS|LESS_EQ) equalexpr|equalexpr; 
equalexpr: logicexpr (EQ|NOT_EQ) logicexpr | logicexpr; 
logicexpr: logicexpr (LOGIC_AND| LOGIC_OR) addsubexpr | addsubexpr; 
addsubexpr: addsubexpr (ADD|SUB) muldivexpr | muldivexpr; 
muldivexpr: muldivexpr (MUL|FLT_DIV|INT_DIV|MOD) expoexpr | expoexpr; 
expoexpr: expoexpr CONCAT notexpr | notexpr; 
notexpr: (LOGIC_NOT) notexpr | unaryexpr; 
unaryexpr: (ADD|SUB) unaryexpr | indexingexpr; 
//indexingexpr: indexingexpr L_SQUARE expr R_SQUARE | dotexpr; 
indexingexpr: indexingexpr L_SQUARE expr R_SQUARE dotchain | indexingexpr L_SQUARE expr R_SQUARE | dotexpr;
dotexpr: primaryexpr dotchain                                       
       | primaryexpr;
primaryexpr: literal
           | ID                                           
           | THIS                                           
           | NEW ID L_PAREN exprlist R_PAREN               
           | L_PAREN expr R_PAREN                      
           | NIL
           | ID L_PAREN exprlist R_PAREN
           | ID L_SQUARE INT_LIT R_SQUARE
           ;
exprlist: exprprime | ; 
exprprime: expr COMMA exprprime | expr; 
dotchain
    : DOT ID L_PAREN exprlist R_PAREN dotchain   // method call chaining
    | DOT ID dotchain                            // field access chaining 
    |
    ;
////////////////////
// LITERALS & ARRAYS
////////////////////
literal: INT_LIT | FLT_LIT | TRUE | FALSE | STR_LIT | array_lit; 
array_lit: L_CURL arraylist R_CURL; 
arraylist: arrayprime | ; 
arrayprime: array_element COMMA arrayprime | array_element; 
//array_element: TRUE | FALSE | INT_LIT | FLT_LIT | STR_LIT; 
array_element: expr; 
idlist: ID COMMA idlist | ID; 
////////////////////
// TYPES
////////////////////
primitive_type: BOOL | INT | STR | FLOAT; 
return_type:  ( primitive_type ampersand_atom) | VOID | array_type ampersand_atom | (ID ampersand_atom) ; 
array_type: (primitive_type|ID) L_SQUARE INT_LIT R_SQUARE ; // cos theer cos class
decl_type: primitive_type | array_type | ID; //ID for class, not have void type
decl_type2: ( primitive_type ampersand_atom) | (array_type ampersand_atom )| (ID ampersand_atom) |;
//////////////////////////////////////////////////////////
// LEXER RULES
//////////////////////////////////////////////////////////

//keyword 
BOOL: 'boolean'; 
BREAK: 'break'; 
CLASS: 'class'; 
CONTINUE: 'continue'; 
DO: 'do'; 
ELSE: 'else'; 
EXTENDS: 'extends'; 
FLOAT: 'float'; 
IF: 'if'; 
INT: 'int'; 
NEW: 'new'; 
STR: 'string'; 
THEN: 'then'; 
FOR: 'for'; 
RETURN: 'return'; 
TRUE: 'true'; 
FALSE: 'false'; 
VOID: 'void'; 
NIL: 'nil'; 
THIS: 'this'; 
FINAL: 'final'; 
STATIC: 'static'; 
TO: 'to'; 
DOWNTO: 'downto'; 


//operator
ADD: '+'; 
SUB: '-'; 
MUL: '*'; 
FLT_DIV: '/'; //check this
INT_DIV: '\\'; 
MOD: '%'; 
NOT_EQ: '!=';  
EQ: '=='; 
LESS: '<'; 
GREATER: '>'; 
LESS_EQ: '<='; 
GREATER_EQ: '>='; 
LOGIC_OR: '||'; 
LOGIC_AND: '&&'; 
LOGIC_NOT: '!'; 
CONCAT: '^'; 
ASSIGN: ':=';



//Seperator
L_SQUARE: '['; 
R_SQUARE: ']'; 
L_PAREN: '('; 
R_PAREN: ')'; 
L_CURL: '{'; 
R_CURL: '}'; 
SEMI: ';'; 
COLON: ':'; 
DOT: '.'; 
COMMA: ','; 


//Special
TILDE: '~'; 
AMPERSAND: '&'; 

//Comment
LINECMT: '#' ~[\n\r]* -> skip; 
BLOCKCMT: '/*' .*? '*/' -> skip;    // non-gready -> meet the first next */ and stop

//Literal
INT_LIT: [0-9]+;
FLT_LIT: INT_PART (DEC_PART|EXP_PART) 
        | INT_PART DEC_PART EXP_PART
        ; 
fragment INT_PART: [0-9]+; 
fragment DEC_PART: '.' [0-9]*; 
fragment EXP_PART: ('E'|'e') ('+'|'-')? [0-9]+;


fragment ESC: '\\' [btnfr"\\];  // \b, \t, \n, \f, \r, \", \\
ILLEGAL_ESCAPE: '"' (~["\\] | '\\' [tnrfb"\\])* '\\' ~[tnrfb"\\] {self.text = self.text[1:]}; 

UNCLOSE_STRING: '"' (~["\\] | '\\' [tnrfb"\\])* EOF  {self.text = self.text[1:]}; 

STR_LIT : '"' ( ~["\\] | '\\' [bfrnt"\\] )* '"' {self.text = self.text[1:-1]}; 
//Identifier
ID: [a-zA-Z_][a-zA-Z0-9_]*; 


WS : [ \t\r\n\f\u00A0]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: .;