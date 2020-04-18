import pandas as pd

raw_df = pd.read_csv('robertparker_raw.csv', header=None)

def split_parker_id(s):
    fields = s.split('=')[1:] # first item provides no useful information
    fields[0] = int(fields[0][:4]) # we know all vintages are 4 digits
    fields[1] = fields[1].split('&')[0] # this returns the country
    fields[2] = fields[2].split('&')[0]  # this returns the region
    # fields[3] returns the subregion and needs no processing
    return fields

raw_df[['vintage', 'country', 'region', 'subregion']] = raw_df[0].apply(split_parker_id)