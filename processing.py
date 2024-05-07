# importing any possible necessary module
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 
import seaborn as sns
import os

# setting variable for EPSG code
utm18n = 32146

# creating an input file directory
dir = "input_files/"

# creating a gpkg file directory 


# creating sample output files that we will run 
out_file_13 = "va_outfile_13.gpkg"
out_file_17 = "va_outfile_17.gpkg"
out_file_20 = "va_outfile_20.gpkg"
out_file_23 = "va_outfile_23.gpkg"

# reading in the relevant files for each year we want to analyze

urban_2008 = gpd.read_file(dir + 'tl_2008_us_uac.zip')
urban_2008 = urban_2008.to_crs(epsg = utm18n)

roads_2013 = gpd.read_file('tl_2013_51_prisecroads.zip')
va_2013_census = gpd.read_file('tl_2013_51_tract.zip')
urban_2013 = gpd.read_file('tl_2013_us_uac10.zip')
urban_2013 = urban_2013.to_crs(epsg = utm18n)

roads_2017 = gpd.read_file('tl_2017_51_prisecroads.zip')
va_2017_census = gpd.read_file('tl_2017_51_tract.zip')
urban_2017 = gpd.read_file('tl_2017_us_uac10.zip')
urban_2017 = urban_2017.to_crs(epsg = utm18n)

roads_2020 = gpd.read_file('tl_2020_51_prisecroads.zip')
va_2020_census = gpd.read_file('tl_2020_51_tract.zip')
urban_2020 = gpd.read_file('tl_2020_us_uac20.zip')
urban_2020 = urban_2020.to_crs(epsg = utm18n)

roads_2023 = gpd.read_file('tl_2023_51_prisecroads.zip')
va_2023_census = gpd.read_file('tl_2023_51_tract.zip')
urban_2023 = gpd.read_file('tl_2023_us_uac20.zip')
urban_2023 = urban_2023.to_crs(epsg = utm18n)

states = gpd.read_file('tl_2023_us_state.zip')

counties = gpd.read_file('tl_2013_us_county.zip')

# getting virginia state from our master zip file for the sake of boundaries
va_state = states.query("STATEFP == '51'")
va_state = va_state.to_crs(epsg = utm18n)

# getting counties from virginia state
va_counties = counties.query("STATEFP == '51'")
va_counties = va_counties.to_crs(epsg = utm18n)

# capturing interstates from the set of roads so we can see population/infrastructure growth from high traffic areas
# mapping everything to the same crs code
# after we capture we dissolve into a single feature
inter_2013 = roads_2013.query("RTTYP == 'I'")
inter_2013 = inter_2013.to_crs(epsg=utm18n)
on_int_dis_13 = inter_2013.dissolve(by='RTTYP',aggfunc="first")

inter_2017 = roads_2017.query("RTTYP == 'I'")
inter_2017 = inter_2017.to_crs(epsg=utm18n)
on_int_dis_17 = inter_2017.dissolve(by='RTTYP',aggfunc="first")

inter_2020 = roads_2020.query("RTTYP == 'I'")
inter_2020 = inter_2020.to_crs(epsg=utm18n)
on_int_dis_20 = inter_2020.dissolve(by='RTTYP',aggfunc="first")

inter_2023 = roads_2023.query("RTTYP == 'I'")
inter_2023 = inter_2023.to_crs(epsg=utm18n)
on_int_dis_23 = inter_2023.dissolve(by='RTTYP',aggfunc="first")

# combining roads and census tracts to see areas so we can see growth of population around major roads
roads_census_2013 = inter_2013.sjoin(va_2013_census, how="left", predicate="intersects")
roads_census_2017 = inter_2017.sjoin(va_2017_census, how="left", predicate="intersects")
roads_census_2020 = inter_2020.sjoin(va_2020_census, how="left", predicate="intersects")
roads_census_2023 = inter_2023.sjoin(va_2023_census, how="left", predicate="intersects")

# plotting roads and census tracts 
fig, ax2 = plt.subplots(dpi=300)

va_state.plot(color='tan',ax=ax2)
va_counties.plot(ax=ax2, edgecolor='black')
va_2013_census.plot(ax=ax2, color='grey')
inter_2013.plot(color='black',ax=ax2)
roads_census_2013.plot(color='tomato',linewidth=0.5,ax=ax2)
ax2.axis("off")

