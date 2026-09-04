# Proyecto Individual: Codificador Educativo de Instrucciones RISC-V
**Instituto Tecnológico de Costa Rica**
**Escuela de Ingenieria en Computadores**
**Curso:** CE-4301 Arquitectura de Computadores I 
**Estudiante:** Joaquín Ramírez Sequeira
**Carné:** 2023301855 

**Fecha:** 4 de septiembre de 2026  

---
## Uso de la herramienta propia

Primero, se debe tener claro cuáles son las instrucciones soportadas.Segun su formato son:

| **R** | **I** | **S** | **B** | 
| :---: | :---: | :---: | :---: | 
| add, sub, and, or | addi, andi, lw, lb | sw, sb | beq, bne |

El uso de la herramienta se hará de la siguiente manera:
- Se abre en terminal Git Bash
- Se ejecuta el comando `./run.sh "instruccion"`
- Presionar Enter y ver resultado en la terminal.

#### Ejemplo
$ ./run.sh "add x7, x20, x6"

Instrucción: add x7, x20, x6
 Formato: R

          +------------+------------+------------+------------+------------+------------+
          |  [31:25]   |  [24:20]   |  [19:15]   |  [14:12]   |   [11:7]   |   [6:0]    |
          +------------+------------+------------+------------+------------+------------+
          |   funct7   |    rs2     |    rs1     |   funct3   |     rd     |   opcode   |
          +------------+------------+------------+------------+------------+------------+
          |  0000000   |   00110    |   10100    |    000     |   00111    |  0110011   |
          +------------+------------+------------+------------+------------+------------+

Palabra binaria: 0000 0000 0110 1010 0000 0011 1011 0011

Explicación:
** Instruccion tipo R: Operaciones aritméticas y lógicas entre registros.
* opcode (0b0110011):Indica la categoría general de la instrucción (OPP).
* rd (x7):Registro donde se guarda el resultado de la operación.
* funct3 (0b000):Indica parte de la operación que se debe realizar.
* rs1 (x20):Registro que contiene el primer operando.
* rs2 (x6):Registro que contiene el segundo operando.
* funct7 (0b0000000):Junto con opcode y funct3, permite identifcar la operación específica(add).

HEX: 0x006a03b3

---
#### Si la instrucción es soportada se mostrará en la terminal una explicación similar a la anterior. Al momento de escribir la isntrucción no deberían existir problemas relacionadas a espacios entre registros o comas, pues la implementación contempla estos casos.
En caso de que aparezca error en la terminal,la razón sería que se está utilizando una instrucción no soportada.

---
## Instalación entorno toolchain

Se instaló el toolchain xPack RISC-V GCC (versión 13.2.0) para Windows, este incluye el ensamblador (riscv-none-elf-as) y objdump(riscv-none-elf-objdump), los cuáles son compatibles con la arquitectura RISC-V de 32 bits.

### Pasos de la instalación

- #### Paso 1: Instalar xpm
    `npm install --global xpm@latest`

- #### Paso 2: Instalar la versión 13.2.0

    `xpm install --global @xpack-dev-tools/riscv-none-elf-gcc@13.2.0-2.1`

- #### Paso 3: Encontrar la futa de instalación 

    `find ~/AppData/Roaming/xPacks -name "riscv-none-elf-gcc.exe" -type f`
- #### Paso 4: Agregar al PATH
  La ruta se copia hasta la carpeta bin.  
  A continuación se brinda un ejemplo:

  `echo 'export PATH="/c/Users/tu_usuario/AppData/Roaming/xPacks/@xpack-dev-tools/riscv-none-elf-gcc/13.2.0-2.1/.content/bin:$PATH"' >> ~/.bashrc`

  `source ~/.bashrc`
- #### Paso 5: Verificar instalación
  Para verificar que fue instalada exitosamente en el Git Bash debe aparecer la version instalada.
  
  `riscv-none-elf-gcc –version`

## Validación
Para validar el correcto funcionamiento del código se creo un archivo `validation.sh`.Su ejecucion es simple:
-   Primero se deben conceder permisos de ejecución al archivo una vez, con el comando: `chmod +x validation.sh`
- Luego se ejecuta sinplemente escribiendo en el Git Bash: `./validation.sh`
  













