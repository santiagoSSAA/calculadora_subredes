# INGRESA AQUÍ TUS EQUIPOS

IP_DIRECTION = "56.204.24.108/16"

GROUPS = {
    "A":160,
    "B":600,
    "C":520,
    "V10":760,
    "V20":140
}

def decimalToBinary(n):
    n = int(n)
    if n > 255:
        return EOFError
    binary_number = str(bin(n).replace("0b", ""))
    while (len(binary_number)) < 8:
        binary_number = "0{}".format(binary_number)
    return binary_number

def dirToBinary(ip):
    binary_numbers = []
    for i in range(len(ip)):
        binary_numbers.append(decimalToBinary(ip[i]))
    return binary_numbers

def binToDecimal(n):
    n = [i for i in n]
    value = 0
    for i in range(len(n)):
        digit = n.pop()
        if digit == '1':
            value = value + pow(2, i)
    return value

def calculateN(devices):
    n = 0
    while ((2**n)-2) < devices:
        n +=1
    return n

def binAdd(*args): return bin(sum(int(x, 2) for x in args))

def subtractionBinary(s1, s2): return bin(int(s1, 2) - int(s2, 2))

if __name__ == "__main__":
    print("dirección ingresada: ", IP_DIRECTION)
    groups = GROUPS
    # 1. Recibir la dirección del usuario, y determinar si es de host
    # o de red.
    input_dir = IP_DIRECTION.split("/")
    input_ip = input_dir[0].split(".")
    bin_input_ip = "".join(dirToBinary(input_ip))
    is_host = False
    for i in range(int(input_dir[1]), len(bin_input_ip)):
        if int(bin_input_ip[i]) == 1:
            is_host=True
    # Si es host, se cuentan los bits en base al numero de la dirección 
    # de subred y a partir de la siguiente posición, convertir todos a 
    # ceros (0).
    if is_host:
        bin_input_ip = [i for i in bin_input_ip]
        for i in range(int(input_dir[1]), len(bin_input_ip)):
            bin_input_ip[i] = "0"
        bin_input_ip = [
            "".join(bin_input_ip)[i:i+8] for i in range(
                0, len("".join(bin_input_ip)), 8)]
        input_ip = [binToDecimal(i) for i in bin_input_ip]
    # 2. Ordenar los grupos de equipos, de mayor a menor (en base al
    # numero de equipos de cada grupo).
    print("tipo de dirección: {}\n".format("host" if is_host else "red"))
    groups = {k: v for k, v in sorted(
        groups.items(), key=lambda item: item[1], reverse=True)}
    universal_ip = input_ip
    for key,value in groups.items():
        if list(groups).index(key) == 0:
            # 3. Tomamos el primer grupo de equipos, y utilizamos la 
            # fórmula (2^N-2 >= No. equipos en el grupo), donde N es el 
            # número de bits prestados (vamos calculando N a pulso, hasta 
            # topar con un valor que satisfaga la desigualdad). N tiene 
            # que ser el número más pequeño tal que se cumpla la 
            # desigualdad.
            n = calculateN(value)
            # 4. Calculamos la nueva máscara de subred para el primer 
            # grupo de equipos, con la fórmula (máscara = 32 - N).
            subnet_mask = 32-n
            # 5. La nueva dirección de red para el primer grupo de 
            # equipos, será la dirección de red original, pero con la 
            # nueva máscara de subred calculada.
            ip = universal_ip
            # 6. Calculamos la dirección de broadcast del primer grupo de 
            # equipos, para esto convertimos la dirección a binario, 
            # contamos de derecha a izquierda N bits (N = 32 - máscara 
            # de subred), y los convertimos todos a uno (1). Después 
            # convertimos la dirección resultante a decimal, y como 
            # resultado, tendremos la dirección de broadcast.
            broadcast_ip = ip
            bin_broadcast_ip = "".join(dirToBinary(broadcast_ip))
            bin_broadcast_ip = bin_broadcast_ip[
                :len(bin_broadcast_ip)-n] + ("1"*n)
            bin_broadcast_ip = [
            "".join(bin_broadcast_ip)[i:i+8] for i in range(
                0, len("".join(bin_broadcast_ip)), 8)]
            broadcast_ip = [binToDecimal(i) for i in bin_broadcast_ip]
            # 7. Calculamos la primera dirección del primer grupo de 
            # equipos, para esto, tomamos la dirección de red, la 
            # convertimos a binario, le sumamos 1 bit, y la devolvemos 
            # a decimal, y así tendremos la primera dirección.
            first_ip_dir = "".join(dirToBinary(ip))
            first_ip_dir = binAdd(first_ip_dir, "1")
            first_ip_dir = [
            "".join(first_ip_dir)[i:i+8] for i in range(
                0, len("".join(first_ip_dir)), 8)]
            first_ip_dir = [binToDecimal(i) for i in first_ip_dir]
            # 8. Calculamos la última dirección del primer grupo de 
            # equipos, para esto, tomamos la dirección de broadcast, la 
            # convertimos a binario, le restamos 1 bit, y la devolvemos 
            # a decimal, y así tendremos la última dirección.
            last_ip_dir = "".join(dirToBinary(broadcast_ip))
            last_ip_dir = subtractionBinary(last_ip_dir, "1")
            last_ip_dir = [
            "".join(last_ip_dir)[i:i+8] for i in range(
                0, len("".join(last_ip_dir)), 8)]
            last_ip_dir = [binToDecimal(i) for i in last_ip_dir]
            # 9. Calculamos la dirección de la máscara de subred del 
            # primer grupo de equipos, para esto, tomamos el número 
            # decimal que representa la máscara (M), creamos una cadena 
            # de 32 bits en cero (0), y de izquierda a derecha, vamos 
            # convirtiendo (M) bits en unos (1). Luego devolvemos la 
            # cadena de bits resultante a decimal, y así tendremos la 
            # máscara de subred del primer grupo de equipos.
            binary_subnet_mask = ["1" for i in ("i"*32)]
            for i in range(subnet_mask, len(binary_subnet_mask)):
                binary_subnet_mask[i] = "0"
            binary_subnet_mask = "".join(binary_subnet_mask)
            binary_subnet_mask = [
            "".join(binary_subnet_mask)[i:i+8] for i in range(
                0, len("".join(binary_subnet_mask)), 8)]
            ip_subnet_mask = [binToDecimal(i) for i in binary_subnet_mask]
            print("GRUPO {}\n".format(key))
            if is_host:
                print("dirección de red base: ",".".join(
                    map(str,ip)),"/{}".format(input_dir[1]))
            print("No. de equipos: ", value)
            print("N: ",n)
            print("dirección de red: ", ".".join(
                map(str,ip)),"/{}".format(subnet_mask))
            print("mascara de subred: ", ".".join(map(str,ip_subnet_mask)))
            print("dirección de broadcast: ", ".".join(
                map(str,broadcast_ip)),"/{}".format(subnet_mask))
            print("primera dirección: ", ".".join(map(str,first_ip_dir)))
            print("última dirección: ", ".".join(map(str,last_ip_dir)))
            print("----------------------------------------------\n")
            universal_ip = ip
        else:
            # 10. Para el siguiente grupo de equipos, tomamos la 
            # dirección de red del primer grupo, contamos de izquierda 
            # a derecha J (donde J = máscara de subred del primer grupo 
            # de equipos), y al bit número J, le sumamos 1 bit.
            ip = universal_ip
            binary_ip = "".join(dirToBinary(ip))
            binary_ip = binary_ip[:subnet_mask]
            binary_ip = binAdd(binary_ip,"1")
            binary_ip = binary_ip + ("0"*(32-subnet_mask))
            binary_ip = [
            "".join(binary_ip)[i:i+8] for i in range(
                0, len("".join(binary_ip)), 8)]
            ip = [binToDecimal(i) for i in binary_ip]
            # 11. Tomamos el nuevo grupo de equipos, y volvemos a 
            # calcular la fórmula (2^N-2).
            n = calculateN(value)
            # 12. Hacemos el mismo proceso que con el primer grupo, para 
            # calcular la nueva máscara de subred (tenemos en cuenta que 
            # nuestra nueva dirección de red es la calculada en el paso 
            # 10).
            subnet_mask = 32-n
            # broadcast ip
            broadcast_ip = ip
            bin_broadcast_ip = "".join(dirToBinary(broadcast_ip))
            bin_broadcast_ip = bin_broadcast_ip[
                :len(bin_broadcast_ip)-n] + ("1"*n)
            bin_broadcast_ip = [
            "".join(bin_broadcast_ip)[i:i+8] for i in range(
                0, len("".join(bin_broadcast_ip)), 8)]
            broadcast_ip = [binToDecimal(i) for i in bin_broadcast_ip]
            # first ip
            first_ip_dir = "".join(dirToBinary(ip))
            first_ip_dir = binAdd(first_ip_dir, "1")
            first_ip_dir = [
            "".join(first_ip_dir)[i:i+8] for i in range(
                0, len("".join(first_ip_dir)), 8)]
            first_ip_dir = [binToDecimal(i) for i in first_ip_dir]
            # last ip
            last_ip_dir = "".join(dirToBinary(broadcast_ip))
            last_ip_dir = subtractionBinary(last_ip_dir, "1")
            last_ip_dir = [
            "".join(last_ip_dir)[i:i+8] for i in range(
                0, len("".join(last_ip_dir)), 8)]
            last_ip_dir = [binToDecimal(i) for i in last_ip_dir]
            # subnet mask
            binary_subnet_mask = ["1" for i in ("i"*32)]
            for i in range(subnet_mask, len(binary_subnet_mask)):
                binary_subnet_mask[i] = "0"
            binary_subnet_mask = "".join(binary_subnet_mask)
            binary_subnet_mask = [
            "".join(binary_subnet_mask)[i:i+8] for i in range(
                0, len("".join(binary_subnet_mask)), 8)]
            ip_subnet_mask = [binToDecimal(i) for i in binary_subnet_mask]
            print("GRUPO {}\n".format(key))
            print("No. de equipos: ", value)
            print("N: ",n)
            print("dirección de red: ", ".".join(
                map(str,ip)),"/{}".format(subnet_mask))
            print("mascara de subred: ", ".".join(map(str,ip_subnet_mask)))
            print("dirección de broadcast: ", ".".join(
                map(str,broadcast_ip)),"/{}".format(subnet_mask))
            print("primera dirección: ", ".".join(map(str,first_ip_dir)))
            print("última dirección: ", ".".join(map(str,last_ip_dir)))
            print("----------------------------------------------\n")
            universal_ip = ip
            pass
