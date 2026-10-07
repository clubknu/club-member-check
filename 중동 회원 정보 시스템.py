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


# 3. bg.png 파일 경로 및 CSS 구성
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
        background-color: transparent !important;
    }}
    [data-testid="stVerticalBlock"] {{
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

# 4. 반투명 팝업 카드 및 UI CSS
st.markdown(
    """
<style>
    /* 상단 헤더 및 필요없는 UI 가리기 */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 전체 폰트 설정 */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* 반투명 팝업 카드 메인 상자 스타일 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.90) !important; /* 반투명 흰색 (0.90) */
        backdrop-filter: blur(12px) !important;            /* 뒤 배경 흐림 블러 효과 */
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 24px !important;                     /* 둥근 모서리 */
        padding: 2.5rem 2rem !important;                    /* 내부 여백 */
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15), 0 1px 3px rgba(0,0,0,0.05) !important; /* 은은한 팝업 그림자 */
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        margin-top: 2rem !important;
    }
    
    /* 입력창 라벨 크기 및 폰트 */
    [data-testid="stWidgetLabel"] label, 
    [data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
    }

    /* 입력창 스타일 커스텀 */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }

    /* 팝업 내부 타이틀 스타일 */
    .popup-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .popup-header h1 {
        color: #0f172a !important;
        font-size: 2.2rem !important;
        font-weight: 800;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }
    .popup-header p {
        color: #475569 !important;
        font-size: 1.05rem !important;
        font-weight: 600;
        margin: 0;
    }
    
    /* 버튼 스타일 (카드 전체 너비 맞춤 및 선명한 파란색) */
    div.stButton > button {
        width: 100% !important;
        background: #007bff !important; /* 선명한 블루 */
        color: white !important;
        border: none;
        padding: 0.85rem 1.5rem;
        font-size: 1.2rem !important;
        font-weight: 700;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        transition: all 0.2s ease;
        margin-top: 0.5rem;
    }
    div.stButton > button:hover {
        background: #0056b3 !important;
        box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
        transform: translateY(-1px);
    }
    
    /* 결과 영역 스타일 */
    .result-card-success {
        background-color: rgba(240, 253, 244, 0.9);
        border: 1.5px solid #bbf7d0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-card-error {
        background-color: rgba(254, 242, 242, 0.9);
        border: 1.5px solid #fecaca;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .badge-success {
        display: inline-block;
        background-color: #16a34a;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .badge-error {
        display: inline-block;
        background-color: #dc2626;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .result-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .result-desc {
        color: #334155;
        font-size: 1rem;
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


# 6. 메인 조회 팝업 카드로 전체 폼 감싸기
df, error_msg = load_data()

with st.container(border=True):
    # 팝업 내 타이틀 영역
    st.markdown(
        """
    <div class="popup-header">
        <h1>🎓 학생 정보 조회</h1>
        <p>학번과 이름을 입력하여 중앙동아리 회원을 조회하세요.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if error_msg:
        st.error(f"⚠️ 데이터 로드 실패: {error_msg}")
    else:
        name_column = None
        if "성명" in df.columns:
            name_column = "성명"
        elif "이름" in df.columns:
            name_column = "이름"

        id_column = "학번" if "학번" in df.columns else None

        if not name_column or not id_column:
            st.error(
                f"⚠️ 엑셀 파일에 '학번' 및 '성명'(또는 '이름') 열이 포함되어 있어야 합니다."
            )
        else:
            # 입력란
            student_id = st.text_input(
                "학번", placeholder="학번 입력", key="id_input"
            )
            name = st.text_input("이름", placeholder="이름 입력", key="name_input")

            # 조회 버튼
            search_btn = st.button("조회하기")

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
                        <div class="result-card-success">
                            <span class="badge-success">✓ 인증 완료</span>
                            <div class="result-title">{name.strip()} ({student_id.strip()}) 님</div>
                            <div class="result-desc">중앙동아리 <b>회원</b>입니다.</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                        <div class="result-card-error">
                            <span class="badge-error">✕ 조회 불가</span>
                            <div class="result-title">중앙동아리 회원이 아닙니다</div>
                            <div class="result-desc">입력하신 정보를 다시 확인해 주세요.</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
