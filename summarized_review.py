# Standard library imports
import os
import heapq
from pprint import pprint

# Third Party library imports
import pandas as pd
from gensim.summarization import summarize
import nltk

nltk.download('punkt')
nltk.download('stopwords')


def summarize_with_nltk(review):
    sentence_list = nltk.sent_tokenize(review)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(review):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7,
                                       sentence_scores,
                                       key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary


"""
Normalized English Reviews CSV Import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './normalized_eng_reviews.csv')
normalized_english_reviews = pd.read_csv(csv_filename)
normalized_english_reviews = normalized_english_reviews.drop(['Unnamed: 0'],
                                                             axis=1)

recommend_df = normalized_english_reviews[
    normalized_english_reviews['recommendationid'] == 42058154]
recommend_review = recommend_df.iloc[[0]]
recommend_review = recommend_review['review']

not_recommend_df = normalized_english_reviews[
    normalized_english_reviews['recommendationid'] == 39326124]
not_recommend_review = not_recommend_df.iloc[[0]]
not_recommend_review = not_recommend_review['review']

# NTLK, GENSIM 문장분석 차이점 각각 2*2
# === RECOMMEND
print("=== RECOMMEND")
print(recommend_review.iloc[0])

# RECOMMEND GENSIM
print("=== GENSIM")
pprint(summarize(recommend_review.iloc[0], ratio=0.1))

# RECOMMEND NLTK
print("=== NLTK")
summarize_text = summarize_with_nltk(recommend_review.iloc[0])
print(summarize_text)

# === NOT RECOMMEND
print("=== NOT RECOMMEND")
print(not_recommend_review.iloc[0])
# NOT RECOMMEND GENSIM
print("=== GENSIM")
pprint(summarize(not_recommend_review.iloc[0], ratio=0.1))

# NOT RECOMMEND NLTK
print("=== NLTK")
summarize_text = summarize_with_nltk(not_recommend_review.iloc[0])
print(summarize_text)
