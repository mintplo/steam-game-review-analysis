# Standard library imports
import os

# Third Party library imports
import pandas as pd
"""
Normalized English Reviews CSV Import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './sentimental_matched_reviews.csv')
normalized_english_reviews = pd.read_csv(csv_filename)

normalized_english_reviews = normalized_english_reviews.drop(
    ['Unnamed: 0', 'index'], axis=1)

print(normalized_english_reviews[normalized_english_reviews['is_not_match'] ==
                                 True].shape[0])
print(normalized_english_reviews[normalized_english_reviews['is_not_match'] ==
                                 False].shape[0])
