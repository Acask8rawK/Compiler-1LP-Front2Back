import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        # Prioritas Regex sangat penting! (Keyword duluan sebelum ID)
        self.token_specs = [
            ('PRINT',  r'print'),           # Keyword
            ('ASSIGN', r':='),              # Operator
            ('ID',     r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identifier
            ('NUM',    r'\d+'),             # Angka
            ('PLUS',   r'\+'),              # +
            ('MINUS',  r'-'),               # -
            ('TIMES',  r'\*'),              # * (x diganti * di program)
            ('DIVIDE', r'/'),               # /
            ('LPAREN', r'\('),              # (
            ('RPAREN', r'\)'),              # )
            ('SEMI',   r';'),               # ;
            ('COMMA',  r','),               # ,
            ('WS',     r'\s+'),             # Spasi/Enter (Skip)
            ('MISMATCH', r'.'),             # Error karakter aneh
        ]
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        combined_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs)
        
        for match in re.finditer(combined_regex, self.text):
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'WS':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Karakter ilegal ditemukan: '{value}'")
            else:
                if kind == 'NUM':
                    value = int(value)
                tokens.append(Token(kind, value))
        
        tokens.append(Token('EOF', None))
        return tokens