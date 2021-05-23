import sys
import os
sys.path.append(os.path.abspath("Functions"))

from CipherBlockChaining import CipherBlockChaining
from ElectronicCodeBook import ElectronicCodeBook
from ElectronicCodeBookBasedOnLibraries import ElectronicCodeBookBasedOnLibraries
from KeysGenerator import GetKeys

if __name__ == '__main__':

    keyLength = 1024
    n, e, d = GetKeys(keyLength)

    imagePath = '../Images/example.png'

    encryptedElectronicCodeBookPath = '../EncryptedImages/exampleEncryptedElectronicCodeBook.png'
    decryptedElectronicCodeBookPath = '../DecryptedImages/exampleDecryptedElectronicCodeBook.png'

    encryptedElectronicCodeBookBasedOnLibrariesPath = '../EncryptedImages/exampleEncryptedElectronicCodeBookBasedOnLibraries.png'
    decryptedElectronicCodeBookBasedOnLibrariesPath = '../DecryptedImages/exampleDecryptedElectronicCodeBookBasedOnLibraries.png'

    encryptedCipherBlockChainingPath = '../EncryptedImages/exampleEncryptedCipherBlockChaining.png'
    decryptedCipherBlockChainingPath = '../DecryptedImages/exampleDecryptedCipherBlockChaining.png'

    electronicCodeBook = ElectronicCodeBook(imagePath, \
                                            encryptedElectronicCodeBookPath, \
                                            decryptedElectronicCodeBookPath, \
                                            n, \
                                            e, \
                                            d)
    electronicCodeBook.PngEncryption()
    electronicCodeBook.PngDecryption()

    electronicCodeBookBasedOnLibraries = ElectronicCodeBookBasedOnLibraries(imagePath, \
                                                                            encryptedElectronicCodeBookBasedOnLibrariesPath, \
                                                                            decryptedElectronicCodeBookBasedOnLibrariesPath, \
                                                                            n, \
                                                                            e, \
                                                                            d)
    electronicCodeBookBasedOnLibraries.PngEncryption()
    electronicCodeBookBasedOnLibraries.PngDecryption()

    cipherBlockChaining = CipherBlockChaining(imagePath, \
                                              encryptedCipherBlockChainingPath, \
                                              decryptedCipherBlockChainingPath, \
                                              n, \
                                              e, \
                                              d)
    cipherBlockChaining.PngEncryption()
    cipherBlockChaining.PngDecryption()