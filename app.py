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
