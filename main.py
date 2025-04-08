class TwoFish:

    def __init__(self, text: str, key: str):
        self._text: bytes = self.pad_text(bytes(text, encoding='utf-8'))
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
        pad_len: int = block_len - length % block_len
        return text + b'\0' * pad_len


if __name__ == '__main__':
    tf = TwoFish('ahdbaosijfaw' * 30, 'ahdbaosijfaw')
    print(tf.text)
    print(tf.key)