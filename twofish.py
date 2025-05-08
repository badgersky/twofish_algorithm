def key_schedule(key: str) -> tuple[list[str], list[str], list[str]]:
    f_key = pad_key(key)
    print(f_key)

    k = len(f_key) // 64
    m = ['0'] * 8 * k
    key_words = ['0'] * 2 * k

    for i in range(len(m)):
        m[i] = f_key[i * 8:(i + 1) * 8]
    print(m)

    for i in range(len(key_words)):
        tmp = 0
        for j in range(4):
            tmp += int(m[4 * i + j], 2) * pow(2, 8 * j)
        key_words[i] = bin(tmp)[2:].zfill(32)

    me = key_words[::2]
    mo = key_words[1::2]

    rs = [[1, 164, 85, 135, 90, 88, 219, 158],
          [164, 86, 130, 243, 30, 198, 104, 229],
          [2, 161, 252, 193, 71, 174, 61, 25],
          [164, 85, 135, 90, 88, 219, 158, 3]]

    s = []
    si = []
    for i in range(k):
        m2 = [
            [int(m[8 * i], 2)],
            [int(m[8 * i + 1], 2)],
            [int(m[8 * i + 2], 2)],
            [int(m[8 * i + 3], 2)],
            [int(m[8 * i + 4], 2)],
            [int(m[8 * i + 5], 2)],
            [int(m[8 * i + 6], 2)],
            [int(m[8 * i + 7], 2)],
        ]
        result = matrix_multiplication(rs, m2, 0x14D)
        tmp = bin(result[3][0])[2:].zfill(8) + bin(result[2][0])[2:].zfill(8) + bin(result[1][0])[2:].zfill(8) + bin(result[0][0])[2:].zfill(8)
        si.append(tmp)

    for i in range(k):
        s.append(si[k - i - 1])

    return me, mo, s

def matrix_multiplication(matrix1: list[list[int]], matrix2: list[list[int]], pol: int) -> list[list[int]]:
    result = [[0] * len(matrix2[0]) for _ in range(len(matrix1))]

    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix1[0])):
                result[i][j] ^= gf_mult(matrix1[i][k], matrix2[k][j], pol)

    return result

def gf_mult(a: int, b: int, pol: int) -> int:
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= pol
        b >>= 1

    return result

def pad_key(key: str) -> str:
    b = str_to_bin(key)
    if len(b) > 256:
        raise ValueError('key too long')
    if len(b) < 128:
        b += '0' * (128 - len(b))
        return b
    if len(b) < 192:
        b += '0' * (192 - len(b))
        return b
    if len(b) < 256:
        b += '0' * (256 - len(b))
        return b

def pad_input(text: str) -> tuple[str, int]:
    b = str_to_bin(text)
    padding = 0

    if len(b) % 128 != 0:
        while len(b) % 128 != 0:
            b += '0'
            padding += 1

    return b, padding

def divide_input_into_blocks(text: str) -> tuple[list[str], int]:
    padded_text, padding = pad_input(text)
    blocks = []
    for i in range(0, len(padded_text), 128):
        blocks.append(padded_text[i:i + 128])

    return blocks, padding

def str_to_bin(text: str) -> str:
    binary = []

    for char in text:
        binary.append(bin(ord(char))[2:].zfill(8))

    return ''.join(binary)

def bin_to_str(binary: str) -> str:
    return ''.join([chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)])


if __name__ == '__main__':
    stext = 'tekst do zaszyfrowania'
    skey = 'secret_key2183791237'


