from math import *
import matplotlib.pyplot as plt

def hatfunc(vec, dy):
    one_over_dy_square = []
    for i in dy:
        one_over_dy_square.append(1 / i ** 2)
    vec_over_dy_square = []
    for i in range(len(vec)):
        vec_over_dy_square.append(vec[i] * one_over_dy_square[i])
    top = sum(vec_over_dy_square)
    bottomn = sum(one_over_dy_square)
    hat = top / bottomn
    return hat


def plot_linear_fit(x, y, dx, dy, a, b, xlabel, ylabel):
    x1 = min(x)
    x2 = max(x)
    x_plot = [x1, x2]
    y_plot = [a * x1 + b, a * x2 + b]
    plt.plot(x_plot, y_plot, color='red', zorder=1)
    plt.errorbar(x, y, yerr=dy, xerr=dx, ls='none', ecolor='blue')
    plt.xlabel(xlabel = xlabel)
    plt.ylabel(ylabel = ylabel)
    # plt.show()
    plt.savefig("linear_fit.svg")


def fit_linear(filename):
    my_file = open(filename, 'r')
    check_r_or_c = my_file.readline()
    check_r_or_c_list = check_r_or_c.split()  # make a list
    temp = check_r_or_c_list[1]  # check second variable in list
    temp = temp.lower()  # lower case
    is_column = 0
    if temp == 'x' or temp == 'dx' or temp == 'y' or temp == 'dy':
        is_column = 1
    x_str = []
    y_str = []
    dx_str = []
    dy_str = []
    x = []
    y = []
    dx = []
    dy = []
    data_list = check_r_or_c_list[:]
    # in case row
    if is_column == 0:
        for i in range(4):
            data_list[0] = data_list[0].lower()
            if data_list[0] == 'x':
                for j in range(1, len(data_list)):
                    x_str.append(data_list[j])
            elif data_list[0] == 'y':
                for j in range(1, len(data_list)):
                    y_str.append(data_list[j])
            elif data_list[0] == 'dx':
                for j in range(1, len(data_list)):
                    dx_str.append(data_list[j])
            elif data_list[0] == 'dy':
                for j in range(1, len(data_list)):
                    dy_str.append(data_list[j])
            data = my_file.readline()
            data_list = data.split()
    # in case columns
    elif is_column == 1:
        column_list = []
        for i in data_list:
            temp = i.lower()
            column_list.append(temp)
        x_index = column_list.index('x')
        y_index = column_list.index('y')
        dx_index = column_list.index('dx')
        dy_index = column_list.index('dy')
        data = my_file.readline()
        data_list = data.split()
        while data_list != []:
            if len(data_list) < 4:
                print('Input file error: Data lists are not the same length.\n')
                exit(1)
            x_str.append(data_list[x_index])
            y_str.append(data_list[y_index])
            dx_str.append(data_list[dx_index])
            dy_str.append(data_list[dy_index])
            data = my_file.readline()
            data_list = data.split()
    for i in x_str:
        x.append(float(i))
    for i in y_str:
        y.append(float(i))
    for i in dx_str:
        dx.append(float(i))
    for i in dy_str:
        dy.append(float(i))
    # values
    N = len(x)
    Ny = len(y)
    Ndx = len(dx)
    Ndy = len(dy)
    # checking errors

    tx = 0  # checks if all dx are pos
    ty = 0  # checks if all dy are pos
    for i in dx:
        if i <= 0:
            tx = 1
    for i in dy:
        if i <= 0:
            ty = 1
    if N != Ny or N != Ndx or N != Ndy:
        print('Input file error: Data lists are not the same length.\n')
        exit(1)
    elif ty == 1 or tx == 1:
        print('Input file error: Not all uncertainties are positive.\n')
        exit(1)
    xy = []
    for i in range(N):
        xy.append(x[i] * y[i])
    x_square = []
    for i in x:
        x_square.append(i ** 2)
    dy_square = []
    for i in dy:
        dy_square.append(i ** 2)

        # hat values
    xhat = hatfunc(x, dy)
    yhat = hatfunc(y, dy)
    xyhat = hatfunc(xy, dy)
    x_square_hat = hatfunc(x_square, dy)
    dy_square_hat = hatfunc(dy_square, dy)

    # outputs
    a = (xyhat - xhat * yhat) / (x_square_hat - xhat * xhat)
    da_square = dy_square_hat / (N * (x_square_hat - xhat * xhat))
    da = sqrt(da_square)
    b = yhat - a * xhat
    db_square = dy_square_hat * x_square_hat / (N * (x_square_hat - xhat * xhat))
    db = sqrt(db_square)
    chi_square_list = []
    for i in range(N):
        temp_var = ((y[i] - a * x[i] - b) / dy[i]) ** 2
        chi_square_list.append(temp_var)
    chi_square = sum(chi_square_list)
    chi_square_reduced = chi_square / (N - 2)
    # prints
    print('a = ' + str(a) + ' +- ' + str(da))
    print('b = ' + str(b) + ' +- ' + str(db))
    print('chi2 = ' + str(chi_square))
    print('chi2_reduced = ' + str(chi_square_reduced))

    xlabel = my_file.readline()
    ylabel = my_file.readline()
    xlabel = xlabel[8:-1]
    ylabel = ylabel[8:-1]


    plot_linear_fit(x,y,dx,dy,a,b,xlabel,ylabel)




fit_linear("input.txt")
