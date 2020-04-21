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
    # provided they're the final 4
    vint_search = re.search('\d{4}$', s)
    if vint_search != None:
        return int(vint_search.group())
    else:
    # choosing to encode NV as 0 to retain int type
        return 0

scrape_df['vintage'] = scrape_df['name'].apply(extract_vintage)

# remove the information we no longer need from the name field
def shorten_name(s):
    return re.sub('\d{4}$|\(.* ?\)', '', s).strip()

scrape_df['name'] = scrape_df['name'].apply(shorten_name)

# parse the rating field
def extract_rating(s):
    # ratings are 2 digit or 100
    rating_search = re.search('(\d{2}\d?)', s)
    if rating_search != None:
        rating = int(rating_search.group(1))
        rater = s[: rating_search.start() - 1]
    else:
        rating = rater = None
    return rating, rater

scrape_df[['rating', 'rater']] = pd.DataFrame(scrape_df['rating'].apply(extract_rating).to_list())

# Now I want to shorten some of the longer rating names
short_dict = {'Robert Parker\'s Wine Advocate': 'Robert Parker',
              'Wilfred Wong of Wine.com': 'wine.com',
              'Connoisseurs\' Guide': 'Conn Guide',
              'International Wine Cellar': 'IWC'}

def shorten(s):
    try:
        return short_dict[s]
    except:
        return s

scrape_df['rater'] = scrape_df['rater'].apply(shorten)

# Now let's clean up the origin field.  There's one missing entry I can fix manually
scrape_df.loc[6496, 'origin'] = 'Barossa Valley, Barossa, South Australia, Australia'
# and some nulls (which are all gift boxes I want to drop)
scrape_df = scrape_df[~scrape_df['origin'].isnull()]
scrape_df.reset_index(inplace=True)

def short_origin(s):
    us = ['California', 'Washington', 'Oregon', 'Other U.S.']
    s = s.split(', ')
    if s[-1] in us:
        s = s + ['USA']
    if len(s) == 1:
        return '', s[-1]
    return s[-2], s[-1]

scrape_df[['subregion', 'country']] = pd.DataFrame(scrape_df['origin'].apply(short_origin).to_list())

# Now let's create a clean dataframe with only the information we need
scrape_df['price'] = scrape_df['price'].astype('float')
scrape_df['price_per_750'] = scrape_df['price'] * (0.75 / scrape_df['liters'])
scrape_df = scrape_df.rename({'brackets': 'notes'}, axis='columns')
scrape_df = scrape_df[['name', 'vintage', 'notes', 'liters', 'price_per_750',
                       'rater', 'rating', 'type', 'varietal', 'country', 'subregion', 'origin']]
# Done! Ready to save to csv
scrape_df.to_csv('wdc_cleaned.csv', index=None)