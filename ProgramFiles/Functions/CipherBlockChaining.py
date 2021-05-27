import ImageHandler
import random
import RSA

class CipherBlockChaining():
    def __init__(self, \
                 image, \
                 encryptedImage, \
                 decryptedImage, \
                 n, \
                 e, \
                 d, \
                 keyLength = 1024, \
                 blockLength = 256):
        self.image = image
        self.encryptedImage = encryptedImage
        self.decryptedImage = decryptedImage
        self.n = n
        self.e = e
        self.d = d
        self.keyLength = keyLength
        self.blockLength = blockLength
        self.initVector = random.getrandbits(blockLength)
        self.previouslyVector = None

    def ExclusiveOrOfTwoElements(self, dataBlock, vector):
        return dataBlock ^ vector

    def BlockEncryption(self, dataBlock):
        blocksLength = 512
        hexBase = 16
        hexFormat = 'x'
        nullCharacter = '0'

        decDataBlock = int(dataBlock, hexBase)
        xoredDataBlock = self.ExclusiveOrOfTwoElements(decDataBlock, self.initVector) \
                            if self.previouslyVector == None \
                            else self.ExclusiveOrOfTwoElements(decDataBlock, self.previouslyVector)

        encryptedBlock = RSA.EncryptData(xoredDataBlock, self.n, self.e)
        self.previouslyVector = encryptedBlock
        hexEncryptedDataBlock = format(encryptedBlock, hexFormat)

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

            self.previouslyVector = None

            newImage = ImageHandler.CreateImageWithNewIdat(hexString, \
                                                           idatData, \
                                                           positionOfPngHeaderInsideHexString, \
                                                           dataLength)
            ImageHandler.CreatePngFromHexString(self.encryptedImage, newImage)

    def BlockDecryption(self, dataBlock):
        hexBase = 16
        hexFormat = 'x'
        evenLength = 2
        nullCharacter = '0'

        decDataBlock = int(dataBlock, hexBase)
        decryptedBlock = RSA.DecryptData(decDataBlock, self.n, self.d)
        xoredDecryptedDataBlock = self.ExclusiveOrOfTwoElements(decryptedBlock, self.initVector) \
                                     if self.previouslyVector == None \
                                     else self.ExclusiveOrOfTwoElements(decryptedBlock, self.previouslyVector)

        self.previouslyVector = decDataBlock
        hexXoredDecryptedDataBlock = format(xoredDecryptedDataBlock, hexFormat)

        while len(hexXoredDecryptedDataBlock) % evenLength != 0:
            hexXoredDecryptedDataBlock = nullCharacter + hexXoredDecryptedDataBlock

        return hexXoredDecryptedDataBlock

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