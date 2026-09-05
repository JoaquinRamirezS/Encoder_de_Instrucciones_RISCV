#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

# Valores que establece RISC-V   para cada instrucción.
instruction_codes = {

     # Instrucciones formato R   
     "R":{
        "opcode": 0b0110011,
        "instructions": {  
            "add":{"funct3": 0b000, "funct7": 0b0000000},
            "sub":{"funct3": 0b000, "funct7": 0b0100000},
            "and":{"funct3": 0b111, "funct7": 0b0000000},
            "or": {"funct3": 0b110, "funct7": 0b0000000},
        }
     },

    # Istrucciones formato I(aritmetica)
    "I_Arithmetic":{
        "opcode": 0b0010011,
        "instructions":{
            "addi":{"funct3": 0b000},
            "andi":{"funct3": 0b111},
        }
    },
    # Instrucciones formato I(carga)
    "I_Load":{
        "opcode": 0b0000011,
        "instructions":{
            "lw":{"funct3": 0b010},
            "lb":{"funct3": 0b000},
        }
    },
    # Instrucciones formato S
    "S":{
        "opcode": 0b0100011,
        "instructions":{
            "sw":{"funct3": 0b010},
            "sb":{"funct3": 0b000},
        }
    },
    # Instrucciones formato B
    "B":{
        "opcode": 0b1100011,
        "instructions":{
            "beq":{"funct3": 0b000},
            "bne":{"funct3": 0b001}
        }
      }
    }

