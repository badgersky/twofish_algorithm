class TwoFish:

    def __init__(self, text: str, key: str):
        self._text: bytes = self.pad_text(bytes(text, encoding='utf-8'), 16)
        self._key: bytes = bytes(key, encoding='utf-8')

        if len(self._key) not in (16, 24, 32):
            raise ValueError('Key must be 16 or 24 or 32 bytes')

    @property
    def text(self) -> bytes:
        return self._text

    @text.setter
    def text(self, value: bytes):
        self._text = value

    @property
    def key(self) -> bytes:
        return self._key

    @key.setter
    def key(self, value: bytes):
        self._key = value

    @staticmethod
    def pad_text(text: bytes, block_len) -> bytes:
        length: int = len(text)
        pad_len: int = block_len - length % block_len if length % block_len else 0
        return text + b'\0' * pad_len

    @staticmethod
    def from_bytes_little(b: bytes) -> int:
        result: int = 0

        for i in range(len(b)):
            result |= b[i] << (8 * i)

        return result

    def divide_text(self) -> list[list[bytes]]:
        length: int = len(self._text)
        blocks: list = []
        block: bytes

        for i in range(0, length, 16):
            block = self._text[i:i + 16]
            blocks.append([self.from_bytes_little(block[j:j + 4]) for j in range(0, len(block), 4)])

        return blocks


if __name__ == '__main__':
    tf = TwoFish('asdu' * 16, 'ayth' * 4)
    print(tf.divide_text())