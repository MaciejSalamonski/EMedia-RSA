import RSA
import ImageHandler

class ElectronicCodeBookCustom():
    def __init__(self, \
                 image, \
                 encryptedImage, \
                 decryptedImage, \
                 n, \
                 e, \
                 d, \
                 keyLength = None \
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

    def PngEncryption(self):
        imageToEncrypt = open(self.image, 'rb')
        hexString = imageToEncrypt.read().hex()

        positionOfPngHeaderInsideHexString = ImageHandler.FindPngHeader(hexString)

        if positionOfPngHeaderInsideHexString != -1:
            fourByteDataLenghtInHex = 8
            dataLength = ImageHandler.GetDataLegnth(hexString, positionOfPngHeaderInsideHexString)

            hexIdatData = hexString[(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex):(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex + dataLength)]
            idatData = ''

            currentBlocksLength = 0
            while currentBlocksLength < dataLength:
                if (currentBlocksLength + self.blockLength) > dataLength:
                    dataBlock = hexIdatData[currentBlocksLength:(currentBlocksLength + (dataLength - currentBlocksLength))]
                else:
                    dataBlock = hexIdatData[currentBlocksLength:currentBlocksLength + self.blockLength]

                currentBlocksLength += self.blockLength
                encrpytedBlock = self.BlockEncryption(dataBlock)
                idatData += encrpytedBlock

            newImage = ImageHandler.CreateAnIdat(hexString, \
                                                 idatData, \
                                                 positionOfPngHeaderInsideHexString, \
                                                 dataLength)
            ImageHandler.CreatePngFromHexString(self.encryptedImage, newImage)

    def BlockEncryption(self, dataBlock):
        hexBase = 16
        blocksLength = 512

        decDataBlock = int(dataBlock, hexBase)
        encryptedBlock = RSA.EncryptData(decDataBlock, self.n, self.e)
        hexEncryptedDataBlock = format(encrpytedBlock, 'x')

        while len(hexEncryptedDataBlock) % blocksLength != 0:
            hexEncryptedDataBlock += '0'

        return hexEncryptedDataBlock

     