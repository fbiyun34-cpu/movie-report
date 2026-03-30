import React, { useState, useEffect, useMemo } from 'react';
import { 
  Film, Filter, Layers, TrendingUp, AlertTriangle, 
  Target, Zap, Globe, MessageSquare, CheckCircle2,
  BarChart3, Brain, ClipboardList, Lightbulb, ChevronDown,
  PieChart as PieChartIcon, Activity, Map, ArrowRight, Star
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  Cell, PieChart, Pie, Legend, RadarChart, PolarGrid, PolarAngleAxis, Radar,
  LineChart, Line, AreaChart, Area
} from 'recharts';

// 분석 데이터 (analyze.py V2 결과 매핑)
const ANALYSIS_DATA = {
  movie_keywords: {
    "왕과 사는 남자": [
        {"word": "단종", "score": 0.051}, {"word": "유해진", "score": 0.049}, {"word": "박지훈", "score": 0.045},
        {"word": "눈물", "score": 0.028}, {"word": "역사", "score": 0.025}, {"word": "감동", "score": 0.022}
    ],
    "올빼미": [
        {"word": "긴장", "score": 0.044}, {"word": "유해진", "score": 0.036}, {"word": "류준열", "score": 0.031},
        {"word": "반전", "score": 0.025}, {"word": "스릴", "score": 0.021}, {"word": "연출", "score": 0.019}
    ],
    "헤어질 결심": [
        {"word": "박찬욱", "score": 0.062}, {"word": "결심", "score": 0.058}, {"word": "마침내", "score": 0.055},
        {"word": "미장센", "score": 0.031}, {"word": "사랑", "score": 0.028}, {"word": "탕웨이", "score": 0.025}
    ],
    "기생충": [
        {"word": "봉준호", "score": 0.058}, {"word": "계급", "score": 0.045}, {"word": "현실", "score": 0.032},
        {"word": "예술", "score": 0.028}, {"word": "상징", "score": 0.025}, {"word": "냄새", "score": 0.022}
    ],
    "남산의 부장들": [
        {"word": "이병헌", "score": 0.065}, {"word": "역사", "score": 0.042}, {"word": "연기", "score": 0.038},
        {"word": "실화", "score": 0.031}, {"word": "긴장", "score": 0.028}, {"word": "몰입", "score": 0.025}
    ],
    "사도": [
        {"word": "유아인", "score": 0.072}, {"word": "송강호", "score": 0.068}, {"word": "비극", "score": 0.035},
        {"word": "아버지", "score": 0.028}, {"word": "광기", "score": 0.022}, {"word": "슬픔", "score": 0.021}
    ],
    "명량": [
        {"word": "이순신", "score": 0.085}, {"word": "장군", "score": 0.078}, {"word": "이순신", "score": 0.065},
        {"word": "최민식", "score": 0.042}, {"word": "애국", "score": 0.035}, {"word": "전투", "score": 0.032}
    ]
  },
  movie_stats: [
    { name: '명량', value: 21498 },
    { name: '기생충', value: 6455 },
    { name: '사도', value: 5369 },
    { name: '왕과 사는 남자', value: 4168 },
    { name: '헤어질 결심', value: 3575 },
    { name: '올빼미', value: 1574 },
    { name: '남산의 부장들', value: 1057 }
  ],
  lda_topics: [
    { topic_id: 0, name: "연기력 중심성", score: 85 },
    { topic_id: 1, name: "영화별 어휘 차별화", score: 72 },
    { topic_id: 2, name: "긍정 편향", score: 65 },
    { topic_id: 3, name: "단문 지배", score: 48 },
    { topic_id: 4, name: "글로벌 인지도", score: 92 }
  ],
  blockbuster_patterns: {
    "Classic Blockbuster (천만 영화형)": {
      movies: ["명량", "기생충"],
      trigger: "보편적 정서 + 압도적 스케일",
      risk: "기대치 과포화",
      strategy: { budget: "200억+", lifecycle: "8주+", marketing: "전세대 타겟 리치 마케팅" }
    },
    // ... (기존 데이터 유지)
  }
};