def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS. Los valores
    de opcode/funct3/funct7 de cada una NO se proveen aquí: deben
    investigarse en el manual oficial de la ISA RISC-V (ver referencia en
    la especificación) y documentarse en el README.
    """
    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.

    # Eliminar espacios al principio y final de la instrucción
    instruction = instruction.strip()

    for name in sorted(SOPORTADAS, key=len, reverse=True): # Busca en la lista de soportadas de mayor cant de caracteres a menor
        if instruction.startswith(name): # Si alguna instrucción pertenece a soportada 
            instruction_name = name # Guarda el nombre
            operands = instruction[len(name):] # Calcula el tamaño de la instrucción encontrada y toma todo lo demás como operandos
            break
    else:
        raise ValueError("La instrucción no es soportada")
        
    # Eliminar espaciones entre operandos 
    operands = operands.replace(" ", "")

    # Verificar que se encuentre la instruccion en instructions code
    for formato, data in instruction_codes.items():
        if instruction_name in data["instructions"]:
            # Obtener códigos de instrucción
            opcode = data["opcode"] # Opcode
            funct3 = data["instructions"][instruction_name]["funct3"] #Obtiene funct3
            funct7 = data["instructions"][instruction_name].get("funct7") # Obtiene funct7 si existe
            break #Termina si encontró la instrucción
    else:
        raise ValueError("La instrucción no es soportada.Revisar lista de soportadas")


    # Parsear operandos
    # Convertir los registros de texto a numero entero
    # Como x5 a solo 5
    operands_numbers=[] # Lista para guardar el numero del operando (x5 se guarda solo el 5)

    if "(" in operands: # Casos para instrucciones con memoria
        register_part, memory_part = operands.split(",")
        reg = register_part.strip().replace("x","")
        operands_numbers.append(int(reg)) # Guardar el registro

        #Separar inmediato de registro
        imm_part, reg_part = memory_part.strip().rstrip(")").split("(")

        #Guardar en operands_numbers
        operands_numbers.append(int(imm_part))
        operands_numbers.append(int(reg_part[1:]))

    else:
        operands_separate = operands.split(',') # Se separan por comas
        for operand in operands_separate:
            if operand.startswith("x"):
                operands_numbers.append(int(operand[1:]))
            else:
                operands_numbers.append(int(operand))

    # Formato R
    if formato == "R":

        #Obtener los registros
        rd = operands_numbers[0]
        rs1 = operands_numbers[1]
        rs2 = operands_numbers[2]

        # Colocar cada campo según el formato de la instrucción
        encoded = (
            (funct7 << 25) | #Bits del 31 al 25
            (rs2 << 20) |    #Bits del 24 al 20
            (rs1 << 15) |    #Bits del 19 al 15
            (funct3 << 12) | #Bits del 14 al 12
            (rd << 7) |      #Bits del 11 al 7
            (opcode)         #Bits del 6 al 0
        )

        return encoded

    # Formato I(aritmetica)
    if formato == "I_Arithmetic":
        #Obtener los registros y valor del inmediato
        rd = operands_numbers[0]
        rs1 = operands_numbers[1]
        imm = operands_numbers[2]

        # Convertir inmediato para negativos(Usa complemento a dos)
        imm = imm & 0xFFF

        # Colocar cada campo según el formato de la instrucción
        encoded = (
            (imm << 20) |    #Bits del 31 al 20
            (rs1 << 15) |    #Bits del 19 al 15
            (funct3 << 12) | #Bits del 14 al 12
            (rd << 7) |      #Bits del 11 al 7
            (opcode)         #Bits del 6 al 0
        )
        return encoded
    
    # Formato I(carga)
    if formato == "I_Load":

        #Obtener los registros y valor del inmediato
        rd = operands_numbers[0]
        imm = operands_numbers[1]
        rs1 = operands_numbers[2]

        # Convertir inmediato para negativos(Usa complemento a dos)
        imm = imm & 0xFFF

        # Colocar cada campo según el formato de la instrucción
        encoded = (
            (imm << 20) |    #Bits del 31 al 20
            (rs1 << 15) |    #Bits del 19 al 15
            (funct3 << 12) | #Bits del 14 al 12
            (rd << 7) |      #Bits del 11 al 7
            (opcode)         #Bits del 6 al 0
        )
        return encoded
    
    # Formato S
    if formato == "S":
        #Obtener los registros y valor del inmediato
        rs2 = operands_numbers[0]
        imm = operands_numbers[1]
        rs1 = operands_numbers[2]

        # Convertir inmediato para negativos(Usa complemento a dos)
        imm = imm & 0xFFF

        # Separar inmediato
        imm_11_5 = (imm >> 5) & 0x7F
        imm_0_4 = imm & 0x1F


        # Colocar cada campo según el formato de la instrucción
        encoded = (
            (imm_11_5 << 25)| #Bits del 31 al 25
            (rs2 << 20 ) |    #Bits del 24 al 20
            (rs1 << 15) |     #Bits del 19 al 15
            (funct3 << 12) |  #Bits del 14 al 12
            (imm_0_4 << 7) |  #Bits del 11 al 7
            (opcode)          #Bits del 6 al 0
        )
        return encoded
    
    # Formato B
    if formato == "B":
        #Obtener los registros y valor del inmediato
        rs1 = operands_numbers[0]
        rs2 = operands_numbers[1]
        imm = operands_numbers[2]

        # Convertir inmediato para negativos(Usa complemento a dos)
        imm = imm & 0x1FFF

        #Separar inmediato
        imm_12 = (imm >> 12) & 0x1 # Mascara de 1 bit
        imm_10_5 = (imm >> 5) & 0x3F # Mascara de 6 bits
        imm_4_1 = (imm >> 1) & 0xF # Mascara de 4 bits
        imm_11 = (imm >> 11) & 0x1 # Mascara de 1 bit

        encoded = (
            (imm_12 << 31)|      # Bit 31 
            (imm_10_5 << 25)|    #Bits del 30 al 25
            (rs2 << 20 ) |       #Bits del 24 al 20
            (rs1 << 15) |        #Bits del 19 al 15
            (funct3 << 12) |     #Bits del 14 al 12
            (imm_4_1 << 8) |     #Bits del 11 al 8
            (imm_11 << 7) |      #Bit 7
            (opcode)             #Bits del 6 al 0
        )

        return encoded 
    
    # raise NotImplementedError("encode_instruction: pendiente de implementar")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # Eliminar espacios al principio y final de la instrucción
    instruction = instruction.strip()

    for name in sorted(SOPORTADAS, key=len, reverse=True): # Busca en la lista de soportadas de mayor cant de caracteres a menor
        if instruction.startswith(name): # Si alguna instrucción pertenece a soportada 
            instruction_name = name # Guarda el nombre
            break
    else:
        raise ValueError("La instrucción no es soportada")

    #Detectar formato
    formato = None #Inicia formato vacio
    #Recorre el diccionario instruction_codes
    for fmt, data in instruction_codes.items():

        #Se verifica si la instrucción que se está verificando esta dentro
        # de las instrucciones de formato
        if instruction_name in data["instructions"]:
             # Si está se guarda el nombre del formato
             formato = fmt
             break
    # Si el formato no se detecta se despliega un msj
    if formato is None:
        return "El formato no se detectó"

    # Extraer campos según formato
    #Utilizando desplazamiento y mascaras para obtener la cantidad de bits requerida por campo

    if formato == "R":
        campos = [
            # Etiquetas y desplazamiento de 25 a la derecha, mascara de 111 1111 para obtener solo los ultimos 7 bits
            # El 7 indica la cantidad de bits que comprende cada campo
            #Aplica igual con las demás
            ("[31:25]","funct7", (word >> 25) & 0x7F, 7),
            ("[24:20]","rs2", (word >> 20) & 0x1F, 5),
            ("[19:15]","rs1", (word >> 15) & 0x1F, 5),
            ("[14:12]","funct3", (word >> 12) & 0x07, 3),
            ("[11:7]","rd", (word >> 7) & 0x1F, 5),
            ("[6:0]","opcode", (word) & 0x7F, 7),
        ]
        #Toma el tercer elemento de cada campo
        f7, rs2_v, rs1_v, f3, rd_v, op =[c[2] for c in campos]
        explicacion = (
            f"** Instrucción tipo R: Operaciones aritméticas y lógicas entre registros.\n"
            f"* opcode (0b{op:07b}): Indica la categoría general de la instrucción (OPP).\n"
            f"* rd (x{rd_v}): Registro donde se guarda el resultado de la operación.\n"
            f"* funct3 (0b{f3:03b}): Indica parte de la operación que se debe realizar.\n"
            f"* rs1 (x{rs1_v}): Registro que contiene el primer operando.\n"
            f"* rs2 (x{rs2_v}): Registro que contiene el segundo operando.\n"
            f"* funct7 (0b{f7:07b}): Junto con opcode y funct3, permite identifcar la operación específica({instruction_name}).\n" 
        )

    elif formato in ["I_Arithmetic","I_Load"]:
        campos = [
            ("[31:20]","imm[11:0]", (word >> 20) & 0xFFF, 12),
            ("[19:15]","rs1", (word >> 15) & 0x1F, 5),
            ("[14:12]","funct3", (word >> 12) & 0x07, 3),
            ("[11:7]","rd", (word >> 7) & 0x1F, 5),
            ("[6:0]","opcode", (word) & 0x7F, 7),
        ]
        #Toma el tercer elemento de cada campo
        imm_v, rs1_v, f3, rd_v, op =[c[2] for c in campos]
        #Detecta si el inmediato es un valor positivo o negativo
        imm_sign = imm_v - 0x1000 if(imm_v & 0x800) else imm_v
        #Diferencia entre I_Arithmetic e I_Load
        if formato == "I_Arithmetic":
            tipo = "aritmético"
            tipo_description ="Operaciones que utilizan un valor inmediato(OP-IMM)"
            imm_description = "Valor inmediato que se utiliza en la operación."
        else:
            tipo = "de carga"
            tipo_description ="Carga desde la memoria"
            imm_description = "Desplazamiento que se suma a rs1 para calcular la dirección de memoria."


        explicacion = (
            f"** Instrucción tipo I ({tipo}): {tipo_description}.\n"
            f"* opcode (0b{op:07b}): Indica la categoría general de la instrucción.\n"
            f"* rd (x{rd_v}): Registro donde se guarda el resultado de la operación.\n"
            f"* funct3 (0b{f3:03b}): Ayuda a identificar la operación que se va a realizar.\n"
            f"* rs1 (x{rs1_v}): Registro que contiene el valor de entrada.\n"
            f"* imm[11:0] ({imm_sign}): {imm_description}\n" 
        )

    elif formato == "S":
        campos = [
            ("[31:25]","imm[11:5]", (word >> 25) & 0x7F, 7),
            ("[24:20]","rs2", (word >> 20) & 0x1F, 5),
            ("[19:15]","rs1", (word >> 15) & 0x1F, 5),
            ("[14:12]","funct3", (word >> 12) & 0x07, 3),
            ("[11:7]","imm[4:0]", (word >> 7) & 0x1F, 5),
            ("[6:0]","opcode", (word) & 0x7F, 7),
        ]
        #Toma el tercer elemento de cada campo
        imm_11_5, rs2_v,rs1_v, f3, imm_4_0, op =[c[2] for c in campos]
        #Recosntruye el inmediato
        imm_v = (imm_11_5 << 5) | imm_4_0
        #Detecta si el inmediato es un valor positivo o negativo
        imm_sign = imm_v - 0x1000 if(imm_v & 0x800) else imm_v

        explicacion = (
            f"** Instrucción tipo S: Operaciones de almacenamiento de memoria.\n"
            f"* opcode (0b{op:07b}): Indica la categoría general de la instrucción (STORE).\n"
            f"* imm[4:0]({imm_4_0}): Parte baja del desplazamiento de memoria\n"
            f"* funct3 (0b{f3:03b}): Indica el tamaño del dato que se va a guardar.\n"
            f"* rs1 (x{rs1_v}): Registo base que contiene la dirección de memoria.\n"                        
            f"* rs2 (x{rs2_v}): Registo que contiene el dato que se va a guardar.\n"
            f"* imm[11:5] ({imm_11_5}): Parte alta del desplazamiento(Offset total = {imm_sign}).\n"      
        )

    elif formato == "B":
        campos = [
            ("[31]","imm[12]", (word >> 31) & 0x01, 1),
            ("[30:25]","imm[10:5]", (word >> 25) & 0x3F, 6),
            ("[24:20]","rs2", (word >> 20) & 0x1F, 5),
            ("[19:15]","rs1", (word >> 15) & 0x1F, 5),
            ("[14:12]","funct3", (word >> 12) & 0x07, 3),
            ("[11:8]","imm[4:1]", (word >> 8) & 0x0F, 4),
            ("[7]","imm[11]", (word >> 7) & 0x01, 1),
            ("[6:0]","opcode", (word) & 0x7F, 7),
        ]
        #Toma el tercer elemento de cada campo
        imm12,imm_10_5, rs2_v,rs1_v, f3, imm_4_1, imm11, op =[c[2] for c in campos]
        #Reconstruye el inmediato
        imm_v = (imm12 << 12) | (imm11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
         #Detecta si el inmediato es un valor positivo o negativo
        imm_sign = imm_v - 0x2000 if(imm_v & 0x1000) else imm_v

        explicacion = (
        f"** Instrucción tipo B: Saltos condicionales.\n"
            f"* opcode (0b{op:07b}): Indica la categoría general de la instrucción (BRANCH).\n"
            f"* imm[12], imm[11], imm[10:5], imm[4:1]: Partes del inmediato que juntas forman el desplazamiento del salto.\n"
            f"* funct3 (0b{f3:03b}): Identifica la condición de salto({instruction_name}).\n"
            f"* rs1 (x{rs1_v}) y rs2 (x{rs2_v}): Registros que se comparan.\n"                        
            f"* Desplazamiento del salto:{imm_sign} bytes desde el PC actual.\n"                 
        )
    else:
        return "Error:Formato no conocido."
    
    # Tabla visual
    #Colores
    Morado = "\033[95m"
    Amarillo = "\033[93m"
    Azul = "\033[94m"
    Reset = "\033[0m"

    #Bordes simples
    col_width = 12

    #Borde superior
    borde = " " * 10 + "+" + "+".join(["-" * col_width for _ in campos]) + "+"

    #Fila de rangos
    fila_ranges = " " * 10 + "|" + "|".join(f"{Morado}{r:^{col_width}}{Reset}" for r, _, _, _ in campos) + "|"
    #Fila de nombres
    fila_names = " " * 10 + "|" + "|".join(f"{Amarillo}{n:^{col_width}}{Reset}" for _, n, _, _ in campos) + "|"
    #Fila Valores
    fila_values = " " * 10 + "|" + "|".join(f"{Azul}{f'{v:0{bits}b}'.center(col_width)}{Reset}" for  _, _, v, bits in campos) + "|"

    #Palabra entera en binario
    binary_word = f"{word:032b}"
    #Palabra binaria dividida en grupos de 4
    binary_word_groups = " ".join(binary_word[i:i+4] for i in range(0, 32, 4))
    #Palabra en hexadecimal
    #hex_word = f"0x{word:08x}"

    return (
        f"Instrucción: {instruction}\n"
        f"Formato: {formato}\n\n"
        f"{borde}\n"
        f"{fila_ranges}\n"
        f"{borde}\n"
        f"{fila_names}\n"
        f"{borde}\n"
        f"{fila_values}\n"
        f"{borde}\n\n"
        f"Palabra binaria: {binary_word_groups}\n\n"
        f"Explicación:\n{explicacion}" 
    )

def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
