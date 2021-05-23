def EncryptData(dataBlock, n, e):
    return pow(dataBlock, e, n)

def DecryptData(cipher, n, d):
    return pow(cipher, d, n)
