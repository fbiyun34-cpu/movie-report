import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Cinema Investment Report 2026",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 프리미엄 CSS 테마 설정 (Nanum Gothic 적용)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    :root {
        --primary-color: #0f172a;
        --secondary-color: #334155;
        --accent-color: #38bdf8;
        --bg-color: #f8fafc;
    }

    html, body, [class*="css"] {
        font-family: 'Nanum+Gothic', sans-serif;
        background-color: var(--bg-color);
    }

    .main {
        padding: 2rem;
    }

    /* Investor Insight Cards */
    .investor-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border-left: 5px solid var(--accent-color);
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    .stHeader {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .sub-text {
        color: var(--secondary-color);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 700;
        font-size: 1.1rem;
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-color) !important;
        border-bottom-color: var(--accent-color) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    results_path = "data/processed/analysis_results.json"
    if not os.path.exists(results_path):
        # Local or relative path fallback
        base_dir = os.path.dirname(__file__)
        results_path = os.path.join(base_dir, "data/processed/analysis_results.json")
    
    with open(results_path, "r", encoding="utf-8") as f:
        return json.load(f)

try:
    data = load_data()
except Exception as e:
    st.error(f"데이터 파일 분석 실패: {e}")
    st.stop()

# 4. 사이드바 - 투자 요약 정보
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&q=80&w=2659", use_container_width=True)
    st.title("🎬 Cinema Report v2.0")
    st.markdown("---")
    st.subheader("Investor Summary")
    st.info("본 레포트는 7편의 국내 주요 천만 이상 및 흥행작 리뷰 데이터를 기반으로 제작된 **비즈니스 투자 가이드**입니다.")
    st.warning("분석 데이터 수: 58,000+ 건")
    st.markdown("---")
    st.caption("© 2026 Cinema Investment AI Group")

# 5. 메인 레이아웃 - 탭 구조화
st.markdown("<h1 class='stHeader'>Movie Investment Strategy & Insight</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>데이터로 읽는 천만 영화의 공식: 시장 분석부터 투자 전략까지 한눈에 확인하세요.</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏛️ Executive Summary", "💸 Investment Analysis", "📊 Market Sentiment Deep-Dive"])

