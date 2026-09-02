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

    # Eliminar espacios al principio y final de la instruccion para evitar errores
    instruction_name, operands = instruction.strip().split(maxsplit=1)
    # Eliminar espaciones entre operandos 
    operands = operands.replace(" ", "")

    # Valores que establece RISC-V   para cada instrucción.
    instruction_codes = {

     # Instrucciones formato R     
     "add":{"opcode": 0b0110011, "funct3": 0b000, "funct7": 0b0000000},
     "sub":{"opcode": 0b0110011, "funct3": 0b000, "funct7": 0b0100000},
     "and":{"opcode": 0b0110011, "funct3": 0b111, "funct7": 0b0000000},
     "or":{"opcode": 0b0110011, "funct3": 0b110, "funct7": 0b0000000},

    # Istrucciones formato I(aritmetica)
    "addi":{"opcode": 0b0010011, "funct3": 0b000, "funct7": None},
    "andi":{"opcode": 0b0010011, "funct3": 0b111, "funct7": None},

    # Instrucciones formato I(carga)
    "lw":{"opcode": 0b0000011, "funct3": 0b010, "funct7": None},
    "lb":{"opcode": 0b0000011, "funct3": 0b000, "funct7": None},

    # Instrucciones formato S
    "sw":{"opcode": 0b0100011, "funct3": 0b010, "funct7": None},
    "sb":{"opcode": 0b0100011, "funct3": 0b000, "funct7": None},

    # Instrucciones formato B
    "beq":{"opcode": 0b1100011, "funct3": 0b000, "funct7": None},
    "bne":{"opcode": 0b1100011, "funct3": 0b001, "funct7": None}
    }

    # Verificar que se encuentre la instruccion en instructions code
    if instruction_name not in instruction_codes:
        raise ValueError("La instrucción no es soportada.Revisar lista de soportadas")

    # Obtener códigos de instrucción
    opcode = instruction_codes[instruction_name]["opcode"]
    funct3 = instruction_codes[instruction_name]["funct3"]
    funct7 = instruction_codes[instruction_name]["funct7"]

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
    if instruction_name in ['add','sub','and','or']:

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
    if instruction_name in ['addi','andi']:
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
    if instruction_name in ['lw','lb']:

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
    if instruction_name in ['sw','sb']:
        #Obtener los registros y valor del inmediato
        rs2 = operands_numbers[0]
        imm = operands_numbers[1]
        rs1 = operands_numbers[2]

        # Convertir inmediato para negativos(Usa complemento a dos)
        imm_11_5 = (imm >> 5) & 0x7F
        imm_0_4 = imm & 0x1F


        # Colocar cada campo según el formato de la instrucción
        encoded = (
            (imm_11_5 << 25)  |    #Bits del 31 al 25
            (rs2 << 20 ) |    #Bits del 24 al 20
            (rs1 << 15) |    #Bits del 19 al 15
            (funct3 << 12) | #Bits del 14 al 12
            (imm_0_4 << 7) |      #Bits del 11 al 7
            (opcode)         #Bits del 6 al 0
        )
        return encoded
    
    # Formato B
    if instruction_name in ['bne','beq']:
        #Obtener los registros y valor del inmediato
        rs1 = operands_numbers[0]
        rs2 = operands_numbers[1]
        imm = operands_numbers[2]

        #Immediatos
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
            (imm_4_1 << 8) |     #Bits del 8 al 11
            (imm_11 << 7) |      #Bit 7
            (opcode)             #Bits del 6 al 0
        )

        return encoded 
    
    raise NotImplementedError("encode_instruction: pendiente de implementar")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # TODO: implementar.
    raise NotImplementedError("explain_instruction: pendiente de implementar")


def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    #print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