plt.title('Census tracts around main roads')
#plt.show()
plt.savefig('output_pics/VA_roads_buffer.png')


# resetting the index
on_int_dis_13 = on_int_dis_13.reset_index()
on_int_dis_17 = on_int_dis_17.reset_index()
on_int_dis_20 = on_int_dis_20.reset_index()
on_int_dis_23 = on_int_dis_23.reset_index()

# radius for the buffer
radius_m = 1000

# creating a buffer layer with the radius
buffer_13 = on_int_dis_13.buffer(radius_m)
buffer_17 = on_int_dis_17.buffer(radius_m)
buffer_20 = on_int_dis_20.buffer(radius_m)
buffer_23 = on_int_dis_23.buffer(radius_m)

# putting files into a list to loop through
#outfile_list = [out_file_13, out_file_17, out_file_20, out_file_23]
# looping through list to check if it exists
#for f in outfile_list:
    # checking if the output file we set the variable to above already exists and if so we delete it 
if os.path.exists(out_file_13):
    os.remove(out_file_13)

if os.path.exists(out_file_17):
    os.remove(out_file_17)

if os.path.exists(out_file_20):
    os.remove(out_file_20)

if os.path.exists(out_file_23):
    os.remove(out_file_23)

# IN THE NEXT SECTION WE ARE GOING TO BE OUTPUTTING EACH OF THE DATA PLOTS FOR THE STATE, HWYS, AND BUFFERS TO THE OUTPUT FILES. IT WILL BE REPETITIVE BUT BEAR WITH ME

# saving the dfs to the same output file using the variable we made earlier and different layers
va_state.to_file(out_file_13, layer="state")
va_counties.to_file(out_file_13, layer="counties")
on_int_dis_13.to_file(out_file_13, layer="interstates")
buffer_13.to_file(out_file_13, layer="buffer")
va_2013_census.to_file(out_file_13, layer="census")

# doing this for 2017
va_state.to_file(out_file_17, layer="state")
va_counties.to_file(out_file_17, layer="counties")
on_int_dis_17.to_file(out_file_17, layer="interstates")
buffer_17.to_file(out_file_17, layer="buffer")
va_2017_census.to_file(out_file_17, layer="census")

# doing this for 2020
va_state.to_file(out_file_20, layer="state")
va_counties.to_file(out_file_20, layer="counties")
on_int_dis_20.to_file(out_file_20, layer="interstates")
buffer_20.to_file(out_file_20, layer="buffer")
va_2020_census.to_file(out_file_20, layer="census")

# doing this for 2023
va_state.to_file(out_file_23, layer="state")
va_counties.to_file(out_file_23, layer="counties")
on_int_dis_23.to_file(out_file_23, layer="interstates")
buffer_23.to_file(out_file_23, layer="buffer")
va_2023_census.to_file(out_file_23, layer="census")
# instantiating new plot 
fig, ax1 = plt.subplots(dpi=300)

# plotting the three dataframes on top of eachother with different colors
va_state.plot(color='tan',ax=ax1)
buffer_13.plot(color='tomato',ax=ax1)
on_int_dis_13.plot(color='black',linewidth=0.5,ax=ax1)

# turning off axis labels 
ax1.axis("off")

# tightening the layout and saving the figure as a png 
fig.tight_layout()
fig.savefig("output_pics/highway_13.png")

# NOW WE DO THIS FOR 2017
# saving the dfs to the same output file using the variable we made earlier and different layers
va_state.to_file(out_file_17, layer="state")
va_counties.to_file(out_file_13, layer="counties")
on_int_dis_17.to_file(out_file_17, layer="interstates")
buffer_17.to_file(out_file_17, layer="buffer")
va_2017_census.to_file(out_file_17, layer="census")

# instantiating new plot 
fig, ax1 = plt.subplots(dpi=300)

# plotting the three dataframes on top of eachother with different colors
va_state.plot(color='tan',ax=ax1)
buffer_17.plot(color='tomato',ax=ax1)
on_int_dis_17.plot(color='black',linewidth=0.5,ax=ax1)

