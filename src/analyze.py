import pandas as pd
import numpy as np
import re
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.cluster import KMeans
from soynlp.tokenizer import MaxScoreTokenizer
from soynlp.word import WordExtractor

# 1. 데이터 로드 및 환경 설정
DATA_DIR = "movie_dash_board/data"
PROCESSED_DIR = "movie_dash_board/data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 영화 ID 매핑
MOVIE_ID_MAP = {
    "명량": "myeongryang",
    "기생충": "parasite",
    "사도": "sado",
    "왕과 사는 남자": "the_kings_garden",
    "왕사남": "the_kings_garden",
    "올빼미": "the_night_owl",
    "남산의 부장들": "the_man_standing_next",
    "헤어질 결심": "decision_to_leave"
}

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # 특수문자 제거 및 한글/공백만 유지
    text = re.sub(r'[^가-힣\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Step 1: 데이터 로드
def load_and_preprocess():
    # 네이버 리뷰 (encoding: utf-8-sig 또는 cp949)
    try:
        naver_df = pd.read_csv(f"{DATA_DIR}/naver_review_data.csv", encoding='utf-8-sig')
    except:
        naver_df = pd.read_csv(f"{DATA_DIR}/naver_review_data.csv", encoding='cp949')
    
    # 왓챠 리뷰
    watcha_pop = pd.read_csv(f"{DATA_DIR}/watcha_reviews_popular_integrated.csv")
    
    # 통합 리뷰 데이터 생성
    # 네이버: review 컬럼, 왓챠: review_text 컬럼
    naver_subset = naver_df[['movie_title', 'review']].rename(columns={'movie_title': 'movieNm', 'review': 'text'})
    # movie_title이 깨졌을 경우를 대비해 수동 보정 (ID 매핑 활용)
    # 실제 데이터 확인 결과 'հ  ' 등 깨짐 현상 있을 수 있음 
    # 여기서는 text 데이터를 기반으로 분석을 우선 수행
    
    watcha_subset = watcha_pop[['movie_id', 'review_text']].rename(columns={'movie_id': 'movie_id', 'review_text': 'text'})
    # ID -> Nm 매핑 역순
    ID_TO_NM = {v: k for k, v in MOVIE_ID_MAP.items()}
    watcha_subset['movieNm'] = watcha_subset['movie_id'].map(ID_TO_NM)
    
    combined_reviews = pd.concat([naver_subset[['movieNm', 'text']], watcha_subset[['movieNm', 'text']]], ignore_index=True)
    combined_reviews = combined_reviews.dropna(subset=['text', 'movieNm'])
    
    # 분석 대상 7편만 필터링
    target_movies = ["명량", "기생충", "사도", "올빼미", "남산의 부장들", "헤어질 결심", "왕과 사는 남자", "왕사남"]
    combined_reviews = combined_reviews[combined_reviews['movieNm'].isin(target_movies)]
    combined_reviews['movieNm'] = combined_reviews['movieNm'].replace("왕사남", "왕과 사는 남자")
    
    # Step 2: 텍스트 정제
    combined_reviews['clean_text'] = combined_reviews['text'].apply(clean_text)
    
    # Step 3: 토큰화 (soynlp 학습)
    word_extractor = WordExtractor()
    word_extractor.train(combined_reviews['clean_text'].tolist())
    words = word_extractor.extract()
    # 점수 기반 토크나이저 생성
    scores = {word: score.cohesion_forward for word, score in words.items()}
    tokenizer = MaxScoreTokenizer(scores=scores)
    
    combined_reviews['tokens'] = combined_reviews['clean_text'].apply(lambda x: " ".join(tokenizer.tokenize(x)))
    
    return combined_reviews

# 분석 수행
print("Step 1-3: 로딩 및 전처리 시작...")
reviews_df = load_and_preprocess()

# Step 4: 불용어 전략 (영화 제목 등 제외)
stopwords = ["진짜", "너무", "진짜", "정말", "영화", "보고", "영화는", "완전", "그냥", "좀", "많이", "있는"]
def remove_stopwords(text):
    return " ".join([w for w in text.split() if w not in stopwords and len(w) > 1])

reviews_df['tokens'] = reviews_df['tokens'].apply(remove_stopwords)

# Step 5: TF-IDF
print("Step 5: TF-IDF 벡터화...")
tfidf = TfidfVectorizer(max_features=1000)
tfidf_matrix = tfidf.fit_transform(reviews_df['tokens'])

# 7. 분석 기법별 결과 도출
results = {}

# 7. 분석 기법별 결과 도출 (시각화 데이터 강화)
results = {}

# (1) 영화별 핵심 키워드 (TF-IDF 상위 + 점수)
movie_keywords = {}
for movie in reviews_df['movieNm'].unique():
    movie_indices = reviews_df[reviews_df['movieNm'] == movie].index
    movie_tfidf = tfidf_matrix[movie_indices].mean(axis=0).tolist()[0]
    top_indices = np.argsort(movie_tfidf)[::-1][:15] # 상위 15개
    features = tfidf.get_feature_names_out()
    movie_keywords[movie] = [
        {"word": features[i], "score": float(movie_tfidf[i])} 
        for i in top_indices
    ]
results['movie_keywords'] = movie_keywords

# (2) 영화별 리뷰 수 (데이터 볼륨)
results['movie_stats'] = reviews_df['movieNm'].value_counts().to_dict()

# (3) LDA 토픽 모델링 (5개)
print("Step: LDA 분석 중...")
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda_output = lda.fit_transform(tfidf_matrix)

lda_topics = []
topic_names = ["연기력 중심성", "영화별 어휘 차별화", "긍정 편향", "단문 지배", "글로벌 인지도"]
features = tfidf.get_feature_names_out()
for idx, topic in enumerate(lda.components_):
    top_indices = topic.argsort()[:-11:-1]
    lda_topics.append({
        "topic_id": idx, 
        "name": topic_names[idx], 
        "words": [features[i] for i in top_indices],
        "values": [float(topic[i]) for i in top_indices]
    })
results['lda_topics'] = lda_topics

# (4) NMF 토픽 모델링 (5개)
print("Step: NMF 분석 중...")
nmf = NMF(n_components=5, random_state=42)
nmf_output = nmf.fit_transform(tfidf_matrix)

nmf_topics = []
for idx, topic in enumerate(nmf.components_):
    top_indices = topic.argsort()[:-11:-1]
    nmf_topics.append({
        "topic_id": idx, 
        "words": [features[i] for i in top_indices],
        "values": [float(topic[i]) for i in top_indices]
    })
results['nmf_topics'] = nmf_topics

# (5) K-Means 군집 분석 (5개)
print("Step: Clustering...")
kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
clusters = kmeans.fit_predict(tfidf_matrix)
reviews_df['cluster'] = clusters

# 군집 특징 (영화 분포 및 상세 수치)
cluster_profile = reviews_df.groupby('cluster')['movieNm'].value_counts().unstack().fillna(0)
results['cluster_profile'] = cluster_profile.to_dict()
results['cluster_stats'] = reviews_df['cluster'].value_counts().to_dict()

# 4대 흥행 패턴 (가공된 인사이트 - 수치 로직 보강 시 필요 데이터 포함)
results['blockbuster_patterns'] = {
    "Classic Blockbuster (천만 영화형)": {
        "movies": ["명량", "기생충"],
        "trigger": "보편적 정서 + 압도적 스케일/작품성",
        "risk": "기대치 과포화",
        "strategy": {"budget": "200억+", "lifecycle": "8주+", "marketing": "전세대 타겟 리치 마케팅"}
    },
    "Steady Long-run (롱런/매니아형)": {
        "movies": ["헤어질 결심", "올빼미"],
        "trigger": "N차 관람 + 팬덤 형성",
        "risk": "초반 화력 부족",
        "strategy": {"budget": "80억-120억", "lifecycle": "12주+", "marketing": "GV, 팬덤 굿즈, SNS 바이럴"}
    },
    "High Tension Drama (사극/드라마형)": {
        "movies": ["사도", "남산의 부장들"],
        "trigger": "배우 연기력 + 역사적 실화 몰입",
        "risk": "신파 논란",
        "strategy": {"budget": "100억-150억", "lifecycle": "6주", "marketing": "배우 중심 마케팅, 관람 후기 강화"}
    },
    "Experimental Focus (비즈니스 집중형)": {
        "movies": ["왕과 사는 남자"],
        "trigger": "독창적 소재 + 타겟팅 명확화",
        "risk": "대중성 확보",
        "strategy": {"budget": "50억-80억", "lifecycle": "4주", "marketing": "플랫폼 최적화, 숏폼 마케팅"}
    }
}

# 8. 최종 결과 저장 (JSON)
with open(f"{PROCESSED_DIR}/analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"분석 완료! 결과 저장됨: {PROCESSED_DIR}/analysis_results.json")
