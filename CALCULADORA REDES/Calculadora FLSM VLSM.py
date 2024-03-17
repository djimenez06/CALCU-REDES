import ipaddress

def calcular_flsm(direccion_ip, prefijo_red, num_subredes, hosts_por_subred):
    try:
        # Convertir la dirección IP y el prefijo de red a un objeto de red
        red = ipaddress.ip_network(f"{direccion_ip}/{prefijo_red}", strict=False)
        
        # Obtener la máscara de subred
        mascara = red.netmask
        
        # Calcular la cantidad de bits disponibles para hosts
        bits_para_hosts = 32 - prefijo_red
        
        # Calcular la cantidad de hosts disponibles por subred
        hosts_disponibles = 2 ** bits_para_hosts
        
        # Verificar si el número de hosts por subred es válido
        if hosts_por_subred < 2 or hosts_por_subred > hosts_disponibles - 2:
            raise ValueError("Número inválido de hosts por subred")
        
        # Calcular el número de bits necesarios para representar el número de subredes
        bits_para_subredes = num_subredes.bit_length()
        
        # Verificar si el número de subredes es válido
        if num_subredes > 2 ** (bits_para_hosts - 2):
            raise ValueError("Número inválido de subredes")
        
        # Obtener el prefijo de red para las subredes
        prefijo_subredes = prefijo_red + bits_para_subredes
        
        # Crear y mostrar las subredes
        print("Resultados de FLSM:")
        for i, subred in enumerate(ipaddress.ip_network(red).subnets(prefixlen_diff=bits_para_subredes)):
            primer_host = subred.network_address + 1
            ultimo_host = subred.broadcast_address - 1
            broadcast = subred.broadcast_address
            print(f"Subred {i + 1}:")
            print(f"Número Subred: {i + 1}")
            print(f"Nº de Hosts: {hosts_por_subred}")
            print(f"IP de red: {subred.network_address}")
            print(f"Máscara: {subred.netmask}")
            print(f"Primer Host: {primer_host}")
            print(f"Último Host: {ultimo_host}")
            print(f"Broadcast: {broadcast}")
            print()
    
    except ValueError as e:
        print(f"Error en FLSM: {e}")

def calcular_vlsm(ip, prefijo_red, num_subredes, num_host_por_subred):
    direccion_red = list(map(int, ip.split(".")))
    mascara_subred = prefijo_red
    parametros_subredes = []

    for i in range(num_subredes):
        bits_subred = 0
        while 2 ** bits_subred - 2 < num_host_por_subred[i]:
            bits_subred += 1
        
        # Cálculo de R
        R = (32 - prefijo_red) - bits_subred
        
        nuevo_prefijo_red = prefijo_red + R
        
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


# Solicitar al usuario que elija entre FLSM o VLSM
opcion = input("Seleccione 'FLSM' o 'VLSM' para calcular: ").upper()

if opcion == 'FLSM':
    # Solicitar datos al usuario para FLSM
    direccion_ip = input("Ingrese la dirección IP en formato CIDR (Ejemplo: 192.168.1.0/24): ")
    prefijo_red = int(input("Ingrese el prefijo de red (Ejemplo: 24): "))
    num_subredes = int(input("Ingrese el número de subredes: "))
    hosts_por_subred = int(input("Ingrese el número de hosts por subred: "))

    # Llamar a la función para calcular y mostrar las subredes FLSM
    calcular_flsm(direccion_ip, prefijo_red, num_subredes, hosts_por_subred)
elif opcion == 'VLSM':
    # Solicitar datos al usuario para VLSM
    ip = input("Ingrese la dirección IP: ")
    prefijo_red = int(input("Ingrese el prefijo de red: "))
    num_subredes = int(input("Ingrese el número de subredes: "))

    num_host_por_subred = []
    for i in range(num_subredes):
        num_host = int(input(f"Ingrese el número de hosts para la subred {i + 1}: "))
        num_host_por_subred.append(num_host)

    resultado = calcular_vlsm(ip, prefijo_red, num_subredes, num_host_por_subred)

    # Mostrar resultados VLSM
    print("\nResultados de VLSM:")
    for i, subred in enumerate(resultado):
        print(f"\nSubred {i + 1}:")
        for parametro, valor in subred.items():
            print(f"{parametro}: {valor}")
else:
    print("Opción no válida. Por favor, seleccione 'FLSM' o 'VLSM'.")
