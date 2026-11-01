import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시재생 내비게이터", page_icon="🏙️", layout="centered")

st.title("🏙️ 전국 시·군·구 정비사업 및 미래 잠재력 진단 대시보드")
st.markdown("**지역 균형발전과 구도심 재개발·재건축 현황을 한눈에 파악하고 미래 가능성을 진단하는 인터랙티브 웹 앱**")
st.divider()

@st.cache_data
def load_data():
    return pd.read_csv('urban_renewal_data.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("데이터 파일('urban_renewal_data.csv')을 찾을 수 없습니다.")
    st.stop()

st.sidebar.header("🔍 전국 시·군·구 탐색")
selected_city = st.sidebar.selectbox("조회할 지역을 선택하세요", df['시군구명'].unique())

city_data = df[df['시군구명'] == selected_city].iloc[0]

st.subheader(f"📍 [{selected_city}] 정비사업 핵심 지표 요약")

col1, col2, col3 = st.columns(3)
col1.metric(label="진행 중 사업 구역 수", value=f"{city_data['사업구역수']} 개소")
col2.metric(label="과거 평균 청약 경쟁률", value=f"{city_data['평균청약경쟁률']} : 1")
col3.metric(label="🚀 종합 정비 잠재력 지수", value=f"{city_data['잠재력점수']} 점", delta="우수 지역")

st.markdown("")
st.subheader("📋 주요 정비사업 추진 사례 및 흥행 성적표")
st.markdown(f"- **대표 추진 단지:** {city_data['주요단지명']}")
st.markdown(f"- **시장 흥행 결과:** {city_data['분양결과']}")
st.markdown(f"- **노후 건축물 비율:** 약 {city_data['노후도비율']}%")

st.subheader("💡 AI 기반 정비사업 추진 잠재력 진단")
score = city_data['잠재력점수']

if score >= 85:
    grade_text = "S등급 (매우 높음 - 적극적 투자 및 선제적 정비 권장)"
    box_type = st.success
elif score >= 75:
    grade_text = "A등급 (높음 - 구도심 주거 수요 풍부, 사업성 우수)"
    box_type = st.info
else:
    grade_text = "B등급 (보통 - 주민 동의 및 분담금 리스크 신중 검토 필요)"
    box_type = st.warning

box_type(f"**[{selected_city} 진단 결과]** 종합 점수 {score}점으로 **{grade_text}**로 평가됩니다. 노후도와 인구 유입 지표를 종합할 때, 향후 체계적인 정비계획 수립 시 높은 사업 추진 가능성이 기대됩니다.")

st.divider()
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>© 2026 Urban Regeneration & Regional Balance Project. All rights reserved.</p>", unsafe_allow_html=True)
