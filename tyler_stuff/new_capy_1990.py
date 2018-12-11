# for downloading city values from 1990
# Tyler Piazza 12/10
import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt

from capy import single_brackets, skew, edge, skew_prime, half_edge, half_edge_infinity, morans_I, dissimilarity, gini

good_city_file_names_1990 = ['Albany-Schenectady-Troy_NY', 'Ann-Arbor_MI', 'Athens-Clarke-County_GA', 'Austin-Round-Rock_TX', 'Bloomington_IN', 'Boulder_CO', 'Bridgeport-Stamford-Norwalk_CT', 'Burlington-South-Burlington_VT', 'Cedar-Rapids_IA', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Colorado-Springs_CO', 'Des-Moines-West-Des-Moines_IA', 'El-Paso_TX', 'Flint_MI',  'Grand-Rapids-Wyoming_MI',  'Harrisburg-Carlisle_PA', 'Huntingdon_PA',  'Iowa-City_IA', 'Ithaca_NY', 'Junction-City_KS', 'Kansas-City_MO-KS', 'Lafayette-West-Lafayette_IN', 'Lancaster_PA', 'Las-Vegas-Henderson-Paradise_NV', 'Lincoln_NE','Madison_WI',  'Los-Angeles-Long-Beach-Anaheim_CA',  'McAllen-Edinburg-Mission_TX','Miami-Fort-Lauderdale-West-Palm-Beach_FL','New-Haven-Milford_CT', 'New-Orleans-Metairie_LA',  'Oklahoma-City_OK','Orlando-Kissimmee-Sanford_FL', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale_AZ', 'Pittsburgh_PA', 'Plattsburgh_NY', 'Providence-Warwick_RI-MA', 'Reno_NV', 'Rio-Grande-City_TX', 'Riverside-San-Bernardino-Ontario_CA', 'Rochester_NY',  'Salt-Lake-City_UT', 'San-Antonio-New-Braunfels_TX', 'San-Diego-Carlsbad_CA', 'Santa-Cruz-Watsonville_CA', 'Santa-Fe_NM', 'Savannah_GA','Syracuse_NY', 'Tallahassee_FL', 'Toledo_OH', 'Tucson_AZ', 'Tuscaloosa_AL', 'Youngstown-Warren-Boardman_OH-PA']


b_scores = [[]]
h_scores = [[]]
a_scores = [[]]


b_scores.append(["City", "Total polulation", "Percent Black", "Percent White", "Edge" , "HEdge", "HEdgeInfinity", "Dissimilarity", "Gini", "Moran's I"])


bEdge = []
bHEdge = []
bDiss = []
bFrey = []
bAssort = []
bMoran = []


#we compute scores
for city in good_city_file_names_1990:
    print (city)
    with open('json90/'+city+'_data.json') as f:
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
    amein = np.zeros((num_vtds,1))
    natpac = np.zeros((num_vtds,1))
    other = np.zeros((num_vtds,1))
    tot = np.zeros((num_vtds,1))
    nb = np.zeros((num_vtds,1))
    nh = np.zeros((num_vtds,1))
    na = np.zeros((num_vtds,1))

    #here we add the demographics we want to compute the scores for. Currently we compute the scores for white - demographic and for demographic and its complementary set.
    dems = [black, asian, hisp]
    comps = [nb, na, nh]

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
        white[i] = g.nodes[i]['nhgis00012']
        black[i] = g.nodes[i]['nhgis00013']
        asian[i] = g.nodes[i]['nhgis00014']

        # add up the different variants of hispanic
        hisp[i] = g.nodes[i]['nhgis00017'] + g.nodes[i]['nhgis00018'] + g.nodes[i]['nhgis00019'] + g.nodes[i]['nhgis00020'] + g.nodes[i]['nhgis00021']

        natpac[i] = g.nodes[i]['nhgis00015']
        other[i] = g.nodes[i]['nhgis00016']
        # need to modify
        tot[i] = white[i] + black[i] + asian[i] + hisp[i] + natpac[i] + other[i]
        nb[i] = tot[i] - black[i]
        nh[i] = tot[i] - hisp[i]
        na[i] = tot[i] - asian[i]


    # maybe I can use these vectors, sum them up, etc.
    total_white = white.sum()
    total_black = black.sum()
    total_pop = tot.sum()

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
    btemplist.append(edge(black, white, A))
    btemplist.append(half_edge(black, white, A))
    btemplist.append(half_edge_infinity(black, white, A))
    btemplist.append(dissimilarity(black, tot))
    btemplist.append(gini(black, tot))
    btemplist.append(morans_I(black,A))

    b_scores.append(btemplist)



with open('city scores BW_1990 with pop and rho.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)
