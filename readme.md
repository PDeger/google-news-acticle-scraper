# Google news RSS feed scraper

## Contents

This repository contains code and sample data used in creating a dataset of google news articles (meaning their titles, urls and sources) over an arbitrary timeframe. 

The following files are included: 

**rss_scraper.py**

This is the main scraping script. It produces a CSV file containing data from german language google news articles. It does this by building RSS search queries for each day from the current to the end data for each of the four categories (Deutschland, Wirtschaft, Technologie, Gesundheit) that where subject to this project. 
The CSV file contains the following columns: titel,source,original_url,published_raw,category,article_date.
Usage: run in cmd or terminal -> python rss_scraper.py

**tf-idf_model_trainer.ipynb**

This is a guided notebook with whom a classifier can be trained and evaluated. This classifier is trained on a ground truth dataset of articles who's actual category is known. This means that their category is directly queried from google news instead of assuming if based on a RSS query with words that are assumed to be likely to yield articles from a certain category. One sich ground truth file that has been build form articles collected over four  weeks is included in this repository. This notebook also guides the user trough extracting actual words that trained classifier was most sensitive towards to find better words to put in the search queries used in the actual scraper script.

**topic_scraper.ipynb**

This notebook provides a tool to create or expand a existing ground truth dataset of google news articles from the four categories. It queries google news with the topic id directly meaning that the returned articles for each topic id really do belong to said category, allowing them to be used as a ground truth for use in the training of the classifier in tf-idf_model_trainer.

**google_news_training_ground_truth.csv**

A dataset of ground truth articles scraped from early June 2026 up to late July 2026 using the topic_scraper

**google_news_6_month_rss_record.csv**

A sample dataset scraped form the google news RSS feed using the query system applied in the rss_scraper script.
