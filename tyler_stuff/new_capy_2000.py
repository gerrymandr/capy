# for downloading city values from 2000
# Tyler Piazza 1/24/19
import numpy as np
import networkx as nx
import json
import csv
import matplotlib.pyplot as plt

from capy import single_brackets, skew, edge, skew_prime, half_edge, half_edge_infinity, morans_I, dissimilarity, gini, true_half_edge_infinity, standard_dev_of_pop

# the cities that were saved easily from the extraction - deal with these first
saved_cities = ['Los-Angeles-Long-Beach-Anaheim_CA', 'Santa-Fe_NM', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Washington-Arlington-Alexandria_DC-VA-MD-WV', 'San-Jose-Sunnyvale-Santa-Clara_CA', 'Dallas-Fort-Worth-Arlington_TX', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Houston-The-Woodlands-Sugar-Land_TX', 'Detroit-Warren-Dearborn_MI', 'Minneapolis-St-Paul-Bloomington_MN-WI', 'Denver-Aurora-Lakewood_CO', 'Cleveland-Elyria_OH', 'St-Louis_MO-IL', 'Orlando-Kissimmee-Sanford_FL', 'Sacramento--Roseville--Arden-Arcade_CA', 'Pittsburgh_PA', 'Charlotte-Concord-Gastonia_NC-SC', 'Cincinnati_OH-KY-IN', 'Kansas-City_MO-KS', 'Indianapolis-Carmel-Anderson_IN', 'Columbus_OH', 'Las-Vegas-Henderson-Paradise_NV', 'Austin-Round-Rock_TX', 'Milwaukee-Waukesha-West-Allis_WI', 'Raleigh_NC', 'Salt-Lake-City_UT', 'Nashville-Davidson--Murfreesboro--Franklin_TN', 'Greensboro-High-Point_NC', 'Louisville-Jefferson-County_KY-IN', 'Hartford-West-Hartford-East-Hartford_CT', 'Oklahoma-City_OK', 'Grand-Rapids-Wyoming_MI', 'Greenville-Anderson-Mauldin_SC', 'Buffalo-Cheektowaga-Niagara-Falls_NY', 'New-Orleans-Metairie_LA', 'Birmingham-Hoover_AL', 'Albany-Schenectady-Troy_NY', 'Rochester_NY', 'Fresno_CA', 'Dayton_OH', 'Knoxville_TN', 'Tulsa_OK', 'Omaha-Council-Bluffs_NE-IA', 'Little-Rock-North-Little-Rock-Conway_AR', 'Baton-Rouge_LA', 'Columbia_SC', 'Toledo_OH', 'Chattanooga_TN-GA', 'Lexington-Fayette_KY', 'Harrisburg-Carlisle_PA', 'Youngstown-Warren-Boardman_OH-PA', 'Wichita_KS', 'Des-Moines-West-Des-Moines_IA', 'Madison_WI', 'Portland-South-Portland_ME', 'Fort-Wayne_IN', 'Mobile_AL', 'Huntsville_AL', 'Port-St-Lucie_FL', 'Lafayette_LA', 'York-Hanover_PA', 'Lansing-East-Lansing_MI', 'Kingsport-Bristol-Bristol_TN-VA']
# the cities that needed extra work to get
problem_cities_save_names = ['New-York-Newark-Jersey-City_NY-NJ-PA', 'Boston-Cambridge-Newton_MA-NH', 'Atlanta-Sandy-Springs-Roswell_GA', 'Seattle-Tacoma-Bellevue_WA', 'North-Port-Sarasota-Bradenton_FL', 'South-Bend-Mishawaka_IN-MI']

# new
cities_from_1990_names = ['Ann-Arbor_MI', 'Athens-Clarke-County_GA', 'Bloomington_IN', 'Bridgeport-Stamford-Norwalk_CT', 'Burlington-South-Burlington_VT', 'Cedar-Rapids_IA', 'Colorado-Springs_CO', 'El-Paso_TX', 'Flint_MI', 'Iowa-City_IA', 'Ithaca_NY', 'Junction-City_KS', 'Lancaster_PA', 'Lincoln_NE', 'McAllen-Edinburg-Mission_TX', 'Miami-Fort-Lauderdale-West-Palm-Beach_FL', 'New-Haven-Milford_CT', 'Phoenix-Mesa-Scottsdale_AZ', 'Plattsburgh_NY', 'Providence-Warwick_RI-MA', 'Reno_NV', 'Rio-Grande-City_TX', 'San-Antonio-New-Braunfels_TX', 'Santa-Cruz-Watsonville_CA', 'Savannah_GA', 'Syracuse_NY', 'Tallahassee_FL', 'Tucson_AZ', 'Tuscaloosa_AL']
# removed 'Riverside-San-Bernardino-Ontario_CA' and 'Jackson_MS'
cities_1990_need_manual = ['Boulder_CO', 'Duluth_MN-WI', 'Huntingdon_PA', 'Jacksonville_FL', 'San-Diego-Carlsbad_CA', 'Tampa-St-Petersburg-Clearwater_FL', 'Virginia-Beach-Norfolk-Newport-News_VA-NC']






