import binascii
import ImageHandler
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

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

        bytesDataBlock = bytes(dataBlock, asciiBase)
        encryptor = PKCS1_OAEP.new(self.publicKey)
        encryptedDataBlock = encryptor.encrypt(bytesDataBlock)
        hexEncryptedDataBlock = binascii.hexlify(encryptedDataBlock)
        hexEncryptedDataBlock = str(hexEncryptedDataBlock, hexBytesToHexString)

        while len(hexEncryptedDataBlock) % blockLength != 0:
            hexEncryptedDataBlock = '0' + hexEncryptedDataBlock
        
        return hexEncryptedDataBlock

    def PngEncryption(self):
        imageToEncrypt = open(self.image, 'rb')
        hexString = imageToEncrypt.read().hex()
        positionOfPngHeaderInsideHexString = ImageHandler.FindPngHeader(hexString)

        if positionOfPngHeaderInsideHexString != -1:
            currentBlocksLength = 0
            fourByteDataLenghtInHex = 8
            idatData = ''

            dataLength = ImageHandler.GetDataLegnth(hexString, positionOfPngHeaderInsideHexString)
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

            newImage = ImageHandler.CreateAnIdat(hexString, \
                                                 idatData, \
                                                 positionOfPngHeaderInsideHexString, \
                                                 dataLength)
            ImageHandler.CreatePngFromHexString(self.encryptedImage, newImage)

    def BlockDecryption(self, dataBlock):
        hexBytesToHexString = 'utf-8'
        evenLength = 2

        decryptor = PKCS1_OAEP.new(self.pairOfKeys)
        bytesDataBlock = str.encode(dataBlock)
        bytesDataBlock = binascii.unhexlify(bytesDataBlock)
        hexDecryptedDataBlock = decryptor.decrypt(bytesDataBlock)
        hexDecryptedDataBlock = str(hexDecryptedDataBlock, hexBytesToHexString)

        while len(hexDecryptedDataBlock) % evenLength != 0:
            hexDecryptedDataBlock = '0' + hexDecryptedDataBlock
        
        return hexDecryptedDataBlock

    def PngDecryption(self):
        imageToDecrypt = open(self.encryptedImage, 'rb')
        hexString = imageToEncrypt.read().hex()
        positionOfPngHeaderInsideHexString = ImageHandler.FindPngHeader(hexString)

        if positionOfPngHeaderInsideHexString != -1:
            currentBlocksLength = 0
            blocksLength = 512
            fourByteDataLenghtInHex = 8
            idatData = ''

            dataLength = ImageHandler.GetDataLegnth(hexString, positionOfPngHeaderInsideHexString)
            hexIdatData = hexString[(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex):(positionOfPngHeaderInsideHexString \
                                                                                                    + fourByteDataLenghtInHex \
                                                                                                    + dataLength)]

            while currentBlocksLength < dataLength
                dataBlock = hexIdatData[currentBlocksLength:(currentBlocksLength + blocksLength)]
                currentBlocksLength += blocksLength
                decryptedBlock = self.BlockDecryption(dataBlock)
                idatData += decryptedBlock
            
            newImage = ImageHandler.CreateAnIdat(hexString, \
                                                 idatData, \
                                                 positionOfPngHeaderInsideHexString, \
                                                 dataLength)
            ImageHandler.CreatePngFromHexString(self.decryptedImage, newImage)