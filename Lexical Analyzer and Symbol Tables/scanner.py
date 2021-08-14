from symbol_table import SymbolTable
from token import (
    RESERVED_WORDS,
    Token,
)
from afd import AFD

class Scanner:
    def __init__(self):
        self.afd = AFD
        self.symb_table = SymbolTable(tokens=RESERVED_WORDS)
        self.cur_state = 0
        self.cur_lexeme = ''
        

    # TODO: conectar e rastrear o erro
    def _error(error_num: int):
        err_msg = f"ERRO{error_num} – Caractere inválido na linguagem, linha 2, coluna 1"
        print(err_msg)

        
        

    def scan(text: str):
        for char in text:
            state = self.afd.run(char, state)
            token_class = self.afd.token_classes.get(state)
            
            # TODO: pegar palavra reservada
            # TODO: checar classe e tipos


            if token_class != None or final_class == 'EOF':
                if token_class == 'NUM':
                    token_type = 'real' if '.' in lexeme else 'inteiro'
                    token = Token(lexema=lexeme, classe=token_class, tipo=token_type)
                elif token_class == 'lit':
                    token_type = 'lit'
                    token = Token(lexema=lexeme, classe=token_class, tipo=token_type)
                elif token_class == 'id':
                    token = self.symb_table.find(lexeme)

                    if token == None:
                        token = Token(lexema=lexeme, classe=token_class, tipo=token_type)
                        self.symb_table.insert(token)
                else:
                    token_type = 'NULO'
                    token = Token(lexema=lexeme, classe=token_class, tipo=token_type)

                return token

                cur_lexeme = '' # TODO: arrumar
            
            
            lexeme = lexeme + char
            prev_final_class = final_class