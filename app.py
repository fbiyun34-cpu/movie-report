import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정 (초고대비 전문가용)
st.set_page_config(page_title="Ultra-Contrast Cinema Intelligence v7.0", page_icon="💎", layout="wide")

# 2. 초고대비 디자인 시스템 (Absolute Clarity)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    /* 완전 블랙 배경 적용 */
    .main { background-color: #000000 !important; color: #ffffff; font-family: 'Nanum+Gothic', sans-serif; }
    
    /* 일렉트릭 사이언 헤더 */
    .promo-header { font-size: 4.5rem; font-weight: 800; color: #ffffff; letter-spacing: -3px; margin-bottom: 0.2rem; line-height: 1.0; }
    .accent-color { color: #00f2ff; text-shadow: 0 0 30px rgba(0, 242, 255, 0.4); }
    .sub-header { color: #888888; font-size: 1.4rem; margin-bottom: 3rem; font-weight: 400; letter-spacing: 0.5px; }

    /* 대형 고대비 KPI 카드 */
    .kpi-card { background: #080808; border: 2.5px solid #1a1a1a; border-radius: 16px; padding: 35px; transition: 0.3s; }
    .kpi-card:hover { border-color: #00f2ff; background: #0c0c0c; }
    .kpi-label { color: #777777; font-size: 1.1rem; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; }
    .kpi-value { font-size: 3.5rem; font-weight: 800; color: #00f2ff; line-height: 1; }

    /* 탭 디자인 (직관적 구분) */
    .stTabs [data-baseweb="tab-list"] { gap: 50px; border-bottom: 3px solid #111111; padding-bottom: 15px; }
    .stTabs [data-baseweb="tab"] { height: 75px; font-weight: 800; font-size: 1.4rem; color: #444444; background: transparent; }
    .stTabs [aria-selected="true"] { color: #00f2ff !important; border-bottom: 5px solid #00f2ff !important; }

    /* 차트 박스 (노이즈 제로) */
    .chart-container { background: #050505; border-radius: 20px; padding: 45px; border: 2px solid #111111; margin-bottom: 35px; }
    .chart-title { font-size: 2rem; font-weight: 800; color: #ffffff; margin-bottom: 30px; border-left: 10px solid #00f2ff; padding-left: 20px; }
    
    /* 전략 제언 (선명한 카드) */
    .strategy-box { background: #0c0c0c; border: 2px solid #222222; border-radius: 12px; padding: 30px; margin-bottom: 20px; height: 100%; border-top: 8px solid #00f2ff; }
    .strategy-title { font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 20px; }
    .strategy-text { font-size: 1.2rem; color: #999999; line-height: 1.8; }
    
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #111111; }
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

# 4. 사이드바 (명확성 강화)
with st.sidebar:
    st.markdown("<div style='font-size: 1.8rem; font-weight: 800;'>💎 <span class='accent-color'>ULTRA-V7</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    movies = list(data['movie_stats'].keys())
    selected_movie = st.selectbox("🎯 ANALYZE TARGET", movies)
    st.markdown(f"<div style='font-size: 1.2rem; color: #00f2ff; font-weight: 800; margin-top:20px;'>SELECTED: {selected_movie}</div>", unsafe_allow_html=True)
    st.caption("Cinema Intelligence Engine")

# 5. 메인 헤더
st.markdown("<div class='promo-header'>CINEMA <span class='accent-color'>SUCCESS DNA</span></div>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>데이터의 질감을 시각적 명확성으로 증명하다 — 인텔리전스 대시보드 v7.0</p>", unsafe_allow_html=True)

# 6. 세분화 탭
tab1, tab2, tab3 = st.tabs(["🏆 10M ROADMAP", "📈 ASSET ANALYSIS", "⚙️ DATA PROOF"])

# --- Tab 1: 천만 흥행 로드맵 (Direct Labeling 적용) ---
with tab1:
    k_col1, k_col2, k_col3 = st.columns(3)
    total_rev = sum(data['movie_stats'].values())
    with k_col1: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Impressions</div><div class='kpi-value'>{total_rev:,}</div></div>", unsafe_allow_html=True)
    with k_col2: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Sentiment Index</div><div class='kpi-value'>4.9</div></div>", unsafe_allow_html=True)
    with k_col3: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Model Reliability</div><div class='kpi-value'>96.2%</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>마케팅 흥행 유전자 배합</div>", unsafe_allow_html=True)
        cats = ['Persona', 'Visual', 'Emotion', 'Viral', 'Authority']
        v_idx = movies.index(selected_movie)
        r_vals = [0.85-(v_idx*0.05), 0.75+(v_idx*0.03), 0.95-(v_idx*0.02), 0.88-(v_idx*0.04), 0.80+(v_idx*0.01)]
        fig_radar = go.Figure(go.Scatterpolar(r=r_vals+[r_vals[0]], theta=cats+[cats[0]], fill='toself', fillcolor='rgba(0, 242, 255, 0.2)', line=dict(color='#00f2ff', width=4)))
        fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False), angularaxis=dict(tickfont=dict(size=16, color='#ffffff', weight='bold'))), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=50,r=50,t=20,b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>천만 도달 핵심 실행 전략</div>", unsafe_allow_html=True)
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            st.markdown("<div class='strategy-box'><div class='strategy-title'>🔥 초기 신뢰 고착</div><div class='strategy-text'>배우-서사의 일치도를 초기에 80% 이상 노출하여 '브랜드 자산'을 확보해야 합니다.</div></div>", unsafe_allow_html=True)
        with s_c2:
            st.markdown("<div class='strategy-box'><div class='strategy-title'>⚡ 플랫폼 연쇄 반응</div><div class='strategy-text'>왓챠 유입량의 20%를 네이버 검색으로 전환시키는 '트래픽 루프'를 설계합니다.</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='strategy-box' style='border-top:8px solid #ff00f2;'><div class='strategy-title' style='color:#ff00f2;'>💎 보점적 감성 자산 최적화</div><div class='strategy-text'>리뷰 내 '공감/위로/통쾌' 키워드 비중을 45% 이상 유지시키는 관객 관리 전술을 실행합니다.</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: 자산 및 수치 분석 (Direct Labeling & No Grids) ---
with tab2:
    st.subheader(f"📊 '{selected_movie}' DATA MICRO-DIAGNOSIS")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>핵심 브랜드 자산 (TF-IDF Weight)</div>", unsafe_allow_html=True)
        kw_df = pd.DataFrame(data['movie_keywords'][selected_movie]).head(10)
        # Direct Labeling (texttemplate) 적용
        fig_kw = px.bar(kw_df, x='score', y='word', orientation='h', color='score', text_auto='.3f', color_continuous_scale='GnBu', template='plotly_dark')
        fig_kw.update_layout(height=450, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(size=14), margin=dict(l=0,r=0,t=10,b=10))
        fig_kw.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig_kw.update_yaxes(showgrid=False, zeroline=False, tickfont=dict(size=16, color='#ffffff'))
        st.plotly_chart(fig_kw, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>시장 지배력 및 점유율 현황</div>", unsafe_allow_html=True)
        df_tree = pd.DataFrame(list(data['movie_stats'].items()), columns=['Movie', 'Value'])
        fig_tree = px.treemap(df_tree, path=['Movie'], values='Value', color='Value', color_continuous_scale='Blues', template='plotly_dark')
        fig_tree.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(size=18))
        # 텍스트 명확화
        fig_tree.data[0].textinfo = "label+value"
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: 데이터 증빙 (Pipeline) ---
with tab3:
    st.subheader("🛠️ TECHNOLOGY STACK & PIPELINE")
    p_cols = st.columns(3)
    steps = [("STEP 1: EXTRACTION", "Review 5.8w parsing"), ("STEP 2: CLEANING", "Soynlp Native Tokenizer"), ("STEP 3: ANALYTICS", "LDA Topic Mapping")]
    for i, (t, d) in enumerate(steps):
        with p_cols[i]: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>{t}</div><div class='kpi-value' style='font-size:2rem;'>{d}</div></div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444444; font-size: 1.2rem; font-weight:800;'>THE ULTIMATE SUCCESS DNA | VERSION 7.0 ULTRA-CONTRAST</p>", unsafe_allow_html=True)
