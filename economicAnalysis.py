import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

plt.style.use('fivethirtyeight')
pd.set_option('display.max_columns',500)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()['color']

from fredapi import Fred

FRED_KEY = '59837b5b01fc74805b5494628f905d89'

# CREATE the FRED OBJECT
fred = Fred(api_key=FRED_KEY)

# Search Fred
sp_search = fred.search('S&P',order_by='popularity')

# Pull Raw Data
sp500 = fred.get_series(series_id='SP500')
#sp500.plot(figsize=(10,5),title='S&P 500',lw=1.5)
#plt.show()

# Pull and join multiple data series
unrate = fred.get_series('UNRATE')
#unrate.plot()
#plt.show()

#unrate = fred.get_series('UNRATE')
#unrate.plot()
#plt.show()
unemployment_results = fred.search('unemployment rate state', filter=('frequency','Monthly'))
unem_query_df=unemployment_results.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
unem_query_df_filtered=unem_query_df.loc[unem_query_df['title'].str.contains('Unemployment Rate')]

all_results = []
for myid in unem_query_df_filtered.index:
    results = fred.get_series(myid)
    results = results.to_frame(name=myid)
    all_results.append(results)

unemp_results_df = pd.concat(all_results, axis =1).drop(['M08310USM156SNBR', 'DSUR'], axis=1)
unemp_states = unemp_results_df.drop('UNRATE',axis=1)

unemp_states.isna().sum(axis=1).plot()
unemp_states = unemp_states.dropna()

fig = px.line(unemp_states)
fig.show()

unemp_states.loc[unemp_states.index == '2020-04-01'].T \
    .sort_values('2020-04-01') \
    .plot(kind='bar', figsize=(10,5))
plt.show()

