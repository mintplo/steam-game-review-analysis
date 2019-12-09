# Standard library imports
import os
import time

# Third Party library imports
import pandas as pd

# Customized imports
import request

url = "https://store.steampowered.com/appreviews/578080"
parameters = {
    'num_per_page': 100,
    'review_type': 'negative',
    'day_range': '730',
    'filter': 'all',
    'cursor': '*'
}

positive_reviews = pd.DataFrame()
"""
Scrap Response Review
"""
for _ in range(0, 51):
    print(parameters)
    response = request.get_request(url=url, parameters=parameters)
    reviews_df = pd.DataFrame(response['reviews'])
    positive_reviews = pd.concat([positive_reviews, reviews_df], axis=0)
    positive_reviews = positive_reviews.drop_duplicates(['recommendationid'],
                                                        keep='first')
    print(positive_reviews)

    # IP 블락킹을 피하기 위해 sleeping
    time.sleep(10)
    """
    다음 리뷰 스크래핑을 위한 CURSOR 할당
    - 다음 리뷰가 없는 경우 스크랩 중단
    """
    next_page_cursor = response['cursor']
    if not next_page_cursor:
        break

    parameters['cursor'] = next_page_cursor
    print(parameters['cursor'])
"""
Positive Reviews CSV Filename for export
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './negative_reviews.csv')
positive_reviews.to_csv(csv_filename, mode='w')