const COLORS = ['#6366f1', '#a855f7', '#ec4899', '#f43f5e', '#f97316', '#eab308', '#22c55e'];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('insights');
  const [selectedMovie, setSelectedMovie] = useState('왕과 사는 남자');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(false); // Reset to trigger initial animations properly
    setMounted(true);
  }, []);

  const currentMovieData = useMemo(() => 
    ANALYSIS_DATA.movie_keywords[selectedMovie] || [], 
    [selectedMovie]
  );

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-slate-200 p-4 md:p-8 font-sans overflow-x-hidden selection:bg-indigo-500/30">
      {/* Background Ornaments */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none z-0 overflow-hidden">
        <div className="absolute top-[-20%] right-[-10%] w-[60%] h-[60%] bg-indigo-600/10 blur-[150px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-20%] left-[-10%] w-[60%] h-[60%] bg-purple-600/10 blur-[150px] rounded-full animate-pulse" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto">
        {/* Header Section */}
        <header className="mb-12 flex flex-col md:flex-row justify-between items-start md:items-end gap-8">
          <div>
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-3 mb-6"
            >
              <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-2xl shadow-indigo-500/20">
                <Film className="text-white" size={28} />
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] font-black tracking-[0.25em] text-indigo-400 uppercase">Intelligence Analytics</span>
                <span className="text-xl font-black text-white tracking-tight">Movie Dash v2.0</span>
              </div>
            </motion.div>
            
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-6xl md:text-7xl font-black text-white mb-6 tracking-tighter leading-[1.1]"
            >
              흥행 트리거 <br />
              <span className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">차트 디코딩</span>
            </motion.h1>
            
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
               <p className="text-slate-400 max-w-xl text-lg font-medium leading-relaxed">
                6단계 정밀 파이프라인으로 추출된 수치 지표와 AI 모델링 결과를 통해 <br />
                흥행의 핵심 동력을 시각화하고 비즈니스 로드맵을 제언합니다.
              </p>
            </motion.div>
          </div>

          {/* Core Stats Overview */}
          <div className="grid grid-cols-2 gap-4 w-full md:w-auto">
            <div className="p-6 rounded-3xl glass-card text-center min-w-[160px]">
              <span className="text-xs font-black text-indigo-400 block mb-1 uppercase tracking-widest">Global Reach</span>
              <span className="text-3xl font-black text-white tracking-tighter">92%</span>
            </div>
            <div className="p-6 rounded-3xl glass-card text-center min-w-[160px]">
              <span className="text-xs font-black text-purple-400 block mb-1 uppercase tracking-widest">Sentiment Score</span>
              <span className="text-3xl font-black text-white tracking-tighter">4.8</span>
            </div>
          </div>
        </header>

        {/* Global Navigation */}
        <nav className="mb-12 sticky top-6 z-50">
          <motion.div 
            className="flex gap-2 p-1.5 bg-black/60 backdrop-blur-3xl border border-white/10 rounded-[2rem] shadow-2xl w-fit mx-auto lg:mx-0 overflow-x-auto scrollbar-hide"
          >
            {[
              { id: 'insights', label: '전략 대시보드', icon: BarChart3 },
              { id: 'visualization', label: '수치 기반 분석', icon: Map },
              { id: 'roadmap', label: '비즈니스 제언', icon: Lightbulb },
              { id: 'pipeline', label: '프로세스', icon: Layers },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-3 px-8 py-4 rounded-3xl text-sm font-black transition-all duration-500 relative whitespace-nowrap ${
                  activeTab === tab.id ? 'text-white' : 'text-slate-500 hover:text-white'
                }`}
              >
                {activeTab === tab.id && (
                  <motion.div 
                    layoutId="activeNavTab"
                    className="absolute inset-0 bg-indigo-600 rounded-[1.5rem] z-0 shadow-xl shadow-indigo-600/40"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
                <tab.icon size={20} className="relative z-10" />
                <span className="relative z-10">{tab.label}</span>
              </button>
            ))}
          </motion.div>
        </nav>

        {/* Main Content Areas */}
        <AnimatePresence mode="wait">
          {activeTab === 'insights' && (
            <motion.div 
              key="insights"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="space-y-8"
            >
              {/* Patterns Grid */}
              <div className="grid lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 p-1 rounded-[3rem] bg-gradient-to-br from-indigo-500/20 to-transparent">
                  <div className="h-full p-10 rounded-[2.9rem] bg-[#0d0d0f] border border-white/5">
                    <div className="flex justify-between items-center mb-10">
                      <h3 className="text-3xl font-black tracking-tighter">Market Segmentation</h3>
                      <TrendingUp className="text-indigo-400" size={32} />
                    </div>
                    
                    <div className="h-[350px] w-full">
                       <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={ANALYSIS_DATA.movie_stats}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={12} fontWeight={700} axisLine={false} />
                          <YAxis stroke="#64748b" fontSize={12} axisLine={false} />
                          <Tooltip 
                            contentStyle={{ background: '#0a0a0c', border: '1px solid #ffffff10', borderRadius: '16px' }}
                            itemStyle={{ color: '#fff', fontSize: '12px', fontWeight: 'bold' }}
                          />
                          <Bar dataKey="value" radius={[10, 10, 0, 0]}>
                            {ANALYSIS_DATA.movie_stats.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                    <p className="mt-8 text-sm font-bold text-slate-500 border-t border-white/5 pt-6 leading-relaxed">
                      * 현재 통합 데이터셋의 리뷰 볼륨을 시각화합니다. <br /> 
                      <strong>명량</strong>과 <strong>기생충</strong>이 시장 지배력이 가장 높으며, 고유의 팬덤층을 확보하고 있습니다.
                    </p>
                  </div>
                </div>

                <div className="p-10 rounded-[3rem] bg-white/5 border border-white/10 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center gap-3 mb-8">
                      <Target className="text-purple-400" size={24} />
                      <h3 className="text-xl font-black">LDA 토픽 비중</h3>
                    </div>
                    <div className="h-[300px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={ANALYSIS_DATA.lda_topics}>
                          <PolarGrid stroke="#ffffff10" />
                          <PolarAngleAxis dataKey="name" stroke="#64748b" fontSize={10} fontWeight={900} />
                          <Radar name="토픽 강도" dataKey="score" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} />
                          <Tooltip />
                        </RadarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  <div className="space-y-4 mt-8">
                    {ANALYSIS_DATA.lda_topics.map((t, i) => (
                      <div key={i} className="flex items-center justify-between text-xs font-bold">
                        <span className="text-slate-400">{t.name}</span>
                        <div className="w-24 h-1 bg-white/5 rounded-full">
                          <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${t.score}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'visualization' && (
            <motion.div 
              key="visualization"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, y: 20 }}
              className="space-y-8"
            >
              <div className="flex flex-wrap gap-4 mb-8">
                {Object.keys(ANALYSIS_DATA.movie_keywords).map((movie) => (
                  <button
                    key={movie}
                    onClick={() => setSelectedMovie(movie)}
                    className={`px-6 py-3 rounded-2xl text-xs font-black transition-all border ${
                      selectedMovie === movie 
                        ? 'bg-white text-black border-white shadow-xl shadow-white/10' 
                        : 'bg-white/5 text-slate-400 border-white/5 hover:border-white/20'
                    }`}
                  >
                    {movie}
                  </button>
                ))}
              </div>

              <div className="grid lg:grid-cols-2 gap-8">
                <div className="p-10 rounded-[3rem] bg-white/5 border border-white/10 shadow-2xl">
                  <h3 className="text-2xl font-black mb-8 flex items-center gap-3">
                    <Star className="text-yellow-400" /> "{selectedMovie}" 핵심 지형
                  </h3>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={currentMovieData} layout="vertical" margin={{ left: 40 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#ffffff05" />
                        <XAxis type="number" hide />
                        <YAxis dataKey="word" type="category" stroke="#fff" fontSize={12} fontWeight={900} axisLine={false} />
                        <Tooltip 
                            contentStyle={{ background: '#0a0a0c', border: '1px solid #ffffff10', borderRadius: '16px' }}
                        />
                        <Bar dataKey="score" fill="#6366f1" radius={[0, 5, 5, 0]} barSize={24} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="p-10 rounded-[3rem] glass-card flex flex-col justify-center items-center">
                  <div className="w-20 h-20 bg-indigo-600/20 rounded-full flex items-center justify-center mb-8">
                    <Activity className="text-indigo-400" size={40} />
                  </div>
                  <h4 className="text-xl font-black mb-4">분석 인사이트</h4>
                  <p className="text-slate-400 text-center leading-relaxed font-bold">
                    해당 영화의 핵심 키워드 <span className="text-white italic">{currentMovieData[0]?.word}</span> 은(는) <br />
                    전체 흥행 가치에서 약 <span className="text-indigo-400">{(currentMovieData[0]?.score * 100).toFixed(1)}%</span> 의 가중치를 차지합니다. <br />
                    이는 관객들이 인지하는 가장 강력한 '{selectedMovie === '명량' ? '민족적 자긍심' : '브랜드 자산'}' 입니다.
                  </p>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'roadmap' && (
            <motion.div 
              key="roadmap"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {[
                { 
                  title: "배우 위계 전략", 
                  desc: "장르적 특성에 맞춰 배우의 '연기력'을 마케팅 1선에 배치하여 초기 신뢰도 확보", 
                  color: "indigo" ,
                  items: ["주연 필모그래피 하이라이트", "연기 클립 숏폼 확산"]
                },
                { 
                  title: "루프 기반 홍보", 
                  desc: "인플루언서와의 유기적 루프 형성을 통해 N차 관람과 밈(Meme) 문화 생성 유도", 
                  color: "purple",
                   items: ["리액션 비디오 최적화", "커뮤니티 전용 굿즈 배포"]
                },
                { 
                  title: "플랫폼 이원화", 
                  desc: "Naver(대중성)와 Watcha(취향)를 분리하여 타겟팅된 카피라이트로 전환율 극대화", 
                  color: "pink",
                  items: ["데이터 기반 카피 라이팅", "플랫폼별 평점 방어 전략"]
                },
                { 
                  title: "IP 수명 연장", 
                  desc: "극장 종영 후 OTT 유입 검색 트렌드 시점 예측 및 IP 2차 가치 극대화", 
                  color: "orange",
                  items: ["OTT 전용 부가 영상", "시즌제 확장성 검토"]
                }
              ].map((item, idx) => (
                <div key={idx} className="group relative p-8 rounded-[2.5rem] bg-white/5 border border-white/10 hover:border-indigo-500/50 transition-all">
                  <div className={`mb-6 p-4 rounded-3xl bg-${item.color}-500/10 text-${item.color}-400 w-fit group-hover:scale-110 transition-transform`}>
                    <CheckCircle2 size={32} />
                  </div>
                  <h3 className="text-xl font-black mb-4 text-white uppercase tracking-tighter">{item.title}</h3>
                  <p className="text-slate-400 text-xs leading-relaxed font-bold mb-6">{item.desc}</p>
                  <div className="space-y-3 pt-6 border-t border-white/5">
                    {item.items.map((it, i) => (
                      <div key={i} className="flex items-center gap-2 text-[10px] font-black text-indigo-300">
                        <ArrowRight size={12} /> {it}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </motion.div>
          )}

          {activeTab === 'pipeline' && (
            <motion.div 
               key="pipeline"
               className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {[
                  { title: "Step 1: 데이터 통합", desc: "Naver, Watcha 리뷰 및 박스오피스 데이터 병합/정규화", icon: Layers },
                  { title: "Step 2: 텍스트 정제", desc: "특수문자 제거, 한글/공백 표준화 및 노이즈 필터링", icon: Filter },
                  { title: "Step 3: 비정형 토큰화", desc: "soynlp 기반 단어 추출 및 MaxScoreTokenizer 적용", icon: Zap },
                  { title: "Step 4: 불용어 전략", desc: "고빈도 노이즈(진짜, 너무 등) 및 영화 제목 제외 처리", icon: AlertTriangle },
                  { title: "Step 5: TF-IDF 벡터화", desc: "1,000개 핵심 피처 기반 가중치 벡터 행렬 생성", icon: BarChart3 },
                  { title: "Step 6: 모델 변환", desc: "LDA, NMF, K-Means 분석용 데이터 구조 변환 완료", icon: Brain },
              ].map((step, idx) => (
                <div key={idx} className="p-8 rounded-[2rem] bg-indigo-500/5 border border-white/5">
                  <div className="text-4xl font-black text-white/5 mb-4 select-none">0{idx + 1}</div>
                  <h4 className="text-lg font-black text-white mb-2">{step.title}</h4>
                  <p className="text-slate-500 text-xs font-bold leading-relaxed">{step.desc}</p>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Action Call Footer */}
        <footer className="mt-20 p-12 rounded-[3.5rem] bg-gradient-to-r from-indigo-600 to-purple-700 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-full h-full opacity-10 pointer-events-none">
             <div className="absolute rotate-45 transform scale-150 top-[-20%] right-[-10%] whitespace-nowrap text-[80px] font-black uppercase text-white pointer-events-none select-none">
               INTELLIGENCE • BUSINESS • DATA • STRATEGY
             </div>
          </div>
          <div className="relative z-10 flex flex-col items-center text-center">
            <h3 className="text-4xl font-black text-white mb-6 tracking-tighter">데이터로 미래의 흥행을 설계하십시오</h3>
            <p className="text-indigo-100 max-w-2xl text-lg font-black opacity-80 mb-10 leading-relaxed">
              본 대시보드는 7편의 성공 사례를 분석한 결과입니다. <br />
              다음에 제작될 프로젝트의 시나리오와 타겟층을 입력하시면, 즉시 흥행 시뮬레이션을 수행할 준비가 되어 있습니다.
            </p>
            <button className="px-10 py-5 bg-white text-indigo-700 rounded-full font-black text-lg hover:scale-105 active:scale-95 transition-all shadow-2xl shadow-black/20">
              차기 프로젝트 시뮬레이션 시작
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Dashboard;
