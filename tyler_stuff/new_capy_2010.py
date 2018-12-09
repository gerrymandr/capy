# for downloading city values from 2010
# Tyler Piazza 12/5
import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt

from capy import single_brackets, skew, edge, skew_prime, half_edge, half_edge_infinity, morans_I, dissimilarity, gini

cities = ['Albany-Schenectady-Troy', 'Ann Arbor MI', 'Athens-Clark County GA', 'Austin-Round Rock TX', 'Bloomington IN', 'Boston-Cambridge-Newton MA', 'Boulder CO', 'Bridgeport-Stamford-Norwalk CT', 'Burlington-South Burlington VT', 'Cedar Rapids IA' , 'Chicago-Naperville-Elgin IL-IN-WI', 'Colorado Springs CO', 'Des Moines-West Des Moines IA', 'Duluth MN-WI', 'El Paso TX', 'Flint MI',  'Grand Rapids-Wyoming MI',  'Harrisburg-Carlisle PA', 'Huntingdon PA',  'Iowa city IA', 'Ithaca NY', 'Jacksonville FL', 'Junction City KS', 'Kansas city MO-KS', 'Lafayette-West Lafayette IN', 'Lancaster PA', 'Las Vegas-Henderson-Paradise NV', 'Lincoln NE', 'Los Angeles-Long Beach-Anaheim CA', 'Madison WI',  'McAllen-Edingburg-Mission TX','Miami-Fort Lauderdale-West Palm Beach FL','New Haven-Milford CT', 'New Orleans-Metairie LA', 'New York-Newark-Jersey City NY-NJ-PA',  'Oklahoma City-OK','Orlando-Kissimmee-Sanford FL', 'Philadelphia-Camden-Wilmington PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale AZ', 'Pittsburgh PA', 'Plattsburgh NY', 'Providence-Warwick RI-MA', 'Reno NV', 'Rio Grande City TX', 'Riverside-San Bernadino-Ontario CA', 'Rochester NY',  'Salt Lake City UT', 'San Antonio-New Braunfels TX', 'San Diego-Carlsbad CA', 'Santa Cruz-Watsonville CA', 'Santa Fe NM', 'Savannah GA','Syracuse NY', 'Tallahassee FL', 'Tampa-St Petersburg-Clearwater FL', 'Toledo OH', 'Tucson AZ', 'Tuscaloosa AL','Virginia Beach-Norfolk-Newport News VA-NC', 'Youngstown-Warren-Boardman OH-PA']
# for now, let's do only a few cities
#cities = ['Albany-Schenectady-Troy', 'Ann Arbor MI', 'Athens-Clark County GA']

b_scores = [[]]
h_scores = [[]]
a_scores = [[]]


b_scores.append(["City", "Total polulation", "Percent Black", "Percent White", "Edge" , "HEdge", "HEdgeInfinity", "Dissimilarity", "Gini", "Moran's I"])


#h_scores.append(["City", "Edge" , "HEdge", "Dissimilarity", "Assortativity", "Moran's I" ])

#a_scores.append(["City", "Edge" , "HEdge", "Dissimilarity", "Assortativity", "Moran's I" ])

bEdge = []
bHEdge = []
bDiss = []
bFrey = []
bAssort = []
bMoran = []

"""
aEdge = []
aHEdge = []
aDiss = []
aFrey = []
aAssort = []
aMoran = []

hEdge = []
hHEdge = []
hDiss = []
hFrey = []
hAssort = []
hMoran = []
"""

#we compute scores
for city in cities:
    print (city)
    with open('json10/'+city+'_data.json') as f:
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

    # assign demographic population per geographic unit
    for i in range(g.number_of_nodes()):
        white[i] = g.nodes[i]['DP0110011']
        black[i] = g.nodes[i]['DP0110012']
        asian[i] = g.nodes[i]['DP0110014']
        hisp[i] = g.nodes[i]['DP0110002']
        natpac[i] = g.nodes[i]['DP0110015']
        amein[i] = g.nodes[i]['DP0110013']
        other[i] = g.nodes[i]['DP0110016']
        tot[i] = g.nodes[i]['DP0110001']
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
    #btemplist.append(asq([black, white], A))
    btemplist.append(morans_I(black,A))

    #bEdge.append(edge(black, white, A))
    #bHEdge.append(half_edge(black, white, A))
    #bDiss.append(dissimilarity(black, tot))
    #bFrey.append(frey(black, white))
    #bAssort.append(asq([black, white], A))
    #bMoran.append(morans_I(black,A))

    b_scores.append(btemplist)

    """

    htemplist = []
    htemplist.append(city)
    htemplist.append(edge(hisp, white, A))
    htemplist.append(half_edge(hisp, white, A))
    htemplist.append(dissimilarity(hisp, tot))
    #htemplist.append(frey(hisp, white))
    #htemplist.append(gini(hisp, tot))
    #htemplist.append(asq([hisp, white], A))
    htemplist.append(morans_I(hisp,A))

    hEdge.append(edge(hisp, white, A))
    hHEdge.append(half_edge(hisp, white, A))
    hDiss.append(dissimilarity(hisp, tot))
    #hFrey.append(frey(hisp, white))
    #hAssort.append(asq([hisp, white], A))
    hMoran.append(morans_I(hisp,A))

    h_scores.append(htemplist)

    atemplist = []
    atemplist.append(city)
    atemplist.append(edge(asian, white, A))
    atemplist.append(half_edge(asian, white, A))
    atemplist.append(dissimilarity(asian, tot))
    #atemplist.append(frey(asian, white))
    #atemplist.append(gini(asian, tot))
    #atemplist.append(asq([asian, white], A))
    atemplist.append(morans_I(asian,A))

    aEdge.append(edge(asian, white, A))
    aHEdge.append(half_edge(asian, white, A))
    aDiss.append(dissimilarity(asian, tot))
    #aFrey.append(frey(asian, white))
    #aAssort.append(asq([asian, white], A))
    aMoran.append(morans_I(asian,A))

    a_scores.append(atemplist)
    """

