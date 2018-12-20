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
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    # plt.show()
    plt.savefig("linear_fit.svg")


def get_data(filename):
    """
    Gets filename and returns 2D array of data split by new lines and ' ' (spaces) and labels
    """
    my_file = open(filename, 'r')
    data = my_file.read().lower()
    table, labels = data.split("\n\n", 1)
    rows = table.split("\n")
    for i in range(len(rows)):
        row = rows[i]
        rows[i] = row.split(" ")

    N = len(rows[0])
    if any(map(lambda row: len(row) != N, rows)):
        print('Input file error: Data lists are not the same length.\n')
        exit(1)

    labels = labels.strip().split("\n")
    x_label = labels[0][8:]
    y_label = labels[1][8:]

    return rows, x_label, y_label


def fit_linear(filename):
    table, xlabel, ylabel = get_data(filename)

    is_column = table[0][1] in ['x', 'dx', 'y', 'dy']
    if is_column:  # Flip table to rows
        table = zip(*table)

    # All this splitting into x, y, dx, dy move to another function
    data = {}
    for row in table:
        data[row[0]] = map(float, row[1:])

    x = data['x']
    y = data['y']

    # values
    N = len(x)
    Ny = len(y)
    Ndx = len(dx)
    Ndy = len(dy)
    # checking errors


    # Extract this function outside of linear_fit
    def any_negative(array):
        for point in array:
            if point <= 0:
                return True
        return False

    if any_negative(dx) or any_negative(dy):
        print('Input file error: Not all uncertainties are positive.\n')
        exit(1)

    # Extract to another function
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

    # Extract calculations to another function
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


    plot_linear_fit(x,y,dx,dy,a,b,xlabel,ylabel)


if __name__ == "__main__":
    fit_linear("input.txt")
