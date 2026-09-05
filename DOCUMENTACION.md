# Proyecto Individual: Codificador Educativo de Instrucciones RISC-V
**Instituto Tecnológico de Costa Rica**
**Escuela de Ingenieria en Computadores**
**Curso:** CE-4301 Arquitectura de Computadores I 
**Estudiante:** Joaquín Ramírez Sequeira
**Carné:** 2023301855 

**Fecha:** 4 de septiembre de 2026  

---

## Descripción de la arquitectura del código
El programa consta de un único archivo `(encoder_skeleton.py)` que contiene la función `encode_instruction()`, que se encarga de tomar la instrucción,parsearla, identificar su formato y generar el código de 32 bits, y la función `explain_instruction()` que toma el código generado y lo desglosa, separándolo por campos y explicando su significado según formato.

La función `main()`, la cual no se modificó, por lo que su propósito sigue siendo el mismo,manejar la entrada por la línea de comandos, imprimir la explicación y la línea HEX. Finalmente, el script `run.sh` es el punto de entrada fijo para la ejecución del programa.


## Decisiones de diseño
- Se decidió utilizar un diccionario global instruction_codes para evitar la duplicación de datos y facilitar la extensión del programa conforme se iban implementando los distintos tipos de instrucciones.
- Los diferentes formatos se manejan mediante condicionales if/elif. Detectan el formato y según la instrucción, aplican desplazamientos y máscaras para obtener la cantidad de bits que requiere cada campo.
- El manejo de instrucciones que utilizaban paréntesis se implementó con un parseo específico que aísla el inmediato y el registro base, asegurando un correcto procesamiento para números positivos y negativos.
- Se optó por utilizar tablas, colores y una lista en la explicación visual para que de este modo sea fácil identificar los diferentes campos de la instrucción, así como su significado. 

## Codificación de cada instrucción

Para el formato y codificación de cada instrucción se utilizó con referencia el Manual Oficial de ISA RISC-V [1]. Se utilizo "Chapter 9: RV32/64G Instruction Set Listings" para las codificaciones y "Chapter 2:RV32I Base Integer Instruction Set,
Version 2.0" para conocer a detalle cada formato.Chapter 2 también se utilizó para poder implementar la explicación visual de cada instrucción.

Dicho lo anterior, se obtuvieron las siguientes tablas para las codificaciones y los formatos:


**Tabla 1. Formatos de instrucciones RV32I**

| Formato | 31–25 | 24–20 | 19–15 | 14–12 | 11–7 | 6–0 |
|:-------:|:-----:|:-----:|:-----:|:-----:|:----:|:---:|
| **R**   | funct7 | rs2 | rs1 | funct3 | rd | opcode |
| **I**   | imm[11:0] | - | rs1 | funct3 | rd | opcode |
| **S**   | imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode |
| **B**   | imm[12\|10:5] | rs2 | rs1 | funct3 | imm[4:1\|11] | opcode |


**Tabla 2.Codificación de cada instrucción**

| Instrucción | Formato | opcode  | funct3 | funct7  |
|:-----------:|:-------:|:-------:|:------:|:-------:|
| add         | R       | 0110011 | 000    | 0000000 |
| sub         | R       | 0110011 | 000    | 0100000 |
| and         | R       | 0110011 | 111    | 0000000 |
| or          | R       | 0110011 | 110    | 0000000 |
| addi        | I (aritmético) | 0010011 | 000 | - |
| andi        | I (aritmético) | 0010011 | 111 | - |
| lw          | I (carga) | 0000011 | 010 | - |
| lb          | I (carga) | 0000011 | 000 | - |
| sw          | S       | 0100011 | 010    | -       |
| sb          | S       | 0100011 | 000    | -       |
| beq         | B       | 1100011 | 000    | -       |
| bne         | B       | 1100011 | 001    | -       |

## Ejemplos de salida explicativa 

### Formato R

$ ./run.sh "sub x5, x7, x18"
Instrucción: sub x5, x7, x18
Formato: R

          +------------+------------+------------+------------+------------+------------+
          |  [31:25]   |  [24:20]   |  [19:15]   |  [14:12]   |   [11:7]   |   [6:0]    |
          +------------+------------+------------+------------+------------+------------+
          |   funct7   |    rs2     |    rs1     |   funct3   |     rd     |   opcode   |
          +------------+------------+------------+------------+------------+------------+
          |  0100000   |   10010    |   00111    |    000     |   00101    |  0110011   |
          +------------+------------+------------+------------+------------+------------+

Palabra binaria: 0100 0001 0010 0011 1000 0010 1011 0011

Explicación:
** Instruccion tipo R: Operaciones aritméticas y lógicas entre registros.
* opcode (0b0110011):Indica la categoría general de la instrucción (OPP).
* rd (x5):Registro donde se guarda el resultado de la operación.
* funct3 (0b000):Indica parte de la operación que se debe realizar.
* rs1 (x7):Registro que contiene el primer operando.
* rs2 (x18):Registro que contiene el segundo operando.
* funct7 (0b0100000):Junto con opcode y funct3, permite identificar la operación específica(sub).

