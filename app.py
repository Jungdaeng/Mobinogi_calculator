import streamlit as st
import pandas as pd

# ==================================================
# 페이지 설정 (테마 무시)
# ==================================================
st.set_page_config(
    page_title="모비노기 도적 보석 태그 효율 계산기",
    layout="wide"
)

# ==================================================
# 강제 UI 스타일 (모바일 다크모드 완전 차단)
# ==================================================
st.markdown("""
<style>
/* ===== 완전 강제 라이트 UI ===== */
html, body, .stApp {
    background-color: #F9FAFB !important;
    color: #111827 !important;
}

/* ===== 모든 텍스트 강제 ===== */
* {
    color: #111827 !important;
    box-shadow: none !important;
}

/* ===== 제목 ===== */
h1 {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
h2, h3 {
    font-weight: 700;
}

/* ===== 설명 텍스트 ===== */
.caption {
    color: #4B5563 !important;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

/* ===== 주의사항 박스 ===== */
.notice-box {
    background-color: #EEF2FF;
    border: 2px solid #2563EB;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

/* ===== 버튼 ===== */
.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-radius: 10px;
    padding: 0.7rem 1.6rem;
    font-weight: 700;
    border: none;
}
.stButton > button:hover {
    background-color: #1D4ED8 !important;
}

/* ===== 입력 라벨 ===== */
label {
    font-weight: 600;
}

/* ===== 테이블 ===== */
[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    background-color: #FFFFFF !important;
}
[data-testid="stDataFrame"] * {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ===== 입력창 (number_input, text_input) ===== */
input, textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
}

/* ===== number_input +/- 버튼 영역 ===== */
button[kind="secondary"] {
    background-color: #E5E7EB !important;
    color: #111827 !important;
}

/* ===== Data Editor 셀 ===== */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] th {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* ===== Data Editor 입력 중 셀 ===== */
[data-testid="stDataFrame"] input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# Session State
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "step" not in st.session_state:
    st.session_state.step = 0
if "gem_data" not in st.session_state:
    st.session_state.gem_data = {
        "스타프리즘": {},
        "스타프리즘S": {},
        "온전한 스타프리즘": {}
    }
if "dps_data" not in st.session_state:
    st.session_state.dps_data = {}
if "green_rate" not in st.session_state:
    st.session_state.green_rate = 0.0

# ==================================================
# 데이터 정의
# ==================================================
TAGS = ["연타", "방해", "소환", "강타", "이동", "생존"]

GEM_RATE = {
    "스타프리즘": 0.020,
    "스타프리즘S": 0.021,
    "온전한 스타프리즘": 0.022,
}

GREEN_HELIO = {
    "선택 안 함": 0.0,
    "그린헬리오도르": 0.015,
    "정제된 그린헬리오도르": 0.021,
    "순수한 그린헬리오도르": 0.022,
}

SKILL_TAGS = {
    "독 폭발": ["연타", "방해", "소환"],
    "기습": ["강타", "이동"],
    "쓰로잉 봄": ["강타", "방해"],
    "은신 추가데미지": ["생존", "이동", "방해"],
    "스크류 대거": ["연타", "방해"],
    "포이즌 트랩": ["연타", "방해", "소환"],
    "평타": [],
    "블리츠 러시": ["연타", "생존"],
}
SKILLS = list(SKILL_TAGS.keys())

# ==================================================
# INTRO PAGE
# ==================================================
if st.session_state.page == "intro":
    st.title("모비노기 도적 보석 태그 효율 계산기")
    st.markdown("<div class='caption'>태그 1개당 효율 점수 비교 도구</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="notice-box">
    <h3>⚠️ 주의사항</h3>
    <ul>
        <li>본 계산기는 <b>보석 태그 효율을 러프하게 비교</b>하기 위한 참고용 도구입니다.</li>
        <li>DPS 표를 기반으로 계산되며, 판·장비·스탯에 따라 결과가 달라질 수 있습니다.</li>
        <li>무방비·연타·강타·치명타·추가타가 반영된 <b>최종 데미지 흐름</b> 기준의 상대적 효율입니다.</li>
        <li><b>DPS 표 입력이 필수</b>입니다.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        if st.button("확인 후 시작"):
            st.session_state.page = "calc"
            st.session_state.step = 0
            st.rerun()

# ==================================================
# CALCULATOR
# ==================================================
else:
    st.title("모비노기 도적 보석 태그 효율 계산기")
    st.markdown("<div class='caption'>태그 1개당 효율 점수</div>", unsafe_allow_html=True)

    # STEP 1
    if st.session_state.step == 0:
        st.subheader("① 보석 정보 입력")
        for gem in st.session_state.gem_data:
            st.markdown(f"**{gem}**")
            cols = st.columns(len(TAGS))
            for col, tag in zip(cols, TAGS):
                key = f"{gem}_{tag}"
                st.session_state.gem_data[gem][tag] = col.number_input(tag, 0, step=1, key=key)
        st.markdown("**그린헬리오도르 (1개 선택)**")
        choice = st.radio("", list(GREEN_HELIO.keys()), horizontal=True)
        st.session_state.green_rate = GREEN_HELIO[choice]
        if st.button("다음 단계 → DPS 입력"):
            st.session_state.step = 1
            st.rerun()

    # STEP 2
    elif st.session_state.step == 1:
        st.subheader("② DPS 기여도 입력")
        for s in SKILLS:
            st.session_state.dps_data.setdefault(s, 0.0)

        df = pd.DataFrame({
            "스킬": SKILLS,
            "데미지 기여도 (%)": [st.session_state.dps_data[s] for s in SKILLS]
        })

        edited = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "데미지 기여도 (%)": st.column_config.NumberColumn(
                    min_value=0.0, max_value=100.0, step=0.1
                )
            }
        )

        total = edited["데미지 기여도 (%)"].sum()
        st.markdown(
            f"<div class='caption'>현재 총 데미지 비율: <b>{total:.1f}%</b><br>"
            "100%가 아니어도 자동으로 정규화됩니다.</div>",
            unsafe_allow_html=True
        )

        if st.button("효율 계산하기"):
            for _, r in edited.iterrows():
                st.session_state.dps_data[r["스킬"]] = r["데미지 기여도 (%)"]
            st.session_state.step = 2
            st.rerun()

    # STEP 3
    else:
        st.subheader("③ 태그 효율 계산 결과")
        total = sum(st.session_state.dps_data.values())
        dps_w = {k: (v / total if total else 0) for k, v in st.session_state.dps_data.items()}

        rows = []
        for t in TAGS:
            tag_w = sum(dps_w[s] for s in SKILLS if t in SKILL_TAGS[s])
            base, cnt = 0.0, 0
            for g, tags in st.session_state.gem_data.items():
                c = tags.get(t, 0)
                base += c * GEM_RATE[g]
                cnt += c
            tag_rate = base / cnt if cnt else 0.0
            score = tag_w * (tag_rate + st.session_state.green_rate)
            rows.append({"태그": t, "보유 개수": cnt, "태그 1개당 효율 점수": round(score * 100, 3)})

        st.dataframe(
            pd.DataFrame(rows).sort_values("태그 1개당 효율 점수", ascending=False),
            hide_index=True,
            use_container_width=True
        )

        if st.button("← 다시 계산하기"):
            st.session_state.page = "intro"
            st.rerun()
