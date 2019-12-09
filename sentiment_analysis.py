# Standard library imports
import os

# Third Party library imports
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
"""
Normalized English Reviews CSV Import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './normalized_eng_reviews.csv')
normalized_english_reviews = pd.read_csv(csv_filename)
"""
Recommend, Not Recommend Fake Data Assembled with Sentiment Analyzer
"""
analyzer = SentimentIntensityAnalyzer()


def sentiment_analysis(sentence, is_recommend):
    vs = analyzer.polarity_scores(sentence)
    print(is_recommend)
    print(vs)
    if vs['compound'] >= 0.5:  # 긍정
        if is_recommend:
            return False
        else:
            return True
    elif vs['compound'] > -0.05 and vs['compound'] < 0.05:  # 중립은 Okay
        return False
    else:  # 부정
        if is_recommend:
            return False
        else:
            return True


# is recommend correct? with Sentiment Analysis
normalized_english_reviews['is_not_match'] = normalized_english_reviews.apply(
    lambda x: sentiment_analysis(x['review'], x['is_recommend']), axis=1)

print(normalized_english_reviews[['review', 'is_recommend', 'is_not_match']])
# 리뷰 문장의 감정 분석 결과와 유저가 선택한 긍정/부정 옵션과 매칭 결과
print(normalized_english_reviews[normalized_english_reviews['is_not_match'] ==
                                 False])
print(normalized_english_reviews[normalized_english_reviews['is_not_match'] ==
                                 True])
"""
Normalized English Reviews CSV Export
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './sentimental_matched_reviews.csv')
normalized_english_reviews.to_csv(csv_filename, mode='w')
