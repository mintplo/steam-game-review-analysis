# Standard library imports
import os

# Third Party library imports
import pandas as pd
"""
Normalized English Reviews CSV Import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './normalized_eng_reviews.csv')
normalized_english_reviews = pd.read_csv(csv_filename)

normalized_english_reviews = normalized_english_reviews.drop(
    ['Unnamed: 0', 'index'], axis=1)

# Normalized English Reviews Data Frame describe
# num_games_owned, num_reviews, playtime_forever, votes_up, votes_funny, comment_count
print(normalized_english_reviews[[
    'num_games_owned', 'num_reviews', 'votes_up', 'votes_funny',
    'comment_count', 'playtime_forever'
]].describe())

# steam_purchase, received_for_free, written_during_early_access
print(normalized_english_reviews[normalized_english_reviews['steam_purchase']
                                 == True].shape[0])
print(normalized_english_reviews[normalized_english_reviews['steam_purchase']
                                 == False].shape[0])

print(normalized_english_reviews[
    normalized_english_reviews['received_for_free'] == True].shape[0])
print(normalized_english_reviews[
    normalized_english_reviews['received_for_free'] == False].shape[0])

print(normalized_english_reviews[
    normalized_english_reviews['written_during_early_access'] ==
    True].shape[0])
print(normalized_english_reviews[
    normalized_english_reviews['written_during_early_access'] ==
    False].shape[0])
