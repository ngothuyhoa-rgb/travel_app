import streamlit as st
from openai import OpenAI
import requests

# ======================
#   OpenAI Client
# ======================
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ======================
#     TRAVEL DATA
# ======================
DEST_DATA = {
    "한국": {
        "display": "한국 (Seoul, Busan, Jeju)",
        "tour": ["경복궁", "부산 해운대", "제주 성산일출봉"],
        "food": ["비빔밥", "삼겹살", "김치찌개"],
        "hotel": ["롯데호텔", "신라호텔"],
        "currency_code": "KRW",
        "weather": "봄 선선 / 여름 더움 / 가을 청량 / 겨울 추움"
    },

    "일본": {
        "display": "일본 (도쿄, 오사카, 교토)",
        "tour": ["도쿄타워", "오사카성", "후시미 이나리"],
        "food": ["초밥", "라멘", "오코노미야키"],
        "hotel": ["APA 호텔", "도요코 인"],
        "currency_code": "JPY",
        "weather": "사계절 뚜렷함"
    },

    "베트남": {
        "display": "베트남 (하노이, 호치민, 다낭)",
        "tour": ["하롱베이", "호이안", "다낭 미케비치"],
        "food": ["쌀국수", "반미", "분짜"],
        "hotel": ["빈펄", "아바니"],
        "currency_code": "VND",
        "weather": "열대 기후"
    },

    "미국": {
        "display": "미국 (뉴욕, LA, 시카고)",
        "tour": ["자유의 여신상", "그랜드 캐니언", "타임스 스퀘어"],
        "food": ["햄버거", "스테이크", "피자"],
        "hotel": ["힐튼", "메리어트"],
        "currency_code": "USD",
        "weather": "지역마다 상이"
    },

    "프랑스": {
        "display": "프랑스 (파리, 니스, 리옹)",
        "tour": ["에펠탑", "루브르 박물관", "몽마르트 언덕"],
        "food": ["크루아상", "에스카르고", "라따뚜이"],
        "hotel": ["Le Meurice", "Hotel Lutetia"],
        "currency_code": "EUR",
        "weather": "온화한 기후"
    },

    "독일": {
        "display": "독일 (베를린, 뮌헨)",
        "tour": ["브란덴부르크 문", "뮌헨 광장"],
        "food": ["독일식 소시지", "프레첼"],
        "hotel": ["힐튼 베를린", "룸메이트 호텔"],
        "currency_code": "EUR",
        "weather": "겨울 매우 추움"
    },

    "스페인": {
        "display": "스페인 (마드리드, 바르셀로나)",
        "tour": ["사그라다 파밀리아", "구엘공원"],
        "food": ["파에야", "타파스"],
        "hotel": ["H10 Madison", "NH Hotel"],
        "currency_code": "EUR",
        "weather": "따뜻하고 화창함"
    },

    "이탈리아": {
        "display": "이탈리아 (로마, 베네치아)",
        "tour": ["콜로세움", "베네치아 운하"],
        "food": ["파스타", "피자"],
        "hotel": ["Hotel Artemide", "NH Venezia"],
        "currency_code": "EUR",
        "weather": "여름 매우 더움"
    },

    "싱가포르": {
        "display": "싱가포르 (마리나베이, 센토사)",
        "tour": ["마리나 베이 샌즈", "센토사", "가든스 바이 더 베이"],
        "food": ["치킨라이스", "칠리크랩"],
        "hotel": ["마리나 베이 샌즈", "Ritz Hotel"],
        "currency_code": "SGD",
        "weather": "일년 내내 더움"
    },

    "태국": {
        "display": "태국 (방콕, 푸껫)",
        "tour": ["왕궁", "푸껫 해변", "치앙마이 사원"],
        "food": ["팟타이", "똠얌꿍"],
        "hotel": ["AVANI", "Centara"],
        "currency_code": "THB",
        "weather": "건기/우기 뚜렷"
    },
}


# ======================
#   1000 KRW TO OTHER CURRENCY
# ======================
def convert_1000_krw(target_currency):
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url).json()

    if response["result"] != "success":
        return None

    rates = response["rates"]

    usd_to_krw = rates.get("KRW")
    usd_to_target = rates.get(target_currency)

    if not usd_to_krw or not usd_to_target:
        return None

    # 1 KRW -> target
    rate_1 = (1 / usd_to_krw) * usd_to_target
    return rate_1 * 1000  # 1000 KRW


# =========================
#  STREAMLIT PAGE SETUP
# =========================
st.set_page_config(page_title="여행 도우미", page_icon="🌏")
st.title("🌏 나만의 여행 도우미")


# =========================
#       TABS
# =========================
tab1, tab2 = st.tabs(["📍 여행 정보", "🤖 질문하기"])


# ============================================
#       TAB 1 — DU LỊCH DÙNG DỮ LIỆU THỦ CÔNG
# ============================================
with tab1:
    st.subheader("원하는 나라를 입력하세요:")
    country = st.text_input("예: 한국, 일본, 미국, 프랑스, 태국 ...")

    if country:
        if country in DEST_DATA:
            data = DEST_DATA[country]

            st.success(f"🌍 여행 국가: {data['display']}")

            st.write("### ✈ 대표 관광지")
            st.write("- " + "\n- ".join(data["tour"]))

            st.write("### 🍜 유명 음식")
            st.write("- " + "\n- ".join(data["food"]))

            st.write("### 🏨 추천 호텔")
            st.write("- " + "\n- ".join(data["hotel"]))

            st.write("### 🌤 날씨")
            st.write(data["weather"])

            # ⭐⭐ HIỆN TỶ GIÁ 1000 KRW ⭐⭐
            currency_code = data["currency_code"]
            rate = convert_1000_krw(currency_code)

            st.write("### 💱 환율 (1000 KRW 기준)")
            if rate:
                st.success(f"1000 KRW = **{rate:,.2f} {currency_code}**")
            else:
                st.warning("환율 정보를 불러올 수 없습니다.")

        else:
            st.warning("⚠ 아직 준비되지 않은 지역입니다.")


# ============================================
#       TAB 2 —  HỎI ĐÁP GPT
# ============================================
with tab2:
    st.subheader("궁금한 여행 질문을 적어보세요!")
    question = st.text_input("예: 일본 5일 여행 일정 추천해줘")

    if question:
        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
