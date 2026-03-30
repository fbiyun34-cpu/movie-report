import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정 (시안 이미지 동기화 모드)
st.set_page_config(page_title="Success Trigger Decoding v12.0", page_icon="🧬", layout="wide")

# 2. 이미지 매칭 디자인 시스템 (Success Trigger Retrofit)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&family=Inter:wght@400;700;900&display=swap');
    
    /* 이미지 전용 베이스 컬러 (#0d0d12) */
    .main { background-color: #0d0d12 !important; color: #ffffff; font-family: 'Inter', 'Nanum+Gothic', sans-serif; font-size: 1.1rem; }
    
    /* 이미지 그라데이션 타이틀 */
    .img-title { font-size: 4.2rem; font-weight: 900; background: linear-gradient(to right, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -4px; margin-bottom: 0.1rem; line-height: 1.0; }
    .img-sub { color: #94a3b8; font-size: 1.2rem; margin-bottom: 3rem; font-weight: 500; letter-spacing: -0.5px; opacity: 0.8; }

    /* 이미지 카드 스타일 (#16161d, 32px radius) */
    .img-card { background: #16161d; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 32px; padding: 40px; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); }
    
    /* 캡슐형 KPI 카드 */
    .kpi-pill { background: #1a1a24; border-radius: 20px; padding: 25px; text-align: center; border: 1px solid rgba(168, 85, 247, 0.1); }
    .kpi-pill-label { color: #6366f1; font-size: 0.8rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px; }
    .kpi-pill-value { font-size: 2.2rem; font-weight: 900; color: #ffffff; }

    /* 이미지 탭 버튼 (Pill Style) */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 20px; border-bottom: none; background: rgba(255,255,255,0.03); 
        padding: 8px; border-radius: 50px; display: inline-flex; margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] { 
        height: 48px; border-radius: 40px; font-weight: 700; font-size: 1rem; color: #64748b; 
        background: transparent; border: none; padding: 0 30px;
    }
    .stTabs [aria-selected="true"] { 
        color: #ffffff !important; background: #6366f1 !important; 
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    /* 이미지 차트 타이틀 */
    .chart-header { font-size: 1.8rem; font-weight: 900; color: #ffffff; margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between; }
    
    [data-testid="stSidebar"] { background-color: #0d0d12 !important; border-right: 1px solid rgba(255,255,255,0.05); }
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

# 4. 이미지 맞춤 컬러 시퀀스 (Purple -> Green)
IMG_COLORS = ['#6366f1', '#a855f7', '#ec4899', '#f43f5e', '#f97316', '#eab308', '#22c55e']

# 5. 헤더 (이미지 동기화)
h_col1, h_col2 = st.columns([1.5, 1])
with h_col1:
    st.markdown("<div class='img-title'>흥행 트리거<br>차트 디코딩</div>", unsafe_allow_html=True)
    st.markdown("<p class='img-sub'>6단계 정밀 파이프라인으로 추출된 수치 지표와 AI 모델링 결과를 통해 흥행의 핵심 동력을 시각화하고 비즈니스 로드맵을 제언합니다.</p>", unsafe_allow_html=True)
with h_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    k_sub1, k_sub2 = st.columns(2)
    with k_sub1: st.markdown("<div class='kpi-pill'><div class='kpi-pill-label'>GLOBAL REACH</div><div class='kpi-pill-value'>92%</div></div>", unsafe_allow_html=True)
    with k_sub2: st.markdown("<div class='kpi-pill'><div class='kpi-pill-label'>SENTIMENT SCORE</div><div class='kpi-pill-value'>4.8</div></div>", unsafe_allow_html=True)

# 6. 이미지 탭 UI
tab1, tab2, tab3, tab4 = st.tabs(["📊 전략 대시보드", "📖 수치 기반 분석", "💡 비즈니스 제언", "📦 프로세스"])

with tab1:
    col_l, col_r = st.columns([1.5, 1])
    
    with col_l:
        st.markdown("<div class='img-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-header'>Market Segmentation <span style='color:#6366f1;'>📈</span></div>", unsafe_allow_html=True)
        
        # 이미지의 정확한 컬러 시퀀스 적용
        df_stats = pd.DataFrame(list(data['movie_stats'].items()), columns=['Movie', 'Volume']).sort_values('Volume', ascending=False)
        fig_bar = px.bar(df_stats, x='Movie', y='Volume', color='Movie', 
                         color_discrete_sequence=IMG_COLORS, template='plotly_dark')
        fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              height=500, margin=dict(l=0,r=0,t=0,b=0))
        fig_bar.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(size=14, color='#94a3b8'))
        fig_bar.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-top:20px;'>* 현재 통합 데이터셋의 리뷰 볼륨을 시각화합니다. 명량과 기생충이 시장 지배력이 가장 높으며, 고유의 팬덤층을 확보하고 있습니다.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='img-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-header'><span style='color:#a855f7;'>◎</span> LDA 토픽 비중</div>", unsafe_allow_html=True)
        
        # 이미지의 퍼플 레이더 차트 재현
        cats = ['연기력 중심성', '영화별 어휘 차별화', '긍정 편향', '단문 지배', '글로벌 인지도']
        pts = [0.92, 0.78, 0.45, 0.82, 0.75]
        fig_radar = go.Figure(go.Scatterpolar(r=pts+[pts[0]], theta=cats+[cats[0]], fill='toself', 
                                              fillcolor='rgba(168, 85, 247, 0.4)', line=dict(color='#a855f7', width=3)))
        fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False), 
                                angularaxis=dict(tickfont=dict(size=12, color='#94a3b8'))), 
                                paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=40,r=40,t=20,b=20), height=350)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # 하단 프로그레스 바 (이미지 스타일)
        st.markdown("<br>", unsafe_allow_html=True)
        for cat, val in zip(cats, pts):
            col_t, col_b = st.columns([1.5, 1])
            with col_t: st.markdown(f"<div style='font-size:0.9rem; color:#94a3b8; margin-bottom:5px;'>{cat}</div>", unsafe_allow_html=True)
            with col_b: st.markdown(f"<div style='height:8px; background:rgba(255,255,255,0.05); border-radius:10px;'><div style='width:{val*100}%; height:100%; background:#6366f1; border-radius:10px;'></div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 7. 사이드바 (최소화)
with st.sidebar:
    st.markdown("<div style='font-size:1.5rem; font-weight:900; color:#6366f1;'>DNA ANALYSIS</div>", unsafe_allow_html=True)
    st.markdown("---")
    selected_movie = st.selectbox("🎯 TARGET SELECT", list(data['movie_stats'].keys()))
    st.markdown(f"<div style='font-size:1.2rem; color:#ffffff; font-weight:800; margin-top:20px;'>{selected_movie}</div>", unsafe_allow_html=True)

# 푸터
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.9rem; margin-top:50px;'>SUCCESS TRIGGER DECODING v12.0 | IMAGE RETROFIT EDITION</p>", unsafe_allow_html=True)
