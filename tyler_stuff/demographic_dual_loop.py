"""
Tyler Piazza
11/27/18
adapting Emilia's code

"""

import os

import networkx as nx
import json

# geospatial
import geopandas as gpd
import pysal as ps
import numpy as np
import make_graph
# visualization
import matplotlib.pyplot as plt
print(os.getcwd())

# from 2010
mysterious_problems = [ 'Los Alamos NM', 'San Jose-Sunnyvale-Santa Clara CA','Wichita KS', ]

index_problem = ['Atlanta-Sandy Springs-Roswell GA','Atlantic City - Hammonton NJ','Charlotte-Concord-Gastonia NC', 'Chattanooga TN-GA','Cleveland-Elyra OH', 'Detroit-Warren-Dearborn MI', 'Greensboro-High Point NC','Hartford CT','Milwaukee-Waukesha-West Allis WI','Raleigh NC', 'Washington-Arlington-Alexandria DC-VA-MD-WV',]

geometry_problem = ['Albuquerque NM','Baltimore-Columbia-Towson MD','Baton Rouge LA', 'Birmingham-Hoover AL', 'Boise City ID', 'Buffalo-Cheektowaga-Niagara Falls NY', 'Champaign-Urbana IL', 'Charlottesville VA','Cincinnati OH-KY-IN', 'Corpus Christi TX', 'Dallas-Fort Worth-Arlington TX', 'Denver-Aurora-Lakewood CO', 'Durham-Chapel Hill NC', 'Eugene OR', 'Fresno CA','Houston-The Woodlands-Sugar Land TX', 'Idaho Falls ID', 'Indianapolis-Carmel-Anderson IN','Jackson MS', 'Knoxville TN', 'Little Rock-North Little Rock-Conway AR','Memphis TN-MS-AR','Merced CA', 'Minneapolis-St Paul-Bloomington MN-WI', 'Modesto CA','Montgomery AL',  'Nashville-Davidson-Murfreesboro-Franklin TN',  'Ogden-Clearfield UT', 'Omaha-Council Bluffs NE-IA','Portland-Vancouver-Hillsboro OR-WA','Provo-Orem UT', 'Richmond VA', 'Sacramento-Roseville-Arden-Arcade CA', 'San Francisco-Oakland-Hayward CA',  'Seattle-Tacoma-Bellevue WA','St Louis MO-IL', 'Tulsa OK', ]

geometry_problem_1_subset = ['Albuquerque NM','Baltimore-Columbia-Towson MD','Baton Rouge LA']

#cities = ['Albany-Schenectady-Troy', 'Ann Arbor MI', 'Athens-Clark County GA', 'Austin-Round Rock TX', 'Bloomington IN', 'Boston-Cambridge-Newton MA', 'Boulder CO', 'Bridgeport-Stamford-Norwalk CT', 'Burlington-South Burlington VT', 'Cedar Rapids IA', 'Chicago-Naperville-Elgin IL-IN-WI', 'Colorado Springs CO', 'Des Moines-West Des Moines IA', 'Duluth MN-WI', 'El Paso TX', 'Flint MI',  'Grand Rapids-Wyoming MI',  'Harrisburg-Carlisle PA', 'Huntingdon PA',  'Iowa city IA', 'Ithaca NY', 'Jacksonville FL', 'Junction City KS', 'Kansas city MO-KS', 'Lafayette-West Lafayette IN', 'Lancaster PA', 'Las Vegas-Henderson-Paradise NV', 'Lincoln NE','Madison WI',  'Los Angeles-Long Beach-Anaheim CA',  'McAllen-Edingburg-Mission TX','Miami-Fort Lauderdale-West Palm Beach FL','New Haven-Milford CT', 'New Orleans-Metairie LA', 'New York-Newark-Jersey City NY-NJ-PA',  'Oklahoma City-OK','Orlando-Kissimmee-Sanford FL', 'Philadelphia-Camden-Wilmington PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale AZ', 'Pittsburgh PA', 'Plattsburgh NY', 'Providence-Warwick RI-MA', 'Reno NV', 'Rio Grande City TX', 'Riverside-San Bernadino-Ontario CA', 'Rochester NY',  'Salt Lake City UT', 'San Antonio-New Braunfels TX', 'San Diego-Carlsbad CA', 'Santa Cruz-Watsonville CA', 'Santa Fe NM', 'Savannah GA','Syracuse NY', 'Tallahassee FL', 'Tampa-St Petersburg-Clearwater FL', 'Toledo OH', 'Tucson AZ', 'Tuscaloosa AL','Virginia Beach-Norfolk-Newport News VA-NC', 'Youngstown-Warren-Boardman OH-PA']


