# Parser - Epstein code programming

"""
EPSTEIN Language Parser - Builds Abstract Syntax Tree
"""

from __future__ import annotations
from typing import List, Any, Optional, Tuple
from dataclasses import dataclass
from python.lexer import Token, TokenType, Lexer


# AST Node definitions
@dataclass
class ASTNode:
    """Base class for AST nodes"""
    pass


@dataclass
class Program(ASTNode):
    """Root node - entire program"""
    statements: List[ASTNode]


@dataclass
class Assignment(ASTNode):
    """Variable assignment: x = value"""
    name: str
    value: ASTNode


@dataclass
class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    op: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """Unary operation: op value"""
    op: str
    operand: ASTNode


@dataclass
class Number(ASTNode):
    """Numeric literal"""
    value: float


@dataclass
class String(ASTNode):
    """String literal"""
    value: str


@dataclass
class Boolean(ASTNode):
    """Boolean literal"""
    value: bool


@dataclass
class Null(ASTNode):
    """Null value (alibi/universe)"""
    pass


@dataclass
class Identifier(ASTNode):
    """Variable reference"""
    name: str


@dataclass
class List(ASTNode):
    """List literal"""
    elements: List[ASTNode]


@dataclass
class Dict(ASTNode):
    """Dictionary literal"""
    pairs: List[Tuple[ASTNode, ASTNode]]


@dataclass
class FunctionCall(ASTNode):
    """Function call: func(args)"""
    name: str
    args: List[ASTNode]


@dataclass
class FunctionDef(ASTNode):
    """Function definition: plot/plan name(params): body"""
    name: str
    params: List[str]
    body: List[ASTNode]


@dataclass
class IfStatement(ASTNode):
    """If statement: if condition: body [else: else_body]"""
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class LoopStatement(ASTNode):
    """Loop statement: loop collection: body"""
    collection: ASTNode
    body: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    """Return statement: suicide [value]"""
    value: Optional[ASTNode] = None


@dataclass
class BreakStatement(ASTNode):
    """Break statement: escape"""
    pass


