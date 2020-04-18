# Process the output of the scrapy process to enrich the data and
# check for null values

import pandas as pd
import re

scrape_df = pd.read_csv('./winedotcom/winedotcom.csv')

# the 'name' field often contains brackets with information we want
# first, we fine out what

def get_brackets(s):
# checks to see if the string contains bracketed text and returns it if so
    brk = re.search('\((.* ?)\)', s)
    if brk == None:
        return None
    else:
        return brk[0].replace('(', '').replace(')', '')

scrape_df['brackets'] = scrape_df['name'].apply(get_brackets)
brk_set = set(scrape_df['brackets']) - {None}

def find_quantity(s):
# parse the string to pull out information on bottle size and quantity
    if s == None:
        return .75
    liters=.75
    # try looking for Liters in the string
    ltr_search = re.search('(\d[\d.]*) ?[Ll]', s)
    if ltr_search != None:
        liters = float(ltr_search.group(1))
    else:
        # try looking for ML
        ml_search =re.search ('(\d[\d.]*) ?ML', s)
        if ml_search != None:
            liters = float(ml_search.group(1))/1000
    # finally check for multipliers
    mult_search = re.search('(\d) bottle', s)
    if mult_search != None:
        liters *= float(mult_search.group(1))
    else:
        mult_search = re.search('(\d)[,-]', s)
        if mult_search != None:
            liters *= float(mult_search.group(1))
    return liters

scrape_df['liters'] = scrape_df['brackets'].apply(find_quantity)