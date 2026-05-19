import streamlit as st

# --- [1] 페이지 기본 설정 ---
st.set_page_config(page_title="PhiloScales: 나의 철학자 찾기", page_icon="📜", layout="centered")

# --- [2] 세션 상태 초기화 (기존 로직 유지) ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'result' not in st.session_state:
    st.session_state.result = None

# --- [3] 데이터 정의 영역 (질문 35개 유지) ---
questions = [
    # [고대 서양 철학 & 덕윤리]
    {"text": "Q1. 인생의 최종 목표는 결국 '행복'이며, 이를 위해선 이성적으로 바르게 행동하는 습관이 중요하다.", "axis": "virtue", "direction": 1},
    {"text": "Q2. 진정한 지혜는 내가 모르는 것이 많다는 사실을 솔직하게 인정하는 것에서 시작된다.", "axis": "rational", "direction": 1},
    {"text": "Q3. 눈에 보이는 현실 세계는 불완전하며, 머릿속으로만 그릴 수 있는 완벽하고 영원한 '이상적인 세계'가 진짜로 존재한다.", "axis": "idealism", "direction": 1},
    {"text": "Q4. 나라는 권력이나 욕심이 아니라, 깊은 지혜와 올바른 지식을 가진 사람이 다스려야 잘 돌아간다.", "axis": "idealism", "direction": 1},
    
    # [동양 철학 - 유가 및 도가]
    {"text": "Q5. 사람들을 다스릴 때는 무서운 벌이나 강제력보다 따뜻한 도덕성과 예의로 모범을 보여야 한다.", "axis": "eastern_confucian", "direction": 1},
    {"text": "Q6. 인간은 본래 태어날 때부터 다른 사람의 불행이나 고통을 보면 마음 아파하는 선한 마음을 가지고 있다.", "axis": "eastern_confucian", "direction": 1},
    {"text": "Q7. 나라의 리더는 자기 권력보다 백성(국민)의 삶을 가장 소중하게 여겨야 한다.", "axis": "eastern_confucian", "direction": 1},
    {"text": "Q8. 인위적으로 만든 규칙이나 도덕은 오히려 사람을 옥죄므로 자연스러운 흐름에 삶을 맡기는 것이 가장 좋다.", "axis": "eastern_dao", "direction": 1},
    {"text": "Q9. 사회가 복잡하고 문명이 발달하는 것보다, 욕심 없이 순박하게 살아가는 작은 사회가 더 행복하다.", "axis": "eastern_dao", "direction": 1},
    
    # [근대 서양 철학 - 합리론 & 변증법]
    {"text": "Q10. 세상 모든 것을 의심하더라도, 지금 이 순간 '의심하고 생각하고 있는 나의 존재'만큼은 확실한 사실이다.", "axis": "rational", "direction": 1},
    {"text": "Q11. 국가나 사회는 원래 자유롭던 개인들이 자신들의 안전을 위해 서로 약속(계약)을 맺어 만든 것이다.", "axis": "existential", "direction": 1},
    {"text": "Q12. 인간은 원래 자유롭고 착하게 태어났지만, 문명과 사유재산이 생기면서 불평등과 구속이 시작되었다.", "axis": "existential", "direction": 1},
    {"text": "Q13. 국가는 단순히 이익을 위해 뭉친 계약 단체를 넘어, 구성원들이 함께 올바른 도덕을 실현하는 가장 큰 공동체이다.", "axis": "idealism", "direction": 1},
    {"text": "Q14. 세상과 역사는 반대되는 생각이나 갈등이 서로 부딪치고 합쳐지면서 더 나은 방향으로 발전해 나간다.", "axis": "idealism", "direction": 1},

    # [의무론, 공리주의, 정의론]
    {"text": "Q15. 올바른 행동이란 나에게 이익이 오거나 결과가 좋아서가 아니라, 인간으로서 마땅히 해야 할 '의무'이기 때문에 하는 것이다.", "axis": "deontology", "direction": 2},
    {"text": "Q16. 내가 하려는 행동이 언제, 어디서, 누구나 똑같이 해도 괜찮은 행동인지를 따져보는 것이 도덕의 핵심이다.", "axis": "deontology", "direction": 2},
    {"text": "Q17. 사람뿐만 아니라 고통과 기쁨을 느낄 수 있는 동물까지도 도덕적으로 존중하고 보호해야 한다.", "axis": "deontology", "direction": -2},
    {"text": "Q18. 고통을 느끼는 능력이 있다면 동물이든 사람이든 그 가치를 차별 없이 동등하게 아끼고 고려해야 한다.", "axis": "deontology", "direction": -2},
    {"text": "Q19. 공정한 사회 규칙을 정할 때는 내가 부자가 될지 가난한 사람이 될지 모르는 평등한 상태에서 토론해야 한다.", "axis": "idealism", "direction": 1},
    {"text": "Q20. 사회적 불평등은 그로 인해 우리 사회에서 '가장 처지가 어렵고 힘든 사람'에게 가장 큰 도움(이익)이 돌아갈 때만 인정될 수 있다.", "axis": "idealism", "direction": 1},

    # [실존주의 및 근현대 철학]
    {"text": "Q21. 정해진 절대적인 도덕이나 정답은 없으며, 인간은 아무도 없는 세상에서 스스로 삶의 의미를 만들어가야 하는 외로운 존재다.", "axis": "existential", "direction": 2},
    {"text": "Q22. 삶이 허무하고 고통스러울지라도 이를 당당히 이겨내고 나 자신의 주인이 되어 당당하게 살아가야 한다.", "axis": "existential", "direction": 2},
    {"text": "Q23. 인간은 세상에 원해서 태어난 게 아니지만, 언젠가 맞이할 죽음을 두려워하지 않고 직시할 때 진짜 내 삶을 살 수 있다.", "axis": "existential", "direction": 2},
    {"text": "Q24. 사람은 태어날 때부터 정해진 정답이나 운명이 없으며, 오직 살아가면서 내리는 선택들로 자기 자신을 완성해간다.", "axis": "existential", "direction": 2},

    # [심화 및 변별 문항]
    {"text": "Q25. 진정한 사랑과 배려는 내 이기적인 욕심을 누르고 상대방을 존중하는 규칙과 예의를 지키는 것에서 나온다.", "axis": "eastern_confucian", "direction": 1},
    {"text": "Q26. 어떤 것이 옳고 좋은지 아는 지식과, 그것을 실제로 행동으로 옮기는 것은 결국 하나로 연결되어 있다.", "axis": "virtue", "direction": 1},
    {"text": "Q27. 나는 먹고 살 만한데 지구 반대편의 굶주리는 사람들을 돕지 않는 것은 도덕적으로 잘못된 일이며, 기부는 선택이 아닌 의무다.", "axis": "deontology", "direction": -1},
    {"text": "Q28. 가장 정의로운 사회는 다른 사람에게 피해를 주지 않는 선에서 모든 사람에게 똑같이 최대한의 자유를 보장하는 사회다.", "axis": "idealism", "direction": 1},
    {"text": "Q29. 우리의 눈과 귀로 느끼는 경험은 착각하기 쉬우므로, 변하지 않는 진리는 오직 이성적인 생각과 논리로만 찾아낼 수 있다.", "axis": "rational", "direction": 1},
    {"text": "Q30. 우주와 세상은 거대한 자연의 법칙에 따라 흘러가므로, 인간이 억지로 뜯어고치려 하지 않을 때 가장 평화롭다.", "axis": "eastern_dao", "direction": 1},
    {"text": "Q31. 사람을 대할 때는 내 목적을 이루기 위한 수단이나 도구로 이용하지 말고, 그 사람 자체를 소중한 목적으로 존중해야 한다.", "axis": "deontology", "direction": 1},
    {"text": "Q32. 올바른 성품과 인격은 머리로 이해하는 것보다 일상생활 속에서 착한 행동을 꾸준히 반복하는 '습관'을 통해 완성된다.", "axis": "virtue", "direction": 1},
    {"text": "Q33. 인간은 나 홀로 완벽하게 존재하는 게 아니라 주변 사람 및 환경과 끊임없이 관계를 맺으며 함께 살아가는 존재다.", "axis": "existential", "direction": 1},
    {"text": "Q34. 정부나 국가는 국민의 재산과 안전을 지켜달라고 권력을 맡긴 것이므로, 국가가 국민을 억압하면 거부하거나 저항할 권리가 있다.", "axis": "existential", "direction": 1},
    {"text": "Q35. 세상에 절대적인 선과 악은 존재하지 않으며 무엇이 옳고 그른지는 시대나 사회적 분위기에 따라 언제든 바뀔 수 있다.", "axis": "existential", "direction": 1}
]

