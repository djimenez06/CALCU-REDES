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
        print("Resultados:")
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
        print(f"Error: {e}")

# Solicitar datos al usuario
direccion_ip = input("Ingrese la dirección IP en formato CIDR (Ejemplo: 192.168.1.0/24): ")
prefijo_red = int(input("Ingrese el prefijo de red (Ejemplo: 24): "))
num_subredes = int(input("Ingrese el número de subredes: "))
hosts_por_subred = int(input("Ingrese el número de hosts por subred: "))

# Llamar a la función para calcular y mostrar las subredes
calcular_flsm(direccion_ip, prefijo_red, num_subredes, hosts_por_subred)
