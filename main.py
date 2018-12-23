from math import *
import matplotlib.pyplot as plt

def hatfunc(vec, dy):
    """
    gets a vector and dy and returns: (sum(vec[i]/dy[i]**2)/sum(1/dy[i]**2))
    """
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
    """
    plots data
    """
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
    Gets filename and returns: 1. 2D array of data split by new lines and ' ' (spaces) 2. axes labels
    """
    my_file = open(filename, 'r')
    data = my_file.read().lower()
    table, labels = data.split("\n\n", 1)
    rows = table.split("\n")
    for i in range(len(rows)):
        row = rows[i]
        rows[i] = row.split()
    # check if all vectors have the same length
    N = len(rows[0])
    for row in rows:
        if len(row) != N:
            print('Input file error: Data lists are not the same length.\n')
            exit(1)

    labels = labels.strip().split("\n")
    x_label = labels[0][8:]
    y_label = labels[1][8:]

    return rows, x_label, y_label

def change_to_float(array):
    """
    gets an array and changes its type to float
    """
    float_array = []
    for i in array:
        float_array.append(float(i))
    return float_array


def get_vectors(table):
    """
    gets table with data and returns x,y,dx,dy in float type
    """
    data = {}
    for row in table:
        data[row[0]] = row[1:]

    x = change_to_float(data['x'])
    y = change_to_float(data['y'])
    dx = change_to_float(data['dx'])
    dy = change_to_float(data['dy'])

    return x,y,dx,dy


def any_negative(array):
    """
    checks if there are negative values or 0 in an array
    """
    for point in array:
        if point <= 0:
            return True
    return False

def get_a_and_b(xhat, yhat, xyhat, x_square_hat, dy_square_hat,N):
    """
    calculate and returns values and uncertainties of a and b
    """
    a = (xyhat - xhat * yhat) / (x_square_hat - xhat * xhat)
    da_square = dy_square_hat / (N * (x_square_hat - xhat * xhat))
    da = sqrt(da_square)
    b = yhat - a * xhat
    db_square = dy_square_hat * x_square_hat / (N * (x_square_hat - xhat * xhat))
    db = sqrt(db_square)
    return a,da,b,db

def fit_linear(filename):
    #get data
    table, xlabel, ylabel = get_data(filename)

    #make data organized by rows
    is_column = table[0][1] in ['x', 'dx', 'y', 'dy']
    if is_column:  # Flip table to rows
        table = zip(*table)

    #get vectors
    x,y,dx,dy = get_vectors(table)
    N = len(x)

    #check if all uncertainties are positive
    if any_negative(dx) or any_negative(dy):
        print('Input file error: Not all uncertainties are positive.\n')
        exit(1)

    # get values of xy, x_square and dy_square
    xy = []
    for i in range(N):
        xy.append(x[i] * y[i])
    x_square = []
    for i in x:
        x_square.append(i ** 2)
    dy_square = []
    for i in dy:
        dy_square.append(i ** 2)

    # hat values: meaning (sum(vec[i]/dy[i]**2)/sum(1/dy[i]**2))
    xhat = hatfunc(x, dy)
    yhat = hatfunc(y, dy)
    xyhat = hatfunc(xy, dy)
    x_square_hat = hatfunc(x_square, dy)
    dy_square_hat = hatfunc(dy_square, dy)

    
    # outputs
    a,da,b,db = get_a_and_b(xhat,yhat,xyhat,x_square_hat,dy_square_hat,N)

    chi_square_list = []
    for i in range(N):
        temp_var = ((y[i] - a * x[i] - b) / dy[i]) ** 2
        chi_square_list.append(temp_var)
    chi_square = sum(chi_square_list)
    chi_square_reduced = chi_square / (N - 2)

    # print
    print('a = ' + str(a) + ' +- ' + str(da))
    print('b = ' + str(b) + ' +- ' + str(db))
    print('chi2 = ' + str(chi_square))
    print('chi2_reduced = ' + str(chi_square_reduced))

    #plot
    plot_linear_fit(x,y,dx,dy,a,b,xlabel,ylabel)


#if __name__ == "__main__":
    #fit_linear("input.txt")