HEX: 0x412382b3

---
### Formato I (aritmético)

$ ./run.sh "addi x5, x25, 2035"
Instrucción: addi x5, x25, 2035
Formato: I_Arithmetic

          +------------+------------+------------+------------+------------+
          |  [31:20]   |  [19:15]   |  [14:12]   |   [11:7]   |   [6:0]    |
          +------------+------------+------------+------------+------------+
          | imm[11:0]  |    rs1     |   funct3   |     rd     |   opcode   |
          +------------+------------+------------+------------+------------+
          |011111110011|   11001    |    000     |   00101    |  0010011   |
          +------------+------------+------------+------------+------------+

Palabra binaria: 0111 1111 0011 1100 1000 0010 1001 0011

Explicación:
** Instrucción tipo I (aritmético): Operaciones que utilizan un valor inmediato(OP-IMM).
* opcode (0b0010011): Indica la categoría general de la instrucción.
* rd (x5): Registro donde se guarda el resultado de la operación.
* funct3 (0b000): Ayuda a identificar la operación que se va a realizar.
* rs1 (x25): Registro que contiene el valor de entrada.
* imm[11:0] (2035): Valor inmediato que se utiliza en la operación.

HEX: 0x7f3c8293

---
### Formato I (de carga)
$ ./run.sh "lb x25, -389(x27) "
Instrucción: lb x25, -389(x27)
Formato: I_Load

          +------------+------------+------------+------------+------------+
          |  [31:20]   |  [19:15]   |  [14:12]   |   [11:7]   |   [6:0]    |
          +------------+------------+------------+------------+------------+
          | imm[11:0]  |    rs1     |   funct3   |     rd     |   opcode   |
          +------------+------------+------------+------------+------------+
          |111001111011|   11011    |    000     |   11001    |  0000011   |
          +------------+------------+------------+------------+------------+

Palabra binaria: 1110 0111 1011 1101 1000 1100 1000 0011

Explicación:
** Instrucción tipo I (de carga): Carga desde la memoria.
* opcode (0b0000011): Indica la categoría general de la instrucción.
* rd (x25): Registro donde se guarda el resultado de la operación.
* funct3 (0b000): Ayuda a identificar la operación que se va a realizar.
* rs1 (x27): Registro que contiene el valor de entrada.
* imm[11:0] (-389): Desplazamiento que se suma a rs1 para calcular la dirección de memoria.

HEX: 0xe7bd8c83

---

### Formato S
$ ./run.sh "sw x31, -411(x23)"                 
Instrucción: sw x31, -411(x23)
Formato: S

          +------------+------------+------------+------------+------------+------------+
          |  [31:25]   |  [24:20]   |  [19:15]   |  [14:12]   |   [11:7]   |   [6:0]    |
          +------------+------------+------------+------------+------------+------------+
          | imm[11:5]  |    rs2     |    rs1     |   funct3   |  imm[4:0]  |   opcode   |
          +------------+------------+------------+------------+------------+------------+
          |  1110011   |   11111    |   10111    |    010     |   00101    |  0100011   |
          +------------+------------+------------+------------+------------+------------+

Palabra binaria: 1110 0111 1111 1011 1010 0010 1010 0011

Explicación:
** Instrucción tipo S: Operaciones de almacenamiento de memoria.
* opcode (0b0100011): Indica la categoría general de la instrucción (STORE).
* imm[4:0](5): Parte baja del desplazamiento de memoria
* funct3 (0b010): Indica el tamaño del dato que se va a guardar.
* rs1 (x23): Registo base que contiene la dirección de memoria.
* rs2 (x31): Registo que contiene el dato que se va a guardar.
* imm[11:5] (115): Parte alta del desplazamiento(Offset total = -411).

HEX: 0xe7fba2a3

---

### Formato B
$ ./run.sh "beq x30, x4, -80"                 
Instrucción: beq x30, x4, -80
Formato: B

          +------------+------------+------------+------------+------------+------------+------------+------------+
          |    [31]    |  [30:25]   |  [24:20]   |  [19:15]   |  [14:12]   |   [11:8]   |    [7]     |   [6:0]    |
          +------------+------------+------------+------------+------------+------------+------------+------------+
          |  imm[12]   | imm[10:5]  |    rs2     |    rs1     |   funct3   |  imm[4:1]  |  imm[11]   |   opcode   |
          +------------+------------+------------+------------+------------+------------+------------+------------+
          |     1      |   111101   |   00100    |   11110    |    000     |    1000    |     1      |  1100011   |
          +------------+------------+------------+------------+------------+------------+------------+------------+

Palabra binaria: 1111 1010 0100 1111 0000 1000 1110 0011

