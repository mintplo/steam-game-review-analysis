# Standard library imports
import os
import ast

# Third Party library imports
import pandas as pd
from pandas.io.json import json_normalize


# Flatten 을 위한 함수
def only_dict(d):
    """
    Convert json string representation of dictionary to a python dict
    """
    return ast.literal_eval(d)


"""
Negative Reviews CSV Filename for import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './negative_reviews.csv')
negative_reviews = pd.read_csv(csv_filename)

# Recommendation ID KEY 중복된 데이터 제거
negative_reviews = negative_reviews.drop_duplicates(['recommendationid'],
                                                    keep='first')
# 쓸모 없는 Column 제거
negative_reviews = negative_reviews.drop(['Unnamed: 0'], axis=1)

# Negative Reviews 데이터 전체 태그
negative_reviews['is_recommend'] = False

# JSON 데이터 형식으로 된 Author 정보 Flatten 처리
negative_authors = negative_reviews['author'].apply(pd.Series)
normalized_negative_authors = json_normalize(
    negative_authors[0].apply(only_dict).tolist())

normalized_negative_reviews = pd.concat([
    negative_reviews.drop(['author'], axis=1),
    json_normalize(negative_authors[0].apply(only_dict).tolist())
],
                                        axis=1)
"""
Positive Reviews CSV Filename for import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './positive_reviews.csv')
positive_reviews = pd.read_csv(csv_filename)

# Recommendation ID KEY 중복된 데이터 제거
positive_reviews = positive_reviews.drop_duplicates(['recommendationid'],
                                                    keep='first')
# 쓸모 없는 Column 제거
positive_reviews = positive_reviews.drop(['Unnamed: 0'], axis=1)

# Negative Reviews 데이터 전체 태그
positive_reviews['is_recommend'] = False

# JSON 데이터 형식으로 된 Author 정보 Flatten 처리
positive_authors = positive_reviews['author'].apply(pd.Series)
normalized_positive_authors = json_normalize(
    positive_authors[0].apply(only_dict).tolist())

normalized_positive_reviews = pd.concat([
    positive_reviews.drop(['author'], axis=1),
    json_normalize(positive_authors[0].apply(only_dict).tolist())
],
                                        axis=1)

# 부정적 리뷰 데이터 세트와 긍정적 리뷰 데이터 세트 MERGE
normalized_reviews = pd.concat(
    [normalized_negative_reviews, normalized_positive_reviews], axis=0)
"""
Nomarlized Reviews Export
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './normalized_reviews.csv')
normalized_reviews.to_csv(csv_filename, mode='w')
