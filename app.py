import streamlit as st
import pandas as pd

# ==================================================
# 페이지 설정
# ==================================================
st.set_page_config(
    page_title="모비노기 도적 보석 태그 효율 계산기",
    layout="wide"
)
st.markdown("""
<style>
/* ===== 기본 배경 ===== */
html, body {
    background-color: #F9FAFB !important;
}

/* ===== 제목 계층 ===== */
h1 {
    color: #0F172A !important;
}
h2, h3 {
    color: #111827 !important;
}

/* ===== 일반 텍스트 (본문) ===== */
.stMarkdown, 
.stText, 
.stSubheader, 
.stHeader,
label {
    color: #111827 !important;
    font-weight: 500;
}

/* ===== 입력창 라벨 ===== */
[data-testid="stWidgetLabel"] {
    color: #0F172A !important;
    font-weight: 600;
}

/* ===== 캡션 / 보조 설명 ===== */
.caption {
    color: #6B7280 !important;
    font-size: 0.9rem;
}

/* ===== 테이블 텍스트 ===== */
[data-testid="stDataFrame"] * {
    color: #111827 !important;
}

/* ===== 버튼 ===== */
.stButton > button {
    background-color: #2F6FED;
    color: #FFFFFF !important;
    font-weight: 600;
}

/* ===== 라디오 / 체크 ===== */
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
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
# 고정 데이터
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
        <li>본 계산기는 <b>보석 태그 효율을 비교</b>하기 위한 참고용 도구입니다.</li>
        <li>DPS 표를 기반으로 계산되며, 판·장비·스탯에 따라 결과가 달라질 수 있습니다.</li>
        <li>무방비·연타·강타·치명타·추가타가 반영된 <b>최종 데미지 흐름</b>을 기준으로 한<br>
            <b>상대적인 효율 점수</b>입니다.</li>
        <li><b>정확한 데미지 증가율을 보장하지 않습니다.</b></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # 주의사항 박스와 버튼 사이 여백
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)

    # 중앙 정렬 버튼
    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col2:
        if st.button("확인 후 시작"):
            st.session_state.page = "calc"
            st.session_state.step = 0
            st.rerun()


# ==================================================
# CALCULATOR
# ==================================================
elif st.session_state.page == "calc":

    st.title("모비노기 도적 보석 태그 효율 계산기")
    st.markdown("<div class='caption'>태그 1개당 효율 점수</div>", unsafe_allow_html=True)

    # ---------- STEP 1
    if st.session_state.step == 0:
        st.subheader("① 보석 정보 입력")

        for gem in st.session_state.gem_data:
            st.markdown(f"**{gem}** (태그 1개당 기준 효율)")
            cols = st.columns(len(TAGS))
            for col, tag in zip(cols, TAGS):
                key = f"{gem}_{tag}"
                st.session_state.gem_data[gem][tag] = col.number_input(
                    tag, min_value=0, step=1, key=key
                )
            st.divider()

        st.markdown("**그린헬리오도르 계열 (1개만 선택 가능)**")
        choice = st.radio("", list(GREEN_HELIO.keys()), horizontal=True)
        st.session_state.green_rate = GREEN_HELIO[choice]

        if st.button("다음 단계 → DPS 입력"):
            st.session_state.step = 1
            st.rerun()

    # ---------- STEP 2
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
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1
                )
            }
        )
        # DPS 입력 테이블 아래 안내 문구
        # 현재 총 데미지 비율 계산
        current_total = edited["데미지 기여도 (%)"].sum()

        st.markdown(
            f"""
            <div class='caption'>
            현재 입력된 총 데미지 비율: <b>{current_total:.1f}%</b><br>
            총 데미지 비율은 100%가 아니어도 괜찮습니다.<br>
            입력된 값은 내부 계산 시 자동으로 정규화되어 반영됩니다.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("효율 계산하기"):
            for _, r in edited.iterrows():
                st.session_state.dps_data[r["스킬"]] = r["데미지 기여도 (%)"]
            st.session_state.step = 2
            st.rerun()

    # ---------- STEP 3
    elif st.session_state.step == 2:
        st.subheader("③ 태그 효율 계산 결과")

        total = sum(st.session_state.dps_data.values())
        dps_w = {k: (v / total if total else 0) for k, v in st.session_state.dps_data.items()}

        tag_w = {t: 0.0 for t in TAGS}
        for s, w in dps_w.items():
            for t in SKILL_TAGS[s]:
                tag_w[t] += w

        rows = []
        for t in TAGS:
            base, cnt = 0.0, 0
            for g, tags in st.session_state.gem_data.items():
                c = tags.get(t, 0)
                base += c * GEM_RATE[g]
                cnt += c
            tag_rate = base / cnt if cnt else 0.0
            score = tag_w[t] * (tag_rate + st.session_state.green_rate)

            rows.append({
                "태그": t,
                "보유 개수": cnt,
                "태그 1개당 효율 점수": round(score * 100, 3)
            })

        st.dataframe(
            pd.DataFrame(rows).sort_values(
                "태그 1개당 효율 점수", ascending=False
            ),
            hide_index=True,
            use_container_width=True
        )

        if st.button("← 다시 계산하기"):
            st.session_state.page = "intro"
            st.rerun()
