import re

def is_valid_license_plate(license_plate):
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

placa1 = "ABC1234"
placa2 = "XYZ0A00"
placa3 = "1234ABC"
placa4 = "ABC12345"
placa5 = "DEF-5678"
placa6 = "ABC0X00"
placa7 = "ABCX00"
placa8 = "ABC12345"

print(verifica_placa(placa1))  # True
print(verifica_placa(placa2))  # True
print(verifica_placa(placa3))  # False
print(verifica_placa(placa4))  # False
print(verifica_placa(placa5))  # True
print(verifica_placa(placa6))  # True
print(verifica_placa(placa7))  # False (faltando um dígito antes do X)
print(verifica_placa(placa8))  # False (mais de 7 dígitos)