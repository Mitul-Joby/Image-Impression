import os
from sys import argv, exit
from numpy import uint8
from imageio import imwrite, imread
from argparse import ArgumentParser


def average(matrix):
    R, G, B = 0, 0, 0
    for row in matrix:
        for pixel in row:
            R += pixel[0]
            G += pixel[1]
            B += pixel[2]
    l = (len(matrix) * len(matrix[0]))
    return [uint8(R/l), uint8(G/l), uint8(B/l)]


def compressMatrix(callback, size, matrix):
    X, Y, Z = matrix.shape
    print(X,Y,Z)
    X = int(X/size)
    Y = int(Y/size)

    newMatrix = []

    for x in range(0, X):
        row = []
        for y in range(0, Y):
            row.append(callback(matrix[x*size:x*size+size, y*size:y*size+size]))
        newMatrix.append(row)
    return newMatrix


if __name__ == '__main__':

    parser = ArgumentParser(description='Simple Image Compresser')
    parser.add_argument('input', nargs='?', help='Input image')
    parser.add_argument('output', nargs='?', help='Output image')
    parser.add_argument('-s', '--size', help='Compression Rate Factor Size', default=4, type=int)

    args = parser.parse_args()

    if len(argv) <= 2:
        parser.print_help()
        exit(1)

    matrix = []

    try:
        matrix = imread(args.input)
    except:
        print('Error: Invalid input file')
        exit(1)

    newMatrix = compressMatrix(average, args.size, matrix)

    print('Compressing...')

    try:
        imwrite(args.output, newMatrix)
    except:
        print('Warning: Invalid output file')
        inpPath = list(os.path.splitext(args.input))
        inpPath.insert(-1, '_compressed')
        args.output = ''.join(inpPath)

        imwrite(args.output, newMatrix)
        print(f'\nNew image at {args.output}')

    print('\nImage compressed successfully!\n')
