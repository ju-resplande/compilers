import string

class AFD():
    def _set_input(char: str) -> str:
        if char in string.digits:
            return 'D'
        elif char in string.ascii_letters:
            return 'L'
        elif char == '.':
            return '\.'
        elif char in _alphabet:
            return char
        else:
            return 'ERRO'

    def run(self, char: str, state: int):
        char_input = self._set_input(char)
        if char_input == 'ERRO':
            return char_input
        elif char_input in self._transitions[state]:
            return self._transitions[state]   

    _alphabet = {
        'D',
        '\.',
        'L',
        'e',
        'E',
        '+',
        '-',
        '_',
        '$',
        '<',
        '>',
        '=',
        '*',
        '/',
        ')',
        '(',
        '{',
        '}',
        ';',
        ',',
        ' ',
        '\t',
        '\n',
    }

    token_classes = {
        2: 'RCB',
        3: 'OPR',
        5: 'id',
        6: 'NUM',
        7: 'NUM',
        10: 'Num',
        12: 'comentário',
        14: 'lit',
        16: 'OPM',
        17: 'AB_P',
        18: 'FC_P',
        19: 'PT_V',
        20: 'Vir',
        21: 'EOF',
    }

    _transitions = {
    0 : {
        '<': 1,
        '=': 3,
        '>': 4,
        'L': 5,
        'D': 6,
        '{': 11,
        '"': 13,
        '+': 16,
        '-': 16,
        '*': 16,
        '/': 16,
        '(': 17,
        ')': 18,
        ';': 19,
        ',': 20,
        '$': 21,
    },
    1: {
        '-': 2,
        '=': 3,
    },
    4: {
        '=': 3,
    },
    5: {
        'L': 5,
        'D': 5,
        '_': 5,
    },
    6: {
        'D': 6,
        '\.': 7,
        'e': 8,
        'E': 8,
    },
    7: {
        'D': 7,
        'e': 8,
        'E': 8,
    },
    8: {
        '+': 9,
        '-': 9,
        'D': 10,
    },
    9: {
        'D': 10,
    },
    10: {
        'D': 10,
    },
    11: {
        '}': 12,
        '{': 11,
        'D': 11,
        '\.': 11,
        'L': 11,
        'e': 11,
        'E': 11,
        '+': 11,
        '-': 11,
        '_': 11,
        '$': 11,
        '<': 11,
        '>': 11,
        '=': 11,
        '*': 11,
        '/': 11,
        ')': 11,
        '(': 11,
        ';': 11,
        ',': 11,
        '"': 11,
        ' ': 11,
        '\t': 11,
        '\n': 11,
    },
    13: {
        '"': 14,
        '}': 13,
        '{': 13,
        'D': 13,
        '\.': 13,
        'L': 13,
        'e': 13,
        'E': 13,
        '+': 13,
        '-': 13,
        '_': 13,
        '$': 13,
        '<': 13,
        '>': 13,
        '=': 13,
        '*': 13,
        '/': 13,
        ')': 13,
        '(': 13,
        ';': 13,
        ',': 13,
        ' ': 13,
        '\t': 13,
        '\n': 13,
    },
}
