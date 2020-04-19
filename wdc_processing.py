# Use regular expressions to extract data from the text
# and produce a clean csv for analysis

import pandas as pd
import re

scrape_df = pd.read_csv('./winedotcom/winedotcom.csv')

# the 'name' field often contains brackets with information we want
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
    # finally check for multipliers like '3 bottles', '2, 1L bottles' or '6-pack'
    mult_search = re.search('(\d) bottle', s)
    if mult_search != None:
        liters *= float(mult_search.group(1))
    else:
        mult_search = re.search('(\d)[,-]', s)
        if mult_search != None:
            liters *= float(mult_search.group(1))
    return liters

scrape_df['liters'] = scrape_df['brackets'].apply(find_quantity)

# extract the vintage information
def extract_vintage(s):
    # 4 digits in the name field represent a vintage
    vint_search = re.search('\d{4}', s)
    if vint_search != None:
        return int(vint_search.group())
    else:
    # choosing to encode NV as 0 to retain int type
        return 0

scrape_df['vintage'] = scrape_df['name'].apply(extract_vintage)

# remove the information we no longer need from the name field
def shorten_name(s):
    return re.sub('\d{4}|\(.* ?\)', '', s)

scrape_df['name'] = scrape_df['name'].apply(shorten_name)

# parse the rating field
def extract_rater(s):
    rater_search = re.search('(\d{2})', s)
    if rater_search != None:
        rater = s[: rater_search.start()-1]
    else:
        rater = None
    return rater

def extract_rating(s):
    rating_search = re.search('(\d{2})', s)
    if rating_search != None:
        rating = int(rating_search.group(1))
    else:
        rating = None
    return rating

scrape_df['rater'] = scrape_df['rating'].apply(extract_rater)
scrape_df['rating'] = scrape_df['rating'].apply(extract_rating)

# Now let's create a clean dataframe with only the information we need
# and save it to csv for the next stage of the project
scrape_df['price'] = scrape_df['price'].astype('float')
scrape_df['price_per_750'] = scrape_df['price'] * scrape_df['liters'] / .75
scrape_df = scrape_df.rename({'brackets': 'notes'}, axis='columns')
scrape_df = scrape_df[['name', 'vintage', 'notes', 'liters', 'price_per_750',
                       'rater', 'rating', 'type', 'varietal', 'origin']]
scrape_df.to_csv('wdc_cleaned.csv', index=None)