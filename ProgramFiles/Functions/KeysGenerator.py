import os
import random

from Crypto.Util import number

def KeysGenerator(keyLength):
    p = number.getPrime(keyLength)
    q = number.getPrime(keyLength)
    n = p * q

    square = 2
    multiplicativeFunction = (p - 1) * (q - 1)

    while True:
        e = random.randrange(square ** (keyLength - 1), square ** (keyLength))
        if number.GCD(e, multiplicativeFunction) == 1:
            break

    d = number.inverse(e, multiplicativeFunction)
    publicKey = (n, e)
    privateKey = d

    return publicKey, privateKey

def CreateKeyFiles(keyLength):
    publicKey, privateKey = KeysGenerator(keyLength)

    publicKeyFile = open('../Keys/PublicKey.txt', 'w')
    publicKeyFile.write('%s,%s,%s' % (keyLength, publicKey[0], publicKey[1]))
    publicKeyFile.close()

    privateKeyFile = open('../Keys/PrivateKey.txt', 'w')
    privateKeyFile.write('%s,%s' % (keyLength, privateKey))
    privateKeyFile.close()

def GetKeys(keyLength):
    if not os.path.exists('../Keys/PublicKey.txt') and \
       not os.path.exists('../Keys/PrivateKey.txt'):
        CreateKeyFiles(keyLength)
    
    with open('../Keys/PublicKey.txt', 'r') as PublicKey:
        for line in PublicKey:
            currentLine = line.split(",")
            n = int(currentLine[1])
            e = int(currentLine[2])

    with open('../Keys/PrivateKey.txt', 'r') as PrivateKey:
        for line in PrivateKey:
            currentLine = line.split(",")
            d = int(currentLine[1])

    return n, e, d