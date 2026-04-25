import streamlit as st

# 페이지 설정 (브라우저 탭 이름과 아이콘)
st.set_page_config(page_title="PhiloScales", page_icon="📜")

# 세션 상태 초기화 (시작 버튼 클릭 여부 확인)
if 'started' not in st.session_state:
    st.session_state.started = False

# --- 메인 첫 화면 ---
if not st.session_state.started:
    st.title("📜 PhiloScales: 나와 닮은 철학자 찾기")
    st.write("---")
    
    # 이곳에 철학적인 배경 이미지를 넣으면 더 예쁩니다.
    st.image("https://images.unsplash.com/photo-1509024644558-2f56ce76c490?q=80&w=1000&auto=format&fit=crop", 
             caption="당신을 정의하는 철학적 신념은 무엇인가요?")
    
    st.info("단 10개의 질문으로 당신의 내면 속에 숨겨진 고대와 현대의 철학자를 찾아보세요.")
    
    # 시작 버튼
    if st.button("🚀 테스트 시작하기", use_container_width=True):
        st.session_state.started = True
        st.rerun()

# --- 설문 조사 화면 ---
else:
    # 기존에 만드신 질문 로직을 여기에 넣으세요
    st.title("질문에 답해주세요")
    
    # (기존 질문 코드...)
    
    # 다시 처음으로 돌아가는 버튼 (선택 사항)
    if st.button("처음으로 돌아가기"):
        st.session_state.started = False
        st.rerun()
        

import streamlit as st

st.title("PhiloScales: 나와 닮은 철학자 찾기")
st.write("질문에 답하면 당신의 철학적 성향과 가장 가까운 철학자를 추천해드립니다.")

questions = [
    {
        "text": "시대와 문화가 달라도 변하지 않는 진리는 존재한다.",
        "axis": "truth",
        "direction": 1
    },
    {
        "text": "옳고 그름은 상황과 맥락에 따라 달라질 수 있다.",
        "axis": "truth",
        "direction": -1
    },
    {
        "text": "좋은 결과를 만든다면 어느 정도의 규칙 위반은 정당화될 수 있다.",
        "axis": "ethics",
        "direction": -1
    },
    {
        "text": "결과가 좋더라도 지켜야 할 원칙은 반드시 지켜야 한다.",
        "axis": "ethics",
        "direction": 1
    },
    {
        "text": "인간은 자신의 삶을 스스로 선택하고 책임질 수 있다.",
        "axis": "freedom",
        "direction": 1
    }
]

scores = {
    "truth": 0,
    "ethics": 0,
    "freedom": 0
}

answer_scores = {
    "매우 반대": -2,
    "반대": -1,
    "중립": 0,
    "동의": 1,
    "매우 동의": 2
}

for i, question in enumerate(questions):
    answer = st.radio(
        f"Q{i + 1}. {question['text']}",
        ["매우 반대", "반대", "중립", "동의", "매우 동의"],
        horizontal=True
    )

    scores[question["axis"]] += answer_scores[answer] * question["direction"]

philosophers = {
    "칸트": {
        "truth": 4,
        "ethics": 4,
        "freedom": 2
    },
    "니체": {
        "truth": -2,
        "ethics": -2,
        "freedom": 4
    },
    "소크라테스": {
        "truth": 3,
        "ethics": 3,
        "freedom": 2
    }
}

# 결과 보기 버튼 및 로직
if st.button("결과 보기", use_container_width=True):
    best_match = None
    best_distance = 999
    
    for philosopher, philosopher_scores in philosophers.items():
        distance = 0
        for axis in scores:
            distance += abs(scores[axis] - philosopher_scores[axis])
        
        if distance < best_distance:
            best_distance = distance
            best_match = philosopher
            
    # 결과를 세션에 저장 (공유 버튼에서 사용하기 위함)
    st.session_state.result = best_match

# 결과가 생성되었을 때만 화면에 표시
if 'result' in st.session_state:
    result_name = st.session_state.result
    st.success(f"🎉 당신과 가장 닮은 철학자는 **{result_name}**입니다!")
    
    st.divider() # 구분선
    
    # 공유 버튼들을 결과 확인 후에만 나타나도록 배치
    st.link_button(
        "🚀 X(트위터)에 결과 공유하기", 
        f"https://twitter.com/intent/tweet?text=나의 철학자 결과는 {result_name}입니다! 여러분도 테스트해보세요!"
    )
    
    if st.button("🔗 결과 링크 복사하기"):
        st.code("https://your-app-link.streamlit.app") # 실제 배포 주소로 변경 가능
        st.toast("링크가 표시되었습니다. 복사해서 사용하세요!")