# --- [4] 철학자 매칭 데이터 및 상세 정보 (14인 전체 반영) ---
# 매칭용 사상 점수 (좌표)
philosophers_data = {
    "아리스토텔레스": {"virtue": 4, "rational": 2, "idealism": 1, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 1, "existential": 0},
    "소크라테스": {"virtue": 3, "rational": 4, "idealism": 2, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 1, "existential": 0},
    "플라톤": {"virtue": 2, "rational": 4, "idealism": 5, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 1, "existential": 0},
    "공자": {"virtue": 3, "rational": 1, "idealism": 2, "eastern_confucian": 5, "eastern_dao": -2, "deontology": 2, "existential": 0},
    "맹자": {"virtue": 3, "rational": 1, "idealism": 2, "eastern_confucian": 5, "eastern_dao": -2, "deontology": 2, "existential": 0},
    "노자": {"virtue": -2, "rational": -1, "idealism": -2, "eastern_confucian": -4, "eastern_dao": 5, "deontology": -2, "existential": 1},
    "피터 싱어": {"virtue": 0, "rational": 2, "idealism": 1, "eastern_confucian": 0, "eastern_dao": 0, "deontology": -4, "existential": 0},
    "롤스": {"virtue": 1, "rational": 2, "idealism": 4, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 2, "existential": 1},
    "칸트": {"virtue": 1, "rational": 4, "idealism": 3, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 5, "existential": 0},
    "데카르트": {"virtue": 0, "rational": 5, "idealism": 2, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 1, "existential": 0},
    "헤겔": {"virtue": 2, "rational": 3, "idealism": 4, "eastern_confucian": 0, "eastern_dao": 0, "deontology": 2, "existential": 1},
    "니체": {"virtue": -1, "rational": -2, "idealism": -3, "eastern_confucian": -2, "eastern_dao": 2, "deontology": -2, "existential": 5},
    "하이데거": {"virtue": 1, "rational": 1, "idealism": 0, "eastern_confucian": 0, "eastern_dao": 2, "deontology": 0, "existential": 4},
    "루소": {"virtue": 2, "rational": 1, "idealism": 1, "eastern_confucian": 0, "eastern_dao": 1, "deontology": 1, "existential": 3}
}

