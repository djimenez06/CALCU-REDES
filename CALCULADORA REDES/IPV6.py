def calcular_ipv6():
    direccion_ip = input("Dirección de IP (formato hexadecimal): ")
    cantidad_subredes = int(input("Cantidad de subredes a crear: "))

    # Convertir la dirección IP en una lista de cuartetos
    direccion_ip_lista = direccion_ip.split(':')

    for subred in range(cantidad_subredes):
        cantidad_host_por_subred = int(input(f"Cantidad de hosts para la Subred {subred+1}: "))

        # Calcular el nuevo prefijo de red
        nuevo_prefijo_red = 128 - cantidad_host_por_subred.bit_length()

        # Mostrar el nuevo prefijo de red
        print("\nSubred", subred+1, ":")
        print("Nuevo prefijo de Red: /{}".format(nuevo_prefijo_red))

        # Calcular y mostrar las direcciones IP
        ultimo_digito = direccion_ip_lista[3]  # Cuarto cuarteto (ID de subred)
        subred_hex = hex(subred)[2:].zfill(4)  # Convertir número de subred a hexadecimal
        nueva_direccion_ip = direccion_ip_lista[:3] + [subred_hex] + ['0000'] + ['0000'] + ['0000']  # Nueva dirección de subred
        for i in range(cantidad_host_por_subred):
            nuevo_digito = format(int(ultimo_digito, 16) + i, 'x').zfill(4)
            nueva_direccion = nueva_direccion_ip[:] + [nuevo_digito]
            nueva_direccion = ':'.join(nueva_direccion)
            print(nueva_direccion, "- Host", i+1)


calcular_ipv6()
