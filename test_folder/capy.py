# to compute various demographic scores
# note: right now, they are made for 2 demographics. Eventually, they will be generalized

import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt

# <x,y> =  x^T(A+I)y = sum_i x_iy_i + sum_{i \sim j}x_iy_i + x_jy_i
def single_brackets(x, y, A):
    return np.matmul(x.T, np.matmul((A + np.identity(A[0].size)), y))


# <x,x> / (<x,x> + 2<x,y>)
# not suitably designed for more than 2 values yet
def skew(x, y, A):
  x_prod = single_brackets(x, x, A)
  return float(x_prod) / float(x_prod + 2 * single_brackets(x, y, A))

def edge(x, y, A):
  # JUST defined for 2 for now

  skew_sum = 0
  for (a,b) in [(x,y), (y, x)]:
    skew_sum += skew(a, b, A)

  edge_result = float(skew_sum) / float(2)
  return edge_result

#<x,x> / (<x,x> + <x,y>)
def skew_prime(x, y, A):
  x_prod = single_brackets(x, x, A)
  return float(x_prod) / float(x_prod + single_brackets(x, y, A))

# note: not made for more than 2 yet
# average the skew primes
def half_edge(x, y, A):
  skew_sum = 0
  for (a,b) in [(x,y), (y, x)]:
    skew_sum += skew_prime(a, b, A)
  edge_result = float(skew_sum) / float(2)
  return edge_result


def half_edge_infinity(x, y, A):
  x_square_sum = 0
  y_square_sum = 0
  first_denom = 0
  second_denom = 0
  n = len(x)
  for i in range(n):
    a = x[i]
    b = y[i]
    x_square_sum += a * a
    y_square_sum += b * b
    first_denom += a + a * a * b
    second_denom += b + b * a * b

  term1 = float(x_square_sum) / float(first_denom)
  term2 = float(y_square_sum) / float(second_denom)
  result = (term1 + term2) / 2.
  return result


# just runs over pairs i,j such that i<j, and sums the matrix, then multiplies by 2
def smart_symmetric_matrix_sum(A):
  n = len(A)
  accumulator = 0
  for i in range(n):
    for j in range(i + 1, n):
      accumulator += A[i,j]

  return float(2 * accumulator)




# moran's I
# n/(|E|) * (v^TAv)/(v^Tv)
# where v is x, minus a vector with just mean
def morans_I(x, A):
  n = float(len(x))
  E = smart_symmetric_matrix_sum(A)
  v = x - np.average(x)
  # (v^TAv)
  r_num = float(np.matmul(v.T, np.matmul((A), v)))
  # (v^Tv)
  r_denom = float(np.matmul(v.T,  v))
  r_quotient = r_num / r_denom
  return (n / E) * r_quotient

# total pop vector is a vector of the TOTAL population of each region, with same indices as x
def dissimilarity(x, total_pop_vector):
  total_pop = np.sum(total_pop_vector)
  x_pop = np.sum(x)
  n = len(x)

  first_term = 1. / float(2 * x_pop * (total_pop - x_pop))
  accumulator = 0.


  for i in range(n):
    accumulator += abs(x[i] * total_pop - total_pop_vector[i] * x_pop)
  return first_term * accumulator

# total_pop_vector similarly defined as before
def gini(x, total_pop_vector):
  total_pop = np.sum(total_pop_vector)
  x_pop = np.sum(x)
  n = len(x)

  first_term = 1. / float(2 * x_pop * (total_pop - x_pop))
  accumulator = 0.

  for i in range(n):
    for j in range(i + 1, n):
      accumulator += abs(x[i] * total_pop_vector[j] - total_pop_vector[i] * x[j])

  # the factor of 2 is necessary because we technically sum over all n^2 pairs (i,j), but I only did distinct pairs, and we ignore i=j
  return first_term * accumulator * 2

























