def FindPngHeader(hexString):
    pngHeader = "49444154"

    return hexString.find(pngHeader)

def GetDataLength(hexString, positionOfPngHeaderInsideHexString):
    fourByteDataLenghtInHex = 8
    hexBase = 16
    sizeOfChar = 2

    hexDataLength = hexString[(positionOfPngHeaderInsideHexString - fourByteDataLenghtInHex):positionOfPngHeaderInsideHexString]
    decDataLengthChunk = int(hexDataLength, hexBase)
    dataLength = sizeOfChar * decDataLengthChunk

    return dataLength

def CreatePngFromHexString(newImageName, dataForImageCreation):
    writeAndBinaryFlag = 'wb'

    data = bytes.fromhex(dataForImageCreation)

    with open(newImageName, writeAndBinaryFlag) as newImage:
        newImage.write(data)
    newImage.close()

def CreateImageWithNewIdat(hexString, idatData, positionOfPngHeaderInsideHexString, dataLength):
    fourByteDataLenghtInHex = 8
    twoDigitHexInsideDataString = 2
    dataStartPosition = 0
    nullCharacter = '0'
    hexFormat = 'x'

    idatLength = int(len(idatData) / twoDigitHexInsideDataString)
    hexIdatLength = format(idatLength, hexFormat)

    dataBeforeIdat = hexString[dataStartPosition:(positionOfPngHeaderInsideHexString - fourByteDataLenghtInHex)]
    idatHeader = hexString[positionOfPngHeaderInsideHexString:(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex)]
    restPngData = hexString[(positionOfPngHeaderInsideHexString + fourByteDataLenghtInHex + dataLength):]

    while len(hexIdatLength) % fourByteDataLenghtInHex != 0:
        hexIdatLength = nullCharacter + hexIdatLength

    newImage = dataBeforeIdat + hexIdatLength + idatHeader + idatData + restPngData 

    return newImage