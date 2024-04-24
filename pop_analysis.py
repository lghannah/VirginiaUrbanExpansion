# importing any possible necessary module
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 
import seaborn as sns
import os

# reading in the relevant files for each year we want to analyze

va_pop = pd.read_csv('rows.csv')
va_pop = va_pop.groupby('Year')
va_pop_yearly_sum = va_pop['Population Estimate'].sum()
print(va_pop_yearly_sum.head())

# creating the bar plot
'''
va_pop_yearly_sum.plot(kind='bar', x = 'Year', y = 'Population Estimate', color ='maroon', 
        width = 0.4)
 
plt.xlabel("Year")
plt.ylabel("Population")
plt.title("Total population growth in Virginia per year")
plt.yticks([83e5,84e5,85e5,86e5])
plt.show()
'''

urban_2008 = gpd.read_file('tl_2008_us_uac.zip')
#urban_2008 = urban_2008.to_crs(epsg = utm18n)

roads_2013 = gpd.read_file('tl_2013_51_prisecroads.zip')
va_2013_census = gpd.read_file('tl_2013_51_tract.zip')
urban_2013 = gpd.read_file('tl_2013_us_uac10.zip')
#urban_2013 = urban_2013.to_crs(epsg = utm18n)

roads_2017 = gpd.read_file('tl_2017_51_prisecroads.zip')
va_2017_census = gpd.read_file('tl_2017_51_tract.zip')
urban_2017 = gpd.read_file('tl_2017_us_uac10.zip')
#urban_2017 = urban_2017.to_crs(epsg = utm18n)

roads_2020 = gpd.read_file('tl_2020_51_prisecroads.zip')
va_2020_census = gpd.read_file('tl_2020_51_tract.zip')
urban_2020 = gpd.read_file('tl_2020_us_uac20.zip')
#urban_2020 = urban_2020.to_crs(epsg = utm18n)

roads_2023 = gpd.read_file('tl_2023_51_prisecroads.zip')
va_2023_census = gpd.read_file('tl_2023_51_tract.zip')
urban_2023 = gpd.read_file('tl_2023_us_uac20.zip')
#urban_2023 = urban_2023.to_crs(epsg = utm18n)

states = gpd.read_file('tl_2023_us_state.zip')
va_state = states.query("STATEFP == '51'")

# reading in a csv file that makes population estimates for urban areas and making a column copy for the sake of merging
pop_by_urban_area = pd.read_csv('/Users/liamhannah/Documents/pai789/Untitled/VirginiaUrbanExpansion/acs5_b01001_populationbyurbanarea.csv')
pop_by_urban_13 = pop_by_urban_area.query('Year == 2013')
pop_by_urban_13['GEOID'] = pop_by_urban_13['UrbanCode']

pop_by_urban_14 = pop_by_urban_area.query('Year == 2014')
pop_by_urban_14['GEOID'] = pop_by_urban_14['UrbanCode']

pop_by_urban_15 = pop_by_urban_area.query('Year == 2015')
pop_by_urban_15['GEOID'] = pop_by_urban_15['UrbanCode']

pop_by_urban_16 = pop_by_urban_area.query('Year == 2016')
pop_by_urban_16['GEOID'] = pop_by_urban_16['UrbanCode']

pop_by_urban_17 = pop_by_urban_area.query('Year == 2017')
pop_by_urban_17['GEOID'] = pop_by_urban_17['UrbanCode']

pop_by_urban_18 = pop_by_urban_area.query('Year == 2018')
pop_by_urban_18['GEOID'] = pop_by_urban_18['UrbanCode']

pop_by_urban_19 = pop_by_urban_area.query('Year == 2019')
pop_by_urban_19['GEOID'] = pop_by_urban_19['UrbanCode']

pop_by_urban_20 = pop_by_urban_area.query('Year == 2020')
pop_by_urban_20['GEOID'] = pop_by_urban_20['UrbanCode']

pop_by_urban_21 = pop_by_urban_area.query('Year == 2021')
pop_by_urban_21['GEOID'] = pop_by_urban_21['UrbanCode']

pop_by_urban_22 = pop_by_urban_area.query('Year == 2022')

# making joined versions of the urban gdf and the census to be able to track urban population growth
urban_2013_census = urban_2013.sjoin(va_2013_census, how='inner', predicate='intersects')
urban_2017_census = urban_2017.sjoin(va_2017_census, how='inner', predicate='intersects')
urban_2020_census = urban_2020.sjoin(va_2020_census, how='inner', predicate='intersects')
urban_2023_census = urban_2023.sjoin(va_2023_census, how='inner', predicate='intersects')

