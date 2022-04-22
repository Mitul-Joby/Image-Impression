import os
from sys import argv, exit
from numpy import uint8
import numpy as np
from imageio import imwrite, imread
from argparse import ArgumentParser
import math
import cv2

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

def im2double(im):
    """method to get double precision of a channel"""
    info = np.iinfo(im.dtype) # Get the data type of the input image
    return im.astype(np.float64) / info.max


def SVD_compress_init(img,factor):
    #This function solely converts the image to seperate channels and calculate the decomposed matrices 
    # of each of these channels using SVD 
    # This alone does not lead to compression 
    # Dropping of the singular values along with the U and Vt counterparts is what leads to 
    # Compression
    print(factor)
    print(img.shape)
    b_channel = im2double(img[:,:,0])
    g_channel = im2double(img[:,:,1])
    r_channel = im2double(img[:,:,2])
    [u_r, s_i_r, vt_r] = np.linalg.svd(r_channel)
    [u_b, s_i_b, vt_b] = np.linalg.svd(b_channel)
    [u_g, s_i_g, vt_g] = np.linalg.svd(g_channel)
    # s_i_b : singular values intermedite, not diagonal array yet
    s_r = np.zeros(( b_channel.shape[0],b_channel.shape[1] ))
    s_b = np.diag(( b_channel.shape[0],b_channel.shape[1] ))
    s_g = np.diag(( b_channel.shape[0],b_channel.shape[1] ))
    print(s_i_r.shape)
    s_r[:img.shape[0],:img.shape[0]] = np.diag(s_i_r)
    s_b[:img.shape[0],:img.shape[0]] = np.diag(s_i_b)
    s_g[:img.shape[0],:img.shape[0]] = np.diag(s_i_g)
    print("Inital number of singular values : ",s_i_r.size,s_i_b.size,s_i_g.size)
    # [u_r_opt,s_r_opt,vt_r_opt] = drop_svals(u_r,s_r,vt_r,s_i_r.size/factor)
    # [u_g_opt,s_g_opt,vt_g_opt] = drop_svals(u_g,s_g,vt_g,s_i_g.size/factor)
    # [u_b_opt,s_b_opt,vt_b_opt] = drop_svals(u_b,s_b,vt_b,s_i_b.size/factor)
    # b_comp = np.dot(u_b_opt,s_b_opt,vt_b_opt)
    # g_comp = np.dot(u_g_opt,s_g_opt,vt_g_opt)
    # r_comp = np.dot(u_r_opt,s_r_opt,vt_r_opt)
    b_comp_t = np.dot(np.dot(u_b,s_b),vt_b)
    r_comp_t = np.dot(np.dot(u_r,s_r),vt_r)
    g_comp_t = np.dot(np.dot(u_g,s_g),vt_g)
    return cv2.merge((b_comp_t,g_comp_t,r_comp_t))

def drop_svals(u,s,vt,k): 

    # Assuming we want B to be of degree k, 
    # we will take the first k singular values, 
    # first k columns of U and first k rows of Vt
    # and get the closest we can get to A with degree k.
    # As for now im dropping x factor of total number of values
    # Later on we will have to optimise the the value of k and also the k's that are dropped
    opt_u = u[:,:math.ceil(k)] #First k cols of u 
    opt_s = s[:math.ceil(k),:math.ceil(k)] #First k cols and rows of k
    opt_vt = vt[:math.ceil(k),:] 
    return [opt_u,opt_s,opt_vt]





if __name__ == '__main__':

    parser = ArgumentParser(description='Simple Image Compresser')
    parser.add_argument('input', nargs='?', help='Input image')
    parser.add_argument('output', nargs='?', help='Output image')
    parser.add_argument('-f', '--factor', help='droppping factor, 0.25 means keep 1/4 the image data', default=0.5, type=float)

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

    print('Compressing...')

    # newMatrix = compressMatrix(average, args.size, matrix)
    comp_matrix = SVD_compress_init(matrix,args.factor)


    try:
        imwrite(args.output, comp_matrix)
    except:
        print('Warning: Invalid output file')
        inpPath = list(os.path.splitext(args.input))
        inpPath.insert(-1, '_compressed')
        args.output = ''.join(inpPath)

        imwrite(args.output, newMatrix)
        print(f'\nNew image at {args.output}')

    print('\nImage compressed successfully!\n')
