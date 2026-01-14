import streamlit as st

st.set_page_config(
    page_title="치명타 계산기",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔️ 치명타 데미지 계산기")

atk = st.number_input("공격력", min_value=0, value=1000, step=50)
crit = st.slider("치명타 확률 (%)", 0, 100, 50)
crit_dmg = st.slider("치명타 배율", 1.0, 3.0, 1.5, step=0.05)

damage = atk * (1 + crit / 100 * (crit_dmg - 1))

st.divider()
st.metric("📊 기대 데미지", f"{damage:,.1f}")
