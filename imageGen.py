from time import time
from numpy import uint8
from imageio import imwrite
from random import randrange, seed


def createSquareMatrix(n):
    matrix = []
    for row in range(n):
        matrix.append([])
        for column in range(n):
            randomRGB = []
            for _ in range(3):
                randomRGB.append(uint8(randrange(0, 255)))
            matrix[row].append(randomRGB)
    return matrix


class Matrix:
    def __init__(self, size):
        self.size = size
        self.matrix = createSquareMatrix(size)

    def getMatrix(self):
        return self.matrix

    def toImage(self):
        imwrite(f'./images/{self.size}x{self.size}.jpg', self.matrix)
        imwrite(f'./images/{self.size}x{self.size}.jpeg', self.matrix)
        imwrite(f'./images/{self.size}x{self.size}.png', self.matrix)
        imwrite(f'./images/{self.size}x{self.size}.tiff', self.matrix)
        imwrite(f'./images/{self.size}x{self.size}.bmp', self.matrix)


if __name__ == "__main__":
    seed(time())
    size = int(input("Enter number of pixels: "))
    matrix = Matrix(size)
    matrix.toImage()
