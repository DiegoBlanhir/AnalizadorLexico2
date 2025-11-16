import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linea = 1
        self.patrones = [
            ('KEYWORD', r'\b(if|while|for|return|int|float|else|char|void)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\d+(\.\d+)?'),
            ('OPERATOR', r'(\+|\-|\*|\/|=|==|!=|>|<|>=|<=)'),
            ('DELIMITER', r'[;,\(\)\{\}]'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n'),
            ('ERROR', r'.'),
        ]

    def tokenizar(self):
        tokens = []
        while self.pos < len(self.codigo):
            encontrado = False
            for tipo, patron in self.patrones:
                regex = re.compile(patron)
                match = regex.match(self.codigo, self.pos)

                if match:
                    valor = match.group(0)

                    if tipo == 'NEWLINE':
                        self.linea += 1
                    elif tipo not in ['WHITESPACE', 'NEWLINE']:
                        tokens.append(Token(tipo, valor, self.linea))

                    self.pos = match.end()
                    encontrado = True
                    break

            if not encontrado:
                self.pos += 1

        return tokens

def leer_archivo(ruta):
    try:
        with open(ruta, 'r') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print("❌ Error: Archivo no encontrado.")
        return None

def generar_tabla(tokens, salida="tabla_simbolos.txt"):
    with open(salida, 'w') as file:
        file.write("Renglon\tToken\tLexema\tCategoria\n")
        for token in tokens:
            file.write(f"{token.linea}\t{token.valor}\t{token.tipo}\t{categoria(token.tipo)}\n")

    print(f"\n✅ Tabla de símbolos generada en: {salida}")


def categoria(tipo):
    if tipo == "KEYWORD": return "PALABRA_RESERVADA"
    if tipo == "IDENTIFIER": return "IDENTIFICADOR"
    if tipo == "NUMBER": return "NUMERO"
    if tipo == "OPERATOR": return "OPERADOR"
    if tipo == "DELIMITER": return "DELIMITADOR"
    if tipo == "ERROR": return "ERROR"
    return "DESCONOCIDO"

print("=" * 50)
print("LECTURA DE ARCHIVO Y TABLA DE TOKENS")
print("=" * 50)

ruta = "correos.txt"

contenido = leer_archivo(ruta)

if contenido:
    lexer = AnalizadorLexico(contenido)
    tokens = lexer.tokenizar()

    print("\nTokens generados:")
    for t in tokens:
        print(f"Línea: {t.linea}\tToken: {t.tipo}\tLexema: {t.valor}")

    generar_tabla(tokens)