
# VARIABLES GLOBALES ───────────────────────────────────────────
n_global      = None
euler_global  = None
d_global      = None
e_global      = None
dec_resultado = None


def es_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True


def mcd(a, b):
    while b:
        a, b = b, a % b
    return a


def calcular_euler(p, q):
    return (p - 1) * (q - 1)


def obtener_candidatos_d(euler):
    return [d for d in range(2, euler) if mcd(d, euler) == 1]


def calcular_e(d, euler):
    return next(x for x in range(2, euler) if (x * d) % euler == 1)


def encriptar(mensaje, e, n):
    import base64, struct
    cifrados      = [pow(ord(c), e, n) for c in mensaje]
    raw_bytes     = b"".join(struct.pack(">I", c) for c in cifrados)
    return base64.b64encode(raw_bytes).decode("utf-8")


def desencriptar(mensaje_b64, d, n):
    import base64, struct
    raw_bytes = base64.b64decode(mensaje_b64.encode("utf-8"))
    cifrados  = [struct.unpack(">I", raw_bytes[i:i+4])[0] for i in range(0, len(raw_bytes), 4)]
    return "".join(chr(pow(c, d, n)) for c in cifrados)