# 보고서용 상세 설명 데이터 (사진 경로를 '철학자사진/이름.png'로 완벽 매칭)
philosophers_info = {
    "아리스토텔레스": {
        "basis": "당신은 구체적인 실천과 습관을 통해 형성되는 도덕적 성품을 중시합니다.",
        "thought": "인간의 궁극적 목적은 행복이며, 이는 이성의 활동인 '중용'의 덕을 실천함으로써 달성됩니다.",
        "books": ["니코마코스 윤리학", "정치학"],
        "reading": "중용은 산술적인 중간이 아닙니다. 그것은 상황에 따라 마땅한 때에, 마땅한 일에 대해, 마땅한 동기로 행하는 탁월함입니다.",
        "image": "철학자사진/아리스토텔레스.png"
    },
    "소크라테스": {
        "basis": "당신은 지식과 도덕이 하나이며, 끊임없는 성찰이 삶의 핵심이라 믿습니다.",
        "thought": "지덕복 합일설. 무지에 대한 자각이 지혜의 시작이며, 선을 아는 자는 악을 행할 수 없습니다.",
        "books": ["소크라테스의 변명", "향연"],
        "reading": "음미되지 않는 삶은 살 가치가 없습니다. 산법술을 통해 스스로 모순을 깨닫고 진리를 찾아가는 과정이 실존의 핵심입니다.",
        "image": "철학자사진/소크라테스.png"
    },
    "플라톤": {
        "basis": "당신은 현실 너머의 완벽한 이상과 이성적 통찰을 가장 높은 가치로 둡니다.",
        "thought": "이데아론. 현실은 그림자일 뿐이며, 이성으로 파악 가능한 영원불변한 이데아의 세계가 진실입니다.",
        "books": ["국가(Republic)", "메논"],
        "reading": "동굴의 비유를 기억하십시오. 우리는 감각의 그림자에서 벗어나 이성의 빛인 '선의 이데아'를 향해 나아가야 합니다.",
        "image": "철학자사진/플라톤.png"
    },
    "공자": {
        "basis": "당신은 사람 간의 사랑(仁)과 사회적 예의(禮)의 조화를 중시하는 도덕적 인간입니다.",
        "thought": "수기안인. 자신을 닦아 남을 편안케 함. 인(仁)을 근본으로 예(禮)를 통해 대동 사회를 지향합니다.",
        "books": ["논어", "효경"],
        "reading": "군자는 조화를 이루되 부화뇌동하지 않습니다. 극기복례, 즉 이기적 욕망을 극복하여 예로 돌아가는 삶이 인의 시작입니다.",
        "image": "철학자사진/공자.png"
    },
    "맹자": {
        "basis": "당신은 인간 본성의 선함을 굳게 믿으며 정의로운 사회를 열망합니다.",
        "thought": "성선설 및 민본주의. 인간에겐 측은지심 등 사단이 있으며, 왕은 백성을 위해 정치해야 합니다.",
        "books": ["맹자"],
        "reading": "백성이 가장 귀하고 사직이 다음이며 군주가 가장 가볍습니다. 본성을 잃지 않는 호연지기를 기르십시오.",
        "image": "철학자사진/맹자.png"
    },
    "노자": {
        "basis": "당신은 인위적인 규범을 거부하고 자연의 순리를 따르는 자유로운 영혼입니다.",
        "thought": "무위자연. 억지로 하지 않고 스스로 그러한 자연의 법칙인 '도(道)'에 순응하는 삶을 지향합니다.",
        "books": ["도덕경"],
        "reading": "최고의 선은 물과 같습니다(상선약수). 물은 만물을 이롭게 하면서도 다투지 않으며 낮은 곳으로 흐릅니다.",
        "image": "철학자사진/노자.png"
    },
    "피터 싱어": {
        "basis": "당신은 모든 생명체의 고통에 공감하며 실천적인 이타주의를 지향합니다.",
        "thought": "이익평등고려의 원칙. 고통을 느끼는 모든 존재(쾌고감수능력)를 도덕적으로 동등하게 고려해야 합니다.",
        "books": ["동물 해방", "실천 윤리학"],
        "reading": "종차별주의는 인종차별과 같습니다. 우리는 절대적 빈곤의 인류와 고통받는 동물을 도덕적 의무로써 도와야 합니다.",
        "image": "철학자사진/피터싱어.png"
    },
    "롤스": {
        "basis": "당신은 절차의 공정성과 사회적 약자에 대한 배려를 정의의 척도로 삼습니다.",
        "thought": "공정으로서의 정의. 무지의 베일 속에서 최소 수혜자에게 최대 혜택을 주는 차등의 원칙을 강조합니다.",
        "books": ["정의론", "정치적 자유주의"],
        "reading": "정의의 제1원칙은 평등한 자유입니다. 제2원칙은 불평등이 가장 불리한 자에게 이익이 될 때만 정당화된다는 것입니다.",
        "image": "철학자사진/롤스.png"
    },
    "칸트": {
        "basis": "당신은 결과보다 동기를, 이익보다 무조건적인 도덕적 의무를 중시합니다.",
        "thought": "의무론 및 정언명령. 네 의지의 준칙이 언제나 보편적 입법의 원리가 되도록 행위하십시오.",
        "books": ["실천이성비판", "윤리형이상학 정초"],
        "reading": "인간을 결코 수단으로 대하지 말고 언제나 목적으로 대우하십시오. 도덕 법칙은 내 마음속의 장엄한 명령입니다.",
        "image": "철학자사진/칸트.png"
    },
    "데카르트": {
        "basis": "당신은 명석판명한 이성적 논리와 확실한 지식의 토대를 중시합니다.",
        "thought": "방법적 회의 및 합리론. '나는 생각한다, 그러므로 존재한다.' 이성은 진리에 이르는 유일한 빛입니다.",
        "books": ["방법서설", "성찰"],
        "reading": "모든 것을 의심해 보십시오. 그 의심 끝에 도달하는 생각하는 주체로서의 '나'만이 가장 확실한 진리의 출발점입니다.",
        "image": "철학자사진/데카르트.png"
    },
    "헤겔": {
        "basis": "당신은 역사의 진보와 도덕적 공동체 안에서의 개인의 실현을 중시합니다.",
        "thought": "변증법적 지양. 역사는 절대정신이 스스로를 실현하는 과정이며, 국가는 인륜의 최고 형태입니다.",
        "books": ["정신현상학", "법철학"],
        "reading": "미네르바의 부엉이는 황혼이 저물 때야 비로소 날개를 편다. 역사는 투쟁과 통합을 통해 이성을 완성해 나갑니다.",
        "image": "철학자사진/헤겔.png"
    },
    "니체": {
        "basis": "당신은 기존의 틀을 깨고 스스로 삶의 가치를 창조하는 강인한 의지를 가졌습니다.",
        "thought": "허무주의 극복 및 초인(위버멘쉬). 자신의 삶을 사랑하고(아모르 파티) 끊임없이 스스로를 극복하십시오.",
        "books": ["짜라투스트라는 이렇게 말했다", "도덕의 계보"],
        "reading": "신은 죽었습니다. 이제 당신이 당신 자신의 입법자가 되어야 합니다. 아이와 같이 순수하게 삶을 긍정하십시오.",
        "image": "철학자사진/니체.png"
    },
    "하이데거": {
        "basis": "당신은 존재의 본질을 탐구하며 죽음을 직시하는 본래적 삶을 추구합니다.",
        "thought": "현존재와 본래성. 죽음을 향한 존재임을 깨달을 때 비로소 일상성에서 벗어나 주체적인 삶을 살 수 있습니다.",
        "books": ["존재와 시간"],
        "reading": "우리는 세상에 내던져진 존재(피투성)이지만, 동시에 자신을 기획하는 존재입니다. 존재의 목소리에 귀를 기울이십시오.",
        "image": "철학자사진/하이데거.png"
    },
    "루소": {
        "basis": "당신은 인간 본연의 자유를 사랑하며 공동체의 일반의지를 존중합니다.",
        "thought": "사회계약론 및 성선설. 자연 상태의 평등을 회복하기 위해 공공의 선인 '일반의지'에 따라야 합니다.",
        "books": ["사회계약론", "에밀"],
        "reading": "인간은 자유롭게 태어났으나 도처에 사슬이 매여 있습니다. 자연으로 돌아가 인간 본연의 선함을 회복해야 합니다.",
        "image": "철학자사진/루소.png"
    }
}

