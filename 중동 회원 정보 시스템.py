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

    # 전체 페이지 기본 배경을 흰색(#ffffff)으로 고정하고, 이미지 영역 설정
    bg_css = f"""
    <style>
    /* 전체 배경(양옆 검은색 부분 포함)을 흰색으로 고정 */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #ffffff !important;
    }}
    
    .stApp {{
        background-image: url("data:{mime_type};base64,{bg_img_base64}");
        background-size: contain; /* 이미지 비율에 맞춰 잘리지 않게 표시 */
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
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

# 4. 공통 커스텀 UI 및 텍스트 색상 CSS
st.markdown(
    """
<style>
    /* 상단 헤더 투명화 및 UI 구성요소 정리 */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 전체 폰트 및 라벨/텍스트 기본 색상을 진한 검은색으로 고정 */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 입력창 라벨(학번, 이름/성명) 글씨색을 진한 검은색(#0f172a)으로 변경 */
    [data-testid="stWidgetLabel"] label, 
    [data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* 메인 타이틀 영역 */
    .main-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    .main-header h1 {
        color: #0f172a !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .main-header p {
        color: #334155 !important;
        font-size: 1.05rem;
        font-weight: 600;
    }
    
    /* 카드 컨테이너 스타일 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(203, 213, 225, 0.8) !important;
        margin-bottom: 1.5rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }
    
    /* 결과 카드 스타일 */
    .result-card-success {
        background-color: rgba(240, 253, 244, 0.95);
        border: 1.5px solid #bbf7d0;
        border-radius: 14px;
        padding: 1.75rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-card-error {
        background-color: rgba(254, 242, 242, 0.95);
        border: 1.5px solid #fecaca;
        border-radius: 14px;
        padding: 1.75rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .badge-success {
        display: inline-block;
        background-color: #16a34a;
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.75rem;
    }
    .badge-error {
        display: inline-block;
        background-color: #dc2626;
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.75rem;
    }
    .result-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .result-desc {
        color: #475569;
        font-size: 0.95rem;
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


# 6. 헤더 영역
st.markdown(
    """
<div class="main-header">
    <h1>🎓 중앙동아리 회원 조회</h1>
    <p>학번과 이름을 입력
