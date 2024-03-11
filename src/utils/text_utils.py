import re

similarity_matrix = {
    ('B', 'C'): 0.728,
    ('B', 'G'): 0.729,
    ('B', '0'): 0.725,
    ('B', '8'): 0.703,
    ('C', 'B'): 0.728,
    ('C', 'E'): 0.714,
    ('C', 'G'): 0.782,
    ('C', 'O'): 0.736,
    ('C', '0'): 0.717,
    ('D', '0'): 0.748,
    ('E', 'C'): 0.714,
    ('G', 'B'): 0.729,
    ('G', 'C'): 0.782,
    ('G', 'U'): 0.704,
    ('G', '0'): 0.712,
    ('H', 'M'): 0.715,
    ('H', 'U'): 0.766,
    ('I', 'T'): 0.738,
    ('I', '1'): 0.711,
    ('M', 'H'): 0.715,
    ('M', 'N'): 0.79,
    ('N', 'M'): 0.79,
    ('O', 'C'): 0.736,
    ('O', 'Q'): 0.767,
    ('O', '0'): 0.757,
    ('Q', 'O'): 0.767,
    ('Q', 'U'): 0.739,
    ('Q', '0'): 0.747,
    ('S', '8'): 0.706,
    ('T', 'I'): 0.738,
    ('U', 'G'): 0.704,
    ('U', 'H'): 0.766,
    ('U', 'Q'): 0.739,
    ('U', '0'): 0.726,
    ('0', 'B'): 0.725,
    ('0', 'C'): 0.717,
    ('0', 'D'): 0.748,
    ('0', 'G'): 0.712,
    ('0', 'O'): 0.757,
    ('0', 'Q'): 0.747,
    ('0', 'U'): 0.726,
    ('0', '5'): 0.712,
    ('1', 'I'): 0.711,
    ('5', '0'): 0.712,
    ('6', '8'): 0.715,
    ('8', 'B'): 0.703,
    ('8', 'S'): 0.706,
    ('8', '6'): 0.715
}

correspondence_matrix = {
    "8": "B",
    "B": "8",
    "S": "5",
    "5": "S",
    "O": "0",
    "0": "O",
    "I": "1",
    "1": "I",
    "T": "7",
    "7": "T",
    "Z": "2",
    "2": "Z",
    "G": "6",
    "6": "G",
    "E": "3",
    "3": "E",
    "A": "4",
    "4": "A"
}


def string_simitality(string_list, plate_code):

    string_size = len(plate_code)
    score_list = []
    for code in string_list:
        simitality = 0
        for a, b in zip(plate_code, code):
            if (a, b) in similarity_matrix:
                simitality += similarity_matrix[(a, b)]
            elif a == b:
                simitality += 1
            else:
                simitality += 0
        score_list.append(simitality / string_size)

    index, score_max = max(enumerate(score_list), key=lambda x: x[1])
    return score_max, string_list[index]


def replace_ocr_code(code):
    str_mask = "AAA0100"
    output_code = ""

    for character, mask in zip(code, str_mask):
        if (character.isdigit() and mask == "A") or (
            character.isalpha() and mask == "0"
        ):
            output_code += correspondence_matrix.get(character, character)

        elif character.isalpha() and mask == "1" and not ("A" <= character <= "J"):
            output_code += correspondence_matrix.get(character, character)

        else:
            output_code += character
    return output_code


def is_valid_license_plate(license_plate):
    try:
        license_plate_no_hyphen = license_plate.replace("-", "")
        pattern = re.compile(
            r"^[A-Z]{3}\d{4}$"  # AAA0000
            r"|"  # Ou
            r"^[A-Z]{3}\d[A-J]\d{2}$"  # AAA0X00 (X pode ser A-J)
        )

        if pattern.match(license_plate_no_hyphen) and len(license_plate_no_hyphen) == 7:
            return True
        else:
            return False

    except Exception as e:
        print("Falha ao verificar string", e)
        return False


if __name__ == "__main__":
    seq = "AAA1284"
    lista_string = ["AAA1234", "HGF2D23", "HFG2233", "FFF1222", "AAA12B4"]
    similaridade_matriz = {
        ("8", "B"): 0.9,
        ("3", "B"): 0.8,
        ("0", "B"): 0.6,
    }

    resultado = string_simitality(lista_string, seq, similaridade_matriz)
    print("Resultado:", resultado)
