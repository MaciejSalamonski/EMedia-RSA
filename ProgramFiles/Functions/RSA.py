def encrpyt(integersBlock, n, e):
    return pow(integersBlock, e, n)

def decrypt(cipher, n, d):
    return pow(cipher, d, n)