# turning off axis labels 
ax1.axis("off")

# tightening the layout and saving the figure as a png 
fig.tight_layout()
fig.savefig("output_pics/highway_17.png")

# NOW WE DO THIS FOR 2020
# saving the dfs to the same output file using the variable we made earlier and different layers
va_state.to_file(out_file_20, layer="state")
va_counties.to_file(out_file_13, layer="counties")
on_int_dis_20.to_file(out_file_20, layer="interstates")
buffer_20.to_file(out_file_20, layer="buffer")
va_2020_census.to_file(out_file_20, layer="census")

# instantiating new plot 
fig, ax1 = plt.subplots(dpi=300)

# plotting the three dataframes on top of eachother with different colors
va_state.plot(color='tan',ax=ax1)
buffer_20.plot(color='tomato',ax=ax1)
on_int_dis_20.plot(color='black',linewidth=0.5,ax=ax1)

# turning off axis labels 
ax1.axis("off")

# tightening the layout and saving the figure as a png 
fig.tight_layout()
fig.savefig("output_pics/highway_20.png")

# LASTLY WE DO THIS FOR 2023
# saving the dfs to the same output file using the variable we made earlier and different layers
va_state.to_file(out_file_23, layer="state")
va_counties.to_file(out_file_13, layer="counties")
on_int_dis_23.to_file(out_file_23, layer="interstates")
buffer_23.to_file(out_file_23, layer="buffer")
va_2023_census.to_file(out_file_23, layer="census")

# instantiating new plot 
fig, ax1 = plt.subplots(dpi=300)

# plotting the three dataframes on top of eachother with different colors
va_state.plot(color='tan',ax=ax1)
buffer_23.plot(color='tomato',ax=ax1)
on_int_dis_23.plot(color='black',linewidth=0.5,ax=ax1)

# turning off axis labels 
ax1.axis("off")

# tightening the layout and saving the figure as a png 
fig.tight_layout()
fig.savefig("output_pics/highway_23.png")

# joining so that we get virginia urban areas for each year interval
va_urban_2008 = urban_2008.sjoin(va_state, how='inner', predicate='intersects')
va_urban_2013 = urban_2013.sjoin(va_state, how='inner', predicate='intersects')
va_urban_2017 = urban_2017.sjoin(va_state, how='inner', predicate='intersects')
va_urban_2020 = urban_2020.sjoin(va_state, how='inner', predicate='intersects')
va_urban_2023 = urban_2023.sjoin(va_state, how='inner', predicate='intersects')

# plotting
fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
va_counties.plot(ax=ax, edgecolor='black')
va_urban_2023.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2023')
ax.axis("off")
#plt.show()
plt.tight_layout()
plt.savefig("output_pics/Virginia_UA_2023.png")

# plotting
fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
va_counties.plot(ax=ax, edgecolor='black')
va_urban_2020.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2020')
ax.axis("off")
# plt.show()
plt.tight_layout()
plt.savefig("output_pics/Virginia_UA_2020.png")

# plotting
fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
va_counties.plot(ax=ax, edgecolor='black')
va_urban_2017.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2017')
ax.axis("off")
# plt.show()
plt.tight_layout()
plt.savefig("output_pics/Virginia_UA_2017.png")

# plotting
fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
va_counties.plot(ax=ax, edgecolor='black')
va_urban_2013.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2013')
ax.axis("off")
# plt.show()
plt.tight_layout()
plt.savefig("output_pics/Virginia_UA_2013.png")

# plotting
fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
va_counties.plot(ax=ax, edgecolor='black')
va_urban_2008.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2008')
ax.axis("off")
# plt.show()
plt.tight_layout()
plt.savefig("output_pics/Virginia_UA_2008.png")

# this section is a series of commented out lines that are useful for testing the code 
# printing heads to see what kind of data we are working with

'''
print(roads_2013.columns)
print(va_2013_census.columns)


print(roads_2013.head())
print(roads_2013.columns)
print(va_2013_census.head())
print(va_2013_census.columns)
print(urban_2013.head())
print(urban_2013.columns)
print(states.head())
print(states.columns)

print(roads_2013.crs)
print(va_2013_census.crs)
print(urban_2013.crs)
print(states.crs)
'''