city_names = saved_cities + problem_cities_save_names + cities_from_1990_names + cities_1990_need_manual
city_names = sorted(city_names)


b_scores = [[]]
h_scores = [[]]
a_scores = [[]]


b_scores.append(["City", "Number of Tracts", "Total polulation", "Percent Black", "Percent White", "Edge" , "Edge rank",  "HEdge", "HEdge rank", "HEdgeInfinity (True)", "HEdgeInfinity (True) rank", "Typo HEI", "Typo HEI rank", "Dissimilarity", "Dissimilarity rank",  "Gini", "Gini rank", "Moran's I", "Moran's I rank", "Population standard deviation"])


bEdge = []
bHEdge = []
bDiss = []
bFrey = []
bAssort = []
bMoran = []


#we compute scores
for city in city_names:
    print (city)
    with open('json2000/'+city+'_data.json') as f:
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
    poc = np.zeros((num_vtds,1))

    #here we add the demographics we want to compute the scores for. Currently we compute the scores for white - demographic and for demographic and its complementary set.
    dems = [black, asian, hisp]
    comps = [nb, na, nh]

    # for 2000, from the codebook (and then the second code is what is in the shapefiles)
    # I am ignoging 007 and 014 for now
    # not hispanic
    #FMS001 or nhgis00014:      Not Hispanic or Latino >> White alone
    #FMS002 or nhgis00015:      Not Hispanic or Latino >> Black or African American alone
    #FMS003 or nhgis00016:      Not Hispanic or Latino >> American Indian and Alaska Native alone
    #FMS004 or nhgis00017:      Not Hispanic or Latino >> Asian alone
    #FMS005 or nhgis00018:      Not Hispanic or Latino >> Native Hawaiian and Other Pacific Islander alone
    #FMS006 or nhgis00019:      Not Hispanic or Latino >> Some other race alone

    #FMS007 or nhgis00020:      Not Hispanic or Latino >> Two or more races

    # hispanic
    #FMS008 or nhgis00021:      Hispanic or Latino >> White alone
    #FMS009 or nhgis00022:      Hispanic or Latino >> Black or African American alone
    #FMS010 or nhgis00023:      Hispanic or Latino >> American Indian and Alaska Native alone
    #FMS011 or nhgis00024:      Hispanic or Latino >> Asian alone
    #FMS012 or nhgis00025:      Hispanic or Latino >> Native Hawaiian and Other Pacific Islander alone
    #FMS013 or nhgis00026:      Hispanic or Latino >> Some other race alone

    #FMS014 or nhgis00027:      Hispanic or Latino >> Two or more races
    n_tracts = g.number_of_nodes()

    if n_tracts <= 30:
        print "NUMBER OF TRACTS IS LOW: " + str(n_tracts)
        continue
    # assign demographic population per geographic unit
    for i in range(n_tracts):
        # I assume that each category is discrete (there are no people in multiple categories)
        white[i] = g.nodes[i]['nhgis00014']
        black[i] = g.nodes[i]['nhgis00015']
        asian[i] = g.nodes[i]['nhgis00017']

        # add up the different variants of hispanic
        hisp[i] = g.nodes[i]['nhgis00021'] + g.nodes[i]['nhgis00022'] + g.nodes[i]['nhgis00023'] + g.nodes[i]['nhgis00024'] + g.nodes[i]['nhgis00025'] + g.nodes[i]['nhgis00026'] + g.nodes[i]['nhgis00027']

        natpac[i] = g.nodes[i]['nhgis00018']
        other[i] = g.nodes[i]['nhgis00016'] + g.nodes[i]['nhgis00019'] + g.nodes[i]['nhgis00020']
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
    btemplist.append(n_tracts)
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
    # for standard deviations
    btemplist.append(standard_dev_of_pop(tot))



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

for i in range(5, 12):
    rank_matrix.append(rank_column(b_scores, i))

# interleaves the scores and the rankings (yes, this should be done programatically)
for i in range(len(b_scores) - 2):
    now_row = b_scores[i + 2]
    rank = column(rank_matrix, i, k=0)
    b_scores[i + 2] = now_row[0:6] + [rank[0], now_row[6], rank[1], now_row[7], rank[2], now_row[8], rank[3], now_row[9], rank[4], now_row[10], rank[5], now_row[11], rank[6]] + [now_row[12]]


with open('2000_with_standard_dev.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerows(b_scores)
