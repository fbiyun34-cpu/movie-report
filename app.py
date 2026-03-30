import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="영화 흥행 패턴 분석 대시보드",
    page_icon="🎬",
    layout="wide"
)

# 폰트 및 스타일 설정 (나눔고딕 권장)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Nanum+Gothic', sans-serif;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stCard {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #1e1e1e;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data
def load_data():
    results_path = "data/processed/analysis_results.json"
    if not os.path.exists(results_path):
        # 상대 경로 대응 (src 하위에 있을 경우 등)
        results_path = os.path.join(os.path.dirname(__file__), "data/processed/analysis_results.json")
    
    with open(results_path, "r", encoding="utf-8") as f:
        return json.load(f)

try:
    data = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바
st.sidebar.title("🎬 영화 분석 메뉴")
menu = st.sidebar.radio("보고 싶은 분석을 선택하세요:", ["종합 대시보드", "영화별 키워드 상세", "토픽 모델링 분석", "흥행 전략 패턴"])

# 본문
if menu == "종합 대시보드":
    st.title("📊 국내 주요 영화 리뷰 및 흥행 분석")
    st.write("분석된 영화 데이터를 바탕으로 시장의 트렌드와 흥행 요인을 한눈에 파악합니다.")
    
    # 상단 요약 지표 (Metric)
    col1, col2, col3 = st.columns(3)
    movie_stats = data['movie_stats']
    total_reviews = sum(movie_stats.values())
    top_movie = max(movie_stats, key=movie_stats.get)
    
    col1.metric("총 분석 리뷰 수", f"{total_reviews:,}건")
    col2.metric("최대 리뷰 영화", top_movie, f"{movie_stats[top_movie]:,}건")
    col3.metric("분석 대상 영화 수", f"{len(movie_stats)}편")
    
    st.divider()
    
    # 영화별 리뷰 수 시각화
    st.subheader("📈 영화별 리뷰 데이터량 (관심도)")
    df_stats = pd.DataFrame(list(movie_stats.items()), columns=['영화명', '리뷰수']).sort_values(by='리뷰수', ascending=True)
    fig_stats = px.bar(
        df_stats, 
        x='리뷰수', 
        y='영화명', 
        orientation='h',
        text='리뷰수',
        color='리뷰수',
        color_continuous_scale='Blues',
        template='plotly_white'
    )
    fig_stats.update_traces(texttemplate='%{text}', textposition='outside')
    fig_stats.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_stats, use_container_width=True)

    # 흥행 패턴 요약
    st.subheader("⭐ 4대 흥행 패턴 전략 가이드")
    patterns = data['blockbuster_patterns']
    p_cols = st.columns(len(patterns))
    for i, (name, details) in enumerate(patterns.items()):
        with p_cols[i]:
            st.markdown(f"""
            <div class='stCard'>
                <h4>{name}</h4>
                <p><b>대상 영화</b>: {', '.join(details['movies'])}</p>
                <p><b>성공 동력</b>: <br>{details['trigger']}</p>
                <p><b>핵심 전략</b>: {details['strategy']['marketing']}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "영화별 키워드 상세":
    st.title("🔍 영화별 핵심 키워드 (TF-IDF)")
    
    selected_movie = st.selectbox("영화를 선택하여 분석된 핵심 단어를 확인하세요:", list(data['movie_keywords'].keys()))
    
    keywords = data['movie_keywords'][selected_movie]
    df_kw = pd.DataFrame(keywords)
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        fig_kw = px.bar(
            df_kw.sort_values(by='score', ascending=True),
            x='score',
            y='word',
            orientation='h',
            title=f"'{selected_movie}'의 핵심 키워드 TOP 15",
            labels={'score': 'TF-IDF 점수', 'word': '단어'},
            color='score',
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        st.plotly_chart(fig_kw, use_container_width=True)
    
    with col_r:
        st.write("### 📝 단어별 점수표")
        st.dataframe(
            df_kw[['word', 'score']],
            column_config={
                "word": "단어",
                "score": st.column_config.ProgressColumn(
                    "중요도 점수",
                    help="TF-IDF 기반 핵심 단어 점수",
                    format="%.4f",
                    min_value=0,
                    max_value=float(df_kw['score'].max() if not df_kw.empty else 1.0),
                )
            },
            hide_index=True,
            use_container_width=True,
            height=450
        )

elif menu == "토픽 모델링 분석":
    st.title("💎 리뷰 토픽 모델링 (LDA)")
    st.write("리뷰 본문에서 추출된 5가지 주요 담론(Topic)을 시각화합니다.")
    
    lda_topics = data['lda_topics']
    
    for topic in lda_topics:
        with st.expander(f"Topic {topic['topic_id']}: {topic['name']}"):
            df_topic = pd.DataFrame({'단어': topic['words'], '가중치': topic['values']})
            fig_topic = px.bar(
                df_topic.sort_values(by='가중치', ascending=True),
                x='가중치',
                y='단어',
                orientation='h',
                color='가중치',
                color_continuous_scale='Sunsetdark',
                template='plotly_white'
            )
            st.plotly_chart(fig_topic, use_container_width=True)

elif menu == "흥행 전략 패턴":
    st.title("🎯 영화 비즈니스 모델 및 전략")
    
    patterns = data['blockbuster_patterns']
    selected_pattern = st.radio("흥행 패턴 유형을 선택하세요:", list(patterns.keys()))
    
    p_info = patterns[selected_pattern]
    
    st.success(f"### {selected_pattern}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **📽️ 대표 사례**: {', '.join(p_info['movies'])}  
        **⚡ 핵심 트리거**: {p_info['trigger']}  
        **⚠️ 주요 리스크**: {p_info['risk']}
        """)
    
    with col2:
        st.info("**📋 실행 전략 (Strategy)**")
        st.write(f"- 💰 예산 규모: {p_info['strategy']['budget']}")
        st.write(f"- ⏳ 수명 주기: {p_info['strategy']['lifecycle']}")
        st.write(f"- 📣 마케팅: {p_info['strategy']['marketing']}")

# 푸터
st.divider()
st.caption("Produced by Cinema Report AI Team | Data Sources: Naver Review & Watcha Integrated")
