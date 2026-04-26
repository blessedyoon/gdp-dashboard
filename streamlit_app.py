import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="PhiloScales", page_icon="📜", layout="centered")

# --- 세션 상태 초기화 ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'result' not in st.session_state:
    st.session_state.result = None

# --- 데이터 정의 (총 11개 질문) ---
questions = [
    {"text": "시대와 문화가 달라도 변하지 않는 진리는 존재한다."},
    {"text": "옳고 그름은 상황과 맥락에 따라 달라질 수 있다."},
    {"text": "좋은 결과를 만든다면 어느 정도의 규칙 위반은 정당화될 수 있다."},
    {"text": "결과가 좋더라도 지켜야 할 원칙은 반드시 지켜야 한다."},
    {"text": "인간은 자신의 삶을 스스로 선택하고 책임질 수 있다."},
    {"text": "개인의 자유, 자기결정권, 자율성을 중시한다."},
    {"text": "사회질서, 타인과의 조화, 공동체 책임을 중시한다."},
    {"text": "감정보다 논리와 이성적 판단을 우선한다."},
    {"text": "삶의 만족, 행복, 쾌감, 심리적 충만을 중시한다."},
    {"text": "보편적 기준, 의무, 옳고 그름의 원칙을 지키려한다."},
    {"text": "이상보다 현실 적용 가능성, 효율, 실제 도움을 우선하려 한다."}
]

philosophers_data = {
    "임마누엘 칸트": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/43/Immanuel_Kant_3.jpg",
        "description": "철저한 원칙주의자 칸트와 닮았군요! 감정보다 도덕적 의무를 중시합니다.",
        "quote": "\"네 의지의 준칙이 언제나 보편적 입법 원리가 되게 하라.\"",
        "scores": [2, -2, -2, 2, 1, 1, 1, 2, -1, 2, -1]
    },
    "존 스튜어트 밀": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/9/99/John_Stuart_Mill_by_London_Stereoscopic_Company%2C_c1870.jpg",
        "description": "합리적인 자유주의자 밀과 닮으셨네요. 개인의 자유와 최대 다수의 행복을 중시합니다.",
        "quote": "\"만족해하는 돼지보다 불만족스러운 인간이 되는 것이 낫다.\"",
        "scores": [1, 1, 2, -1, 2, 2, 1, 1, 2, 0, 2]
    },
    "아리스토텔레스": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Aristotle_Altemps_Inv8575.jpg",
        "description": "중용과 공동체의 덕을 중시하는 아리스토텔레스 타입입니다.",
        "quote": "\"탁월함은 행위가 아니라 습관이다.\"",
        "scores": [1, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1]
    },
    "프리드리히 니체": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Nietzsche187c.jpg",
        "description": "기존의 틀을 깨고 자신만의 가치를 창조하는 니체와 닮았군요!",
        "quote": "\"나를 죽이지 못하는 것은 나를 더 강하게 만든다.\"",
        "scores": [-1, 2, 1, -2, 2, 2, -2, 0, 1, -2, 0]
    }
}

# --- 전역 스타일 (가로 정렬 및 버튼 디자인) ---
st.markdown("""
    <style>
    /* 라디오 버튼 가로 일직선 강제 정렬 */
    div[role="radiogroup"] {
        flex-direction: row !important;
        justify-content: space-between !important;
        display: flex !important;
        flex-wrap: nowrap !important;
    }
    div[role="radiogroup"] label {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 50px;
    }
    /* 결과 이미지 모서리 둥글게 */
    .res-img { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 메인 로직 ---
if st.session_state.result:
    # --- 결과 화면 ---
    res_name = st.session_state.result
    p_info = philosophers_data[res_name]
    st.balloons()
    st.title(f"🎉 당신은 **{res_name}** 타입!")
    st.image(p_info["image"], width=350)
    st.info(p_info["description"])
    st.markdown(f"> **{p_info['quote']}**")
    
    st.write("---")
    st.subheader("📲 결과 공유하기")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("𝕏 (Twitter) 공유", "https://twitter.com/intent/tweet?text=나의 철학자 매칭 결과는 " + res_name + "!", use_container_width=True)
    with col2:
        st.link_button("📸 Instagram 인증", "https://www.instagram.com/", use_container_width=True)
    
    st.write("")
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        st.session_state.result = None
        st.session_state.started = False
        st.rerun()

elif st.session_state.started:
    # --- 설문 화면 ---
    st.title("📜 당신의 생각은?")
    user_responses = []
    score_map = {"매우 비동의": -2, "비동의": -1, "중립": 0, "동의": 1, "매우 동의": 2}

    for i, q in enumerate(questions):
        st.markdown(f"#### {i+1}. {q['text']}")
        choice = st.radio(
            f"q_{i}",
            options=["매우 비동의", "비동의", "중립", "동의", "매우 동의"],
            index=2,
            horizontal=True,
            key=f"radio_{i}",
            label_visibility="collapsed"
        )
        # 양쪽 끝 라벨 표시
        c1, _, c2 = st.columns([1, 3, 1])
        with c1: st.caption("매우 비동의")
        with c2: st.caption("매우 동의")
        st.write("---")
        user_responses.append(score_map[choice])

    if st.button("결과 보기 🔍", use_container_width=True):
        best_match = min(philosophers_data.keys(), key=lambda name: sum((u - p)**2 for u, p in zip(user_responses, philosophers_data[name]["scores"])))
        st.session_state.result = best_match
        st.rerun()

else:
    # --- 시작 화면 ---
    st.title("📜 PhiloScales")
    intro_url = "https://images.unsplash.com/photo-1502139214982-d0ad755818d8?auto=format&fit=crop&q=80&w=1000"
    st.image(intro_url, use_container_width=True, caption="나와 닮은 철학자는 누구일까요?")
    st.write("**총 11개의 문항**으로 당신의 철학적 성향을 분석합니다.")
    if st.button("🚀 테스트 시작하기", use_container_width=True):
        st.session_state.started = True
        st.rerun()
        