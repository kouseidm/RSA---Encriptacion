# 🔐 RSA Encriptación

Implementación del algoritmo de cifrado **RSA** desde cero en Python con interfaz gráfica.

---

## 📌 Descripción

Aplicación de escritorio que permite encriptar y desencriptar mensajes usando el algoritmo RSA, mostrando paso a paso el proceso matemático: generación de claves, selección de parámetros y cifrado por caracteres ASCII con codificación Base64.

---

## ✨ Características

- Validación de números primos `p` y `q`
- Cálculo automático de `n`, `φ(n)`, candidatos de `d` y clave pública `e`
- Encriptación carácter a carácter usando `c = m^e mod n`
- Desencriptación usando `m = c^d mod n`
- Codificación Base64 para el mensaje cifrado
- Exportación e importación de claves en `.txt`
- Consola de proceso paso a paso

---

## 🗂️ Estructura del proyecto

```
RSA-Encryption/
│
├── main.py           # Interfaz gráfica principal (Tkinter)
├── rsa_logic.py      # Funciones matemáticas del algoritmo RSA
├── file_handler.py   # Manejo de archivos: exportar e importar claves y mensajes
└── README.md
```

---

## ▶️ Cómo ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/kouseidm/RSA-Encryption.git
cd RSA-Encryption

# Ejecutar la aplicación
python main.py
```

> Requiere Python 3.x. No necesita dependencias externas, solo librerías estándar (`tkinter`, `base64`, `struct`).

---

## 🔑 Cómo usar

**Encriptar:**
1. Ingresa dos números primos `p` y `q` (el producto `n = p × q` debe ser mayor a 255)
2. Selecciona el valor de `d` de los candidatos válidos
3. Exporta las claves generadas en `.txt`
4. Escribe o carga el mensaje a encriptar
5. Guarda el mensaje cifrado

**Desencriptar:**
1. Importa el archivo `.txt` con las claves `(n, d)`
2. Pega o carga el mensaje cifrado en Base64
3. Obtén el mensaje original

---

## 🧮 Fundamento matemático

| Variable | Descripción |
|----------|-------------|
| `p`, `q` | Números primos distintos |
| `n = p × q` | Módulo RSA |
| `φ(n) = (p-1)(q-1)` | Función de Euler |
| `d` | Clave privada: `mcd(d, φ(n)) = 1` |
| `e` | Clave pública: `e × d ≡ 1 mod φ(n)` |
| `c = m^e mod n` | Encriptación |
| `m = c^d mod n` | Desencriptación |

---

## 👥 Autores

| Autor | GitHub |
|-------|--------|
| Alexis Huamán | [@kouseidm](https://github.com/kouseidm) |
| Antony Yomar | [@antonyyomar-dev](https://github.com/antonyyomar-dev) |
| Joseph Hidalgo | [@darkjoshid](https://github.com/darkjoshid) |
