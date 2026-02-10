# Lexer - Tokenizes EPSTEIN code

import re
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Keywords
    TRUTH = auto()
    LIE = auto()
    ALIBI = auto()
    UNIVERSE = auto()

    # Control
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    LOOP = auto()
    PLOT = auto()
    PLAN = auto()
    SUICIDE = auto()
    ESCAPE = auto()

    # Built-in functions
    FILES = auto()
    RISK = auto()
    THEORY = auto()
    MONEY = auto()
    
    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    
    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    COMMENT = auto()


@dataclass
class Token: 
    """Represents a token in EPSTEIN code"""
    type: TokenType
    value: any
    line: int
    column: int

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line}, column={self.column})'
    
class Lexer:
    """Lexical analyzer for EPSTEIN code"""

    KEYWORDS = {
        'truth': TokenType.TRUTH,
        'lie': TokenType.LIE,
        'alibi': TokenType.ALIBI,
        'universe': TokenType.UNIVERSE,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'elif': TokenType.ELIF,
        'loop': TokenType.LOOP,
        'plot': TokenType.PLOT,
        'plan': TokenType.PLAN,
        'suicide': TokenType.SUICIDE,
        'escape': TokenType.ESCAPE,
        'files': TokenType.FILES,
        'risk': TokenType.RISK,
        'theory': TokenType.THEORY,
        'money': TokenType.MONEY,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }

    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]
    
    def error(self, msg: str):
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset"""
        pos = self.pos + offset
        if pos < len(self.code):
            return self.code[pos]
        return '\0'
    
    def advance(self) -> str:
        """Move to next character"""
        if self.pos < len(self.code):
            char = self.code[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return '\0'
    
    def skip_whitespace(self):
        """Skip spaces and tabs (but not newlines)"""
        while self.peek() in ' \t':
            self.advance()
    
    def skip_comment(self):
        """Skip comment until end of line"""
        while self.peek() != '\n' and self.peek() != '\0':
            self.advance()
    
    def read_string(self) -> str:
        """Read string literal"""
        quote = self.advance()  # " or '
        value = ""
        
        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                # Handle escape sequences
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                value += escape_map.get(next_char, next_char)
            else:
                value += self.advance()
        
        if self.peek() == '\0':
            self.error("Unterminated string")
        
        self.advance()  # Closing quote
        return value
    
    def read_number(self) -> float:
        """Read numeric literal"""
        num_str = ""
        has_dot = False
        
        while self.peek().isdigit() or self.peek() == '.':
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.advance()
        
        return float(num_str) if has_dot else int(num_str)
    
    def read_identifier(self) -> str:
        """Read identifier or keyword"""
        ident = ""
        
        while self.peek().isalnum() or self.peek() == '_':
            ident += self.advance()
        
        return ident
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        self.tokens = []
        
        # Handle initial indentation
        self.handle_indentation()
        
        while self.pos < len(self.code):
            self.skip_whitespace()
            
            # Check for end of input
            if self.peek() == '\0':
                break
            
            # Comment
            if self.peek() == '#':
                self.skip_comment()
                continue
            
            # Newline
            if self.peek() == '\n':
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                self.handle_indentation()
                continue
            
            # String
            if self.peek() in '"\'':
                value = self.read_string()
                token = Token(TokenType.STRING, value, self.line, self.column)
                self.tokens.append(token)
                continue
            
            # Number
            if self.peek().isdigit():
                value = self.read_number()
                token = Token(TokenType.NUMBER, value, self.line, self.column)
                self.tokens.append(token)
                continue
            
            # Identifier or keyword
            if self.peek().isalpha() or self.peek() == '_':
                ident = self.read_identifier()
                token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
                token = Token(token_type, ident, self.line, self.column)
                self.tokens.append(token)
                continue
            
            # Operators and delimiters
            char = self.peek()
            
            # Two-character operators
            if char == '=' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.EQUALS, '==', self.line, self.column))
                self.advance()
                self.advance()
            elif char == '!' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', self.line, self.column))
                self.advance()
                self.advance()
            elif char == '<' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.column))
                self.advance()
                self.advance()
            elif char == '>' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column))
                self.advance()
                self.advance()
            # Single-character operators
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.column))
                self.advance()
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, self.column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, self.column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, self.column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, self.column))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', self.line, self.column))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, '<', self.line, self.column))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, '>', self.line, self.column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, self.column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, self.column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self.advance()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, self.column))
                self.advance()
            else:
                self.error(f"Unexpected character: {char}")
        
        # Handle final dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, '', self.line, self.column))
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def handle_indentation(self):
        """Handle indentation at beginning of line"""
        indent = 0
        while self.peek() in ' \t':
            if self.peek() == ' ':
                indent += 1
            else:  # tab
                indent += 4
            self.advance()
        
        # Skip empty lines and comments
        if self.peek() in '\n#':
            return
        
        current_indent = self.indent_stack[-1]
        
        if indent > current_indent:
            self.indent_stack.append(indent)
            self.tokens.append(Token(TokenType.INDENT, '', self.line, self.column))
        elif indent < current_indent:
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT, '', self.line, self.column))
            
            if self.indent_stack[-1] != indent:
                self.error("Inconsistent indentation")