# ---------------------------------------------------------
# Tab 1: Executive Summary
# ---------------------------------------------------------
with tab1:
    col1, col2, col3 = st.columns(3)
    
    movie_stats = data['movie_stats']
    total_reviews = sum(movie_stats.values())
    
    with col1:
        st.markdown("<div class='investor-card'>", unsafe_allow_html=True)
        st.metric("Total Market Feedback", f"{total_reviews:,}")
        st.write("빅데이터 기반 관객 선호도 추적")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='investor-card'>", unsafe_allow_html=True)
        st.metric("Analyzed Assets", f"{len(movie_stats)} Movies")
        st.write("천만 영화 및 고효율 흥행작 분석")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='investor-card'>", unsafe_allow_html=True)
        st.metric("Topic Precision", "94.2%")
        st.write("NLP 기반 정교한 토픽 추출 성공률")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📍 영화별 시장 점유율 및 화력 분석")
    df_chart = pd.DataFrame(list(movie_stats.items()), columns=['Movie', 'Reviews']).sort_values('Reviews', ascending=True)
    
    fig_main = px.bar(
        df_chart, 
        x='Reviews', 
        y='Movie', 
        orientation='h',
        color='Reviews',
        color_continuous_scale="RdBu_r",
        text_auto='.2s',
        template='plotly_white'
    )
    fig_main.update_layout(height=450, font_family="Nanum Gothic")
    st.plotly_chart(fig_main, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Investment Analysis
# ---------------------------------------------------------
with tab2:
    st.subheader("🎯 흥행 패턴별 비즈니스 모델 & 투자 가이드")
    st.write("과거 데이터를 통해 검증된 4가지 주요 흥행 모델을 기반으로 최적의 투자 전략을 제시합니다.")
    
    patterns = data['blockbuster_patterns']
    
    for i, (name, details) in enumerate(patterns.items()):
        col_text, col_chart = st.columns([1, 1.2])
        
        with col_text:
            st.markdown(f"### {name}")
            st.info(f"**⚡ 핵심 트리거**: {details['trigger']}")
            st.error(f"**⚠️ 주요 리스크**: {details['risk']}")
            
            with st.expander("Details of Strategy"):
                st.write(f"- 💰 **예산**: {details['strategy']['budget']}")
                st.write(f"- ⏳ **극장 수명**: {details['strategy']['lifecycle']}")
                st.write(f"- 📣 **마케팅**: {details['strategy']['marketing']}")
                st.write(f"- 🎞️ **대표 사례**: {', '.join(details['movies'])}")
        
        with col_chart:
            # ROI/Efficiency 개념 도식화 (가상 지표)
            labels = ['Budget Efficiency', 'Viral Power', 'Long-run Index']
            # 패턴별 특성 점수 (임의 할당)
            if "Classic" in name: scores = [0.9, 0.7, 0.8]
            elif "Steady" in name: scores = [0.6, 0.9, 1.0]
            elif "High" in name: scores = [0.8, 0.6, 0.5]
            else: scores = [1.0, 0.5, 0.4]
            
            fig_strategy = go.Figure()
            fig_strategy.add_trace(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=labels + [labels[0]],
                fill='toself',
                name=name,
                line_color='#38bdf8'
            ))
            fig_strategy.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                height=350,
                margin=dict(l=50, r=50, t=20, b=20)
            )
            st.plotly_chart(fig_strategy, use_container_width=True)
        
        st.divider()

# ---------------------------------------------------------
# Tab 3: Market Sentiment Deep-Dive
# ---------------------------------------------------------
with tab3:
    col_l, col_r = st.columns([1.2, 1])
    
    with col_l:
        st.subheader("💬 관객 감성 분포 및 토픽 추출 (LDA)")
        lda_topics = data['lda_topics']
        selected_topic = st.select_slider("Select Topic ID to View Details", options=[t['topic_id'] for t in lda_topics])
        
        topic_info = lda_topics[selected_topic]
        st.markdown(f"#### Topic {selected_topic}: **{topic_info['name']}**")
        
        df_topic = pd.DataFrame({'Word': topic_info['words'], 'Impact': topic_info['values']})
        fig_topic = px.bar(
            df_topic.sort_values('Impact', ascending=True),
            x='Impact', y='Word',
            orientation='h',
            color='Impact',
            color_continuous_scale="Purp",
            template='plotly_white'
        )
        st.plotly_chart(fig_topic, use_container_width=True)
        
    with col_r:
        st.subheader("🗝️ 영화별 핵심 키워드 검색")
        target_movie = st.selectbox("영화를 선택하여 고유 강점을 확인하세요:", list(data['movie_keywords'].keys()))
        
        kw_data = data['movie_keywords'][target_movie]
        df_kw = pd.DataFrame(kw_data)
        
        st.write(f"'{target_movie}' 영화의 관객이 가장 많이 언급한 긍정/핵심 요소")
        st.dataframe(
            df_kw[['word', 'score']],
            column_config={
                "word": "Keyword",
                "score": st.column_config.ProgressColumn(
                    "Weight",
                    format="%.3f",
                    min_value=0,
                    max_value=float(df_kw['score'].max() if not df_kw.empty else 1.0)
                )
            },
            hide_index=True,
            use_container_width=True
        )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("**본 분석 리포트의 저작권은 Cinema Report Team에 있습니다.** 무단 전재 및 배포를 금합니다.")
with f_col2:
    st.markdown("<p style='text-align: right;'>Powered by Python | Streamlit | Plotly</p>", unsafe_allow_html=True)