Explicación:
** Instrucción tipo B: Saltos condicionales.
* opcode (0b1100011): Indica la categoría general de la instrucción (BRANCH).
* imm[12], imm[11], imm[10:5], imm[4:1]: Partes del inmediato que juntas forman el desplazamiento del salto.
* funct3 (0b000): Identifica la condición de salto(beq).
* rs1 (x30) y rs2 (x4): Registros que se comparan.
* Desplazamiento del salto:-80 bytes desde el PC actual.

HEX: 0xfa4f08e3

---

## Validación contra toolchain
Para la validación del toolchain se probaron 3 casos de prueba distintos para cada una de las 12 instrucciones. Se cubren distintos escenarios según aplique para cada instrucción:valores positivos,negativos y límite. 

**NOTA**:La instalación del Toolchain se muestra en el archivo `README.md`.

Aplicando lo anterior, se obtuvieron los siguientes resultados:

#### Tabla de validación contra toolchain oficial

| Instrucción | HEX oficial (objdump) | HEX herramienta (run.sh) | Coincidencia |
|-------------|-----------------------|--------------------------|--------------|
| `add x0, x7, x8` | `0x00838033` | `0x00838033` | PASS |
| `add x1, x0, x9` | `0x009000b3` | `0x009000b3` | PASS |
| `add x0, x0, x0` | `0x00000033` | `0x00000033` | PASS |
| `sub x0, x9, x7` | `0x40748033` | `0x40748033` | PASS |
| `sub x1, x0, x2` | `0x402000b3` | `0x402000b3` | PASS |
| `sub x0, x0, x0` | `0x40000033` | `0x40000033` | PASS |
| `and x5, x14, x0` | `0x000772b3` | `0x000772b3` | PASS |
| `and x0, x1, x2` | `0x0020f033` | `0x0020f033` | PASS |
| `and x0, x0, x0` | `0x00007033` | `0x00007033` | PASS |
| `or x0, x2, x7` | `0x00716033` | `0x00716033` | PASS |
| `or x0, x4, x6` | `0x00626033` | `0x00626033` | PASS |
| `or x0, x0, x0` | `0x00006033` | `0x00006033` | PASS |
| `addi x6, x0, 2047` | `0x7ff00313` | `0x7ff00313` | PASS |
| `addi x0, x2, -2048` | `0x80010013` | `0x80010013` | PASS |
| `addi x0, x0, 0` | `0x00000013` | `0x00000013` | PASS |
| `andi x0, x3, 2047` | `0x7ff1f013` | `0x7ff1f013` | PASS |
| `andi x1, x0, -2048` | `0x80007093` | `0x80007093` | PASS |
| `andi x0, x0, 0` | `0x00007013` | `0x00007013` | PASS |
| `lw x14, 0(x8)` | `0x00042703` | `0x00042703` | PASS |
| `lw x9, -2048(x0)` | `0x80002483` | `0x80002483` | PASS |
| `lw x2, 2047(x3)` | `0x7ff1a103` | `0x7ff1a103` | PASS |
| `lb x11, 0(x8)` | `0x00040583` | `0x00040583` | PASS |
| `lb x12, -2048(x0)` | `0x80000603` | `0x80000603` | PASS |
| `lb x7, 2047(x3)` | `0x7ff18383` | `0x7ff18383` | PASS |
| `sw x1, 0(x4)` | `0x00122023` | `0x00122023` | PASS |
| `sw x10, -2048(x9)` | `0x80a4a023` | `0x80a4a023` | PASS |
| `sw x2, 2047(x3)` | `0x7e21afa3` | `0x7e21afa3` | PASS |
| `sb x3, 0(x4)` | `0x00320023` | `0x00320023` | PASS |
| `sb x15, -2048(x9)` | `0x80f48023` | `0x80f48023` | PASS |
| `sb x7, 2047(x3)` | `0x7e718fa3` | `0x7e718fa3` | PASS |
| `beq x0, x1, 0` | `0x00100063` | `0x00100063` | PASS |
| `beq x7, x8, -4096` | `0x80838063` | `0x80838063` | PASS |
| `beq x3, x4, 4094` | `0x7e418fe3` | `0x7e418fe3` | PASS |
| `bne x0, x12, 0` | `0x00c01063` | `0x00c01063` | PASS |
| `bne x9, x10, -4096` | `0x80a49063` | `0x80a49063` | PASS |
| `bne x3, x4, 4094` | `0x7e419fe3` | `0x7e419fe3` | PASS |

## Referencias
[1] A. Waterman, Y. Lee, D. A. Patterson, and K. Asanović, *The RISC-V Instruction Set Manual, Volume I: User-Level ISA, Version 2.1*, Tech. Rep. UCB/EECS-2016-118, EECS Department, University of California, Berkeley, May 31, 2016. [Online].
 Available: https://docs.alexrp.com/riscv/riscv_unpriv_v2_1.pdf. [Accessed: Aug. 29, 2026]
