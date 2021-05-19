def EncryptData(decDataBlock, n, e):
    return pow(integersBlock, e, n)

def DecryptData(cipher, n, d):
    return pow(cipher, d, n)