class Parser:
    """Parser for EPSTEIN language"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            raise SyntaxError(f"Line {token.line}, Column {token.column}: {msg}")
        raise SyntaxError(f"Unexpected end of input: {msg}")
    
    def peek(self, offset: int = 0) -> Token:
        """Peek at token at current position + offset"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        """Move to next token"""
        token = self.peek()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect specific token type"""
        token = self.advance()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return token
    
    def skip_newlines(self):
        """Skip any newline tokens"""
        while self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        """Parse entire program"""
        statements = []
        
        self.skip_newlines()
        
        while self.peek().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        self.skip_newlines()
        token = self.peek()
        
        # Function definition
        if token.type in (TokenType.PLOT, TokenType.PLAN):
            return self.parse_function_def()
        
        # If statement
        if token.type == TokenType.IF:
            return self.parse_if_statement()
        
        # Loop statement
        if token.type == TokenType.LOOP:
            return self.parse_loop()
        
        # Return statement
        if token.type == TokenType.SUICIDE:
            return self.parse_return()
        
        # Break statement
        if token.type == TokenType.ESCAPE:
            self.advance()
            self.skip_newlines()
            return BreakStatement()
        
        # Assignment or expression
        # Check for assignment: identifier/keyword = value
        if token.type == TokenType.IDENTIFIER or token.type in (TokenType.TRUTH, TokenType.LIE, TokenType.UNIVERSE, TokenType.ALIBI):
            # Look ahead for assignment
            if self.peek(1).type == TokenType.ASSIGN:
                return self.parse_assignment()
        
        # Expression statement (like function call)
        expr = self.parse_expression()
        self.skip_newlines()
        return expr
    
    def parse_function_def(self) -> FunctionDef:
        """Parse function definition: plot/plan name(): body"""
        self.advance()  # plot or plan
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        
        # Parse parameters (currently empty, can be extended)
        params = []
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)
        
        # Parse body
        body = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        if self.peek().type == TokenType.DEDENT:
            self.advance()
        
        return FunctionDef(name, params, body)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statement"""
        self.expect(TokenType.IF)
        
        condition = self.parse_expression()
        
        self.expect(TokenType.COLON)
        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)
        
        # Parse then body
        then_body = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        
        if self.peek().type == TokenType.DEDENT:
            self.advance()
        
        # Parse else clause
        else_body = None
        self.skip_newlines()
        
        if self.peek().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            self.expect(TokenType.NEWLINE)
            self.expect(TokenType.INDENT)
            
            else_body = []
            while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
            
            if self.peek().type == TokenType.DEDENT:
                self.advance()
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_loop(self) -> LoopStatement:
        """Parse loop statement: loop collection: body"""
        self.expect(TokenType.LOOP)
        
        collection = self.parse_expression()
        
        self.expect(TokenType.COLON)
        self.expect(TokenType.NEWLINE)
        self.expect(TokenType.INDENT)
        
        # Parse body
        body = []
        while self.peek().type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        if self.peek().type == TokenType.DEDENT:
            self.advance()
        
        return LoopStatement(collection, body)
    
    def parse_return(self) -> ReturnStatement:
        """Parse return statement: suicide [value]"""
        self.expect(TokenType.SUICIDE)
        
        value = None
        if self.peek().type not in (TokenType.NEWLINE, TokenType.EOF):
            value = self.parse_expression()
        
        self.skip_newlines()
        return ReturnStatement(value)
    
    def parse_assignment(self) -> Assignment:
        """Parse assignment: name = value"""
        name_token = self.peek()
        
        # Handle special case: truth = truth, lie = lie, universe = universe, etc.
        # The left side should be treated as identifier, right side as value
        if name_token.type in (TokenType.TRUTH, TokenType.LIE, TokenType.UNIVERSE, TokenType.ALIBI):
            name = name_token.value  # Get the string value
            self.advance()
        else:
            name_token = self.expect(TokenType.IDENTIFIER)
            name = name_token.value
        
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.skip_newlines()
        
        return Assignment(name, value)
    
    def parse_expression(self) -> ASTNode:
        """Parse expression"""
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        """Parse logical OR"""
        left = self.parse_and()
        
        while self.peek().type == TokenType.OR:
            self.advance()
            right = self.parse_and()
            left = BinaryOp('or', left, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """Parse logical AND"""
        left = self.parse_comparison()
        
        while self.peek().type == TokenType.AND:
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp('and', left, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison operators"""
        left = self.parse_additive()
        
        while self.peek().type in (TokenType.EQUALS, TokenType.NOT_EQUALS, 
                                    TokenType.LESS_THAN, TokenType.GREATER_THAN,
                                    TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op_token = self.advance()
            op = op_token.value
            right = self.parse_additive()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = op_token.value
            right = self.parse_multiplicative()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication, division, modulo"""
        left = self.parse_unary()
        
        while self.peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.advance()
            op = op_token.value
            right = self.parse_unary()
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary operators"""
        if self.peek().type in (TokenType.NOT, TokenType.MINUS):
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOp(op_token.value, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions"""
        token = self.peek()
        
        # Number
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        
        # String
        if token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        
        # Boolean - truth
        if token.type == TokenType.TRUTH:
            self.advance()
            return Boolean(True)
        
        # Boolean - lie
        if token.type == TokenType.LIE:
            self.advance()
            return Boolean(False)
        
        # Null - alibi/universe
        if token.type in (TokenType.ALIBI, TokenType.UNIVERSE):
            self.advance()
            return Null()
        
        # List literal
        if token.type == TokenType.LBRACKET:
            return self.parse_list()
        
        # Dict literal
        if token.type == TokenType.LBRACE:
            return self.parse_dict()
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Identifier or function call
        if token.type == TokenType.IDENTIFIER:
            name = self.advance().value
            
            # Function call
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call(name)
            
            # Variable reference
            return Identifier(name)
        
        # Built-in function call
        if token.type == TokenType.FILES:
            return self.parse_files_call()
        
        self.error(f"Unexpected token: {token.type.name}")
    
    def parse_list(self) -> List:
        """Parse list literal: [1, 2, 3]"""
        self.expect(TokenType.LBRACKET)
        
        elements = []
        
        while self.peek().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            
            if self.peek().type == TokenType.COMMA:
                self.advance()
            elif self.peek().type != TokenType.RBRACKET:
                self.error("Expected ',' or ']'")
        
        self.expect(TokenType.RBRACKET)
        return List(elements)
    
    def parse_dict(self) -> Dict:
        """Parse dict literal: {key: value}"""
        self.expect(TokenType.LBRACE)
        
        pairs = []
        
        while self.peek().type != TokenType.RBRACE:
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            
            if self.peek().type == TokenType.COMMA:
                self.advance()
            elif self.peek().type != TokenType.RBRACE:
                self.error("Expected ',' or '}'")
        
        self.expect(TokenType.RBRACE)
        return Dict(pairs)
    
    def parse_function_call(self, name: str) -> FunctionCall:
        """Parse function call: func(args)"""
        self.expect(TokenType.LPAREN)
        
        args = []
        
        while self.peek().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            
            if self.peek().type == TokenType.COMMA:
                self.advance()
            elif self.peek().type != TokenType.RPAREN:
                self.error("Expected ',' or ')'")
        
        self.expect(TokenType.RPAREN)
        return FunctionCall(name, args)
    
    def parse_files_call(self) -> FunctionCall:
        """Parse files (print) call - special syntax without parens"""
        self.expect(TokenType.FILES)
        
        args = []
        
        # Allow both files(x) and files x syntax
        if self.peek().type == TokenType.LPAREN:
            self.advance()
            
            while self.peek().type != TokenType.RPAREN:
                args.append(self.parse_expression())
                
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                elif self.peek().type != TokenType.RPAREN:
                    break
            
            if self.peek().type == TokenType.RPAREN:
                self.advance()
        else:
            # files x, y, z syntax
            while self.peek().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.COLON):
                args.append(self.parse_expression())
                
                if self.peek().type == TokenType.COMMA:
                    self.advance()
                else:
                    break
        
        return FunctionCall('files', args)