# --- [5] UI 및 앱 분기 제어 (인트로 - 테스트 - 결과) ---

# 1. 인트로 화면
if not st.session_state.started:
    st.title("📜 PhiloScales")
    st.subheader("제작: 성균관대학교_문제해결과 컴퓨팅사고 프로젝트팀")
    st.write("---")
    st.image("https://images.unsplash.com/photo-1509024644558-2f56ce76c490?w=1200", use_container_width=True)
    st.markdown("""
    ### [철학자 성향 테스트] 당신 내면의 철학자를 만나보세요.
    어렵게만 느껴졌던 철학, Philoscales을 통해 잠재된 철학을 깨워보세요!
    """)
    if st.button("🚀 테스트 시작하기", use_container_width=True):
        st.session_state.started = True
        st.rerun()

# 2. 테스트 진행 화면
elif st.session_state.started and st.session_state.result is None:
    st.title("🧩 당신의 생각을 들려주세요")
    st.info("중립보다는 '동의' 혹은 '반대'를 선택할수록 결과가 더 정확해집니다.")
    
    user_scores = {ax: 0 for ax in ["virtue", "rational", "idealism", "eastern_confucian", "eastern_dao", "deontology", "existential"]}
    mapping = {"매우 반대": -2, "반대": -1, "중립": 0, "동의": 1, "매우 동의": 2}
    
    for i, q in enumerate(questions):
        ans = st.radio(q["text"], list(mapping.keys()), index=2, key=f"q_{i}")
        user_scores[q["axis"]] += mapping[ans] * q["direction"]
        st.write("") 

    if st.button("📊 나의 철학자 확인하기", use_container_width=True):
        # 유클리드 거리 기반 최적 매칭 알고리즘
        best_match = None
        min_distance = float('inf')
        for phil, p_scores in philosophers_data.items():
            dist = sum(abs(user_scores[ax] - p_scores[ax]) for ax in user_scores)
            if dist < min_distance:
                min_distance = dist
                best_match = phil
        st.session_state.result = best_match
        st.rerun()

