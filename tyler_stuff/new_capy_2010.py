# for downloading city values from 2000
# Tyler Piazza 1/24/19
import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt
import os
import csv

from capy import single_brackets, skew, edge, skew_prime, half_edge, half_edge_infinity, morans_I, dissimilarity, gini, true_half_edge_infinity


CSA_code_dict = {}

# first get a dictionary of CSA codes
with open('CSA_Codes.csv' , 'rU') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] != "Metro Area" and row[0]:
            code = row[0]
            code = code[0 : len(code) - 3]
            CSA_code_dict[row[1]] = code


b_scores = [[]]
h_scores = [[]]
a_scores = [[]]


b_scores.append(["City", "Total polulation", "Percent Black", "Percent White", "Edge" , "Edge rank",  "HEdge", "HEdge rank", "HEdgeInfinity (True)", "HEdgeInfinity (True) rank", "Typo HEI", "Typo HEI rank", "Dissimilarity", "Dissimilarity rank",  "Gini", "Gini rank", "Moran's I", "Moran's I rank"])


bEdge = []
bHEdge = []
bDiss = []
bFrey = []
bAssort = []
bMoran = []


#we compute scores
#for city in city_names:


for filename in os.listdir("2010_JSONS"):
    #print filename
    city = CSA_code_dict[filename]
    print (city)
    # this isn't entirely accurate...
    #with open('2010_JSONS/'+city+'_data.json') as f:
        #data = json.load(f)
    with open('2010_JSONS/'+filename) as f:
        data = json.load(f)
    #g = nx.adjacency_graph(data)
    g = nx.readwrite.json_graph.adjacency_graph(data)
    g = nx.convert_node_labels_to_integers(g)

    num_vtds = g.number_of_nodes()

    # get demographic and total population vectors
    white = np.zeros((num_vtds,1))
    black = np.zeros((num_vtds,1))
    asian = np.zeros((num_vtds,1))
    hisp = np.zeros((num_vtds,1))

    """
    hisp_w = np.zeros((num_vtds,1))
    hisp_b = np.zeros((num_vtds,1))
    hisp_a = np.zeros((num_vtds,1))
    hisp_n = np.zeros((num_vtds,1))
    hisp_o = np.zeros((num_vtds,1))
    """







    amein = np.zeros((num_vtds,1))
    natpac = np.zeros((num_vtds,1))
    other = np.zeros((num_vtds,1))
    tot = np.zeros((num_vtds,1))
    nb = np.zeros((num_vtds,1))
    nh = np.zeros((num_vtds,1))
    na = np.zeros((num_vtds,1))
    poc = np.zeros((num_vtds,1))

    #here we add the demographics we want to compute the scores for. Currently we compute the scores for white - demographic and for demographic and its complementary set.
    dems = [black, asian, hisp]
    comps = [nb, na, nh]

    # for 2000, from the codebook (and then the second code is what is in the shapefiles)
    # I am ignoging 007 and 014 for now
    # not hispanic
    #nhgis00012: NOT HISPANIC, WHITE ALONE
       #nhgis00013: NOT HISPANIC, BLACK ALONE
       #nhgis00014: NOT HISPANIC, ASIAN ALONE
       #nhgis00015: NOT HISPANIC, NATIVE HAWAIIAN/PACIFIC ISLANDER ALONE
       #nhgis00016: NOT HISPANIC, OTHER RACE ALONE

       # and then the HISPANIC portion
       #nhgis00017: HISPANIC, WHITE
       #nhgis00018: HISPANIC, BLACK
       #nhgis00019: HISPANIC, ASIAN
       #nhgis00020: HISPANIC, NATIVE HAWAIIAN/PACIFIC ISLANDER
       #nhgis00021: HISPANIC, OTHER RACE

    # assign demographic population per geographic unit
    for i in range(g.number_of_nodes()):
        # I assume that each category is discrete (there are no people in multiple categories)
        white[i] = g.nodes[i]['NH_WHITE']
        black[i] = g.nodes[i]['NH_BLACK']
        asian[i] = g.nodes[i]['NH_ASIAN']

        # add up the different variants of hispanic
        hisp[i] =  float(g.nodes[i]['H_WHITE']) + float(g.nodes[i]['H_BLACK']) + float(g.nodes[i]['H_ASIAN']) + float(g.nodes[i]['H_NAHI']) + float(g.nodes[i]['H_OTH'])
        """
        hisp_w[i] = g.nodes[i]['H_WHITE']
        hisp_b[i] = g.nodes[i]['H_BLACK']
        hisp_a[i] = g.nodes[i]['H_ASIAN']
        hisp_n[i] = g.nodes[i]['H_NAHI']
        hisp_o[i] = g.nodes[i]['H_OTH']
        """

        natpac[i] = g.nodes[i]['NH_NAHI']
        other[i] = g.nodes[i]['NH_OTH']
        # need to modify
        tot[i] = white[i] + black[i] + asian[i] + hisp[i] + natpac[i] + other[i]
        nb[i] = tot[i] - black[i]
        nh[i] = tot[i] - hisp[i]
        na[i] = tot[i] - asian[i]

        poc[i] = tot[i] - white[i]



    # maybe I can use these vectors, sum them up, etc.
    total_white = white.sum()
    total_black = black.sum()
    total_pop = tot.sum()

    """
    print "white pop is " + str(total_white)
    print "black pop is " + str(total_black)
    print "total pop is " + str(total_pop)
    print "total hispanic pop is " + str(hisp.sum())
    print "total natpac pop is " + str(natpac.sum())
    print "total other pop is " + str(other.sum())
    print "total h_w is " + str(hisp_w.sum())
    print "total h_b is " + str(hisp_b.sum())
    print "total h_a is " + str(hisp_a.sum())
    print "total h_n is " + str(hisp_n.sum())
    print "total h_o is " + str(hisp_o.sum())
    """




    white_rho = float(total_white) / float(total_pop) * 100.
    black_rho = float(total_black) / float(total_pop) * 100.

    print "white_rho is " + str(white_rho) + " and black rho is " + str(black_rho)

    # make adjacency matrix
    A = nx.to_numpy_matrix(g)


    #compute and store the energy scores in a csv
    btemplist = []
    # info, like name, population, black rho, and white rho (percentage of that pop in the city)
    btemplist.append(city)
    btemplist.append(total_pop)
    btemplist.append(black_rho)
    btemplist.append(white_rho)

    # now compute interesting scoprs
    btemplist.append(edge(poc, white, A))
    btemplist.append(half_edge(poc, white, A))
    # note: this is the real half edge infinity
    btemplist.append(true_half_edge_infinity(poc, white, A))
    # note - this is the TYPO half edge infinity
    btemplist.append(half_edge_infinity(poc, white, A))
    btemplist.append((dissimilarity(poc, tot)[0]))
    btemplist.append((gini(poc, tot)[0]))
    btemplist.append(morans_I(poc, A))
    b_scores.append(btemplist)

