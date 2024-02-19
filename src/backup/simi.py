

def string_simitality(string_list, seq, similaridade_matriz):
    string_size = len(seq)
    score_list = []

    for code in string_list:
        simitality = 0
        for a, b in zip(seq, code):
            if (a, b) in similaridade_matriz:
                simitality += similaridade_matriz[(a, b)]
            elif(a == b):
                simitality += 1
            else:
                simitality += 0
        score_list.append(simitality/string_size)
        
    index, score_max = max(enumerate(score_list), key=lambda x: x[1])
   
    return score_max, string_list[index]



# Exemplo de uso
seq = "AAA1284"
lista_string=['AAA1234','HGF2D23','HFG2233','FFF1222', 'AAA12B4']
similaridade_matriz = {
    ('8', 'B'): 0.9,
    ('3', 'B'): 0.8,
    ('0', 'B'): 0.6,
}

resultado = string_simitality(lista_string, seq, similaridade_matriz)
print("Resultado:", resultado)