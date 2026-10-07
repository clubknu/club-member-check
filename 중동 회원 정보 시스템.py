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
        background-size: 750px !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: #ffffff !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }}
    </style>
    """
else:
    bg_css = """
    <style>
    html, body, .stApp {
        background-color: #ffffff !important;
    }
    [data-testid="stMain"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }
    </style>
    """

st.markdown(bg_css, unsafe_allow_html=True)

# 4. UI 스타일 및 간격 균일화 CSS
st.markdown(
    """
<style>
    /* 불필요한 Streamlit 헤더/푸터 숨김 */
    [data-testid="stHeader"], #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* 입력창 클릭 시 우측 하단 "Press Enter to submit form" 박스 제거 */
    [data-testid="InputInstructions"], 
    div[data-testid="InputInstructions"],
    small[data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* 중앙 배치 컨테이너 크기 및 마진 설정 */
    .main .block-container {
        max-width: 480px !important;
        width: 100% !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    /* 반투명 팝업 카드 설정 */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(2px) !important;
        border-radius: 24px !important;
        padding: 2.5rem 2.2rem 2.2rem 2.2rem !important;
        
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18), 0 2px 6px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
    }

    /* 타이틀 디자인 */
    .popup-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #000000 !important;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    /* 입력창 배경 하얀색 & 검은색 글자 적용 */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"],
    div[data-testid="stTextInput"] > div > div {
        background-color: #ffffff !important;
        border-radius: 6px !important;
        border: 1px solid #8e8e8e !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-testid="stTextInput"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-size: 1.05rem !important;
        padding: 10px 12px !important;
        text-align: center !important;
        -webkit-text-fill-color: #000000 !important;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #555555 !important;
        opacity: 0.8 !important;
        text-align: center !important;
        -webkit-text-fill-color: #555555 !important;
    }

    /* 📌 컬럼 및 버튼 영역 상단 여백 최소화 */
    [data-testid="stHorizontalBlock"] {
        margin-top: 0.8rem !important;
    }

    div[data-testid="stFormSubmitButton"] {
        margin-top: 0px !important;
    }

    /* 파란색 조회하기 버튼 커스텀 스타일링 */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #007bff !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.65rem 0 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        text-align: center !important;
        cursor: pointer !important;
        width: 100% !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #0056b3 !important;
        color: #ffffff !important;
    }

    /* 📌 결과 및 경고 메시지 상단 간격 축소 (버튼과의 간격을 동일하게 조정) */
    .result-box {
        text-align: center !important;
        margin-top: 0.9rem !important;
        font-size: 1.2rem;
        font-weight: 700;
        color: #000000 !important;
        line-height: 1.4;
        width: 100% !important;
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


# 6. st.form을 활용한 팝업 카드 렌더링
df, error_msg = load_data()

with st.form("student_search_form", clear_on_submit=False):
    # 타이틀
    st.markdown(
        '<div class="popup-title">중앙동아리 회원 정보 조회</div>', unsafe_allow_html=True
    )

    if error_msg:
        st.error(f"⚠️ {error_msg}")
        _, btn_col, _ = st.columns([1, 1.2, 1])
        with btn_col:
            search_btn = st.form_submit_button("조회하기", use_container_width=True)
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
            _, btn_col, _ = st.columns([1, 1.2, 1])
            with btn_col:
                search_btn = st.form_submit_button("조회하기", use_container_width=True)
        else:
            # 1. 이름 입력 (상단)
            name = st.text_input(
                "이름", placeholder="이름 입력", label_visibility="collapsed"
            )
            # 2. 학번 입력 (하단)
            student_id = st.text_input(
                "학번", placeholder="학번 입력", label_visibility="collapsed"
            )

            # 3. 중앙 정렬 버튼 배치
            _, btn_col, _ = st.columns([1, 1.2, 1])
            with btn_col:
                search_btn = st.form_submit_button("조회하기", use_container_width=True)

            # 조회 로직 및 결과 출력
            if search_btn:
                # 입력값이 비어있을 때
                if not student_id.strip() or not name.strip():
                    st.markdown(
                        """
                        <div class="result-box">
                            학번과 이름을 모두 입력해 주세요.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    match = df[
                        (df[id_column].astype(str).str.strip() == student_id.strip())
                        & (df[name_column].astype(str).str.strip() == name.strip())
                    ]

                    if not match.empty:
                        st.markdown(
                            f"""
                        <div class="result-box">
                            {name.strip()}님은 중앙동아리 회원입니다.
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                        <div class="result-box" style="color: #d32f2f !important;">
                            {name.strip()}님은 중앙동아리 회원이 아닙니다.
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