# from 1990
"""
city_file_names_1990 = ['Albany-Schenectady-Troy_NY', 'Ann-Arbor_MI', 'Athens-Clarke-County_GA', 'Austin-Round-Rock_TX', 'Bloomington_IN', 'Boston-Cambridge-Newton,MA-NH', 'Boulder_CO', 'Bridgeport-Stamford-Norwalk_CT', 'Burlington-South-Burlington_VT', 'Cedar-Rapids_IA', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Colorado-Springs_CO', 'Des-Moines-West-Des-Moines_IA', 'Duluth,MN-WI', 'El-Paso_TX', 'Flint_MI',  'Grand-Rapids-Wyoming_MI',  'Harrisburg-Carlisle_PA', 'Huntingdon_PA',  'Iowa-City_IA', 'Ithaca_NY', 'Jacksonville,FL', 'Junction-City_KS', 'Kansas-City_MO-KS', 'Lafayette-West-Lafayette_IN', 'Lancaster_PA', 'Las-Vegas-Henderson-Paradise_NV', 'Lincoln_NE','Madison_WI',  'Los-Angeles-Long-Beach-Anaheim_CA',  'McAllen-Edinburg-Mission_TX','Miami-Fort-Lauderdale-West-Palm-Beach_FL','New-Haven-Milford CT', 'New-Orleans-Metairie_LA', 'New-York-Newark-Jersey-City_NY-NJ-PA',  'Oklahoma-City_OK','Orlando-Kissimmee-Sanford_FL', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale_AZ', 'Pittsburgh_PA', 'Plattsburgh_NY', 'Providence-Warwick_RI-MA', 'Reno_NV', 'Rio-Grande-City_TX', 'Riverside-San-Bernardino-Ontario_CA', 'Rochester-NY',  'Salt-Lake-City_UT', 'San-Antonio-New-Braunfels_TX', 'San-Diego-Carlsbad_CA', 'Santa-Cruz-Watsonville_CA', 'Santa-Fe_NM', 'Savannah_GA','Syracuse_NY', 'Tallahassee_FL', 'Tampa-St-Petersburg-Clearwater,FL', 'Toledo_OH', 'Tucson_AZ', 'Tuscaloosa_AL','Virginia-Beach-Norfolk-Newport-News_VA-NC', 'Youngstown-Warren-Boardman_OH-PA']


# good city file names, the ones that weren't strange
good_city_file_names_1990 = ['Albany-Schenectady-Troy_NY', 'Ann-Arbor_MI', 'Athens-Clarke-County_GA', 'Austin-Round-Rock_TX', 'Bloomington_IN', 'Boulder_CO', 'Bridgeport-Stamford-Norwalk_CT', 'Burlington-South-Burlington_VT', 'Cedar-Rapids_IA', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Colorado-Springs_CO', 'Des-Moines-West-Des-Moines_IA', 'El-Paso_TX', 'Flint_MI',  'Grand-Rapids-Wyoming_MI',  'Harrisburg-Carlisle_PA', 'Huntingdon_PA',  'Iowa-City_IA', 'Ithaca_NY', 'Junction-City_KS', 'Kansas-City_MO-KS', 'Lafayette-West-Lafayette_IN', 'Lancaster_PA', 'Las-Vegas-Henderson-Paradise_NV', 'Lincoln_NE','Madison_WI',  'Los-Angeles-Long-Beach-Anaheim_CA',  'McAllen-Edinburg-Mission_TX','Miami-Fort-Lauderdale-West-Palm-Beach_FL','New-Haven-Milford_CT', 'New-Orleans-Metairie_LA',  'Oklahoma-City_OK','Orlando-Kissimmee-Sanford_FL', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Phoenix-Mesa-Scottsdale_AZ', 'Pittsburgh_PA', 'Plattsburgh_NY', 'Providence-Warwick_RI-MA', 'Reno_NV', 'Rio-Grande-City_TX', 'Riverside-San-Bernardino-Ontario_CA', 'Rochester_NY',  'Salt-Lake-City_UT', 'San-Antonio-New-Braunfels_TX', 'San-Diego-Carlsbad_CA', 'Santa-Cruz-Watsonville_CA', 'Santa-Fe_NM', 'Savannah_GA','Syracuse_NY', 'Tallahassee_FL', 'Toledo_OH', 'Tucson_AZ', 'Tuscaloosa_AL', 'Youngstown-Warren-Boardman_OH-PA']

# these are the ones that were hand picked, so they need special attention
bad_city_file_names_1990 = [ 'Boston-Cambridge-Newton,MA-NH','Duluth,MN-WI', 'Jacksonville,FL', 'New-York-Newark-Jersey-City,NY-NJ-PA','Tampa-St-Petersburg-Clearwater,FL', 'Virginia-Beach-Norfolk-Newport-News_VA-NC']
"""


#input your shape file

for city in geometry_problem_1_subset:

    # be sure to change the folder
    county_shp = "Geometry_problem_shapefiles_1_2010 /"+city+".shp"
    print "I want to open the shapefile called " + county_shp
    df_counties = gpd.read_file(county_shp)
    df_counties.plot()

    county_centroids = df_counties.centroid

    c_x = county_centroids.x
    c_y = county_centroids.y

    # Spatial Weights
    rW = ps.rook_from_shapefile(county_shp)
    #rW[10] # View neighbors for specific row -> note, all weights = 1.0
    #rW.neighbors # View all neighbors
    #rW.full()[0] # View full contiguity matrix

    # Would be nice to see attributes for neighbors:
    self_and_neighbors = [10]
    self_and_neighbors.extend(rW.neighbors[10])
    df_counties.iloc[self_and_neighbors, :5]

    #this just keeps track of progress

    # below are the relevent quantities that are used, by the codes in the files

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



    # this line is if you are dealing with 2010 values
    graph = make_graph.construct_graph_from_file(county_shp, 'GEOID10', ['DP0110001', 'DP0110002','DP0110011','DP0110012','DP0110013', 'DP0110014','DP0110015', 'DP0110016'])
    # this line is if you want 1990 values
    #graph = make_graph.construct_graph(county_shp, id_col="fid",  data_cols=['nhgis00012', 'nhgis00013','nhgis00014','nhgis00015','nhgis00016', 'nhgis00017','nhgis00018', 'nhgis00019', 'nhgis00020', 'nhgis00021'], data_source_type="fiona")
    nx.draw(graph)





    # per suggestion by Max, I'm going to delete geometry

    """
    # this may have been necessary for 1990
    for node in graph.nodes:
        if str(graph.nodes[node]['boundary_node']) == "True":
            graph.nodes[node]['boundary_node'] = 'true'
        elif str(graph.nodes[node]['boundary_node']) == "False":
            graph.nodes[node]['boundary_node'] = 'false'
    """

    #plt.show()
    #we're saving the demographic dual graph as a json, to compute the energies from.

    data = nx.readwrite.json_graph.adjacency_data(graph)
    #print data

    print "about to write into file..."
    with open("json10/"+city+"_data.json", "w") as f:
        json.dump(data, f)





