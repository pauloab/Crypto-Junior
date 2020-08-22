__author__ = "Paulo Aguilar"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "paguilar8@utmachala.edu.ec"
__status__ = "Development"

# Diccionario de encriptación base
desc_dictionary = {
" ":0,
"a":1,
"b":2,
"c":3,
"d":4,
"e":5,
"f":6,
"g":7,
"h":8,
"i":9,
"j":10,
"k":11,
"l":12,
"m":13,
"n":14,
"ñ":15,
"o":16,
"p":17,
"q":18,
"r":19,
"s":20,
"t":21,
"u":22,
"v":23,
"w":24,
"x":25,
"y":26,
"z":27}

# Obtiene la matriz solicitandola por consola y devolviendo una matriz ordenada cuadrada
def get_matrix():
    # Ciclo infinito hasta conseguir la matriz
    matrix_undefined = True
    while matrix_undefined:
        matrix_string = input("Ingrese la matriz encriptadora (3x3) separando los valores de la fila con un espacio: ")
        # Crea un arreglo vectorial separando los caracteres como números
        matrix_string_splited = matrix_string.split(" ")
        # Crea una matriz poblada de ceros de orden 3X3
        bounded_matrix = [[0 for x in range(3)] for y in range(3)] 
        # Recorre cada item buscando convertirlo en entero, sino, da error
        f=0
        c=0
        for item in matrix_string_splited:
            try:
                int_item = int(item)
            except ValueError:
                print("Error: Por favor introduzca solo números")
                break
            # Si l valor es convertible lo añade a la matriz vacía
            bounded_matrix[f][c] = int_item
            # Valida que los iteradores (f,c) estén en la última posición permitida de la matriz
            if f==2 and c==2:
                # Una vez completa, se valida que la matriz sea invertible, para poder desencriptar
                if is_invertible(bounded_matrix):
                    # Se cambia la flag y se rompe el ciclo
                    matrix_undefined = False
                    break
                else:
                    print("Error: La matriz ingresada no es invertible")
            # Si el iterador c (columna), llega a 2, pasa el iterador f a la siguiente fila
            # y reinicia c a 0 
            elif c==2:
                f += 1
                c=0
            else:
                c += 1
        # Si el bucle for termina y los iteradores f y c no representan la posición 2,2,
        # La matríz está incompleta
        if f<2 and c<2:
            print("Matriz incompleta, por favor, introduzca 9 valores enteros")
    return bounded_matrix

# Imprime matrices de forma ordenada (útil en desarrollo)
def print_matrix(matrix):
    for row in matrix:
        print(row)

# Valida si una matriz de orden 3X3 es invertible
def is_invertible(input_matrix):
    # Crea una matrix poblada de ceros de orden 5x3 (necesaria para sacar determinantes)
    matrix = [[0 for x in range(3)] for y in range(5)]
    # Puebla la matrix 3X5 con los valores de la matriz de entrada
    k = 0
    for i in range(0,5):  
        matrix[i] = input_matrix[k]
        if k==2:
            k=-1
        k += 1

    asc, desc = 0, 0

    # Calcula las descendentes
    last_value = 1
    for f in range(0,3):
        for c in range(0,3):
            last_value*=matrix[f][c] 
            f+=1
        desc +=last_value
        last_value = 1

    last_value = 1

    # Calcula las ascendentes
    for f in range(0,3):
        for c in reversed(range(0,3)):
            last_value*=matrix[f][c]
            f+=1
        asc += last_value
        last_value = 1

    # Determina si es o no invertible
    if desc-asc == 0:
        return False
    return True

# Multiplica una matriz de orden 1X3 y otra 3X3
def multiply_matrix(sub_matrix,crypter_matrix):
    
    result_matrix = []
    # Al seruna matriz cuadrada n y m son iguales, por tanto se
    # Asume que la longitud de filas es equivalente a col
    for col in range(len(crypter_matrix)):
        sub_res = 0
        # Recorre cada elemento de el vector/matriz 1x3 multiplicando FxC y
        # Acumulandolo en el sub_resultado
        for j in range(3):
            sub_res += sub_matrix[j]*crypter_matrix[j][col]
        # Una vez calculado el sub resultado, lo añade a una matriz/vector
        # que será de orden 1x3
        result_matrix.append(sub_res)
    return result_matrix

