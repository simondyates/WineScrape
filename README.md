# WineScrape

Findings from the data in this project are summarized in a Powerpoint presentation that can be found <a href="https://www.dropbox.com/sh/jugwemsfmztxtru/AACp-hIdi7YghRfmWCjuDdnQa?dl=0">here</a>.

The folder winedotcom contains the files used by Scrapy to generate the data.  The data is then cleaned and enhanced by wdc_processing.py, which outputs the file wdc_cleaned.csv used for analysis.  Initial exploration of this output data was done in the Jupyter Notebook WineDataExploration.ipynb.

Analysis of the correlation of ratings to price, and between raters is performed by rater_correls.py.  This outputs to ratercorrels.csv.

A simple tool for identifying the best-rated wines for a variety of criteria was created in the Jupyter Notebook WineChooser.ipynb.

The file selenium_scrape.py uses Selenium to scrape the vintage table on robertparker.com.  Selenium is necessary because this site uses Ajax.  This generates output stored in robertparker_raw.csv.  Currently, this data is not used in the project but will be incorporated in subsequent stages.

WineChooser.ipynb is hosted on Binder as a web app.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/simondyates/WineScrape/master?urlpath=%2Fvoila%2Frender%2FWineChooser.ipynb)
