# Tabla de validación contra toolchain oficial

| Instrucción | HEX oficial (objdump) | HEX herramienta (run.sh) | Coincidencia |
|-------------|-----------------------|--------------------------|--------------|
| `add x5, x6, x7` | `0x007302b3` | `0x007302b3` | PASS |
| `add x0, x1, x2` | `0x00208033` | `0x00208033` | PASS |
| `add x15, x15, x15` | `0x00f787b3` | `0x00f787b3` | PASS |
| `sub x5, x6, x7` | `0x407302b3` | `0x407302b3` | PASS |
| `sub x0, x1, x2` | `0x40208033` | `0x40208033` | PASS |
| `sub x10, x0, x5` | `0x40500533` | `0x40500533` | PASS |
| `and x5, x6, x7` | `0x007372b3` | `0x007372b3` | PASS |
| `and x0, x1, x2` | `0x0020f033` | `0x0020f033` | PASS |
| `and x10, x10, x10` | `0x00a57533` | `0x00a57533` | PASS |
| `or x5, x6, x7` | `0x007362b3` | `0x007362b3` | PASS |
| `or x0, x1, x2` | `0x0020e033` | `0x0020e033` | PASS |
| `or x10, x10, x10` | `0x00a56533` | `0x00a56533` | PASS |
| `addi x5, x0, 10` | `0x00a00293` | `0x00a00293` | PASS |
| `addi x5, x0, -10` | `0xff600293` | `0xff600293` | PASS |
| `addi x5, x0, 2047` | `0x7ff00293` | `0x7ff00293` | PASS |
| `andi x5, x0, 10` | `0x00a07293` | `0x00a07293` | PASS |
| `andi x5, x0, -10` | `0xff607293` | `0xff607293` | PASS |
| `andi x5, x0, 2047` | `0x7ff07293` | `0x7ff07293` | PASS |
| `lw x5, 0(x6)` | `0x00032283` | `0x00032283` | PASS |
| `lw x5, -100(x6)` | `0xf9c32283` | `0xf9c32283` | PASS |
| `lw x5, 2047(x6)` | `0x7ff32283` | `0x7ff32283` | PASS |
| `lb x5, 0(x6)` | `0x00030283` | `0x00030283` | PASS |
| `lb x5, -100(x6)` | `0xf9c30283` | `0xf9c30283` | PASS |
| `lb x5, 2047(x6)` | `0x7ff30283` | `0x7ff30283` | PASS |
| `sw x5, 0(x6)` | `0x00532023` | `0x00532023` | PASS |
| `sw x5, -100(x6)` | `0xf8532e23` | `0xf8532e23` | PASS |
| `sw x5, 2047(x6)` | `0x7e532fa3` | `0x7e532fa3` | PASS |
| `sb x5, 0(x6)` | `0x00530023` | `0x00530023` | PASS |
| `sb x5, -100(x6)` | `0xf8530e23` | `0xf8530e23` | PASS |
| `sb x5, 2047(x6)` | `0x7e530fa3` | `0x7e530fa3` | PASS |
| `beq x5, x6, 0` | `0x00628063` | `0x00628063` | PASS |
| `beq x5, x6, -8` | `0xfe628ce3` | `0xfe628ce3` | PASS |
| `beq x5, x6, 124` | `0x06628e63` | `0x06628e63` | PASS |
| `bne x5, x6, 0` | `0x00629063` | `0x00629063` | PASS |
| `bne x5, x6, -8` | `0xfe629ce3` | `0xfe629ce3` | PASS |
| `bne x5, x6, 124` | `0x06629e63` | `0x06629e63` | PASS |
