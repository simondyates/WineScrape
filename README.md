# WineScrape

Findings from the data in this project are summarized in a Powerpoint presentation that can be found <a href="https://www.dropbox.com/sh/jugwemsfmztxtru/AACp-hIdi7YghRfmWCjuDdnQa?dl=0">here</a>.

The folder winedotcom contains the files used by Scrapy to generate the data.  The data is then cleaned and enhanced by wdc_processing.py, which outputs the file wdc_cleaned.csv used for analysis.

Analysis of the correlation of ratings to price, and between raters is performed by rater_correls.py.  This outputs to ratercorrels.csv.

The file selenium_scrape.py uses Selenium to scrape the vintage table on robertparker.com.  Selenium is necessary because this site uses Ajax.  This generates output stored in robertparker_raw.csv.  Currently, this data is not used in the project but will be incorporated in subsequent stages.
