# for downloading city values from 1990
# Tyler Piazza 12/10
import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt

from capy import single_brackets, skew, edge, skew_prime, half_edge, half_edge_infinity, morans_I, dissimilarity, gini, true_half_edge_infinity

# removed 'Riverside-San-Bernardino-Ontario_CA' to match with 2000
good_city_file_names_1990 = ['Albany-Schenectady-Troy_NY', 'Ann-Arbor_MI', 'Athens-Clarke-County_GA', 'Austin-Round-Rock_TX', 'Bloomington_IN', 'Boulder_CO', 'Bridgeport-Stamford-Norwalk_CT', 'Burlington-South-Burlington_VT', 'Cedar-Rapids_IA', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Colorado-Springs_CO', 'Des-Moines-West-Des-Moines_IA', 'El-Paso_TX', 'Flint_MI',  'Grand-Rapids-Wyoming_MI',  'Harrisburg-Carlisle_PA', 'Huntingdon_PA',  'Iowa-City_IA', 'Ithaca_NY', 'Junction-City_KS', 'Kansas-City_MO-KS', 'Lafayette-West-Lafayette_IN', 'Lancaster_PA', 'Las-Vegas-Henderson-Paradise_NV', 'Lincoln_NE','Madison_WI',  'Los-Angeles-Long-Beach-Anaheim_CA',  'McAllen-Edinburg-Mission_TX','Miami-Fort-Lauderdale-West-Palm-Beach_FL','New-Haven-Milford_CT', 'New-Orleans-Metairie_LA',  'Oklahoma-City_OK','Orlando-Kissimmee-Sanford_FL', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale_AZ', 'Pittsburgh_PA', 'Plattsburgh_NY', 'Providence-Warwick_RI-MA', 'Reno_NV', 'Rio-Grande-City_TX', 'Rochester_NY',  'Salt-Lake-City_UT', 'San-Antonio-New-Braunfels_TX', 'San-Diego-Carlsbad_CA', 'Santa-Cruz-Watsonville_CA', 'Santa-Fe_NM', 'Savannah_GA','Syracuse_NY', 'Tallahassee_FL', 'Toledo_OH', 'Tucson_AZ', 'Tuscaloosa_AL', 'Youngstown-Warren-Boardman_OH-PA']


bad_city_file_names_1990 = ['Boston-Cambridge-Newton,MA-NH','Duluth,MN-WI', 'Jacksonville,FL', 'New-York-Newark-Jersey-City,NY-NJ-PA','Tampa-St-Petersburg-Clearwater,FL', 'Virginia-Beach-Norfolk-Newport-News,VA-NC']

# the new cities from the 2000 names, for 1990
# we remove Riverside =
new_city_names_for_1990 = ['Baton-Rouge_LA', 'Buffalo-Cheektowaga-Niagara-Falls_NY',  'Charlotte-Concord-Gastonia_NC-SC', 'Chattanooga_TN-GA', 'Cincinnati_OH-KY-IN', 'Cleveland-Elyria_OH', 'Columbia_SC', 'Columbus_OH', 'Dallas-Fort-Worth-Arlington_TX', 'Dayton_OH', 'Denver-Aurora-Lakewood_CO', 'Detroit-Warren-Dearborn_MI', 'Fort-Wayne_IN', 'Greensboro-High-Point_NC', 'Greenville-Anderson-Mauldin_SC', 'Hartford-West-Hartford-East-Hartford_CT', 'Huntsville_AL', 'Indianapolis-Carmel-Anderson_IN', 'Knoxville_TN', 'Lexington-Fayette_KY', 'Little-Rock-North-Little-Rock-Conway_AR', 'Louisville-Jefferson-County_KY-IN', 'Milwaukee-Waukesha-West-Allis_WI', 'Minneapolis-St-Paul-Bloomington_MN-WI',  'Omaha-Council-Bluffs_NE-IA', 'Port-St-Lucie_FL', 'Portland-South-Portland_ME', 'Raleigh_NC', 'Sacramento--Roseville--Arden-Arcade_CA', 'San-Jose-Sunnyvale-Santa-Clara_CA', 'St-Louis_MO-IL', 'Tulsa_OK', 'Washington-Arlington-Alexandria_DC-VA-MD-WV', 'Wichita_KS', 'York-Hanover_PA']


new_city_names_manual_for_1990 = ['Atlanta-Sandy-Springs-Gainesville_GA-AL', 'Birmingham-Hoover_AL','Fresno_CA' , 'Houston-The-Woodlands-Sugar-Land_TX', 'Kingsport-Bristol-Bristol_TN-VA', 'Lansing-East-Lansing_MI', 'Mobile_AL', 'Nashville-Davidson--Murfreesboro--Franklin_TN', 'Sarasota-Bradenton-Punta-Gorda_FL', 'Seattle-Tacoma-Olympia_WA', 'South-Bend-Mishawaka_IN-MI']




city_names_1990 = good_city_file_names_1990 + bad_city_file_names_1990 + new_city_names_for_1990 + new_city_names_manual_for_1990
city_names_1990 = sorted(city_names_1990)



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
for city in city_names_1990:
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
    # the score that we will be using
    poc = np.zeros((num_vtds,1))

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
        poc[i] = tot[i] - white[i]


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
    btemplist.append(edge(poc, white, A))
    btemplist.append(half_edge(poc, white, A))
    btemplist.append(true_half_edge_infinity(poc, white, A))
    btemplist.append(half_edge_infinity(poc, white, A))
    btemplist.append((dissimilarity(poc, tot))[0])
    btemplist.append((gini(poc, tot))[0])
    btemplist.append(morans_I(poc,A))

    b_scores.append(btemplist)

# get the ith column of a 2D list
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

for i in range(4, 11):
    rank_matrix.append(rank_column(b_scores, i))

# interleaves the scores and the rankings (yes, this should be done programatically)
for i in range(len(b_scores) - 2):
    now_row = b_scores[i + 2]
    rank = column(rank_matrix, i, k=0)
    b_scores[i + 2] = now_row[0:5] + [rank[0], now_row[5], rank[1], now_row[6], rank[2], now_row[7], rank[3], now_row[8], rank[4], now_row[9], rank[5], now_row[10], rank[6]]



with open('POC_W_capy_scores_1990.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)
