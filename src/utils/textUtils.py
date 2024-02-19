import re

similarity_matrix =  {
        ('8', 'B'): 0.9,
        ('3', 'B'): 0.8,
        ('0', 'B'): 0.6,
    }

correspondence_matrix = {
        '8': 'B',
        'B': '8',

        'S': '5',
        '5': 'S',

        'O': '0',
        '0': 'O',

        'I': '1',
        '1': 'I',

        'T': '7',
        '7': 'T',

        'Z': '2',
        '2': 'Z',

        'G': '6',
        '6': 'G',
        
        'E': '3',
        '3': 'E',
    }


def string_simitality(string_list, plate_code):
    
    string_size = len(plate_code)
    score_list = []
    for code in string_list:
        simitality = 0
        for a, b in zip(plate_code, code):
            if (a, b) in similarity_matrix:
                simitality += similarity_matrix[(a, b)]
            elif(a == b):
                simitality += 1
            else:
                simitality += 0
        score_list.append(simitality/string_size)
        
    index, score_max = max(enumerate(score_list), key=lambda x: x[1])
    return score_max, string_list[index]


def replace_ocr_code(code):
    str_mask = 'AAA0100'
    output_code = '' 

    for character, mask  in zip(code, str_mask):
        if (character.isdigit() and mask == 'A') or (character.isalpha() and mask == '0'):
            output_code += correspondence_matrix.get(character, character)

        elif(character.isalpha() and mask == '1' and not('A' <= character <= 'J')):
            output_code += correspondence_matrix.get(character, character)

        else:
            output_code += character
    return output_code

def is_valid_license_plate(license_plate):
    try:
        license_plate_no_hyphen  = license_plate.replace("-", "")
        pattern = re.compile(
            r'^[A-Z]{3}\d{4}$'        # AAA0000
            r'|'                      # Ou
            r'^[A-Z]{3}\d[A-J]\d{2}$' # AAA0X00 (X pode ser A-J)
        )

        if pattern.match(license_plate_no_hyphen ) and len(license_plate_no_hyphen ) == 7:
            return True
        else:
            return False

    except Exception as e:
        print('Falha ao verificar string', e)
        return False

if __name__ == '__main__':
    seq = "AAA1284"
    lista_string=['AAA1234','HGF2D23','HFG2233','FFF1222', 'AAA12B4']
    similaridade_matriz = {
        ('8', 'B'): 0.9,
        ('3', 'B'): 0.8,
        ('0', 'B'): 0.6,
    }

    resultado = string_simitality(lista_string, seq, similaridade_matriz)
    print("Resultado:", resultado)