# Función que se llama desde el main 
# recibe una cadena de tamaño 3 o mayor y una matriz 3x3 invertible
# retorna una cadena de caracteres resultante del encriptado
def encrypt(message,crypter_matrix):
    # Debido a que el diccionario de encriptado solo contempla minúsculas
    # se converte la cadena completa a minúsculas
    message = message.lower()
    sub_matrix = []
    crypted_string = ""
    i = 1
    # Recorre cada caracter del mensaje a encriptar
    for caracter in message:
        # Crea un vector con los valores asignados a cada letra en el diccionario
        sub_matrix.append(desc_dictionary[caracter])
        # Verifica que si es la última iteración del bucle,
        # y de serlo, si el vector es menor a 3 (orden de la matriz encriptadora)
        # llena esos espacios con 0
        if i == len(message) and len(sub_matrix) != 3:
            while True:
                sub_matrix.append(0)
                if len(sub_matrix) == 3:
                    break
        # Verifica si el tamaño vector es igual a 3 
        if len(sub_matrix) == 3:
            # multiplica los valores del vector de orden 3
            # por la matriz encriptadora de orden 3X3
            vector = multiply_matrix(sub_matrix,crypter_matrix)
            # Llena una cadena con los valores obtenidos después del encriptado
            # y reinicia el tamaño del vector a 0
            for n in vector:
                crypted_string += " "+str(n)
            sub_matrix = []
        i +=1
    return crypted_string

# Multiplica una matriz de orden 1x3 por la inversa de una segunda matriz de orden 3X3
def divide_matrix(row_matrix,crypter_matrix):
    result_matrix = [] 
    # Obtiene la inversa de la matrix 3X3 (encriptadora)
    crypter_inverted_matrix = get_inverse(crypter_matrix)
    # Recorre la matriz, multiplica FXC y lo acumula en un vector resultado 1x3
    for col in range(len(crypter_inverted_matrix)):
        sub_res = 0
        for j in range(3):
            sub_res += row_matrix[j]*crypter_inverted_matrix[j][col]
        result_matrix.append(sub_res)
    return result_matrix

# Recibe una matrix cuadrada y retorna su inversa (método de cofactores)
def get_inverse(input_matrix):
    # Calcula la determinante de la matriz de entrada 
    # Similar a el método is_inverse()
    matrix = [[0 for x in range(3)] for y in range(5)]
    k = 0
    for i in range(0,5):  
        matrix[i] = input_matrix[k]
        if k==2:
            k=-1
        k += 1
    
    asc, desc = 0, 0
    last_value = 1
    for f in range(0,3):
        for c in range(0,3):
            last_value*=matrix[f][c] 
            f+=1
        asc +=last_value
        last_value = 1

    last_value = 1

    for f in range(0,3):
        for c in reversed(range(0,3)):
            last_value*=matrix[f][c]
            f+=1
        desc += last_value
        last_value = 1

    det = asc+(desc*-1)

    # Crea una matriz padre que contendrá las submatrices de orden (F-1)X(C-1)
    matrix_of_matrices = []
    # Matriz vacía que será de orden (F-1)X(C-1)
    matrix_of_submatrices = []
    # Vector 1x(C-1) 
    sub_matrix = []
    # Determina el tamaño máximo de las submatrices generadas
    # Para la multiplicación de cofactores
    max_len = len(input_matrix)-1
    #Iterador de bloqueo en X
    for lock_row in range(len(input_matrix)):
        #Iterador de bloqueo en y
        for lock_col in range(len(input_matrix[lock_row])):
            # iterador de acceso en x
            for ac_row in range(len(input_matrix)):
                if ac_row != lock_row:
                    # iterador de acceso en y
                    for ac_col in range(len(input_matrix[ac_row])):
                        # Verifica que la columna de acceso no sea igual a la de bloqueo
                        if ac_col != lock_col:
                            # Accede a la posición permitida y añade el valor a un vector 1x(C-1)
                            sub_matrix.append(input_matrix[ac_row][ac_col])
                            # Verifica que la vector esté poblada hasta la posición 1x(C-1)
                            if len(sub_matrix)==max_len:
                                # Añade el vector 1x(C-1) a una sumbatriz de orden (F-1)X(C-1)
                                matrix_of_submatrices.append(sub_matrix)
                                # Reinicia el vector 1x(C-1)
                                sub_matrix = []
                                # Verifica que la matriz de orden (F-1)X(C-1)
                                if len(matrix_of_submatrices) == max_len:
                                    # Añade la matriz (F-1)X(C-1) a una matriz de submatrices 
                                    matrix_of_matrices.append(matrix_of_submatrices)
                                    # reinicia la matriz (F-1)X(C-1)
                                    matrix_of_submatrices = []
    inversed_matrix = []
    inversed_vector = []
    # Iteradores que permitirán validar la regla del método +-+-+-...
    i = 1
    max_len +=1
    # Toma cada matriz de orden (F-1)X(C-1) y saca sus determinantes
    # las cuales se dividirán para la deerminante de la matriz de entrada
    # aplicando la regla +-+-+...
    for matrix in matrix_of_matrices:
        # Calcula las determinantes de manera similar a is_inverted()
        c = 0
        asc, desc = 1, 1
        for row in matrix:
            asc *= row[c]
            c += 1
        c = 0
        for row in reversed(matrix):
            desc *= row[c]
            c += 1
        # almacena la determinante de la submatriz 
        sub_det = asc-desc
        # Toma en cuenta la regla +-+-+... 
        # basándose en si la iteración es par o no
        # y divide ela sub_determinante para la determinante de la matriz
        if i % 2 == 0:
            sub_det = sub_det/det*-1
        else:
            sub_det = sub_det/det
        # Añade el valor calculado a un vector de orden 1XC
        inversed_vector.append(sub_det)
        # Determina que el tamaño del vector sea igual a C
        if len(inversed_vector) == max_len:
            # Añade el vector 1XC a la matriz de resultados de orden FXC
            inversed_matrix.append(inversed_vector)
            inversed_vector = []
        i +=1
    # Transpone la matriz debido a como se procesaron los datos
    inversed_matrix = list(zip(*inversed_matrix))
    return inversed_matrix

