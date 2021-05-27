import ImageHandler
import RSA

class ElectronicCodeBook():
    def __init__(self, \
                 image, \
                 encryptedImage, \
                 decryptedImage, \
                 n, \
                 e, \
                 d, \
                 keyLength = None, \
                 blockLength = None):
        self.image = image
        self.encryptedImage = encryptedImage
        self.decryptedImage = decryptedImage
        self.n = n
        self.e = e
        self.d = d

        if not keyLength:
            keyLength = 1024
        self.keyLength = keyLength

        if not blockLength:
            blockLength = 256
        self.blockLength = blockLength

    def BlockEncryption(self, dataBlock):
        hexBase = 16
        hexFormat = 'x'
        blocksLength = 512
        nullCharacter = '0'

        decDataBlock = int(dataBlock, hexBase)
        encryptedBlock = RSA.EncryptData(decDataBlock, self.n, self.e)
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
        hexDecryptedDataBlock = format(decryptedBlock, hexFormat)

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