def column(matrix, i, k=0):
    # have to start it at 2 because of the way we formatted b_scores
    return [row[i] for row in matrix[k:]]

def calculate_rank(vector):
    # 1 goes to largest element, and then 2 goes to the second largest, etc.
    a = {}
    rank = 1
    rev_sorted_list = sorted(vector)
    rev_sorted_list.reverse()
    for num in rev_sorted_list:
        if num not in a:
            a[num] = rank
            rank = rank + 1
    return[a[i] for i in vector]

# returns vector of ratings
def rank_column(matrix, i):
    col = column(matrix, i, k=2)
    return calculate_rank(col)

# for saving ranks - 1 means largest number, 2 means 2nd largest number, etc.
rank_matrix = []

# modify this to 11 (it used to be 10)
for i in range(4, 11):
    rank_matrix.append(rank_column(b_scores, i))

# interleaves the scores and the rankings (yes, this should be done programatically)
for i in range(len(b_scores) - 2):
    now_row = b_scores[i + 2]
    rank = column(rank_matrix, i, k=0)
    b_scores[i + 2] = now_row[0:5] + [rank[0], now_row[5], rank[1], now_row[6], rank[2], now_row[7], rank[3], now_row[8], rank[4], now_row[9], rank[5], now_row[10], rank[6]]



# sort by city names
#b_scores.sort(key=lambda x: x[0])

with open('POC_W_capy_scores_2010.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)
