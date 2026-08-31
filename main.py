import streamlit as st

# 페이지 기본 설정 (와이드 레이아웃 및 타이틀)
st.set_page_config(
    page_title="✨ MBTI 진로 탐험 대작전! 🚀",
    page_icon="🌈",
    layout="wide"
)

# 커스텀 CSS (화려한 스타일링 및 카드 디자인)
st.markdown("""
<style>
    /* 전체 배경에 은은한 그라데이션 추가 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 20px;
    }
    
    /* 서브 타이틀 스타일 */
    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 30px;
    }
    
    /* 추천 직업 카드 스타일 */
    .job-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .job-card:hover {
        transform: translateY(-5px);
    }
    
    /* 카드 이미지 스타일 */
    .job-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    
    /* 직업 제목 스타일 */
    .job-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    
    /* 직업 설명 스타일 */
    .job-desc {
        font-size: 0.95rem;
        color: #666666;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h1 class='main-title'>✨ 🔮 MBTI 맞춤 진로 탐험관 🔮 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>🎉 나의 성격 유형에 딱 맞는 꿈의 직업과 멋진 풍경을 확인해보세요! 🚀🎨📊</p>", unsafe_allow_html=True)

# MBTI 데이터 베이스 (키워드 기반 이미지 URL 포함)
mbti_data = {
    "INTJ 🧠": {
        "tag": "용의주도한 전략가 ♟️",
        "desc": "독립적이고 분석적이며, 복잡한 문제를 해결하는 데 뛰어난 능력을 발휘해요! 💡",
        "jobs": [
            {
                "title": "🤖 AI 연구원 / 데이터 과학자",
                "desc": "복잡한 데이터를 분석하고 미래를 예측하는 AI 모델을 만들어요.",
                "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🏗️ 시스템 아키텍트",
                "desc": "거대한 IT 시스템의 구조를 설계하고 효율적으로 구축해요.",
                "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "📈 투자 전략가 / 펀드매니저",
                "desc": "시장 동향을 파악하고 정밀한 전략을 세워 자산을 운용해요.",
                "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "INTP 🧪": {
        "tag": "아이디어 파신기 논리술사 🔬",
        "desc": "호기심이 많고 지적 호기심이 풍부하며, 독창적인 해결책을 만드는 것을 좋아해요! ⚡",
        "jobs": [
            {
                "title": "💻 백엔드 / 소프트웨어 개발자",
                "desc": "논리적인 코드로 프로그램의 핵심 로직을 설계하고 구현해요.",
                "image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🔬 과학 연구원",
                "desc": "새로운 가설을 세우고 실험을 통해 세상을 바꿀 원리를 탐구해요.",
                "image": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🕵️‍♂️ 사이버 보안 전문가",
                "desc": "해킹 수법을 분석하고 안전한 보안 시스템을 구축해요.",
                "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ENTJ 👑": {
        "tag": "대담한 통솔자 🎯",
        "desc": "비전이 뛰어나고 리더십이 강하며, 목표를 향해 조직을 이끄는 데 능숙해요! 🔥",
        "jobs": [
            {
                "title": "💼 경영 컨설턴트",
                "desc": "기업의 문제점을 진단하고 성장하기 위한 최선의 전략을 제시해요.",
                "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🚀 스타트업 창업가 (CEO)",
                "desc": "새로운 시장을 개척하고 팀을 이끌어 아이디어를 현실로 만들어요.",
                "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "⚖️ 기업 전문 변호사",
                "desc": "논리적인 변론과 법률 지식으로 중요한 계약과 분쟁을 해결해요.",
                "image": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ENTP 💡": {
        "tag": "뜨거운 논쟁을 즐기는 변론가 🗣️",
        "desc": "창의적이고 끊임없이 새로운 아이디어를 떠올리며 도전하는 것을 즐겨요! 🎈",
        "jobs": [
            {
                "title": "📢 서비스 기획자 (PM)",
                "desc": "새로운 아이템을 발굴하고 혁신적인 서비스를 만들어내요.",
                "image": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🎬 크리에이티브 디렉터",
                "desc": "독창적인 컨셉으로 광고나 브랜드의 마케팅 전략을 총괄해요.",
                "image": "https://images.unsplash.com/photo-1542744094-3a31b272c490?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🎙️ 방송 프로듀서 (PD)",
                "desc": "사람들의 시선을 사로잡는 재미있고 유익한 콘텐츠를 제작해요.",
                "image": "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "INFJ 🔮": {
        "tag": "선의의 옹호자 🕊️",
        "desc": "통찰력이 깊고 이상주의적이며, 사람들에게 영감을 주고 돕는 일에 보람을 느껴요! 🌟",
        "jobs": [
            {
                "title": "🧘 심리상담사 / 치료사",
                "desc": "사람들의 마음속 아픔을 깊이 공감하고 치유되도록 도와요.",
                "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "✍️ 작가 / 에세이스트",
                "desc": "글을 통해 깊이 있는 메시지를 전달하고 사람들에게 감동을 줘요.",
                "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🏫 교육 공학자",
                "desc": "더 효과적이고 가치 있는 교육 프로그램과 환경을 디자인해요.",
                "image": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "INFP 🎨": {
        "tag": "열정적인 중재자 🌸",
        "desc": "감수성이 풍부하고 가치관을 중시하며, 자신만의 독창적인 예술 세계를 넓혀가요! 🌈",
        "jobs": [
            {
                "title": "🎨 일러스트레이터 / 작가",
                "desc": "풍부한 상상력을 바탕으로 캐릭터와 이야기를 그려내요.",
                "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🎵 음악 프로듀서 / 작곡가",
                "desc": "감성적인 멜로디로 사람들의 마음을 울리는 음악을 만들어요.",
                "image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🌿 환경 운동가 / NGO 활동가",
                "desc": "더 나은 세상과 자연을 위해 가치 있는 캠페인을 기획해요.",
                "image": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ENFJ ☀️": {
        "tag": "정의로운 사회운동가 🤝",
        "desc": "카리스마와 공감 능력을 갖추고 있어 타인의 성장을 돕고 용기를 주는 데 탁월해요! 💖",
        "jobs": [
            {
                "title": "👩‍🏫 교사 / 교육 전문가",
                "desc": "학생들의 가능성을 끌어내고 올바른 길로 이끌어줘요.",
                "image": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🤝 HR (인사) 담당자",
                "desc": "인재를 발굴하고 구성원들이 즐겁게 일할 수 있는 환경을 만들어요.",
                "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🌐 국제기구 활동가",
                "desc": "글로벌 사회 문제를 해결하고 평화를 위해 일해요.",
                "image": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ENFP 🎈": {
        "tag": "재발랄한 활동가 🤩",
        "desc": "에너지가 넘치고 열정적이며, 사람들과 소통하며 새로운 경험을 하는 것을 좋아해요! 🎉",
        "jobs": [
            {
                "title": "📱 페스티벌 기획자",
                "desc": "모두가 즐겁게 즐길 수 있는 신나는 축제와 행사를 만들어요.",
                "image": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "✈️ 여행 크리에이터",
                "desc": "전 세계를 누비며 멋진 풍경과 다채로운 경험을 사람들과 공유해요.",
                "image": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🛍️ 마케팅 홍보 전문가",
                "desc": "톡톡 튀는 아이디어로 제품의 매력을 널리 알려요.",
                "image": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ISTJ 📐": {
        "tag": "청렴결백한 논리주의자 📋",
        "desc": "책임감이 강하고 신중하며, 규칙과 질서를 지키며 정확하게 처리하는 것을 잘해요! 🏛️",
        "jobs": [
            {
                "title": "📊 회계사 / 세무사",
                "desc": "재무 정보를 정확하게 기록하고 관리하여 신뢰성을 높여요.",
                "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🏛️ 행정 관리자",
                "desc": "사회 규정과 제도를 정확하게 준수하며 효율성을 높여요.",
                "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🛡️ 품질 관리 전문가 (QA)",
                "desc": "제품이나 서비스의 오차를 검수하여 완벽한 품질을 유지해요.",
                "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ISFJ 🛡️": {
        "tag": "용감한 수호자 💐",
        "desc": "헌신적이고 세심하며, 주변 사람들을 꼼꼼하게 챙기고 도우며 안정감을 줘요! 💝",
        "jobs": [
            {
                "title": "🩺 간호사 / 의료 전문가",
                "desc": "환자를 정성껏 돌보고 따뜻한 마음으로 건강 회복을 도와요.",
                "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🧸 유치원 / 보육교사",
                "desc": "아이들의 성장과 안전을 따뜻한 사랑으로 지켜줘요.",
                "image": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "📚 사서 / 기록 관리사",
                "desc": "지식과 정보를 깔끔하게 정리하고 가치 있는 자료를 보존해요.",
                "image": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ESTJ 🏛️": {
        "tag": "엄격한 관리자 👔",
        "desc": "체계적이고 리더십이 있으며, 규칙을 세우고 효율적으로 조직을 운영하는 데 능해요! ⏱️",
        "jobs": [
            {
                "title": "📊 프로젝트 매니저 (PM)",
                "desc": "일정과 자원을 완벽하게 관리하여 프로젝트를 성공으로 이끌어요.",
                "image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🏢 금융 지점장 / 지배인",
                "desc": "조직의 목표 달성을 위해 구성원들을 효율적으로 관리해요.",
                "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "👮 경찰관 / 소방관",
                "desc": "사회의 질서와 안전을 확립하기 위해 투철한 책임감을 발휘해요.",
                "image": "https://images.unsplash.com/photo-1582139329536-e7284fece509?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ESFJ 🌺": {
        "tag": "사교적인 외교관 🥳",
        "desc": "친절하고 분위기를 밝게 만들며, 다른 사람들과 협력하고 조화를 이루는 것을 즐겨요! 🤝",
        "jobs": [
            {
                "title": "✈️ 항공기 승무원",
                "desc": "고객에게 최고의 서비스와 편안함을 제공하며 안전을 책임져요.",
                "image": "https://images.unsplash.com/photo-1540339832862-47459980783b?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🤝 고객 경험 (CX) 매니저",
                "desc": "소비자의 의견을 경청하고 불편 사항을 친절하게 해결해요.",
                "image": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🏨 호텔 지배인",
                "desc": "따뜻한 환대로 방문객들에게 특별한 경험을 선물해요.",
                "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ISTP 🛠️": {
        "tag": "만능 재주꾼 🔧",
        "desc": "객관적이고 실용적이며, 도구를 활용해 문제를 직접 해결하는 것을 좋아해요! 🏎️",
        "jobs": [
            {
                "title": "🏎️ 자동차 정비 / 레이서",
                "desc": "기계의 메커니즘을 이해하고 정밀하게 조율하거나 제어해요.",
                "image": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🚁 항공기 조종사 (파일럿)",
                "desc": "침착한 상황 판단으로 비행기를 안전하게 운항해요.",
                "image": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🎧 음향 엔지니어",
                "desc": "각종 장비를 자유자재로 다루어 최고의 소리를 만들어내요.",
                "image": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ISFP 🎨": {
        "tag": "호기심 많은 예술가 🌿",
        "desc": "겸손하고 예술적 감각이 뛰어나며, 현재의 순간을 즐기고 감성을 표현해요! 📸",
        "jobs": [
            {
                "title": "📸 사진작가 (포토그래퍼)",
                "desc": "아름다운 순간과 감정을 카메라 앵글 속에 담아내요.",
                "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "👗 패션 디자이너",
                "desc": "트렌드와 감성을 조합해 세련된 의상과 스타일을 완성해요.",
                "image": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🌿 플로리스트 / 원예가",
                "desc": "꽃과 식물을 다루며 자연의 아름다움을 디자인해요.",
                "image": "https://images.unsplash.com/photo-1563241527-3004b7be0ffd?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ESTP ⚡": {
        "tag": "수완 좋은 활동가 🏄",
        "desc": "스릴을 즐기고 순발력이 뛰어난 모험가 스타일! 행동력이 최고예요! 💥",
        "jobs": [
            {
                "title": "🏄 스포츠 선수 / 트레이너",
                "desc": "뛰어난 신체 감각과 순발력으로 목표에 도전해요.",
                "image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "📈 주식 트레이더",
                "desc": "빠르게 변화하는 시장 흐름을 즉각적으로 판단하여 투자해요.",
                "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🚑 응급구조사",
                "desc": "긴박한 상황에서도 위기 대응 능력을 발휘해 인명을 구해요.",
                "image": "https://images.unsplash.com/photo-1587745416684-47953f16f02f?auto=format&fit=crop&w=600&q=80"
            }
        ]
    },
    "ESFP 🌟": {
        "tag": "자유로운 영혼의 연예인 🎉",
        "desc": "주변을 항상 즐겁게 만들고, 주목받는 것을 좋아하며 에너지와 유쾌함이 넘쳐요! 🎭",
        "jobs": [
            {
                "title": "🎭 배우 / 뮤지컬 배우",
                "desc": "무대 위에서 다양한 캐릭터를 연기하며 사람들에게 감동을 줘요.",
                "image": "https://images.unsplash.com/photo-1469488865564-c2de10f69f96?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "📢 쇼호스트 / 인플루언서",
                "desc": "매력적인 말솜씨로 상품의 매력을 살리고 사람들과 소통해요.",
                "image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80"
            },
            {
                "title": "🕺 댄서 / 안무가",
                "desc": "리듬감과 표현력을 살려 화려한 퍼포먼스를 만들어내요.",
                "image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=600&q=80"
            }
        ]
    }
}

# 사이드바에서 MBTI 선택
st.sidebar.header("🎯 MBTI 선택하기")
selected_mbti = st.sidebar.selectbox(
    "당신의 MBTI 유형을 골라보세요! 👇",
    list(mbti_data.keys())
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: 진로 선택은 참고용일 뿐, 여러분의 가능성은 무궁무진하답니다! 🌈")

# 메인 콘텐츠 영역
info = mbti_data[selected_mbti]

# MBTI 헤더 카드
st.markdown(f"## {selected_mbti} - {info['tag']}")
st.success(f"✨ **특징**: {info['desc']}")

st.markdown("---")
st.markdown("### 🌟 추천 직업 BEST 3")

# 직업 카드를 3개 컬럼으로 나눠서 출력
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, job in enumerate(info["jobs"]):
    with cols[i]:
        st.markdown(f"""
        <div class="job-card">
            <img src="{job['image']}" class="job-img" alt="{job['title']}">
            <div class="job-title">{job['title']}</div>
            <div class="job-desc">{job['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# 하단 효과 및 응원 메시지
st.markdown("---")
st.balloons()  # 축하 풍선 효과!
st.markdown("<h3 style='text-align: center; color: #ff6b6b;'>🔥 당신의 멋진 미래를 응원합니다! 🔥</h3>", unsafe_allow_html=True)
