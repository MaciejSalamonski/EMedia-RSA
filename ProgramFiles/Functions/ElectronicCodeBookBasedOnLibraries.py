import binascii
import ImageHandler

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class ElectronicCodeBookBasedOnLibraries():
    def __init__(self, \
                 image, \
                 encryptedImage, \
                 decryptedImage, \
                 n, \
                 e, \
                 d, \
                 blockLength = None):
        self.image = image
        self.encryptedImage = encryptedImage
        self.decryptedImage = decryptedImage
        self.KeysGenerator(n, e, d)
        (self.pairOfKeys, self.publicKey) = self.KeysGenerator(n, e, d)
        if blockLength is None:
            blockLength = 64
        self.blockLength = blockLength

    def KeysGenerator(self, n, e, d):
        pairOfKeys = RSA.construct((n, e, d))
        publicKey = pairOfKeys.publickey()

        return pairOfKeys, publicKey

    def BlockEncryption(self, dataBlock):
        asciiBase = 'ascii'
        blocksLength = 512
        hexBytesToHexString = 'utf-8'
        nullCharacter = '0'

        bytesDataBlock = bytes(dataBlock, asciiBase)
        encryptor = PKCS1_OAEP.new(self.publicKey)
        encryptedDataBlock = encryptor.encrypt(bytesDataBlock)
        hexBytesEncryptedDataBlock = binascii.hexlify(encryptedDataBlock)
        hexEncryptedDataBlock = str(hexBytesEncryptedDataBlock, hexBytesToHexString)

        while len(hexEncryptedDataBlock) % blocksLength != 0:
            hexEncryptedDataBlock = nullCharacter + hexEncryptedDataBlock
        
        return hexEncryptedDataBlock

    def PngEncryption(self):
        readBinaryFlag = 'rb'

        imageToEncrypt = open(self.image, readBinaryFlag)
        hexString = imageToEncrypt.read().hex()
        positionOfPngHeaderInsideHexString = ImageHandler.FindPngHeader(hexString)

        if positionOfPngHeaderInsideHexString != -1:
            currentBlocksLength = 0
            fourByteDataLenghtInHex = 8
            idatData = ''

            dataLength = ImageHandler.GetDataLength(hexString, positionOfPngHeaderInsideHexString)
            hexIdatData = hexString[(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex):(positionOfPngHeaderInsideHexString \
                                                                                                    + fourByteDataLenghtInHex \
                                                                                                    + dataLength)]

            while currentBlocksLength < dataLength:
                if (currentBlocksLength + self.blockLength) > dataLength:
                    dataBlock = hexIdatData[currentBlocksLength:(currentBlocksLength + (dataLength - currentBlocksLength))]
                else:
                    dataBlock = hexIdatData[currentBlocksLength:currentBlocksLength + self.blockLength]

                currentBlocksLength += self.blockLength
                encryptedBlock = self.BlockEncryption(dataBlock)
                idatData += encryptedBlock

            newImage = ImageHandler.CreateImageWithNewIdat(hexString, \
                                                           idatData, \
                                                           positionOfPngHeaderInsideHexString, \
                                                           dataLength)
            ImageHandler.CreatePngFromHexString(self.encryptedImage, newImage)

    def BlockDecryption(self, dataBlock):
        hexBytesToHexString = 'utf-8'
        evenLength = 2
        nullCharacter = '0'

        decryptor = PKCS1_OAEP.new(self.pairOfKeys)
        hexBytesDataBlock = str.encode(dataBlock)
        bytesDataBlock = binascii.unhexlify(hexBytesDataBlock)
        bytesDecryptedDataBlock = decryptor.decrypt(bytesDataBlock)
        hexDecryptedDataBlock = str(bytesDecryptedDataBlock, hexBytesToHexString)

        while len(hexDecryptedDataBlock) % evenLength != 0:
            hexDecryptedDataBlock = nullCharacter + hexDecryptedDataBlock
        
        return hexDecryptedDataBlock

    def PngDecryption(self):
        readBinaryFlag = 'rb'

        imageToDecrypt = open(self.encryptedImage, readBinaryFlag)
        hexString = imageToDecrypt.read().hex()
        positionOfPngHeaderInsideHexString = ImageHandler.FindPngHeader(hexString)

        if positionOfPngHeaderInsideHexString != -1:
            currentBlocksLength = 0
            blocksLength = 512
            fourByteDataLenghtInHex = 8
            idatData = ''

            dataLength = ImageHandler.GetDataLength(hexString, positionOfPngHeaderInsideHexString)
            hexIdatData = hexString[(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex):(positionOfPngHeaderInsideHexString \
                                                                                                    + fourByteDataLenghtInHex \
                                                                                                    + dataLength)]

            while currentBlocksLength < dataLength:
                dataBlock = hexIdatData[currentBlocksLength:(currentBlocksLength + blocksLength)]
                currentBlocksLength += blocksLength
                decryptedBlock = self.BlockDecryption(dataBlock)
                idatData += decryptedBlock
            
            newImage = ImageHandler.CreateImageWithNewIdat(hexString, \
                                                           idatData, \
                                                           positionOfPngHeaderInsideHexString, \
                                                           dataLength)
            ImageHandler.CreatePngFromHexString(self.decryptedImage, newImage)