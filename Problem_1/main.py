from kuntz import *
from convert_to_su2 import convert
import matplotlib.pyplot as plt




def make_trap_mesh(b, alpha, N_x, N_y, filename):
    """

    :param b: jet diameter
    :param alpha: degrees of inclined plate
    :return: None

    creates and saves mesh into <filename>.dat
    """


    """
    CONSTANTS
    """
    l = 120  # length of plate (ochevidno from picture)

    """
    VARIABLES
    """
    #b = 0.04  # jet diameter
    #alpha = 30  # degrees of inclined plate
    alpha_rad = math.pi / 180 * alpha

    INF = 99999999999999999999999999999

    COEF_DENS = 1
    #N_x = 100
    #N_y = 40

    X1 = np.linspace(0, 1 - 1 / (N_x * COEF_DENS), N_x * COEF_DENS)
    Y1 = np.linspace(0, 1, N_y * COEF_DENS)

    Q1 = Quadrangle([Line2D([0, 0], -math.tan(alpha_rad),
                            [l * math.cos(-alpha_rad), l * math.sin(-alpha_rad)], -math.tan(alpha_rad), 0),
                     Line2D([l * math.cos(-alpha_rad), l * math.sin(-alpha_rad)], INF, [l * math.cos(-alpha_rad), b],
                            INF, 1),
                     Line2D([0, 0], INF, [0, b], INF, 1),
                     Line2D([0, b], 0, [l * math.cos(-alpha_rad), b], 0, 0)])

    K1 = np.ndarray(shape=(len(Y1), len(X1), 2), dtype=float)
    for i in range(len(Y1)):
        for j in range(len(X1)):
            K1[i, j] = Q1.Kuntz(X1[j], Y1[i])

    SK = np.flip(K1, (1, 0))

    with open(filename + '.dat', 'w') as f:
        f.write(str(N_y) + ' ' + str(N_x) + '\n')
        for i in range(len(SK)):
            for j in range(len(SK[0])):
                f.write(str(SK[i][j][0]))
                f.write(' ')
                f.write(str(SK[i][j][1]))
                f.write('\n')



def main():
    filename = 'test_mesh'
    make_trap_mesh(0.04, 3, 100, 50, filename)
    convert(filename)

if __name__ == '__main__':
    main()