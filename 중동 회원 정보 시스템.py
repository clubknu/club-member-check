import base64
import mimetypes
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="중앙동아리 회원 정보 조회",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 2. 로컬 이미지를 base64로 변환하는 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# 3. bg.png 파일 경로 및 배경 CSS 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(BASE_DIR, "bg.png")

if os.path.exists(bg_image_path):
    bg_img_base64 = get_base64_of_bin_file(bg_image_path)
    mime_type, _ = mimetypes.guess_type(bg_image_path)
    mime_type = mime_type or "image/png"

    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
    }}
    [data-testid="stMain"] {{
        background-image: url("data:{mime_type};base64,{bg_img_base64}") !important;
        background-size: 700px !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: transparent !important;
    }}
    </style>
    """
else:
    bg_css = """
    <style>
    html, body, .stApp {
        background-color: #ffffff !important;
    }
    </style>
    """

st.markdown(bg_css, unsafe_allow_html=True)

# 4. 반투명 팝업 카드를 위한 스타일 정의
st.markdown(
    """
<style>
    /* 상단 헤더 및 불필요한 UI 숨김 */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* 메인 폼 컨테이너 너비 및 중앙 정렬 */
    .block-container {
        max-width: 480px !important;
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }

    /* 반투명 카드 스타일 */
    .popup-box {
        background: rgba(255, 255, 255, 0.92);  /* 반투명 흰색 배경 */
        backdrop-filter: blur(10px);             /* 배경 블러 처리 */
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;                     /* 모서리 둥글게 */
        padding: 30px 28px 35px 28px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2), 0 3px 10px rgba(0,0,0,0.05); /* 은은한 그림자 */
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 20px;
    }

    /* 타이틀 디자인 */
    .popup-header {
        text-align: center;
        margin-bottom: 25px;
    }
    .popup-header h2 {
        color: #000000 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.5px;
    }

    /* Streamlit 입력창 라벨/텍스트 박스 커스텀 */
    div[data-baseweb="input"] {
        border-radius: 8px !important;
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #007bff !important;
    }

    /* 버튼 스타일 (파란색 전체 너비 버튼) */
    div.stButton > button {
        width: 100% !important;
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        padding: 12px 0px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #0056b3 !important;
        box-shadow: 0 6px 14px rgba(0, 123, 255, 0.4) !important;
    }

    /* 결과 텍스트 스타일 */
    .result-text {
        text-align: center;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 20px;
        color: #111827;
        line-height: 1.5;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 5. 데이터 로드 함수
@st.cache_data
def load_data():
    excel_path = os.path.join(BASE_DIR, "members.xlsx")

    if not os.path.exists(excel_path):
        return None, "members.xlsx 파일을 찾을 수 없습니다."

    try:
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.strip()
        return df, None
    except Exception as e:
        return None, str(e)


# 6. 반투명 팝업 네모 상자 시작 (<div class="popup-box">)
st.markdown(
    """
<div class="popup-box">
    <div class="popup-header">
        <h2>학생 정보 조회</h2>
    </div>
""",
    unsafe_allow_html=True,
)

# 데이터 로드
df, error_msg = load_data()

if error_msg:
    st.error(f"⚠️ {error_msg}")
else:
    name_column = None
    if "성명" in df.columns:
        name_column = "성명"
    elif "이름" in df.columns:
        name_column = "이름"

    id_column = "학번" if "학번" in df.columns else None

    if not name_column or not id_column:
        st.error(
            "⚠️ 엑셀 파일에 '학번' 및 '성명'(또는 '이름') 열이 포함되어 있어야 합니다."
        )
    else:
        # 입력 필드
        student_id = st.text_input(
            "학번", placeholder="학번 입력", label_visibility="collapsed"
        )
        name = st.text_input(
            "이름", placeholder="이름 입력", label_visibility="collapsed"
        )

        # 조회하기 버튼
        search_btn = st.button("조회하기")

        # 결과 출력
        if search_btn:
            if not student_id.strip() or not name.strip():
                st.warning("학번과 이름을 모두 입력해 주세요.")
            else:
                match = df[
                    (df[id_column].astype(str).str.strip() == student_id.strip())
                    & (df[name_column].astype(str).str.strip() == name.strip())
                ]

                if not match.empty:
                    st.markdown(
                        f"""
                    <div class="result-text">
                        <b>{name.strip()}</b>님은 중앙동아리회원입니다.<br>
                        결과: <b>중앙동아리회원</b>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div class="result-text" style="color: #dc2626;">
                        <b>{name.strip()}</b>님은 회원 목록에 존재하지 않습니다.<br>
                        결과: <b>비회원</b>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

# 반투명 팝업 네모 상자 닫기 (</div>)
st.markdown("</div>", unsafe_allow_html=True)
