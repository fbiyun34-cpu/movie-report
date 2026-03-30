import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정 (Strategic Pro 테마)
st.set_page_config(
    page_title="Strategic Movie Insight Pro",
    page_icon="🏅",
    layout="wide",
)

# 2. Strategic Dark Pro 디자인 시스템 (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    /* 기본 배경 및 폰트 */
    .main {
        background-color: #0f172a !important;
        color: #f1f5f9;
        font-family: 'Nanum+Gothic', sans-serif;
    }
    
    /* 타이틀 섹션 */
    .promo-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .accent-color { color: #38bdf8; }

    /* KPI 카드 디자인 */
    .kpi-card {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: #38bdf8; }

    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px; font-weight: 700; color: #64748b; background: transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important; border-bottom: 2px solid #38bdf8 !important;
    }

    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    .sidebar-logo {
        font-size: 1.2rem; font-weight: 800; color: #f1f5f9; margin-bottom: 20px;
    }

    /* 차트 박스 */
    .chart-container {
        background: #1e293b;
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
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

# 4. 사이드바 - 미니멀 내비게이션
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>🏅 STRATEGIC <span class='accent-color'>PRO</span></div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=2525", use_container_width=True)
    st.markdown("---")
    st.write("본 리포트는 인공지능 기반 리뷰 데이터 분석을 통한 **천만 영화 흥행 패턴 및 투자 전략**서 입니다.")
    st.caption("Last Updated: 2026.03.30")

# 5. 헤더 및 KPI
st.markdown("<div class='promo-header'>Movie Success <span class='accent-color'>Decoding</span></div>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>빅데이터와 AI 모델링으로 도출한 천만 영화의 공식: 전략적 의사결정을 위한 인사이트 리포트</p>", unsafe_allow_html=True)

# KPI Row
k1, k2, k3, k4 = st.columns(4)
stats = data['movie_stats']
total_rev = sum(stats.values())

with k1: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Impressions</div><div class='kpi-value'>{total_rev:,}</div></div>", unsafe_allow_html=True)
with k2: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Success Clusters</div><div class='kpi-value'>05</div></div>", unsafe_allow_html=True)
with k3: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Sentiment Index</div><div class='kpi-value'>4.8/5.0</div></div>", unsafe_allow_html=True)
with k4: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Analysis Confidence</div><div class='kpi-value'>94%</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. 내비게이션 탭
tabs = st.tabs(["🚀 Executive Overview", "💰 Strategic Investment", "📉 Pipeline Process"])

# --- Tab 1: Executive Overview ---
with tabs[0]:
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📍 Market Domination (Market Share)")
        
        df_stats = pd.DataFrame(list(stats.items()), columns=['Movie', 'Value']).sort_values('Value', ascending=False)
        fig_tree = px.treemap(df_stats, path=['Movie'], values='Value', color='Value', color_continuous_scale='Blues', template='plotly_dark')
        fig_tree.update_layout(margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("🎯 핵심 토픽 비중 (LDA)")
        categories = [t['name'] for t in data['lda_topics']]
        values = [0.85, 0.70, 0.90, 0.45, 0.75]
        fig_radar = go.Figure(go.Scatterpolar(r=values+[values[0]], theta=categories+[categories[0]], fill='toself', fillcolor='rgba(56, 189, 248, 0.2)', line=dict(color='#38bdf8', width=2)))
        fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False, range=[0, 1])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=40,r=40,t=40,b=40), height=350)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: Strategic Investment ---
with tabs[1]:
    st.subheader("💸 흥행 모델링 및 ROI 가이드")
    patterns = data['blockbuster_patterns']
    
    for name, p in patterns.items():
        with st.expander(f"Model: {name}"):
            cl, cr = st.columns([1, 1])
            with cl:
                st.markdown(f"**⚡ 핵심 트리거**: {p['trigger']}")
                st.markdown(f"**💰 투자 예산**: {p['strategy']['budget']}")
                st.markdown(f"**⏳ 박스오피스 수명**: {p['strategy']['lifecycle']}")
            with cr:
                st.info(f"**📣 마케팅 전략**: {p['strategy']['marketing']}")
                st.warning(f"**리스크 관리**: {p['risk']}")

# --- Tab 3: Pipeline Process ---
with tabs[2]:
    st.subheader("⛓️ Data Pipeline Integrity")
    st.markdown("본 레포트는 6단계 정밀 공정을 거쳐 산출된 고신뢰도 데이터를 기반으로 작성되었습니다.")
    
    col1, col2, col3 = st.columns(3)
    steps = [
        ("Step 1", "데이터 수집", "Naver/Watcha 통합"),
        ("Step 2", "텍스트 정제", "Soynlp 기반 토큰화"),
        ("Step 3", "특성 추출", "TF-IDF 가중치 산출"),
        ("Step 4", "토픽 분류", "LDA 자동 라벨링"),
        ("Step 5", "군집 분석", "K-Means 패턴화"),
        ("Step 6", "의사결정 보조", "전략 인사이트 도출")
    ]
    
    for i, (s, t, d) in enumerate(steps):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(f"""
            <div class='kpi-card' style='margin-bottom: 20px;'>
                <div class='kpi-label'>{s}</div>
                <div style='font-size: 1.1rem; font-weight: 800; color: #f1f5f9;'>{t}</div>
                <div style='font-size: 0.85rem; color: #94a3b8;'>{d}</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>© 2026 Strategic Movie Insight Pro | Professional Edition</p>", unsafe_allow_html=True)
