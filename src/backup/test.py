
def corrigir_ocr(input_str):

    matriz_correspondencia = {
        '8': 'B',
        'B': '8',

        'S': '5',
        '5': 'S',

        'O': '0',
        '0': 'O',

        'I': '1',
        '1': 'I',
    }

    str_mascara = 'AAA0100'
    output_str = '' 

    for caracter, mascara  in zip(input_str, str_mascara):
        if (caracter.isdigit() and mascara == 'A') or (caracter.isalpha() and mascara == '0'):
            output_str += matriz_correspondencia.get(caracter, caracter)

        elif(caracter.isalpha() and mascara == '1' and not('A' <= caracter <= 'J')):
            output_str += matriz_correspondencia.get(caracter, caracter)

        else:
            output_str += caracter
    return output_str

if __name__ == '__main__':
    string_ocr = "BRA20I2"
    string_corrigida = corrigir_ocr(string_ocr)
    print("String original:", string_ocr)
    print("String corrigida:", string_corrigida)