'''pop_census_13 = va_2013_census.merge(pop_by_urban_13, on="GEOID", how="left")
pop_census_17 = va_2017_census.merge(pop_by_urban_17, on="GEOID", how="left")
pop_census_20 = va_2020_census.merge(pop_by_urban_20, on="GEOID", how="left")

pop_urban_2013_census = urban_2013_census.merge(pop_by_urban_13, on="GEOID", how="left")
pop_urban_2017_census = urban_2017_census.merge(pop_by_urban_17, on="GEOID", how="left")
pop_urban_2020_census = urban_2020_census.merge(pop_by_urban_20, on="GEOID", how="left")

print(pop_census_13.head())
print(pop_census_13.columns)
'''

years = ['2013','2017','2020','2022']
#pop_est_totals = [pop_urban_2013_census['TotalPopulationEstimate'].sum(), pop_urban_2017_census['TotalPopulationEstimate'].sum(),pop_urban_2020_census['TotalPopulationEstimate'].sum()]
pop_est_totals = [pop_by_urban_13['TotalPopulationEstimate'].sum(), pop_by_urban_17['TotalPopulationEstimate'].sum(),pop_by_urban_20['TotalPopulationEstimate'].sum(), pop_by_urban_22['TotalPopulationEstimate'].sum()]
covid_dec = pop_by_urban_20['TotalPopulationEstimate'].sum() - pop_by_urban_17['TotalPopulationEstimate'].sum()
post_covid_inc = pop_by_urban_22['TotalPopulationEstimate'].sum() - pop_by_urban_20['TotalPopulationEstimate'].sum()
inc_since_17 = pop_by_urban_22['TotalPopulationEstimate'].sum() - pop_by_urban_17['TotalPopulationEstimate'].sum()

print("Decrease in estimated urban population during covid:",  covid_dec)
print("Increase in urban population estimate after covid pandemic:", post_covid_inc)
print("Difference in urban population estimate from post-covid times and pre-covid times:", inc_since_17)

# making a bar graph
plt.bar(years, pop_est_totals, color=['blue', 'green', 'red', 'purple'])

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Population Sum in 10 Millions')
plt.title('Population Estimates for Urban Areas in Virginia')

# Show the plot
plt.show()

sum_13 = pop_by_urban_13['TotalPopulationEstimate'].sum()
sum_14 = pop_by_urban_14['TotalPopulationEstimate'].sum()
sum_15 = pop_by_urban_15['TotalPopulationEstimate'].sum()
sum_16 = pop_by_urban_16['TotalPopulationEstimate'].sum()
sum_17 = pop_by_urban_17['TotalPopulationEstimate'].sum()
sum_18 = pop_by_urban_18['TotalPopulationEstimate'].sum()
sum_19 = pop_by_urban_19['TotalPopulationEstimate'].sum()
sum_20 = pop_by_urban_20['TotalPopulationEstimate'].sum()
sum_21 = pop_by_urban_21['TotalPopulationEstimate'].sum()
sum_22 = pop_by_urban_22['TotalPopulationEstimate'].sum()

sum_df = pd.DataFrame({
    'Year':[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'TotalUrbanPopulationByYear': [sum_13, sum_14, sum_15, sum_16, sum_17, sum_18, sum_19, sum_20, sum_21, sum_22]})
plt.plot(sum_df['Year'],sum_df['TotalUrbanPopulationByYear'])

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Urban Population Sum')
plt.title('Population Estimate Trend for Urban Areas in Virginia')

# Show the plot
plt.show()

#print(va_2013_census.head())
#print(va_2013_census.columns)

# making joined versions of the roads gdf and the census to be able to track population growth around major roads
roads_2013_census = roads_2013.sjoin(va_2013_census, how='inner', predicate='intersects')
roads_2017_census = roads_2017.sjoin(va_2017_census, how='inner', predicate='intersects')
roads_2020_census = roads_2020.sjoin(va_2020_census, how='inner', predicate='intersects')
roads_2023_census = roads_2023.sjoin(va_2023_census, how='inner', predicate='intersects')

fig, ax = plt.subplots(dpi=300)
ax = va_state.plot(color='white', edgecolor='black')
roads_2023_census.plot(ax=ax, color='red', alpha=0.5)
plt.title('Urban Areas in Virginia 2023')
plt.show()

'''
print(urban_2013.head())
print(urban_2013.columns)

print(roads_2013.head())
print(roads_2013.columns)

print(va_2013_census.head())
print(va_2013_census.columns)

print(va_state.head())
print(va_state.columns)

'''