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

# from 2000
"""
# the cities that were saved easily from the extraction - deal with these first
saved_cities = ['Los-Angeles-Long-Beach-Anaheim_CA', 'Chicago-Naperville-Elgin_IL-IN-WI', 'Washington-Arlington-Alexandria_DC-VA-MD-WV', 'San-Jose-Sunnyvale-Santa-Clara_CA', 'Dallas-Fort-Worth-Arlington_TX', 'Philadelphia-Camden-Wilmington_PA-NJ-DE-MD', 'Houston-The-Woodlands-Sugar-Land_TX', 'Detroit-Warren-Dearborn_MI', 'Minneapolis-St-Paul-Bloomington_MN-WI', 'Denver-Aurora-Lakewood_CO', 'Cleveland-Elyria_OH', 'St-Louis_MO-IL', 'Orlando-Kissimmee-Sanford_FL', 'Sacramento--Roseville--Arden-Arcade_CA', 'Pittsburgh_PA', 'Charlotte-Concord-Gastonia_NC-SC', 'Cincinnati_OH-KY-IN', 'Kansas-City_MO-KS', 'Indianapolis-Carmel-Anderson_IN', 'Columbus_OH', 'Las-Vegas-Henderson-Paradise_NV', 'Austin-Round-Rock_TX', 'Milwaukee-Waukesha-West-Allis_WI', 'Raleigh_NC', 'Salt-Lake-City_UT', 'Nashville-Davidson--Murfreesboro--Franklin_TN', 'Greensboro-High-Point_NC', 'Louisville-Jefferson-County_KY-IN', 'Hartford-West-Hartford-East-Hartford_CT', 'Oklahoma-City_OK', 'Grand-Rapids-Wyoming_MI', 'Greenville-Anderson-Mauldin_SC', 'Buffalo-Cheektowaga-Niagara-Falls_NY', 'New-Orleans-Metairie_LA', 'Birmingham-Hoover_AL', 'Albany-Schenectady-Troy_NY', 'Rochester_NY', 'Fresno_CA', 'Dayton_OH', 'Knoxville_TN', 'Tulsa_OK', 'Omaha-Council-Bluffs_NE-IA', 'Little-Rock-North-Little-Rock-Conway_AR', 'Baton-Rouge_LA', 'Columbia_SC', 'Syracuse_NY', 'Toledo_OH', 'Chattanooga_TN-GA', 'Lexington-Fayette_KY', 'Harrisburg-Carlisle_PA', 'Youngstown-Warren-Boardman_OH-PA', 'Wichita_KS', 'Des-Moines-West-Des-Moines_IA', 'Madison_WI', 'Portland-South-Portland_ME', 'Fort-Wayne_IN', 'Mobile_AL', 'Huntsville_AL', 'Jackson_MS', 'Port-St-Lucie_FL', 'Lafayette_LA', 'York-Hanover_PA', 'Lansing-East-Lansing_MI', 'Kingsport-Bristol-Bristol_TN-VA']

# the cities that needed extra work to get
problem_cities_save_names = ['New-York-Newark-Jersey-City_NY-NJ-PA', 'Boston-Cambridge-Newton_MA-NH', 'Atlanta-Sandy-Springs-Roswell_GA', 'Seattle-Tacoma-Bellevue_WA', 'North-Port-Sarasota-Bradenton_FL', 'South-Bend-Mishawaka_IN-MI']
"""



#input your shape file

for city in geometry_problem_1_subset:

    # be sure to change the folder as needed
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
    # for 1990
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



    # this line is if you are dealing with 2010 values
    graph = make_graph.construct_graph_from_file(county_shp, 'GEOID10', ['DP0110001', 'DP0110002','DP0110011','DP0110012','DP0110013', 'DP0110014','DP0110015', 'DP0110016'])
    # this line is if you want 1990 values
    #graph = make_graph.construct_graph(county_shp, id_col="fid",  data_cols=['nhgis00012', 'nhgis00013','nhgis00014','nhgis00015','nhgis00016', 'nhgis00017','nhgis00018', 'nhgis00019', 'nhgis00020', 'nhgis00021'], data_source_type="fiona")
    # this line if you want 2000
    # graph = make_graph.construct_graph(county_shp, id_col="fid",  data_cols=['nhgis00014','nhgis00015','nhgis00016', 'nhgis00017','nhgis00018', 'nhgis00019', 'nhgis00021', 'nhgis00022', 'nhgis00023', 'nhgis00024', 'nhgis00025', 'nhgis00026'],data_source_type="fiona")


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





