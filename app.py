import streamlit as st
import pandas as pd

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="모비노기 도적 보석 태그 효율 계산기",
    layout="wide"
)

# ===============================
# Safe CSS (data_editor 안 깨짐)
# ===============================
st.markdown("""
<style>
html, body, .stApp {
    background-color: #F9FAFB !important;
}

/* 제목 */
h1, h2, h3 {
    color: #111827 !important;
    font-weight: 700;
}

/* 일반 텍스트 */
.stMarkdown, label, p {
    color: #111827 !important;
}

/* 버튼 */
.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
}

/* number_input */
input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
}

/* number_input +/- */
[data-testid="stNumberInput"] button {
    background-color: #E5E7EB !important;
    color: #111827 !important;
}

/* data_editor */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] td {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* 안내 박스 */
.notice {
    background: #EEF2FF;
    border: 2px solid #2563EB;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0;
}
.caption {
    color: #4B5563 !important;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Session State
# ===============================
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

# ===============================
# Constants
# ===============================
TAGS = ["연타", "방해", "소환", "강타", "이동", "생존"]

GEM_RATE = {
    "스타프리즘": 0.020,
    "스타프리즘S": 0.021,
    "온전한 스타프리즘": 0.022
}

GREEN_HELIO = {
    "선택 안 함": 0.0,
    "그린헬리오도르": 0.015,
    "정제된 그린헬리오도르": 0.021,
    "순수한 그린헬리오도르": 0.022
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

# ===============================
# INTRO
# ===============================
if st.session_state.page == "intro":
    st.title("모비노기 도적 보석 태그 효율 계산기")
    st.markdown("<div class='caption'>태그 1개당 효율 점수 비교 도구</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="notice">
    <b>⚠️ 주의사항</b>
    <ul>
        <li>본 계산기는 보석 태그 효율을 러프하게 비교하기 위한 참고용 도구입니다.</li>
        <li>DPS 표 기반 계산으로, 장비·판·스탯에 따라 결과가 달라질 수 있습니다.</li>
        <li>무방비·연타·강타·치명타·추가타가 반영된 최종 데미지 흐름 기준의 상대 효율입니다.</li>
        <li><b>DPS 기여도 입력은 필수</b>입니다.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("확인 후 시작"):
        st.session_state.page = "calc"
        st.session_state.step = 0
        st.rerun()

# ===============================
# CALCULATOR
# ===============================
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
                if key not in st.session_state:
                    st.session_state[key] = st.session_state.gem_data[gem].get(tag, 0)

                val = col.number_input(tag, min_value=0, step=1, key=key)
                st.session_state.gem_data[gem][tag] = val

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
        weights = {k: (v / total if total else 0) for k, v in st.session_state.dps_data.items()}

        rows = []
        for tag in TAGS:
            tag_weight = sum(weights[s] for s in SKILLS if tag in SKILL_TAGS[s])
            base, cnt = 0.0, 0
            for gem, tags in st.session_state.gem_data.items():
                c = tags.get(tag, 0)
                base += c * GEM_RATE[gem]
                cnt += c

            score = tag_weight * ((base / cnt) + st.session_state.green_rate if cnt else st.session_state.green_rate)
            rows.append({
                "태그": tag,
                "보유 개수": cnt,
                "태그 1개당 효율 점수": round(score * 100, 3)
            })

        st.dataframe(
            pd.DataFrame(rows).sort_values("태그 1개당 효율 점수", ascending=False),
            hide_index=True,
            use_container_width=True
        )

        if st.button("← 다시 계산하기"):
            st.session_state.step = 0
            st.rerun()
