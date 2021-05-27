def EncryptData(decDataBlock, n, e):
    return pow(decDataBlock, e, n)

def DecryptData(decCipher, n, d):
    return pow(decCipher, d, n)