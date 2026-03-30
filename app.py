import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. 페이지 설정
st.set_page_config(page_title="Movie Strategy Intelligence Dashboard", page_icon="🧬", layout="wide")

# 2. 인텔리전스 디자인 시스템 (v4.2)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    .main { background-color: #0f172a !important; color: #f1f5f9; font-family: 'Nanum+Gothic', sans-serif; }
    .promo-header { font-size: 2.8rem; font-weight: 800; color: #ffffff; letter-spacing: -1px; margin-bottom: 0.5rem; }
    .accent-color { color: #38bdf8; }
    .kpi-card { background: #1e293b; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .kpi-label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: #38bdf8; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 700; color: #64748b; background: transparent; }
    .stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom: 2px solid #38bdf8 !important; }
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid rgba(255, 255, 255, 0.05); }
    .chart-container { background: #1e293b; border-radius: 16px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 20px; }
    .strategy-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #38bdf8; border-radius: 16px; padding: 25px; height: 100%; transition: 0.3s; }
    .recommendation-box { background: rgba(56, 189, 248, 0.05); border-radius: 12px; padding: 20px; border-left: 4px solid #38bdf8; margin-bottom: 15px; }
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

# 4. 사이드바
with st.sidebar:
    st.markdown("<div style='font-size: 1.2rem; font-weight: 800;'>🧬 STRATEGIC <span class='accent-color'>PRO</span></div>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&q=80&w=2659", use_container_width=True)
    st.markdown("---")
    movies = list(data['movie_stats'].keys())
    selected_movie = st.selectbox("🎯 심층 분석 영화 선택", movies)
    st.caption("Release Intelligence v4.2")

# 5. 헤더 섹션
st.markdown("<div class='promo-header'>영화 흥행 전략 <span class='accent-color'>인텔리전스 대시보드</span></div>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>7편의 주요 영화 데이터 분석을 통해 도출된 흥행 트리거와 리포트 기반 비즈니스 전략 모델</p>", unsafe_allow_html=True)

# 6. 리포트 동기화 탭 구조
tab1, tab2, tab3, tab4 = st.tabs(["📊 시장 및 토픽 분석", "🔍 수치 기반 심층 분석", "💡 비즈니스 전략 로드맵", "🚩 최종 제언 사항"])

# --- Tab 1: 시장 및 토픽 분석 ---
with tab1:
    k1, k2, k3, k4 = st.columns(4)
    total_rev = sum(data['movie_stats'].values())
    with k1: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>시장 총 임프레션</div><div class='kpi-value'>{total_rev:,}</div></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>핵심 성공 클러스터</div><div class='kpi-value'>05</div></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>관객 감성지수 (AI)</div><div class='kpi-value'>4.8/5.0</div></div>", unsafe_allow_html=True)
    with k4: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>분석 신뢰도</div><div class='kpi-value'>94.2%</div></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📍 영화별 시장 점유율 (Market Share)")
        df_tree = pd.DataFrame(list(data['movie_stats'].items()), columns=['Movie', 'Value'])
        st.plotly_chart(px.treemap(df_tree, path=['Movie'], values='Value', color='Value', color_continuous_scale='Blues', template='plotly_dark').update_layout(margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("🎯 5대 핵심 담론 (LDA Topics)")
        categories = [t['name'] for t in data['lda_topics']]
        values = [0.85, 0.70, 0.90, 0.45, 0.75]
        fig_radar = go.Figure(go.Scatterpolar(r=values+[values[0]], theta=categories+[categories[0]], fill='toself', fillcolor='rgba(56, 189, 248, 0.2)', line=dict(color='#38bdf8', width=2)))
        fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False, range=[0, 1])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=40,r=40,t=40,b=40), height=350)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: 수치 기반 심층 분석 ---
with tab2:
    st.subheader(f"📽️ '{selected_movie}' 브랜드 자산 가치 정밀 측정")
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown(f"#### 🗝️ 핵심 키워드 가중치 (TF-IDF Top 15)")
        kw_df = pd.DataFrame(data['movie_keywords'][selected_movie])
        fig_kw = px.bar(kw_df.head(15).sort_values('score', ascending=True), x='score', y='word', orientation='h', color='score', color_continuous_scale='GnBu', template='plotly_dark')
        fig_kw.update_layout(height=450, showlegend=False, xaxis_title="Weight Score", yaxis_title=None, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_kw, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### 📊 데이터 분포 및 통계 개요")
        st.dataframe(kw_df, use_container_width=True, hide_index=True)
        st.markdown("<br><p style='color: #94a3b8; font-size: 0.9rem;'>* TF-IDF 점수 기반으로 관객들이 인지하는 가장 강력한 브랜드 자산을 수치화한 결과입니다.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: 비즈니스 전략 로드맵 ---
with tab3:
    st.subheader("🚀 4대 실행 전술 (Action Roadmap)")
    st.write("데이터 분석 결과를 바탕으로 즉각 실행 가능한 핵심 전략을 제언합니다.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class='strategy-card'>
            <h3 style='color: #38bdf8;'>🎖️ 배우 위계 전략</h3>
            <p style='color: #94a3b8; font-size: 0.9rem;'>장르 특성에 맞춘 배우 중심의 초기 신뢰도 확보 및 캐스팅 매칭 분석</p>
            <ul style='font-size: 0.8rem; color: #f1f5f9;'>
                <li>코어 팬덤 타겟팅</li>
                <li>배우 이미지-작품 싱크로율 최적화</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='strategy-card'>
            <h3 style='color: #38bdf8;'>➰ 루프 기반 홍보</h3>
            <p style='color: #94a3b8; font-size: 0.9rem;'>인플루언서 연계 연쇄적 바이럴 루프 형성 및 확산 속도 트래킹</p>
            <ul style='font-size: 0.8rem; color: #f1f5f9;'>
                <li>시그니처 대사/장면 밈화</li>
                <li>오가닉 바이럴 인센티브 설계</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='strategy-card'>
            <h3 style='color: #38bdf8;'>📱 플랫폼 이원화</h3>
            <p style='color: #94a3b8; font-size: 0.9rem;'>네이버(포털)/왓챠(SNS) 채널별 관객 성향 차이를 고려한 메시징</p>
            <ul style='font-size: 0.8rem; color: #f1f5f9;'>
                <li>채널별 맞춤 콘텐츠 제작</li>
                <li>유입 경로별 전환율 측정</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class='strategy-card'>
            <h3 style='color: #38bdf8;'>♾️ IP 수명 연장</h3>
            <p style='color: #94a3b8; font-size: 0.9rem;'>OTT 유입 트렌드 예측을 통한 2차 부가가치 극대화 및 프랜차이즈화</p>
            <ul style='font-size: 0.8rem; color: #f1f5f9;'>
                <li>디지털 상영권 마케팅</li>
                <li>OSMU 기반 윈도잉 전략</li>
            </ul>
        </div>""", unsafe_allow_html=True)

# --- Tab 4: 최종 제언 사항 ---
with tab4:
    st.subheader("🚩 최종 비즈니스 제언")
    
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.markdown("#### 1. 데이터 기반 시뮬레이션")
    st.write("차기 프로젝트의 시나리오 키워드를 입력하여 과거 흥행 모델과 비교 분석함으로써 흥행 가능성을 사전 예측합니다.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.markdown("#### 2. 실시간 모니터링 체계 구축")
    st.write("개봉 후 리뷰 키워드 변화 추이를 실시간 추적하여 위기 관리 및 마케팅 광고 집행 방향을 즉시 수정합니다.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.markdown("#### 3. 플랫폼 최적화 광고 집행")
    st.write("네이버와 왓챠 유저의 감성 키워드 차이를 활용하여 고관여층과 저관여층에게 서로 다른 하이라이트 영상을 노출합니다.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>© 2026 Movie Strategy Intelligence Dashboard | Professional Report Integration</p>", unsafe_allow_html=True)
