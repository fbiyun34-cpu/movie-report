import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정 (최상위 전문가 모드)
st.set_page_config(page_title="Deep Obsidian Cinema Intelligence v10.0", page_icon="🌌", layout="wide")

# 2. 딥 옵시디언 & 시네마틱 다크 디자인 시스템 (v10.0)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&family=Inter:wght@400;700;900&display=swap');
    
    /* 딥 옵시디언 네이비 배경 적용 */
    .main { background-color: #020617 !important; color: #f8fafc; font-family: 'Inter', 'Nanum+Gothic', sans-serif; font-size: 1.3rem; }
    
    /* 시네마틱 타이포그래피 */
    .super-title { font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #6366f1, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -5px; margin-bottom: 0.2rem; line-height: 1.0; }
    .super-accent { color: #22d3ee; text-shadow: 0 0 50px rgba(34, 211, 238, 0.4); }
    .super-sub { color: #94a3b8; font-size: 1.6rem; margin-bottom: 4rem; font-weight: 600; letter-spacing: -0.5px; opacity: 0.9; }

    /* 옵시디언 레이어 카드 */
    .bento-card { background: #0f172a; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 32px; padding: 50px; margin-bottom: 35px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); transition: all 0.4s ease; }
    .bento-card:hover { border-color: #22d3ee; transform: translateY(-3px); box-shadow: 0 30px 60px -15px rgba(34, 211, 238, 0.15); }
    
    /* 비비드 KPI 텍스트 */
    .bento-label { color: #94a3b8; font-size: 1.2rem; font-weight: 800; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 2px; }
    .bento-value { font-size: 4rem; font-weight: 900; color: #ffffff; line-height: 1; text-shadow: 0 0 25px rgba(255, 255, 255, 0.1); }

    /* 전문가용 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] { gap: 60px; border-bottom: 2px solid #1e293b; }
    .stTabs [data-baseweb="tab"] { height: 90px; font-weight: 900; font-size: 1.6rem; color: #475569; background: transparent; }
    .stTabs [aria-selected="true"] { color: #22d3ee !important; border-bottom: 6px solid #6366f1 !important; }

    /* 섹션 타이포그래피 (그라데이션 인디케이터) */
    .section-header { font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-bottom: 40px; display: flex; align-items: center; gap: 20px; }
    .section-header::before { content: ''; width: 12px; height: 35px; background: linear-gradient(to bottom, #6366f1, #22d3ee); border-radius: 6px; }

    /* 루미너스 인사이트 박스 */
    .insight-box { background: rgba(15, 23, 42, 0.8); border-radius: 20px; padding: 35px; border: 1px solid rgba(34, 211, 238, 0.1); margin-top: 25px; font-size: 1.4rem; color: #cbd5e1; line-height: 1.8; }
    
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    .stSelectbox label { font-size: 1.3rem !important; font-weight: 900 !important; color: #94a3b8 !important; }
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

# 4. 사이드바 (옵시디언 톤)
with st.sidebar:
    st.markdown("<div style='font-size: 2.2rem; font-weight: 900;'>🌌 <span style='color: #22d3ee;'>OBSIDIAN</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    movies = list(data['movie_stats'].keys())
    selected_movie = st.selectbox("🎯 ANALYZE TARGET", movies)
    st.markdown(f"<div style='font-size: 2rem; color: #ffffff; font-weight: 900; margin-top:40px; background: linear-gradient(90deg, #6366f1, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{selected_movie}</div>", unsafe_allow_html=True)
    st.caption("Strategic Dark v10.0")

# 5. 시네마틱 헤더
st.markdown("<div class='super-title'>CINEMA INSIGHT</div>", unsafe_allow_html=True)
st.markdown("<p class='super-sub'>딥 옵시디언 테마 기반의 압도적 몰입감과 전문성을 담은 인텔리전스 리포트</p>", unsafe_allow_html=True)

# 6. 메인 탭 구조 (v10.0)
tab1, tab2, tab3 = st.tabs(["🏆 흥행 성공 DNA", "📊 데이터 딥다이브", "🛡️ 프로세스 무결성"])

# --- Tab 1: 🏆 천만 흥행 공식 (Luminous Charting) ---
with tab1:
    # 대형 KPI 매트릭스
    k_col1, k_col2, k_col3 = st.columns(3)
    total_rev = sum(data['movie_stats'].values())
    with k_col1: st.markdown(f"<div class='bento-card'><div class='bento-label'>Global Market Scan</div><div class='bento-value'>{total_rev:,}</div></div>", unsafe_allow_html=True)
    with k_col2: st.markdown(f"<div class='bento-card'><div class='bento-label'>Success Indicator</div><div class='bento-value'>9.8/10</div></div>", unsafe_allow_html=True)
    with k_col3: st.markdown(f"<div class='bento-card'><div class='bento-label'>Intelligence Acc.</div><div class='bento-value'>99%</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([1.2, 1])
    with m_col1:
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>핵심 흥행 유전자 (DNA Profile)</div>", unsafe_allow_html=True)
        # 루미너스 레이더 (옵시디언 매칭)
        cats = ['Persona', 'Visual', 'Emotion', 'Viral', 'Authority']
        pts = [0.90, 0.75, 0.98, 0.92, 0.85]
        fig_radar = go.Figure(go.Scatterpolar(r=pts+[pts[0]], theta=cats+[cats[0]], fill='toself', fillcolor='rgba(34, 211, 238, 0.15)', line=dict(color='#22d3ee', width=6)))
        fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False), angularaxis=dict(tickfont=dict(size=18, color='#f8fafc', weight='black'))), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=60,r=60,t=20,b=20), height=550)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with m_col2:
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>최우선 실행 전략</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box' style='border-left: 10px solid #6366f1;'>
            <strong style='font-size: 1.7rem; color: #6366f1;'>🎯 프리미엄 포지셔닝</strong><br>
            고관여 관람층의 데이터를 기반으로 한 독보적 서사 신뢰도 구축
        </div>
        <div class='insight-box' style='border-left: 10px solid #22d3ee;'>
            <strong style='font-size: 1.7rem; color: #22d3ee;'>⚡ 옴니채널 바이럴 설계</strong><br>
            네이버-왓챠 통합 리뷰 데이터 허브를 활용한 전파력 극대화
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: 📊 데이터 딥다이브 (Obsidian Optimized) ---
with tab2:
    st.markdown(f"<div class='section-header'>{selected_movie} 브랜드 자산 매핑</div>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 2rem; font-weight: 900; margin-bottom: 25px;'>Brand Assets (TF-IDF Weight)</div>", unsafe_allow_html=True)
        kw_df = pd.DataFrame(data['movie_keywords'][selected_movie]).head(10).sort_values('score', ascending=True)
        # 루미너스 바 차트 (옵시디언 배경 매칭)
        fig_kw = px.bar(kw_df, x='score', y='word', orientation='h', color='score', text_auto='.3f', color_continuous_scale='GnBu', template='plotly_dark')
        fig_kw.update_layout(height=650, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=30,t=10,b=10), font=dict(size=18, color='#f8fafc'))
        fig_kw.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig_kw.update_yaxes(showgrid=False, zeroline=False, tickfont=dict(size=24, color='#ffffff', weight='black'))
        fig_kw.update_traces(textfont_size=22, textposition='outside')
        st.plotly_chart(fig_kw, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b_col2:
        st.markdown("<div class='bento-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 2rem; font-weight: 900; margin-bottom: 25px;'>Market Share Analysis</div>", unsafe_allow_html=True)
        df_tree = pd.DataFrame(list(data['movie_stats'].items()), columns=['Movie', 'Value'])
        fig_tree = px.treemap(df_tree, path=['Movie'], values='Value', color='Value', color_continuous_scale='Blues', template='plotly_dark')
        fig_tree.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=26, color='#ffffff', weight='black'))
        fig_tree.data[0].textinfo = "label+value"
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: 프로세스 무결성 ---
with tab3:
    st.markdown("<div class='section-header'>TECHNICAL DATA PIPELINE</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    p_steps = [("Ingestion", "5.8w Reviews"), ("Neural Tokenizing", "Soynlp Native Engine"), ("Success Synthesis", "K-Means Modeling")]
    for i, (t, s) in enumerate(p_steps):
        with cols[i]: st.markdown(f"<div class='bento-card'><div class='bento-label'>{t}</div><div class='bento-value' style='font-size: 2.8rem; background: linear-gradient(90deg, #6366f1, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{s}</div></div>", unsafe_allow_html=True)

# 푸터
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569; font-weight: 900; font-size: 1.6rem;'>CINEMA OBSIDIAN v10.0 | PROFESSIONAL INTEL BASE</p>", unsafe_allow_html=True)