# I commented the below out because newline was invalid in Python 2.7

"""
with open('city scores BW_1105.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)

with open('city scores HW_1105.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(h_scores)

with open('city scores AW_1105.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(a_scores)
"""

with open('city scores BW_1105 with pop and rho.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)

"""
with open('city scores HW_1105.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(h_scores)

with open('city scores AW_1105.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(a_scores)
"""

"""
#These are the rhos for the cities (in order) I couldn't integrate this into the script, if you find a way that'd be great

percb = [6.3,10.8, 18.5,6.8, 2.4, 6.2,0.7, 8.9,1.4, 2.8,16.8,5.2,4.2,1.3, 2.5,17.2, 5.4,7.7, 2.5,3.2, 2.7,21.2,11.5, 11.8, 2.5, 3.1, 9.7,2.8, 6.7, 3.6,0.3, 19.6,10.3, 32.3,15.6,9.5, 14.2,19.4,4.5,7.7,2.8,4.1, 2.1, 0.04, 6.9,9.9, 1.3,5.9,4.7, 0.85, 0.62,33.1,6.7,31.9,11,11.7,3.1,34.3,30.7,8.8]

perca = [2.8, 7.3,2.5, 4.5, 3.2, 6.2, 3.8, 4.3, 1.8, 1.3, 5.5, 2.4, 2.7, 0.7, 0.9, 0.8, 1.9, 2.4, 0.8, 4, 5.9, 3.2, 2.2, 2.1, 3.8, 1.6, 8.2, 2.9, 3.2, 14.4, 0.9, 2.2, 3.2, 2.4, 9.5, 2.6, 3.7, 4.7, 3.2, 1.6, 0.9, 2.5, 4.5, 0.2, 6.2, 2.3, 3, 1.9, 10.5, 4.2,1.2,1.9, 2.1,2, 2.8, 1.3, 2.4, 0.8, 3.3, 0.5]

perch = [3.9, 3.7, 6.9, 30.9, 2.2, 8.5, 12.3, 16.3, 1.57, 2.2, 20.3, 14.5, 6.1, 1.3, 82.1, 2.9, 7.8, 4.3, 1.3, 5.5, 3.4, 6.8, 9.2, 7.9, 6, 7.4, 28.8, 5.8, 4.9, 44.2, 90.6, 41.4, 13.5, 7.2, 22.3, 10.8, 24.4, 7.8, 29.2, 1.2, 2.2, 9.5, 21.3, 95.6, 46.3, 5.6, 16.2, 53.4, 32, 32.4, 48, 5.4, 3.1, 5.6, 16.1, 5.7, 34.6, 2.3, 5.2, 2.3]


fig, ax = plt.subplots()
ax.scatter(percb, bEdge, c='r', marker='.', label='Black - White')
ax.scatter(perch, hEdge, c= 'b', marker='.', label='Hispanic - White')
ax.scatter(perca, aEdge, c='g', marker='.', label='Asian - White')

ax.set_ylabel('Edge Capy Scores')
ax.set_xlabel('Percentage Minority Population')
ax.set_title('Edge Capy scores and minority percentages in 60 US cities')
legend = ax.legend(loc='left', fontsize='small')

plt.savefig('Edge', dpi=100)

fig, ax = plt.subplots()
ax.scatter(percb, bHEdge, c='r', marker='.', label='Black - White')
ax.scatter(perch, hHEdge, c= 'b', marker='.', label='Hispanic - White')
ax.scatter(perca, aHEdge, c='g', marker='.', label='Asian - White')

ax.set_ylabel('Half Edge Capy Scores')
ax.set_xlabel('Percentage Minority Population')
ax.set_title('Half Edge Capy scores and minority percentages in 60 US cities')
legend = ax.legend(loc='left', fontsize='small')

plt.savefig('HEdge', dpi=100)

fig, ax = plt.subplots()
ax.scatter(percb, bDiss, c='r', marker='.', label='Black - White')
ax.scatter(perch, hDiss, c= 'b', marker='.', label='Hispanic - White')
ax.scatter(perca, aDiss, c='g', marker='.', label='Asian - White')

ax.set_ylabel('Dissimilarity Scores')
ax.set_xlabel('Percentage Minority Population')
ax.set_title('Dissimilarity scores and minority percentages in 60 US cities')
legend = ax.legend(loc='left', fontsize='small')

plt.savefig('Diss', dpi=100)

fig, ax = plt.subplots()

ax.scatter(percb, bMoran, c='r', marker='.', label='Black - White')
ax.scatter(perch, hMoran, c= 'b', marker='.', label='Hispanic - White')
ax.scatter(perca, aMoran, c='g', marker='.', label='Asian - White')
ax.set_ylabel('Morans I Scores')
ax.set_xlabel('Percentage Minority Population')
ax.set_title('Morans i scores and minority percentages in 60 US cities')
legend = ax.legend(loc='left', fontsize='small')
plt.savefig('Moran', dpi=100)
"""
