## Steam Game Review Analysis

## 개발환경설정 (based on MacOSX)
### 🔥 Requirements
- [Python 3.7](https://www.python.org/)
- [Pipenv](https://github.com/pypa/pipenv)

#### 1. Pipenv 설치

Mac OSX의 패키지 매니저인 Homebrew를 이용해 설치한다.
```
$ brew install pipenv
```

### 📦 Libraries
- [Python Pandas](https://pandas.pydata.org/)
- [Python Numpy](https://numpy.org/)
- [spaCy](https://spacy.io/)
- [Gensim](https://radimrehurek.com/gensim/)
- [vadersentiment](https://github.com/cjhutto/vaderSentiment)
- [nltk](https://www.nltk.org/)

## Specification

### Object
- 유저가 남긴 리뷰와 유저가 선택한 추천/비추천 관계를 통해 아래의 항목을 보고자 한다.
  - 유저가 추천한다고 선택한 리뷰에서 자주 쓰는 단어
  - 유저가 비 추천한다고 선택한 리뷰에서 자주 쓰는 단어
- 유저가 남긴 리뷰의 `Sentimental Analysis`, 유저 `게임 추천 여부 정보`와 정합성
- NTLK, GENSIM 문장 요약 차이 확인 (추천, 비추천 리뷰 각각 1개에 대해)

### Data Analysis

#### 1. Steam User Reviews 데이터 획득 `scrap_steam_reviews.py`
- `requests` 라이브러리 사용
- `Steam UserReview API`
- 변수 파라미터 `review_type`의 `positive`, `negative`에 따라 5100개씩 획득, 총 10200개

#### 2. 데이터 전처리
부정적 리뷰 세트, 긍정적 리뷰 세트 각각에 대해 아래의 처리를 진행

- `review_type: positive, negative`에 따른 `is_recommend` FLAG 추가
- `recommendationid` KEY 중복된 데이터 제거
- JSON 데이터 형식으로 된 `author` 정보 Flatten 처리
- 부정적 리뷰 데이터 세트와 긍정적 리뷰 데이터 세트 MERGE
- 영어로 된 리뷰만 텍스트 마이닝 분석 대상 처리

#### 3. EDA
아래 변수에 대한 기본 통계 분석 실시

**정수형**
- `num_games_owned`
- `num_reviews`
- `playtime_forever`
- `votes_up`
- `votes_funny`
- `comment_count`

**논리형**
- `steam_purchase`
- `received_for_free`
- `written_during_early_access`

#### 4. 텍스트 프로세싱
전체 리뷰에 대해 아래의 텍스트 프로세싱

- 이모지, 특수문자 제거
- NEWLINE 제거
- `STOP_WORD` 불용어 제거
- POS_TAG에 따라 `명사`, `형용사`, `동사` 분류
- `명사`, `형용사`, `동사`, `전체` 4가지 경우에 대한 WORD FREQ 데이터 추출

**EDA 분석에 따른 텍스트 프로세싱 추가 진행 (아래의 목록 대상)**
- Recommend/Not Recommend
- 무료로 받은 사람 T/F
- Early Access 사용자 T/F
- VOTES_UP 50% 구간 2개 초과/2개 이하
- PLAYTIME_FOREVER 25% 구간 6381 초과/6381 이하
- NUM_GAMES_OWNED 50% 구간 66개 초과/66개 이하
- NUM_REVIEWS 50% 구간 3개 이상/3개 이하

#### 5. 감정 분석
`vaderSentiment` 이용, 전체 리뷰에 대해 감정 분석을 실시하여 실제 유저가 선택한 추천/비추천 정보와 맞는지 확인

- 각 리뷰 문장에 대해 `polarity_scores` 산출
- `compound` 수치로 긍정, 중립, 부정 분류
  - >= 0.5: 긍정
  - > -0.05 and < 0.05: 중립
  - < -0.05: 부정
- `is_not_match` 정보 생성
- 기본 `EDA` 진행

#### 6. 문장 분석

- NLTK, GENSIM으로 각각 문장 분석 진행 + 차이점 확인

## 🔥 Running

#### 1. Pipenv를 이용해 의존성 패키지 설치

```
$ pipenv install
```

#### 2. 위 단계에 맞게 Python 실행 
```
$ python path/to/file.py
```

&nbsp;
--------

The source code of *mintplo* is primarily distributed under the terms
of the [GNU Affero General Public License v3.0] or any later version. See
[COPYRIGHT] for details.

[GNU Affero General Public License v3.0]: LICENSE
[COPYRIGHT]: COPYRIGHT
