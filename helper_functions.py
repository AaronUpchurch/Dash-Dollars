# text to dataframe function
def text_to_df(text,manual=False):

    import pandas as pd
    import numpy as np
    from datetime import datetime
    import re

    # check that correct text has been inputed
    if text[0:21] != 'LeftSideNavigationBar':
        return pd.DataFrame(columns = ['Resturant','Date','Price','running_total_price','day_of_week'])

    # remove header information
    start_index = text.find('Orders\nCompleted') + len('Orders\nCompleted')
    text = text[start_index:]

    # add regex header to first order
    if manual: 
        header = '\nâ€¢ Leave a review'
    else: 
        header = '\• Leave a review'
    text = header + text

    # define order regex
    if manual:
        regex = r'\â€¢ Leave a review\n([\w\s\'\-\&]*)\n([{a-zA-z,1-9\s]*) â€¢ \$([0-9\.]*) â€¢'
    else:
        regex = r'\• Leave a review\n([\w\s\'$\-\&]*)\n([{a-zA-z,1-9\s]*) • \$([0-9\.]*) •'

    
    # get regex matches
    data = re.findall(regex,text)
    
    # convert to dateframe
    df = pd.DataFrame(columns = ['Resturant','Date','Price'])
    for i in range(len(data)): df.loc[len(df.index)] = [data[i][0],data[i][1],data[i][2]]
    
    # change datetype
    df.Price = df.Price.astype(float)

    # Issue: Year of order is not specified in order history. Must manually calcualte years.
    
    # define month int map
    month_map = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    
    # define current year and month
    years = []
    curr_year = datetime.now().year
    curr_month = re.findall(r'\w\w\w, (\w\w\w)',df.iloc[0].Date)[0]
    
    # for each row calculate year
    for i in range(len(df.index)-1):
    
        # record year
        years = np.append(years,curr_year)
    
        # get following month
        next_month = re.findall(r'\w\w\w, (\w\w\w)',df.iloc[i+1].Date)[0]
    
        # if next order's month is 'above' current order's month, a year has ended
        if month_map[curr_month] < month_map[next_month]:
            curr_year = curr_year - 1
    
        # move to next order
        curr_month = next_month
    
    years = np.append(years,curr_year)
    
    years = np.array(years).astype(int)
    
    def make_datetime(x):
        month = re.findall(r'\w\w\w, (\w\w\w)',x.Date)[0]
        day = int(re.findall(r'\w\w\w, \w\w\w ([1-9]*)',x.Date)[0])
        return datetime(years[x.name],month_map[month],day)
    
    df.Date = df.apply(make_datetime,axis=1)

    df['running_total_price'] = [df.Price[i:].sum() for i in np.arange(0,df.shape[0])]

    df['day_of_week'] = df.Date.apply(lambda x: x.strftime('%A'))

    return df