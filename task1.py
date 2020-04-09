#!/usr/bin/env python
# coding: utf-8

# ### Step 0
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.

# In[8]:


# Import pandas
import pandas as pd
import numpy as np
energy = pd.read_excel('/home/hihsma/Downloads/Task 1-20200324T140729Z-001/Task 1/data/Energy Indicators.xls',  skiprows = range(1, 18), usecols="C:F", skipfooter=38, na_values=["..."])
energy.columns = ["Country","Energy Supply","Energy Supply per Capita","% Renewable"]
energy['Energy Supply'] = energy['Energy Supply'].apply(lambda x: x*1000)
energy['Country'] = energy['Country'].str.replace(r"\(.*\)","")
energy['Country'] = energy['Country'].str.replace("[0-9()]+$", "")
energy['Country']=energy['Country'].replace({"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"})
for i, row in energy.iterrows():
    print(row["Country"])


# ### Step 1
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>

# In[11]:


GDP=pd.read_csv('/home/hihsma/Downloads/Task 1-20200324T140729Z-001/Task 1/data/world_bank.csv',skiprows=4 )
GDP = GDP.rename(columns={'Country Name': 'Country'})
GDP[['Country']]=GDP[['Country']].astype(str)
GDP['Country']=GDP['Country'].replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"
})
GDP.head()


# ### Step 2
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

# In[12]:


# Import pandas
import pandas as pd
# Let's investigate the dataset at first
ScimEn = pd.read_excel('/home/hihsma/Downloads/Task 1-20200324T140729Z-001/Task 1/data/scimagojr-3.xlsx', footer=0 )
# View info
ScimEn.head(15)


# ### Step 3
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This step should yeild a DataFrame with 20 columns and 15 entries.*

# In[19]:


result= pd.merge(pd.merge( ScimEn[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index']],GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']],on='Country'),
energy[['Country','Energy Supply', "Energy Supply per Capita", '% Renewable']],on='Country')
result=result.loc[(result['Rank'] <= 15 )]
result.head(16)


# ### Step 4
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This step should yield a single number.*

# In[20]:


(ScimEn['Country'].isin(energy['Country'].isin(GDP['Country']))).value_counts()


# ### Step 5
# 
# #### Answer the following questions in the context of only the top 15 countries by Scimagojr Rank 
# 
# 
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This step should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[22]:


avgGDP = result[['Country']].join(result.loc[:, '2006':'2015'])
avgGDP ['mean'] = avgGDP .mean(axis=1,skipna = True)
avgGDP.sort_values('mean', axis = 0, ascending = False, inplace=True)
avgGDP ['mean']


# In[39]:


result


# ### Step  6
# What is the mean `Energy Supply per Capita`?
# 
# *This step should return a single number.*

# In[23]:


result[["Energy Supply per Capita"]].mean(axis=0,skipna = True)


# ### Step 7
# What country has the maximum % Renewable and what is the percentage?
# 
# *This step should return a tuple with the name of the country and the percentage.*

# In[40]:



val = result["% Renewable"].max()
for i, row in result.iterrows():
    if row["% Renewable"]== val:
        print(f"({row['Country']},{val}%)")
#(country, val)


# ### Step 8
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This step should return a tuple with the name of the country and the ratio.*

# In[43]:


result['ratio'] = result['Self-citations'] / result['Self-citations'].sum()
maxratio=result['ratio'].max()
for i, row in result.iterrows():
    if row['ratio']== maxratio:
        print(f"({row['Country']},{maxratio})")


# ### Step 9
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This step should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[44]:


ratio_median= result['% Renewable'].median(axis = 0, skipna = True)
result['HighRenew'] = result['% Renewable'].apply(lambda x : '1' if x >= ratio_median  else '0' )

result


# ### Step 10
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[52]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
Top15 = pd.DataFrame({'Country':['China','United States','Japan','United Kingdom','Russian Federation',
'Canada','Germany','India','France','South Korea','Italy','Spain','Iran','Australia','Brazil']})
Top15


# In[53]:


Top15['Continent'] = Top15['Country'].map(ContinentDict)
Top15['Estimated_population'] = Top15['Country'].str.len()*1000000
Top15 = Top15.groupby('Continent')['Estimated_population'].agg(['size', 'sum','mean','std'])


# In[49]:


Top15


# In[ ]:




