def calcular_mascara_subred(prefijo_red, bits_subred):
    nuevo_prefijo_red = prefijo_red + bits_subred
    return nuevo_prefijo_red

def calcular_mascara_direccion_ip(bits_mascara):
    mascara = [0, 0, 0, 0]
    for i in range(4):
        if bits_mascara >= 8:
            mascara[i] = 255
            bits_mascara -= 8
        elif bits_mascara > 0:
            mascara[i] = 256 - 2**(8 - bits_mascara)
            bits_mascara = 0
    return ".".join(map(str, mascara))

def calcular_salto_red(mascara_subred):
    ultimo_octeto = 256 - mascara_subred
    return ultimo_octeto

def calcular_parametros_red(direccion_red, num_host_subred):
    primer_host = [x for x in direccion_red]
    primer_host[-1] += 1
    ultimo_host = [x for x in direccion_red]
    ultimo_host[-1] += num_host_subred + 1  # Sumar 1 más para obtener el último host
    direccion_broadcast = [x for x in ultimo_host]
    direccion_broadcast[-1] += 1
    siguiente_subred = [x for x in direccion_broadcast]
    siguiente_subred[-1] += 1
    return primer_host, ultimo_host, direccion_broadcast, siguiente_subred

def calcular_vlsm(ip, prefijo_red, num_subredes, num_host_por_subred):
    direccion_red = list(map(int, ip.split(".")))
    mascara_subred = prefijo_red
    salto_red = calcular_salto_red(mascara_subred)
    parametros_subredes = []

    for i in range(num_subredes):
        bits_subred = 0
        while 2 ** bits_subred - 2 < num_host_por_subred[i]:
            bits_subred += 1
        
        # Cálculo de R
        R = (32 - prefijo_red) - bits_subred
        
        nuevo_prefijo_red = calcular_mascara_subred(prefijo_red, R)
        
        primer_host, ultimo_host, direccion_broadcast, siguiente_subred = calcular_parametros_red(
            direccion_red.copy(), num_host_por_subred[i])
        parametros_subredes.append({
            "Direccion Red": ".".join(map(str, direccion_red)),
            "Mascara de Subred (Bits)": nuevo_prefijo_red,
            "Mascara de Subred": calcular_mascara_direccion_ip(nuevo_prefijo_red),
            "Primer Host": ".".join(map(str, primer_host)),
            "Ultimo Host": ".".join(map(str, ultimo_host)),
            "Direccion Broadcast": ".".join(map(str, direccion_broadcast)),
            "Siguiente Subred": ".".join(map(str, siguiente_subred))
        })
        direccion_red = siguiente_subred.copy()  # Usar la siguiente subred como inicio para la siguiente iteración

    return parametros_subredes

# Ejemplo de uso
ip = input("Ingrese la dirección IP: ")
prefijo_red = int(input("Ingrese el prefijo de red: "))
num_subredes = int(input("Ingrese el número de subredes: "))

num_host_por_subred = []
for i in range(num_subredes):
    num_host = int(input(f"Ingrese el número de hosts para la subred {i + 1}: "))
    num_host_por_subred.append(num_host)

resultado = calcular_vlsm(ip, prefijo_red, num_subredes, num_host_por_subred)

# Mostrar resultados
for i, subred in enumerate(resultado):
    print(f"\nSubred {i + 1}:")
    for parametro, valor in subred.items():
        print(f"{parametro}: {valor}")
