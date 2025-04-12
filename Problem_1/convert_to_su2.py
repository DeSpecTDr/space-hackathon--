# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 13:19:28 2024

@author: alexl
"""
import numpy as np


def npnt(i, j, jmax):
    return j + i * jmax


def convert(filename):
    struct_mesh = filename + '.dat'
    su2_mesh = filename + '.su2'
    with open(struct_mesh, 'r') as f:
        dims = [int(x) for x in f.readline().split()]
        grd = f.readlines()
    print(dims)
    # print (grd)

    NELEM = (dims[0] - 1) * (dims[1] - 1)
    NPOIN = dims[0] * dims[1]

    if len(grd) != NPOIN:
        print('Error in struct_mesh file!!!')
        exit()
    with open(su2_mesh, 'w') as f:
        f.write('%\n')
        f.write('% Problem dimension\n')
        f.write('%\n')
        f.write('NDIME= 2\n')
        f.write('%\n')
        f.write('% Inner element connectivity\n')
        f.write('%\n')
        f.write('NELEM= ' + str(NELEM) + '\n')
        nel = 0
        for i in range(dims[0] - 1):
            for j in range(dims[1] - 1):
                f.write(' 9  {0} {1} {2} {3} {4}\n'.format(npnt(i, j, dims[1]), npnt(i, j + 1, dims[1]),
                                                           npnt(i + 1, j + 1, dims[1]), npnt(i + 1, j, dims[1]), nel))
                nel += 1

        f.write('%\n')
        f.write('% Node coordinates \n')
        f.write('%\n')
        f.write('NPOIN= ' + str(NPOIN) + '\n')
        for ist, st in enumerate(grd):
            f.write(st[:-1] + ' ' + str(ist) + '\n')
        f.write('%\n')
        f.write('% Boundary elements \n')
        f.write('%\n')
        f.write('NMARK= 4\n')
        f.write('MARKER_TAG= inlet\n')
        f.write('MARKER_ELEMS= ' + str(dims[0] - 1) + '\n')
        for i in range(dims[0] - 1):
            f.write(' 3  {0} {1}\n'.format(npnt(i, 0, dims[1]), npnt(i + 1, 0, dims[1])))

        f.write('MARKER_TAG= lower\n')
        f.write('MARKER_ELEMS= ' + str(dims[1] - 1) + '\n')
        for j in range(dims[1] - 1):
            f.write(' 3  {0} {1}\n'.format(npnt(0, j, dims[1]), npnt(0, j + 1, dims[1])))

        f.write('MARKER_TAG= outlet\n')
        f.write('MARKER_ELEMS= ' + str(dims[0] - 1) + '\n')
        for i in range(dims[0] - 2, -1, -1):
            f.write(' 3  {0} {1}\n'.format(npnt(i, dims[1] - 1, dims[1]), npnt(i + 1, dims[1] - 1, dims[1])))

        f.write('MARKER_TAG= upper\n')
        f.write('MARKER_ELEMS= ' + str(dims[1] - 1) + '\n')
        for j in range(dims[1] - 1):
            f.write(' 3  {0} {1}\n'.format(npnt(dims[0] - 1, j + 1, dims[1]), npnt(dims[0] - 1, j, dims[1])))