# Toma de valores de entrada un texto encriptado y una matriz
# encriptadora de orden 3X3 y retorna una cadena decodificada
def de_encrypt(crypted,crypter_matrix):
    crypted_matrix = [[]]
    # Crea un vector con los valores de la cadena encriptada
    # separandola por sus espacios
    crypted = crypted.split(" ")
    i,j = 0, 0
    # Toma cada número de la cadena encriptada,
    # la converte en entero y añade a una matriz de orden Lx3
    for val in crypted:
        crypted_matrix[j].append(int(val))
        if i == 2:
            j += 1
            i = -1
            crypted_matrix.append([])
        i+=1
    # remueve una última fila vacía añadida en el proceso anterior
    crypted_matrix.remove(crypted_matrix[len(crypted_matrix)-1])
    divided_matrix = []
    decrypted = ""
    # Transpone el diccionario para poder acceder de manera inversa al mismo 
    den_dict = {}
    for k,v in desc_dictionary.items():
        den_dict[v] = k
    
    # Toma la matriz de los valores encriptados LX3
    # y divide cada fila por la matriz encriptadora
    for row in crypted_matrix:
        divided_matrix.append(divide_matrix(row,crypter_matrix))
    # Toma la matriz con los valores decodificados 
    # y accede al diccionario transpuesto para obtener su letra asignada
    for row in divided_matrix:
        for character in row: 
            # Observación importante
            # debido a la forma en como se procesan los números 
            # es necesario redondear el valor para obtener el resultado correcto
            decrypted += den_dict[round(character,0)]
    return decrypted

# Función de flujo principal
def main_function():
    print("Programa para encriptar/desencriptar mensajes mediante el producto matricial")
    print("Elaborado por: Paulo Aguilar")
    while True:
        print("\n===============================================================")
        print("============================== Menú ===========================")
        print("===============================================================\n")
        print("\n 1. Encriptar un mensaje \n 2. Desencriptar un mensaje \n 3. Salir")
        sel = input("Ingrese su selección: ")
        if sel == "1":
            print("\n===============================================================")
            print("===================== Encriptar un mensaje ====================")
            print("===============================================================\n")
            message = ""
            while len(message)<3:
                message = input("Ingresa el mensaje a encriptar (min 3 caracteres): ")
            crypter_matrix = get_matrix()
            print("====================\n Matriz Encripadora\n====================")
            print_matrix(crypter_matrix)
            crypted = encrypt(message,crypter_matrix)
            print(f"Texto encriptado: {crypted}")
        elif sel == "2":
            print("\n===============================================================")
            print("=================== Desencriptar un mensaje ===================")
            print("===============================================================\n")
            crypted = input("Ingrese el texto encriptado: ")
            crypter_matrix = get_matrix()
            get_inverse(crypter_matrix)
            decripted = de_encrypt(crypted,crypter_matrix)
            print(f"Texto desencriptado: {decripted}")
        elif sel == "3":
            print("\n========== Hasta la próxima ==========\n")
            break
        else:
            print("Selección no válida")
        print("\n========== Proceso terminado =========\n")

if __name__ == "__main__":
    main_function()


