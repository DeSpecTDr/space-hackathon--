import numpy as np
import math


class Line2D:
    """
    class describes a 2d-curve on flat

    ...
    Attributes
    ----------
    private (float, float) a, b - initial condition points
    private float ak, bk - initial condition derivatives
    private axis: bool - shows the orientation of curve: axis ? y(x) : x(y)

    K: float[1x4]

    is a Vector[1x4] from SLAE:
    if axis = 0:

                    (x**3)
                    (x**2)
    (y) = (A B C D) (x   )
                    (1   )

    if axis = 1:

                    (y**3)
                    (y**2)
    (x) = (A B C D) (y   )
                    (1   )

    Methods
    -------

    void __spline(self, a, ak, b, bk, axis)
        finds spline2D vector K[1x4] from initial conditions (a, ak, b, bk), where ak, bk = dy/dx in points a, b
        sets K field of an object


    (float, float) f(t), where 0 <= t <= 1
        returns (x, y) of curve, parametrized with t

    """

    def __init__(self, a, ak, b, bk, axis):
        # Инициализация происходит двумя точками на плоскости и заданными в них производными dy/dx в глобальной с.к.
        self.__a = a
        self.__b = b
        self.__ak = ak
        self.__bk = bk
        self.__axis = axis
        self.__K = [0, 0, 0, 0]

        self.__spline(a, ak, b, bk, axis)

    def __spline(self, a, ak, b, bk, axis):
        la = a
        lb = b

        if axis:
            la = (a[1], a[0])
            lb = (b[1], b[0])
            ak = 1 / ak
            bk = 1 / bk

        h = lb[0] - la[0]

        D0 = la[1]
        C0 = ak
        A0 = (h * bk - 2 * lb[1] + C0 * h + 2 * D0) / h ** 3
        B0 = (3 * lb[1] - h * bk - 2 * C0 * h - 3 * D0) / h ** 2

        A = A0
        B = B0 - 3 * A0 * la[0]
        C = 3 * A0 * la[0] ** 2 - 2 * B0 * la[0] + C0
        D = -C0 * la[0] + B0 * la[0] ** 2 - A0 * la[0] ** 3 + D0
        self.__K = [A, B, C, D]

    def get_K(self):
        return self.__K

    def get_axis(self):
        return self.__axis

    def get_IC(self):
        return self.__a, self.__ak, self.__b, self.__bk

    def f(self, t):  # firstly, linear
        if not (0 <= t <= 1):
            raise Exception('line2d: f', 't not in [0, 1]')
        else:
            h = self.__a[self.__axis] + (self.__b[self.__axis] - self.__a[self.__axis]) * t
            K = self.__K
            return h, K[0] * h ** 3 + K[1] * h ** 2 + K[2] * h + K[3]


class Quadrangle:
    '''
    Class, representing a quadrangle.

    ...
    Attributes
    ----------
    private Lines: Line2D[4] - contains border lines


    Methods
    ----------
    (float, float) Kuntz - F: [0, 1]^2 -> Inner area of 4 curves

    '''

    def __init__(self, Lines):
        self.__Lines = Lines

    def Kuntz(self, u, v):
        return (1 - v) * np.array(self.__Lines[0].f(1 - u)) + v * np.array(self.__Lines[3].f(1 - u)) + \
            np.flip((1 - u) * np.array(self.__Lines[1].f(v)) + u * np.array(self.__Lines[2].f(v))) - \
            np.flip(((1 - u) * (1 - v) * np.array(self.__Lines[1].f(0)) + u * (1 - v) * np.array(self.__Lines[2].f(0)) + \
                     v * (1 - u) * np.array(self.__Lines[1].f(1)) + u * v * np.array(self.__Lines[2].f(1))))

    def get_line(self, i):
        return self.__Lines[i]


def get_tangent_points(a, k):
    X = np.linspace(-0.1, 0.1, 10)
    Y = k*X
    return a[0]+X, a[1]+Y

def get_spline_points(a, b, K, axis):
    if axis:
        Y = np.linspace(a[1], b[1], 100)
        X = K[0]*Y**3+K[1]*Y**2+K[2]*Y+K[3]*np.ones(len(Y))
    else:
        X = np.linspace(a[0], b[0], 100)
        Y = K[0]*X**3+K[1]*X**2+K[2]*X+K[3]*np.ones(len(X))
    return X, Y