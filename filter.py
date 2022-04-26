import os
import cv2 
import math
import numpy as np
from sys import argv, exit
from imageio import imwrite, imread
from argparse import ArgumentParser

def im2double(im):
    """Method to get double precision of a channel"""
    info = np.iinfo(im.dtype) # Get the data type of the input image
    return im.astype(np.float64) / info.max

def SVD_compress_init(img, R, G, B):
    """
    This function solely converts the image to seperate channels and calculate the decomposed matrices 
    of each of these channels using SVD. This alone does not lead to compression 
    Dropping of the singular values along with the U and Vt counterparts is what leads to compression
    """
    print(img.shape)
    b_channel = im2double(img[:,:,0])
    g_channel = im2double(img[:,:,1])
    r_channel = im2double(img[:,:,2])
    [u_r, s_i_r, vt_r] = np.linalg.svd(r_channel)
    [u_b, s_i_b, vt_b] = np.linalg.svd(b_channel)
    [u_g, s_i_g, vt_g] = np.linalg.svd(g_channel)
    print("Inital number of singular values : ", s_i_r.size,s_i_b.size,s_i_g.size)
    [u_r_opt, s_r_opt, vt_r_opt] = drop_svals(u_r, s_i_r, vt_r, B)
    [u_g_opt, s_g_opt, vt_g_opt] = drop_svals(u_g, s_i_g, vt_g, G)
    [u_b_opt, s_b_opt, vt_b_opt] = drop_svals(u_b, s_i_b, vt_b, R)
    print(s_b_opt.shape)
    b_comp_t = np.dot(np.dot(np.matrix( u_b_opt ),np.diag( s_b_opt )),np.matrix( vt_b_opt ))
    r_comp_t = np.dot(np.dot(np.matrix( u_r_opt ),np.diag( s_r_opt )),np.matrix( vt_r_opt ))
    g_comp_t = np.dot(np.dot(np.matrix( u_g_opt ),np.diag( s_g_opt )),np.matrix( vt_g_opt ))
    return cv2.merge((b_comp_t, g_comp_t, r_comp_t))

def drop_svals(u, s, vt, k): 
    """
    Assuming we want B to be of degree k, we will take the first k singular values, 
    first k columns of U and first k rows of Vt and get the closest we can get to A with degree k.
    As for now im dropping x factor of total number of values. Later on we will have to optimise 
    the the value of k and also the k's that are dropped
    """
    print(k)
    opt_u = u[:,:math.ceil(k)] #First k cols of u 
    opt_s = s[:math.ceil(k)] #First k values
    opt_vt = vt[:math.ceil(k),:] 
    return [opt_u, opt_s, opt_vt]


if __name__ == '__main__':

    parser = ArgumentParser(description='Simple Image Compresser')
    parser.add_argument('input', nargs='?', help='Input image')
    parser.add_argument('output', nargs='?', help='Output image')
    parser.add_argument('-r', '--red', help='Number of values to keep for red.', default=250, type=int)
    parser.add_argument('-g', '--green', help='Number of values to keep for green.', default=250, type=int)
    parser.add_argument('-b', '--blue', help='Number of values to keep for blue.', default=250, type=int)

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

    comp_matrix = SVD_compress_init(matrix, args.red, args.green, args.blue)

    try:
        imwrite(args.output, comp_matrix)
    except:
        print('Warning: Invalid output file')
        inpPath = list(os.path.splitext(args.input))
        inpPath.insert(-1, '_compressed')
        args.output = ''.join(inpPath)

        imwrite(args.output, comp_matrix)
        print(f'\nNew image at {args.output}')
