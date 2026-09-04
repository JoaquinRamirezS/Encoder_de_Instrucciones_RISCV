#!/usr/bin/env bash
set -uo pipefail

#Archivo donde se guardara la tabla
Output="tabla_validacion.md"

#Verificacion que el ensamblador este instalado y siponible en el PATH
if ! command -v riscv-none-elf-as > /dev/null 2>&1; then
    echo "ERROR: riscv-none-elf-as no encontrado."
    exit 1
fi
#Casos a probar:Se contemplan limites, positivos,negativos,desplazamientos 0 y registros x0.
Casos=(
    #FORMATO R
    "add x0, x7, x8" "add x1, x0, x9" "add x0, x0, x0"
    "sub x0, x9, x7" "sub x1, x0, x2" "sub x0, x0, x0"
    "and x5, x14, x0" "and x0, x1, x2" "and x0, x0, x0"
    "or x0, x2, x7"  "or x0, x4, x6"  "or x0, x0, x0"
    #FORMATO I
    "addi x6, x0, 2047" "addi x0, x2, -2048" "addi x0, x0, 0"
    "andi x0, x3, 2047" "andi x1, x0, -2048" "andi x0, x0, 0"
    "lw x14, 0(x8)"    "lw x9, -2048(x0)"  "lw x2, 2047(x3)"
    "lb x11, 0(x8)"    "lb x12, -2048(x0)"  "lb x7, 2047(x3)"
    #FORMATO S
    "sw x1, 0(x4)"    "sw x10, -2048(x9)"  "sw x2, 2047(x3)"
    "sb x3, 0(x4)"    "sb x15, -2048(x9)"  "sb x7, 2047(x3)"
    #FORMATO B
    "beq x0, x1, 0"   "beq x7, x8, -4096"   "beq x3, x4, 4094"
    "bne x0, x12, 0"   "bne x9, x10, -4096"   "bne x3, x4, 4094"
)
#Estructura del encabezado de la tabla
echo "# Tabla de validación contra toolchain oficial" > "$Output"
echo "" >> "$Output"
echo "| Instrucción | HEX oficial (objdump) | HEX herramienta (run.sh) | Coincidencia |" >> "$Output"
echo "|-------------|-----------------------|--------------------------|--------------|" >> "$Output"

# Bucle para probra cada instrucciones
for instr in "${Casos[@]}"; do
    echo "Probando: $instr"
    #Conversión para instrucciones de salto
    if [[ "$instr" =~ ^(beq|bne)[[:space:]]+([^,]+),[[:space:]]*([^,]+),[[:space:]]*([-+]?[0-9]+)$ ]]; then
        #Datos capturados
        mnemonic="${BASH_REMATCH[1]}"
        rs1="${BASH_REMATCH[2]}"
        rs2="${BASH_REMATCH[3]}"
        offset="${BASH_REMATCH[4]}"
        #Si el offset es negativo se aplica .-
        if [[ "$offset" == -* ]]; then
            instr_asm="$mnemonic $rs1, $rs2, .$offset"
        #Si es positivo se usa .+
        else
            instr_asm="$mnemonic $rs1, $rs2, .+$offset"
        fi
    else
        instr_asm="$instr"
    fi
    #Escribe archivo temporal .s
    echo ".text" > temp.s
    echo "$instr_asm" >> temp.s

    # Convierte temp.s a temp.o
    riscv-none-elf-as -march=rv32i -o temp.o temp.s 2> as_error.log
    if [ $? -ne 0 ] || [ ! -f temp.o ]; then
        hex_odicial="ERROR" #Si falla se asigna ERROR
    else
        #Se desensambla y se extrae el código hexadecimal de la isntrucción
        hex_odicial=$(riscv-none-elf-objdump -d temp.o 2>/dev/null | grep -E '^ +[0-9a-f]+:' | head -1 | awk '{print $2}')
        [ -z "$hex_odicial" ] && hex_odicial="ERROR" #Sino se obtuvo nada se asigna error
    fi
    #Ejecuta la instrucción con ./run.sh y guarda la salida
    #Busca la línea que contiene HEX y se toma la útlima coincidencia
    resultado=$(./run.sh "$instr" 2>/dev/null)
    hex_propio=$(echo "$resultado" | grep -i "HEX:" | tail -1 | awk '{print $NF}')
    [ -z "$hex_propio" ] && hex_propio="NO_OBTENIDO" # Sino se encuentra asignar NO OBTENIDO
    #Elimina 0X para comparar solo digitos
    if [ "${hex_odicial#0x}" == "${hex_propio#0x}" ]; then
        concidencia="PASS" #Si son iguales
    else
        concidencia="FAIL" #Sino coinciden
    fi
    #Escribir la fila en la tabla
    echo "| \`$instr\` | \`0x$hex_odicial\` | \`$hex_propio\` | $concidencia |" >> "$Output"
    #Eliminar archivos temporalew
    rm -f temp.s temp.o as_error.log
done
#Mensaje de generación
echo "Tabla generada en $Output"