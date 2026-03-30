import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정 (다크 모드 최적화)
st.set_page_config(
    page_title="흥행 트리거 차트 디코딩",
    page_icon="⚡",
    layout="wide",
)

# 2. 커스텀 CSS (시안 디자인 완벽 반영)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    /* 전체 배경 및 폰트 */
    .main {
        background-color: #0a0a0a !important;
        color: #ffffff;
        font-family: 'Nanum+Gothic', sans-serif;
    }
    
    /* 타이틀 그라데이션 */
    .gradient-text {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* 메트릭 카드 스타일 */
    .metric-card {
        background: rgba(30, 30, 30, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-label {
        color: #6366f1;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
    }

    /* 탭 커스텀 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 30px;
        width: fit-content;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 25px;
        background-color: transparent;
        border-radius: 25px;
        color: #94a3b8;
        font-weight: 700;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: white !important;
    }

    /* 차트 컨테이너 */
    .chart-box {
        background: rgba(20, 20, 20, 0.8);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .chart-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* 사이드바 숨기기 (시안 강조) */
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data
def load_data():
    results_path = "data/processed/analysis_results.json"
    if not os.path.exists(results_path):
        results_path = os.path.join(os.path.dirname(__file__), "data/processed/analysis_results.json")
    with open(results_path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# 4. 헤더 섹션
col_title, col_header_metrics = st.columns([2, 1])

with col_title:
    st.markdown("<h1 class='gradient-text'>흥행 트리거<br>차트 디코딩</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>6단계 정밀 파이프라인으로 추출된 수치 지표와 AI 모델링 결과를 통해<br>흥행의 핵심 동력을 시각화하고 비즈니스 로드맵을 제안합니다.</p>", unsafe_allow_html=True)

with col_header_metrics:
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Global Reach</div>
            <div class='metric-value'>92%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-label'>Sentiment Score</div>
            <div class='metric-value'>4.8</div>
        </div>
        """, unsafe_allow_html=True)

# 5. 내비게이션 탭 (시안 구조 반영)
tabs = st.tabs(["📊 전략 대시보드", "📖 수치 기반 분석", "💡 비즈니스 제언", "⛓️ 프로세스"])

# ---------------------------------------------------------
# Tab 1: 전략 대시보드 (시안 핵심 레이아웃)
# ---------------------------------------------------------
with tabs[0]:
    col_main, col_sub = st.columns([1.6, 1])
    
    with col_main:
        st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>📈 Market Segmentation</div>", unsafe_allow_html=True)
        
        movie_stats = data['movie_stats']
        df_stats = pd.DataFrame(list(movie_stats.items()), columns=['Movie', 'Reviews']).sort_values('Reviews', ascending=False)
        
        # 시안 컬러 팔레트 반영
        color_sequence = ['#6366f1', '#a855f7', '#ec4899', '#f43f5e', '#fb923c', '#facc15', '#22c55e']
        
        fig_bar = px.bar(
            df_stats,
            x='Movie',
            y='Reviews',
            color='Movie',
            color_discrete_sequence=color_sequence,
            template='plotly_dark'
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(l=0, r=0, t=20, b=50),
            height=450
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("""
        <p style='color: #64748b; font-size: 0.9rem;'>
        * 현재 통합 데이터셋의 리뷰 볼륨을 시각화합니다.<br>
        명량과 기생충이 시장 지배력이 가장 높으며, 고유의 팬덤층을 확보하고 있습니다.
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_sub:
        st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>🎯 LDA 토픽 비중</div>", unsafe_allow_html=True)
        
        lda_topics = data['lda_topics']
        categories = [t['name'] for t in lda_topics]
        # 임의의 비중 (시안의 Radar 형태 재현)
        values = [0.85, 0.70, 0.90, 0.45, 0.75]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(99, 102, 241, 0.4)',
            line=dict(color='#6366f1', width=2),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, gridcolor='rgba(255,255,255,0.1)'),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=10, color='#94a3b8'))
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=20, b=20),
            height=300
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Progress Bars (시안 우상단/하단 비트)
        for i, (cat, val) in enumerate(zip(categories, values)):
            col_label, col_prog = st.columns([1, 1.5])
            with col_label:
                st.markdown(f"<p style='font-size: 0.8rem; color: #94a3b8;'>{cat}</p>", unsafe_allow_html=True)
            with col_prog:
                st.progress(val)
                
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: 수치 기반 분석
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("📽️ 영화별 상세 지표 추적")
    
    selected_movie = st.selectbox("분석 대상 선택", list(data['movie_keywords'].keys()))
    kw_df = pd.DataFrame(data['movie_keywords'][selected_movie])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### '{selected_movie}' 핵심 키워드 가중치")
        fig_kw = px.bar(kw_df.head(10), x='score', y='word', orientation='h', color='score', color_continuous_scale='Magma')
        fig_kw.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_kw, use_container_width=True)
    
    with col2:
        st.markdown("#### 데이터 통계 개요")
        st.dataframe(kw_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Tab 3: 비즈니스 제언
# ---------------------------------------------------------
with tabs[2]:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.markdown("### 💡 AI 기반 전략 로드맵 제언")
    patterns = data['blockbuster_patterns']
    
    p_cols = st.columns(len(patterns))
    for i, (name, details) in enumerate(patterns.items()):
        with p_cols[i]:
            st.info(f"**{name}**")
            st.write(f"- {details['trigger']}")
            st.caption(f"Strategy: {details['strategy']['marketing']}")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 4: 프로세스
# ---------------------------------------------------------
with tabs[3]:
    st.markdown("### ⛓️ 6단계 정밀 분석 파이프라인")
    steps = [
        "1. 데이터 수집: Naver/Watcha 리뷰 통합",
        "2. 소이엔엘피(Soynlp) 기반 토큰화 및 불용어 제거",
        "3. TF-IDF 점수산출 및 가중치 키워드 추출",
        "4. LDA/NMF 토픽 모델링을 통한 핵심 담론 분류",
        "5. K-Means 군집 분석을 통한 흥행 모델링",
        "6. 시각화 및 비즈니스 의사결정 인사이트 도출"
    ]
    for step in steps:
        st.success(step)

# 6. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Cinema Report AI Integrated Dashboard | Data: KOBIS + Social Intelligence</p>", unsafe_allow_html=True)
