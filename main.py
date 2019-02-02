from math import *
from sys import *
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

def plot_chi2_a(x_plot, b_chosen, chi_square_func):
    """
    plots chi2 as a function of a for the best b
    for bonus part
    """
    ylabel = 'chi2(a,b = {0:.1f})'.format(b_chosen)
    plt.figure('new figure in case they run both regular and bonus together')
    plt.plot(x_plot, chi_square_func, color= 'blue')
    plt.xlabel(xlabel='a')
    plt.ylabel(ylabel=ylabel)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(3,3))
    #plt.show()
    plt.savefig("numeric_sampling.svg")


def get_data(filename,bool):
    """
    Gets filename and returns: 1. 2D array of data split by new lines and ' ' (spaces) 2. axes labels 3. 2D array of bonus data
    """
    my_file = open(filename, 'r')
    data = my_file.read()
    if bool == 0:
        table, labels = data.split("\n\n", 1)
    else:
        table, labels, params = data.split("\n\n", 2)
    rows = table.lower().split("\n")
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

    if bool == 1:
        parameters = params.split("\n")
        for i in range(len(parameters)):
            parameter = parameters[i]
            parameters[i] = parameter.split()
        return rows, x_label, y_label, parameters[0:-1]

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

def get_bonus_data(params):
    """
    gets table with bonus data and returns a and b in float type
    """
    data = {}
    for row in params:
        data[row[0]] = row[1:]

    a = change_to_float(data['a'])
    b = change_to_float(data['b'])

    return a,b


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

def chi2_calculator(x,y,dy,a,b):
    """
    calculates and returns chi2 and chi2 reduced
    """
    N = len(x)
    chi_list = []
    for i in range(N):
        temp_var = ((y[i] - a * x[i] - b) / dy[i]) ** 2
        chi_list.append(temp_var)
    chi_square = sum(chi_list)
    chi_square_reduced = chi_square / (N - 2)
    return chi_square, chi_square_reduced

def fit_linear(filename):
    #get data
    table, xlabel, ylabel = get_data(filename, 0)

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

    #get chi2 and chi2 reduced
    chi_square, chi_square_reduced = chi2_calculator(x,y,dy,a,b)


    # print
    print('a = ' + str(a) + ' +- ' + str(da))
    print('b = ' + str(b) + ' +- ' + str(db))
    print('chi2 = ' + str(chi_square))
    print('chi2_reduced = ' + str(chi_square_reduced))

    #plot
    plot_linear_fit(x,y,dx,dy,a,b,xlabel,ylabel)

def search_best_parameter(filename):
    # get data
    table, xlabel, ylabel, params = get_data(filename, 1)

    # make data organized by rows
    is_column = table[0][1] in ['x', 'dx', 'y', 'dy']
    if is_column:  # Flip table to rows
        table = zip(*table)

    # get vectors
    x, y, dx, dy = get_vectors(table)
    N = len(x)

    # check if all uncertainties are positive
    if any_negative(dx) or any_negative(dy):
        print('Input file error: Not all uncertainties are positive.\n')
        exit(1)

    #get a and b data
    a,b = get_bonus_data(params)
    a_initial = a[0]
    a_stepsize = a[2]
    a_final = a[1]
    b_initial = b[0]
    b_stepsize = b[2]
    b_final = b[1]

    #find the best chi square and the best parameters
    chi_square, chi_square_reduced = chi2_calculator(x,y,dy,a_initial,b_initial)
    a_chosen = a_initial
    b_chosen = b_initial

    #make a_initial smaller than a_final and samr for b
    if a_final < a_initial:
        temp = a_final
        a_final = a_initial
        a_initial = temp
        a_stepsize = a_stepsize*(-1)
    if b_final < b_initial:
        temp = b_final
        b_final = b_initial
        b_initial = temp
        b_stepsize = b_stepsize*(-1)

    i = a_initial
    while i < a_final:
        j = b_initial
        while j < b_final:
            chi_square_temp, chi_square_reduced_temp = chi2_calculator(x,y,dy,i,j)
            if chi_square_temp < chi_square:
                chi_square = chi_square_temp
                chi_square_reduced = chi_square / (N - 2)
                a_chosen = i
                b_chosen = j
            j = j + b_stepsize
        i = i + a_stepsize
    # print
    print('a = ' + str(a_chosen) + ' +- ' + str(a_stepsize))
    print('b = ' + str(b_chosen) + ' +- ' + str(b_stepsize))
    print('chi2 = ' + str(chi_square))
    print('chi2_reduced = ' + str(chi_square_reduced))

    #create chi square vector for best b
    chi_square_func = []
    i = a_initial
    x_plot = []
    while i < a_final:
        x_plot.append(i)
        chi_square_temp, chi_square_reduced_temp = chi2_calculator(x,y,dy,i,b_chosen)
        chi_square_func.append(chi_square_temp)
        i = i + a_stepsize

    #plot
    plot_chi2_a(x_plot, b_chosen, chi_square_func)


#if __name__ == "__main__":
    #fit_linear("input.txt")
    #search_best_parameter('bonus.txt')