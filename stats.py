# stdlib
from math import e


def mean(lon):
    '''Calculate the mean of a list of numbers.
    [number] --> float
    '''
    return sum(lon) / float(len(lon))


def mvue(lon, mu):
    '''Calculate the variance of a list of numbers given the mean.
    [number] number --> float
    '''
    return sum([(n - mu) ** 2 for n in lon]) / float(len(lon) - 1)


def stddev(var):
    '''Calculate a standard deviation given a variance.'''
    return var ** 0.5


def zscore(lon, mu, sd):
    '''Calculate the z-scores of a list of numbers given the mean and std dev.
    [number] number number --> [float]
    '''
    return [(n - mu) / float(sd) for n in lon]


def dotprod(lona, lonb):
    '''Calculate the dot product between two lists of numbers.
    [number] [number] -> number
    '''
    return sum([a * b for a, b in zip(lona, lonb)])


def logistic(x):
    '''Maps the real numbers to the range [0, 1] placing 0 at 1/2.
    number --> float
    '''
    return 1 / (1 + (e ** -x))


def sse(lona, lonb):
    '''Calculate the sum squared error between two lists of numbers.
    [number] [number] --> number
    '''
    return sum([(a - b) ** 2 for a, b in zip(lona, lonb)])


def rmse(lona, lonb):
    '''Calculate the root mean squared error between two lists of numbers.
    [number] [number] --> float
    '''
    return (sse(lona, lonb) / float(len(lona))) ** 0.5
