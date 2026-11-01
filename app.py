import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="전국 정비사업 내비게이터", page_icon="🏙️", layout="wide")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('urban_renewal_data.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("데이터 파일('urban_renewal_data.csv')을 찾을 수 없습니다.")
    st.stop()

# 메인 타이틀
st.title("🏙️ 전국 시·군·구 정비사업 현황 및 미래 잠재력 진단 대시보드")
st.caption("공공데이터포털 정비사업 통계 및 청약홈 데이터를 기반으로 한 데이터 기반 의사결정 지원 시스템")
st.divider()

# 사이드바: 검색 기능 및 드롭박스
st.sidebar.header("🔍 전국 시·군·구 탐색")

# 1. 키워드 검색창 추가
search_kw = st.sidebar.text_input("🔎 지역명 검색 (예: 진주, 영등포)", "")

# 검색어에 따라 드롭박스 리스트 필터링
all_cities = df['시군구명'].tolist()
if search_kw:
    filtered_cities = [c for c in all_cities if search_kw.strip() in c]
    if not filtered_cities:
        st.sidebar.warning("검색 결과가 없습니다.")
        filtered_cities = all_cities
else:
    filtered_cities = all_cities

selected_city = st.sidebar.selectbox("지역을 선택하세요", filtered_cities)

# 선택된 데이터 추출
data = df[df['시군구명'] == selected_city].iloc[0]

# 상단 대시보드 메트릭 카드 (6개 지표)
st.subheader(f"📍 [{selected_city}] 정비사업 핵심 종합 지표")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("총 정비구역 수", f"{data['총사업구역수']} 개소")
col2.metric("평균 청약경쟁률", f"{data['평균청약경쟁률']} : 1")
col3.metric("노후 건축물 비율", f"{data['노후건축물비율']} %")
col4.metric("10년 인구변동률", f"{data['10년인구변동률']} %")
col5.metric("🚀 잠재력 스코어", f"{data['잠재력점수']} 점")

st.markdown("<br>", unsafe_allow_html=True)

# 2열 레이아웃: 사업 유형별 분배 & 추진 단계별 현황
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏗️ 사업 유형별 구역 분포")
    type_df = pd.DataFrame({
        "사업 유형": ["재개발", "재건축", "기타 정비사업"],
        "구역 수": [data['재개발구역수'], data['재건축구역수'], data['기타정비구역수']]
    })
    st.dataframe(type_df, use_container_width=True, hide_index=True)

with c2:
    st.subheader("🔄 추진 단계별 진행 현황")
    step_df = pd.DataFrame({
        "추진 단계": ["1. 조합설립인가", "2. 사업시행인가", "3. 관리처분인가", "4. 착공 및 분양"],
        "진행 구역 수": [data['조합설립단계'], data['사업시행인가단계'], data['관리처분인가단계'], data['착공분양단계']]
    })
    st.dataframe(step_df, use_container_width=True, hide_index=True)

st.divider()

# 종합 AI 진단 및 리포트
st.subheader("💡 데이터 기반 종합 정비 잠재력 진단")
score = data['잠재력점수']

if score >= 82:
    grade = "S등급 (매우 높음)"
    st.success(f"**진단 결과: {grade}** — 노후도({data['노후건축물비율']}%) 대비 입지 선호도와 청약 수요({data['평균청약경쟁률']}:1)가 매우 높아 정비사업 추진 시 빠른 사업 진행과 높은 대외 사업성이 기대되는 핵심 거점 지역입니다.")
elif score >= 70:
    grade = "A등급 (높음)"
    st.info(f"**진단 결과: {grade}** — 구도심 재개발·재건축 수요가 안정적으로 존재하며, 공공 및 민간 주도 정비사업 추진 시 주거 환경 개선 효과가 크게 나타날 수 있는 지역입니다.")
else:
    grade = "B등급 (신중 검토 필요)"
    st.warning(f"**진단 결과: {grade}** — 인구 변동률 및 분양 성적을 고려할 때 사업성 확보를 위한 가중치 조정 및 공공재개발 등 정책적 지원책 연계가 권장됩니다.")

st.markdown("<br><p style='text-align: center; color: gray; font-size: 12px;'>Data Source: Public Data Portal & REB Infrastructure Analysis Model</p>", unsafe_allow_html=True)
