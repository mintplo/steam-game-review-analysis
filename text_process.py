# Standard library imports
import os
import re
import itertools
import time
from collections import Counter

# Third Party library imports
import pandas as pd
import spacy
import simplejson


def extract_common_words(list_of_list, n=10):
    """
    Return N-Most Common Words with list of list
    """
    list_of_list = list(itertools.chain(*list_of_list))
    list_freq = Counter(list_of_list)
    list_freq_words = list_freq.most_common(n)

    return list_freq_words


"""
Normalized English Reviews CSV Import
"""
dirname = os.path.dirname(__file__)
csv_filename = os.path.join(dirname, './normalized_eng_reviews.csv')
normalized_english_reviews = pd.read_csv(csv_filename)

# Spacy NLP
nlp = spacy.load('en_core_web_lg')  # Use Large Model


def analyze_frequently_words(reviews, n=10, file_name=None):
    """
    들어온 REVIEWS 대상으로 자주 빈출되는 단어 분석 출력
    """
    # 텍스트, 명사, 동사, 형용사 정보
    texts = []
    noun_list = []
    verb_list = []
    adj_list = []
    for document in reviews:
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+",
            flags=re.UNICODE)
        emoji_stripped_doc = emoji_pattern.sub(r'', document)
        newline_stripped_doc = re.sub(
            '\s+|█|░|▀|▒|▄|⠀|─|☐|game',
            ' ',  # game 단어 제거
            emoji_stripped_doc)  # █ ░ remove + newline stripped

        print(newline_stripped_doc)

        text = []
        noun = []
        verb = []
        adj = []

        doc = nlp(newline_stripped_doc)
        for w in doc:
            # 동사 단어 추가
            if not w.is_stop and w.pos_ == "VERB":
                verb.append(w.lemma_)

            # 명사 단어 추가
            if not w.is_stop and w.pos_ == "NOUN":
                noun.append(w.lemma_)

            # 형용사 단어 추가
            if not w.is_stop and w.pos_ == "ADJ":
                adj.append(w.lemma_)

            # 불용어 + is_punct + line_num 제거
            if not w.is_stop and not w.is_punct and not w.like_num:
                text.append(w.lemma_)

        # 최종 정보 취합
        noun_list.append(noun)
        verb_list.append(verb)
        adj_list.append(adj)
        texts.append(text)

    # File Name is None
    if file_name is None:
        # file_name =
        file_name = time.strftime("%Y%m%d_%H%M%S")

    dirname = os.path.dirname(__file__)
    pkl_filename = os.path.join(dirname, './text_processing/',
                                file_name + '.txt')

    # 명사 Freq
    noun_freq_words = extract_common_words(noun_list, n)
    print(noun_freq_words)

    # 동사 Freq
    verb_freq_words = extract_common_words(verb_list, n)
    print(verb_freq_words)

    # 형용사 Freq
    adj_freq_words = extract_common_words(adj_list, n)
    print(adj_freq_words)

    # 전체 텍스트 Freq
    all_freq_words = extract_common_words(texts, n)

    f = open(pkl_filename, 'w')
    simplejson.dump(noun_freq_words, f)
    simplejson.dump(verb_freq_words, f)
    simplejson.dump(adj_freq_words, f)
    simplejson.dump(all_freq_words, f)
    f.close()


# 전체 리뷰 대상 분석
analyze_frequently_words(normalized_english_reviews['review'],
                         n=10,
                         file_name='all')

# Recommend/Not Recommend
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['is_recommend'] == True]['review'],
                         n=10,
                         file_name='recommend')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['is_recommend'] == False]['review'],
                         n=10,
                         file_name='not_recommend')

# 무료로 받은 사람 T/F
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['received_for_free'] == True]['review'],
                         n=10,
                         file_name='received_for_free')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['received_for_free'] == False]['review'],
                         n=10,
                         file_name='received_for_not_free')

# Early Access 사용자 T/F
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['written_during_early_access'] == True]
                         ['review'],
                         n=10,
                         file_name='written_during_early_access')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['written_during_early_access'] == False]
                         ['review'],
                         n=10,
                         file_name='not_written_during_early_access')

# VOTES_UP 50% 구간 2개 초과/2개 이하
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['votes_up'] > 2]['review'],
                         n=10,
                         file_name='votes_up_2_high')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['votes_up'] <= 2]['review'],
                         n=10,
                         file_name='votes_up_2_low')

# PLAYTIME_FOREVER 25% 구간 6381 초과/6381 이하
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['playtime_forever'] > 6381]['review'],
                         n=10,
                         file_name='playtime_forever_6381_high')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['playtime_forever'] <= 6381]['review'],
                         n=10,
                         file_name='playtime_forever_6381_low')

# NUM_GAMES_OWNED 50% 구간 66개 초과/66개 이하
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['num_games_owned'] > 66]['review'],
                         n=10,
                         file_name='num_games_owned_66_high')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['num_games_owned'] <= 66]['review'],
                         n=10,
                         file_name='num_games_owned_66_low')

# NUM_REVIEWS 50% 구간 3개 이상/3개 이하
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['num_reviews'] > 3]['review'],
                         n=10,
                         file_name='num_reviews_3_high')
analyze_frequently_words(normalized_english_reviews[
    normalized_english_reviews['num_reviews'] <= 3]['review'],
                         n=10,
                         file_name='num_reviews_3_low')