# 3. 결과 화면 (2차 보고서 4대 요소 반영)
else:
    phil_name = st.session_state.result
    info = philosophers_info[phil_name]
    
    st.title("🏆 테스트 결과")
    st.success(f"당신과 가장 닮은 철학자는 **{phil_name}**입니다!")
    
    # 철학자 이미지
    st.image(info["image"], use_container_width=True)
    st.write("---")
    
    # 보고서 4대 요소 렌더링
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 가치관 근거")
        st.write(info["basis"])
        
        st.subheader("🧠 핵심 사상")
        st.write(info["thought"])

    with col2:
        st.subheader("📚 추천 도서")
        for book in info["books"]:
            st.write(f"- {book}")
            
    st.write("---")
    st.subheader("📖 심화 읽을거리")
    st.info(info["reading"])
    
    
    
    # --- 공유 영역
    st.divider()
    
    # 버튼 영역 (다시 테스트하기)
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        st.session_state.started = False
        st.session_state.result = None
        st.rerun()
    
    # SNS 공유 영역 (가로로 배치)
    st.write("📢 **나의 결과 동네방네 소문내기**")
    share_col1, share_col2, share_col3 = st.columns(3)
    
    with share_col1:
        # 1. 카카오톡 공유 (나의 결과 이름이 포함된 링크 전송)
        kakao_text = f"나의 PhiloScales 결과는 {phil_name}입니다! 여러분도 테스트해보세요!"
        kakao_url = f"https://sharer.kakao.com/talk/friends/picker/link?app_key=YOUR_APP_KEY_IF_ANY&shortKey=1234&url=https://gdp-dashboard-jdzthcv3w47.streamlit.app/&title={kakao_text}"
        st.link_button("💬 카카오톡 공유", kakao_url, use_container_width=True)
        
    with share_col2:
        # 2. X(트위터) 공유 (기존 기능 유지)
        st.link_button("🚀 X(트위터) 공유", f"https://twitter.com/intent/tweet?text=나의 철학자 결과는 {phil_name}입니다! 여러분도 확인해보세요!", use_container_width=True)
        
    with share_col3:
        # 3. 인스타그램 공유 (안내 메시지 띄우기 버튼)
        if st.button("📸 인스타그램 공유", use_container_width=True):
            st.session_state.show_insta_info = True

    # 인스타그램 버튼 클릭 시 안내 문구 출력
    if st.session_state.get('show_insta_info', False):
        st.info("💡 **인스타그램 공유 팁:** 멋진 철학자 결과 화면을 캡처(스크린샷)한 후, 인스타 스토리나 피드에 `#PhiloScales` 해시태그와 함께 올려 친구들에게 자랑해 보세요!")
        