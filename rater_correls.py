# Analyse correlations between ratings
#
# The first study is what correlation do each of the raters have to price?
# The second is how much do they correlate with each other?

import pandas as pd
import numpy as np, numpy.linalg as lin
from math import sqrt

wine = pd.read_csv('wdc_cleaned.csv')
raters = wine['rater'].value_counts().sort_values(ascending=False).index.tolist()[:10]

# There are duplicates in the data because wine.com sells the same wine in different formats
# e.g. single bottle, case of 12, 1.5l magnum etc.  Let's get rid of these
wine['id'] = wine['nameyear'] + str(wine['rating']) + wine['rater']
wine = wine.sort_values(by=['id', 'price_per_750'])
wine['duplicate'] = (wine['id'] == wine['id'].shift())
wine = wine[~wine['duplicate']]
wine = wine.drop(['id', 'duplicate'], axis = 1)

# I'm going to normalize X and Y for means but not standard deviation
# Ratings go from 87 to 100 so clearly we want to mean subtract these
# Also, I think that quality should drive how far price is from average:
# all wines cost something to make, so price is similarly floored
# However, I think standard deviation is interesting information about a rater
# so I don't want to remove it.
wine['rating'] = wine['rating'] - wine['rating'].mean()
wine['price_per_750'] = wine['price_per_750'] - wine['price_per_750'].mean()

# First let's look at correlation between raters
# This is slightly unusual analysis because we can only
# look at correlation on the subset of wines that they both reviewed
# so each correlation will be estimated from a different number of samples
# We need to check we have enough for meaningful analysis

rater_corr = np.identity(len(raters))
t_stats = np.identity(len(raters)) * 2  # I'm going to test for t-stats < 2 but don't want to ditch diagonals
for i in range(len(raters)):
    for j in range(i+1, len(raters)):
        rater1 = wine[wine['rater'] == raters[i]][['rating', 'nameyear']]
        rater2 = wine[wine['rater'] == raters[j]][['rating', 'nameyear']]
        shared = pd.merge(rater1, rater2, on='nameyear')
        if shared.shape[0] > 2:
            X = shared['rating_x']
            Y = shared['rating_y']
            rater_corr[i, j] = rater_corr[j, i] =  X.T @ Y / (lin.norm(X) * lin.norm(Y))
            t_stats[i, j] = t_stats[j, i] = rater_corr[i, j] * sqrt(shared.shape[0] - 2) / sqrt(1 - rater_corr[i, j]**2)
        else:
            rater_corr[i, j] = rater_corr[j, i] = 0
# Reject values below t=2
rater_corr[t_stats<2] = 0
rater_infl = np.linalg.norm(rater_corr, axis=0)
rater_corr_df = pd.DataFrame(rater_corr, index=raters, columns=raters)
rater_infl_s = pd.Series(rater_infl, index=raters).sort_values(ascending=False)
print(rater_infl_s)
print(rater_corr_df)
rater_corr_df.to_csv('ratercorrels.csv')

# Now, let's regress raters against price
# I want to winsorize the data first: throw out wines over $500 a bottle
wine = wine[wine['price_per_750']<=500]

price_corr = np.zeros(len(raters))
for i in range(len(raters)):
    X = wine[wine['rater'] == raters[i]]['rating'].to_numpy()
    Y = wine[wine['rater'] == raters[i]]['price_per_750'].to_numpy()
    price_corr[i] = X.T @ Y / (lin.norm(X) * lin.norm(Y))

price_corr_s = pd.Series(price_corr, index=raters).sort_values()
print(price_corr_s)

# Things to write about:
# wine.com is 72% correlated to price.  They're just trying to sell the expensive wines! Throw them out
# Wine Spectator, burghound, Vinous and Dunnuck are prepared to give high ratings to cheaper wines.
# They will likely be useful for value hunting
# For the other higher correlations - do they have a taste for expensive wine, or do they drive it?
# people believe Robert Parker drives prices
# No surprise that RP has the highest correlations "influence" on everybody else (sum sq metric)





