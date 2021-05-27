import os
import random

from Crypto.Util import number

def KeysGenerator(keyLength):
    minimumValueOfPublicKeyPart = 65537

    p = number.getPrime(keyLength)
    q = number.getPrime(keyLength)
    n = p * q
    multiplicativeFunction = (p - 1) * (q - 1)

    while True:
        e = random.randrange(minimumValueOfPublicKeyPart, multiplicativeFunction - 1)
        if number.GCD(e, multiplicativeFunction) == 1:
            break

    d = number.inverse(e, multiplicativeFunction)
    publicKey = (n, e)
    privateKey = d

    return publicKey, privateKey

def CreateKeyFiles(keyLength):
    writeFlag = 'w'
    publicKeyFilePath = '../Keys/PublicKey.txt'
    privateKeyFilePath = '../Keys/PrivateKey.txt'

    publicKey, privateKey = KeysGenerator(keyLength)

    publicKeyFile = open(publicKeyFilePath, writeFlag)
    publicKeyFile.write('%s,%s,%s' % (keyLength, publicKey[0], publicKey[1]))
    publicKeyFile.close()

    privateKeyFile = open(privateKeyFilePath, writeFlag)
    privateKeyFile.write('%s,%s' % (keyLength, privateKey))
    privateKeyFile.close()

def GetKeys(keyLength):
    readFlag = 'r'
    separator = ','
    publicKeyFilePath = '../Keys/PublicKey.txt'
    privateKeyFilePath = '../Keys/PrivateKey.txt'

    if not os.path.exists(publicKeyFilePath) and \
       not os.path.exists(privateKeyFilePath):
        CreateKeyFiles(keyLength)
    
    with open(publicKeyFilePath, readFlag) as PublicKey:
        for line in PublicKey:
            currentLine = line.split(separator)
            n = int(currentLine[1])
            e = int(currentLine[2])

    with open(privateKeyFilePath, readFlag) as PrivateKey:
        for line in PrivateKey:
            currentLine = line.split(separator)
            d = int(currentLine[1])

    return n, e, d