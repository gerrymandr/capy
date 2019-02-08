# capy
clustering propensity scores for demographic segregation

Work flow:

I am working using a similar framework to Emilia's code, so see her files if there are specifics about certain syntax choices of pulling shapefiles, turning them to .jsons, etc.

Ultimately, we want to get the relevent scores from 1990, 2000, and 2010.

Below are some notes specific to how I (Tyler) am handling certain things:

If your goal is to from SHAPEFILES -> JSON -> CAPY SCORES, you should go to demographic_dual_loop.py for the first arrow, and the second arrow (saved to a .csv file) can be accomplished by emulating files like new_capy_2000.py

capy.py -- this is the file which contains the methods that compute the scores. 

NOTE: what we refer to as "typo", "HEI Typo", etc. is the function half_edge_infinity. The function as written is a typo on the "true" half edge infinity (which is located in the function true_half_edge_infinity), and this "typo" ends up prediciting descripancies between edge and half edge.

capy_tests.py -- this file tests the functions by iterating through 4 imagined regions, looping through various adjacency, population, and demographic information.

demographic_dual_loop -- this file converts SHAPEFILES -> JSON, by taking advantage of make_graph.py. 
Make sure that you have the right codes (and be sure that you have all of the codes that you need. At one point, I did not record the codes for people of mixed race, so be sure you know what information is necessary). Also be sure to skim through demographi_dual_loop to be sure that you have sufficiently modified what is specific to your problem, like: 
- do you have the correct list of file names? 
- do you reference the correct folder of .shp files
- around line 128, do you have the right "graph" definition? you need certain codes in the data_cols (make sure that you actually know the codes that you are putting in and double checking that you have all of them)
- are you writing into the correct folder name at the end?

new_capy_2000.py -- this file converts JSON -> CAPY SCORES (csv), using the jsons that you have
As with demographic_dual_loop, be sure that you have skimmed through this file to make sure that you have changed the necessary information, like:
- do you have the correct list of file names (json file names now, but they should be the same)?
- are you opening the right folder?
- are you correctly inputting the demographic codes around line 87?
- are you dealing with the correct populations (this file at one point dealt with WHITE and BLACK (both nonhispanic), but you may want to modify the populations that you are dealing with)?
- are you writing into the correct file name?
