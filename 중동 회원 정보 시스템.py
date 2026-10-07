import base64
import mimetypes
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="학생 정보 조회",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 2. 로컬 이미지를 base64로 변환하는 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# 3. bg.png 배경 이미지 설정
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
        background-size: 680px !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: #ffffff !important;
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

# 4. 카드 팝업 및 컴포넌트 커스텀 CSS
st.markdown(
    """
<style>
    /* 불필요한 Streamlit 헤더/푸터 숨김 */
    [data-testid="stHeader"], #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* 중앙 배치 영역 너비 조정 및 여백 */
    .main .block-container {
        max-width: 480px !important;
        padding-top: 5rem !important;
        padding-bottom: 3rem !important;
    }

    /* 폼(st.form) 자체를 반투명 카드 팝업으로 변경 */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.4) !important; /* 반투명 흰색 */
        backdrop-filter: blur(0px) !important;            /* 뒤 배경 흐림 효과 */
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;                     /* 모서리 둥글게 */
        padding: 2.2rem 2rem 2rem 2rem !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important; /* 은은한 팝업 그림자 */
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
    }

    /* 타이틀 스타일 */
    .popup-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        color: #000000;
        margin-bottom: 1.8rem;
        letter-spacing: -0.5px;
    }

    /* 입력창 디자인 (흰색 배경 + 깔끔한 테두리) */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
        border: 1px solid #767676 !important;
    }
    div[data-baseweb="input"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="input"] input::placeholder {
        color: #757575 !important;
    }

    /* 버튼 디자인 (첫 번째 첨부 사진과 동일한 원색 파란색 & 꽉 찬 너비) */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #007bff !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 0 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        margin-top: 0.5rem !important;
        box-shadow: none !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #0056b3 !important;
        color: #ffffff !important;
    }

    /* 결과 텍스트 스타일 */
    .result-box {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 1.15rem;
        color: #000000;
        line-height: 1.6;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 5. 엑셀 데이터 로드 함수
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


# 6. st.form을 사용하여 타이틀, 입력창, 버튼을 하나의 반투명 팝업 카드로 결합
df, error_msg = load_data()

with st.form("student_search_form", clear_on_submit=False):
    # 타이틀
    st.markdown(
        '<div class="popup-title">학생 정보 조회</div>', unsafe_allow_html=True
    )

    if error_msg:
        st.error(f"⚠️ {error_msg}")
        search_btn = st.form_submit_button("조회하기")
    else:
        name_column = None
        if "성명" in df.columns:
            name_column = "성명"
        elif "이름" in df.columns:
            name_column = "이름"

        id_column = "학번" if "학번" in df.columns else None

        if not name_column or not id_column:
            st.error(
                "⚠️ 엑셀 파일에 '학번' 및 '성명'(또는 '이름') 열이 필요합니다."
            )
            search_btn = st.form_submit_button("조회하기")
        else:
            # 입력창 (라벨 숨기고 placeholder 지정)
            student_id = st.text_input(
                "학번", placeholder="학번 입력", label_visibility="collapsed"
            )
            name = st.text_input(
                "이름", placeholder="이름 입력", label_visibility="collapsed"
            )

            # 조회하기 버튼
            search_btn = st.form_submit_button("조회하기")

            # 조회 로직 및 결과 출력 (팝업 카드 내부 하단에 출력)
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
                        <div class="result-box">
                            <b>{name.strip()}</b>님은 중앙동아리회원입니다. 결과: <b>중앙동아리회원</b>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                        <div class="result-box" style="color: #d32f2f;">
                            <b>{name.strip()}</b>님은 회원 목록에 존재하지 않습니다. 결과: <b>비회원</b>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
