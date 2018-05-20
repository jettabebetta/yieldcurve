import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime
import seaborn as sns
from sklearn import linear_model
import math
import matplotlib.ticker as ticker
from datetime import datetime, timedelta

#Enter the year for which you want your yieldcurve data
year = input('Enter year for which you want data: ')
while year.isdigit() == False:
	year = input('Enter year for which you want data: ')

#Request from website
url = ('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year='+year)
r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')

#Initialize pandas
columnnames = ['1mo','3mo','6mo','1yr','2yr','3yr','5yr','7yr','10yr','20yr','30yr']
df = pd.DataFrame(columns=columnnames)

#Scrape data from website 
table = soup.select('table')[1]
rows = table.findAll('tr')

for table_row in rows:
	cells = table_row.findAll('td')
	templist = []
	for item in cells:
		if 'N/A' not in item.contents[0]:
			templist.append(item.contents[0])
		else:
			templist.append('N/A')
	#Put into dataframe row
	if (templist != []) and ('N/A' not in templist):
		tempseries = pd.Series(templist[1:],index=columnnames,name=templist[0])
		df = df.append(tempseries,ignore_index=False)

#Find slopes
xaxis = pd.DataFrame([1/2, 3/12, 0.5, 1, 2, 3, 5, 7, 10])
for element in df.index:
	regr = linear_model.LinearRegression()
	slope = regr.fit(xaxis,df.ix[element][0:9])
	df.at[element,'slope']=slope.coef_
	df.at[element,'intercept']=slope.intercept_

df['date'] = df.index

#Plotting
sns.set_style('darkgrid')
ax = sns.pointplot(x='date',y='slope',data=df,scale=0.3)
plt.ylabel('Yield curve slope')
plt.xlabel('Date')

#Set y axis
lowerlim = math.floor(df['slope'].min()*10)/10
upperlim = math.ceil(df['slope'].max()*10)/10
if lowerlim > 0:
	lowerlim = 0

plt.xticks(rotation=-90)
plt.ylim(lowerlim,upperlim)
#ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.title('Yield curve for year ' + year)
plt.show()
df.ix[3:100,'date'] = 'test'
