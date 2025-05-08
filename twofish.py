def generate_round_keys(me: list[str], mo: list[str]) -> list[str]:
    rho = pow(2, 24) + pow(2, 16) + pow(2, 8) + pow(2, 0)

    k = []
    for i in range(20):
        a = bin(2 * i * rho)[2:].zfill(32)
        key1 = int(h_func(a, me), 2)

        b = bin(((2 * i) + 1) * rho)[2:].zfill(32)
        key2 = int(rotate_left(h_func(b, mo), 8, 32), 2)

        k.append(bin((key1 + key2) % pow(2, 32))[2:].zfill(32))
        k.append(rotate_left(bin((key1 + (2 * key2)) % pow(2, 32))[2:].zfill(32), 9, 32))

    return k

def h_func(word: str, words_l: list[str]) -> str:
    mds = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    if len(words_l) == 4:
        x0 = word[24:32]
        x1 = word[16:24]
        x2 = word[8:16]
        x3 = word[:8]

        x0 = q1(x0)
        x1 = q0(x1)
        x2 = q0(x2)
        x3 = q1(x3)

        word = x3 + x2 + x1 + x0
        word = int(word, 2) ^ int(words_l[3], 2)
        word = bin(word)[2:].zfill(32)

    if len(words_l) >= 3:
        x0 = word[24:32]
        x1 = word[16:24]
        x2 = word[8:16]
        x3 = word[:8]

        x0 = q1(x0)
        x1 = q1(x1)
        x2 = q0(x2)
        x3 = q0(x3)

        word = x3 + x2 + x1 + x0
        word = int(word, 2) ^ int(words_l[2], 2)
        word = bin(word)[2:].zfill(32)

    x0 = word[24:32]
    x1 = word[16:24]
    x2 = word[8:16]
    x3 = word[:8]

    x0 = q0(x0)
    x1 = q1(x1)
    x2 = q0(x2)
    x3 = q1(x3)

    word = x3 + x2 + x1 + x0
    word = int(word, 2) ^ int(words_l[1], 2)
    word = bin(word)[2:].zfill(32)

    x0 = word[24:32]
    x1 = word[16:24]
    x2 = word[8:16]
    x3 = word[:8]

    x0 = q0(x0)
    x1 = q0(x1)
    x2 = q1(x2)
    x3 = q1(x3)

    word = x3 + x2 + x1 + x0
    word = int(word, 2) ^ int(words_l[0], 2)
    word = bin(word)[2:].zfill(32)

    x0 = word[24:32]
    x1 = word[16:24]
    x2 = word[8:16]
    x3 = word[:8]

    x0 = q1(x0)
    x1 = q0(x1)
    x2 = q1(x2)
    x3 = q0(x3)

    word_v = [[int(x0, 2)], [int(x1, 2)], [int(x2, 2)], [int(x3, 2)]]
    c = matrix_multiplication(mds, word_v, 0x169)
    res = bin(c[3][0])[2:].zfill(8) + bin(c[2][0])[2:].zfill(8) + bin(c[1][0])[2:].zfill(8) + bin(c[0][0])[2:].zfill(8)
    return res

def q0(num: str) -> str:
    num = int(num, 2)
    t0 = [8, 1, 7, 13, 6, 15, 3, 2, 0, 11, 5, 9, 14, 12, 10, 4]
    t1 = [14, 12, 11, 8, 1, 2, 3, 5, 15, 4, 10, 6, 7, 0, 9, 13]
    t2 = [11, 10, 5, 14, 6, 13, 9, 0, 12, 8, 15, 3, 2, 4, 7, 1]
    t3 = [13, 7, 15, 4, 1, 2, 6, 14, 9, 11, 3, 0, 8, 5, 12, 10]

    a0 = num // 16
    b0 = num % 16

    a1 = a0 ^ b0
    b1 = ((a0 ^ int(rotate_right(bin(b0)[2:].zfill(4), 1, 4), 2)) ^ (8 * a0)) % 16

    a2 = t0[a1]
    b2 = t1[b1]

    a3 = a2 ^ b2
    b3 = ((a2 ^ int(rotate_right(bin(b2)[2:].zfill(4), 1, 4), 2)) ^ (8 * a2)) % 16

    a4 = t2[a3]
    b4 = t3[b3]

    result = 16 * b4 + a4
    return bin(result)[2:].zfill(8)

def q1(num: str) -> str:
    num = int(num, 2)
    t0 = [2, 8, 11, 13, 15, 7, 6, 14, 3, 1, 9, 4, 0, 10, 12, 5]
    t1 = [1, 14, 2, 11, 4, 12, 3, 7, 6, 13, 10, 5, 15, 9, 0, 8]
    t2 = [4, 12, 7, 5, 1, 6, 9, 10, 0, 14, 13, 8, 2, 11, 3, 15]
    t3 = [11, 9, 5, 1, 12, 3, 13, 14, 6, 4, 7, 15, 2, 0, 8, 10]

    a0 = num // 16
    b0 = num % 16

    a1 = a0 ^ b0
    b1 = ((a0 ^ int(rotate_right(bin(b0)[2:].zfill(4), 1, 4), 2)) ^ (8 * a0)) % 16

    a2 = t0[a1]
    b2 = t1[b1]

    a3 = a2 ^ b2
    b3 = ((a2 ^ int(rotate_right(bin(b2)[2:].zfill(4), 1, 4), 2)) ^ (8 * a2)) % 16

    a4 = t2[a3]
    b4 = t3[b3]

    result = 16 * b4 + a4
    return bin(result)[2:].zfill(8)

def rotate_right(num: str, x: int, width: int) -> str:
    rotated = num[-(x % width):] + num[:-(x % width)]
    return rotated

def rotate_left(num: str, x: int, width: int) -> str:
    rotated = num[(x % width):] + num[:(x % width)]
    return rotated

def key_schedule(key: str) -> tuple[list[str], list[str], list[str]]:
    f_key = pad_key(key)

    k = len(f_key) // 64
    m = ['0'] * 8 * k
    key_words = ['0'] * 2 * k

    for i in range(len(m)):
        m[i] = f_key[i * 8:(i + 1) * 8]

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

def g_func(word: str, s: list[str]) -> str:
    return h_func(word, s)

def f_func(word1: str, word2: str, round: int, k: list[str], s: list[str]) -> tuple[str, str]:
    t0 = g_func(word1, s)
    t1 = g_func(rotate_left(word2, 8, 32), s)

    f0 = (int(t0, 2) + int(t1, 2) + int(k[2 * round + 8], 2)) % pow(2, 32)
    f1 = (int(t0, 2) + 2 * int(t1, 2) + int(k[2 * round + 9], 2)) % pow(2, 32)

    f0 = bin(f0)[2:].zfill(32)
    f1 = bin(f1)[2:].zfill(32)
    return f0, f1

def input_whitening_cypher(text: str, k: list[str]) -> tuple[str, str, str, str]:
    r0 = text[0:32]
    r1 = text[32:64]
    r2 = text[64:96]
    r3 = text[96:128]

    r0 = bin(int(r0, 2) ^ int(k[0], 2))[2:].zfill(32)
    r1 = bin(int(r1, 2) ^ int(k[1], 2))[2:].zfill(32)
    r2 = bin(int(r2, 2) ^ int(k[2], 2))[2:].zfill(32)
    r3 = bin(int(r3, 2) ^ int(k[3], 2))[2:].zfill(32)

    return r0, r1, r2, r3

def output_whitening_cypher(r0: str, r1: str, r2: str, r3: str,  k: list[str]) -> tuple[str, str, str, str]:
    r0 = bin(int(r0, 2) ^ int(k[4], 2))[2:].zfill(32)
    r1 = bin(int(r1, 2) ^ int(k[5], 2))[2:].zfill(32)
    r2 = bin(int(r2, 2) ^ int(k[6], 2))[2:].zfill(32)
    r3 = bin(int(r3, 2) ^ int(k[7], 2))[2:].zfill(32)

    return r0, r1, r2, r3

def encrypt(text: str, key: str) -> str:
    me, mo, s = key_schedule(key)
    blocks, padding = divide_input_into_blocks(text)
    k = generate_round_keys(me, mo)
    res_blocks = []

    temp = '0' * 128
    for block in blocks:
        r0, r1, r2, r3 = input_whitening_cypher(block, k)

        f0, f1 = f_func(r0, r1, 0, k, s)
        c2 = rotate_right(bin(int(f0, 2) ^ int(r2, 2))[2:].zfill(32), 1, 32)
        c3 = bin(int(rotate_left(r3, 1, 32), 2) ^ int(f1, 2))[2:].zfill(32)

        for i in range(15):
            r2, r3, r0, r1 = r0, r1, c2, c3
            f0, f1 = f_func(r0, r1, i + 1, k, s)
            c2 = rotate_right(bin(int(f0, 2) ^ int(r2, 2))[2:].zfill(32), 1, 32)
            c3 = bin(int(rotate_left(r3, 1, 32), 2) ^ int(f1, 2))[2:].zfill(32)


        r0, r1, r2, r3 = output_whitening_cypher(r0, r1, r2, r3, k)
        temp = r0 + r1 + r2 + r3
        res_blocks.append(temp)

    res = ''.join(res_blocks)
    return res

if __name__ == '__main__':
    msg = "a"
    k = "a"

    encrypted = encrypt(msg, k)
    print(hex(int(encrypted, 0))[2:].zfill(32))