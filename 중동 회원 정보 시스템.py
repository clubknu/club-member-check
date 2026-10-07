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

# 4. 공통 커스텀 UI 및 텍스트/버튼 크기 CSS
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
    
    /* 입력창 라벨(학번, 이름/성명) 크기 확대 */
    [data-testid="stWidgetLabel"] label, 
    [data-testid="stWidgetLabel"] p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important; /* 글자 크기 상향 */
    }

    /* 메인 타이틀 영역 (크기 2배 확대 & 위로 끌어올림) */
    .main-header {
        text-align: center;
        padding: 0.5rem 0 1rem 0; /* 위쪽 여백 축소로 위로 올림 */
        margin-top: -1.5rem;
    }
    .main-header h1 {
        color: #0f172a !important;
        font-size: 3.8rem !important; /* 약 2배 확대 (기존 2.2rem) */
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .main-header p {
        color: #334155 !important;
        font-size: 1.25rem !important; /* 부제목 크기 확대 */
        font-weight: 600;
    }
    
    /* 버튼 스타일 (너비 및 폰트 확대) */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        padding: 0.85rem 2rem;
        font-size: 1.25rem !important; /* 버튼 글자 크기 증가 */
        font-weight: 700;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
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
        padding: 0.4rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
    }
    .badge-error {
        display: inline-block;
        background-color: #dc2626;
        color: white;
        padding: 0.4rem 1.2rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
    }
    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .result-desc {
        color: #475569;
        font-size: 1.05rem;
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


# 6. 헤더 영역 (크기와 위치가 조정된 메인 제목)
st.markdown(
    """
<div class="main-header">
    <h1>🎓 중앙동아리 회원 조회</h1>
    <p>학번과 이름을 입력하여 중앙동아리 회원 인증을 하세요.</p>
</div>
""",
    unsafe_allow_html=True,
)

# 7. 메인 조회 폼
df, error_msg = load_data()

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
            f"⚠️ 엑셀 파일에 '학번' 및 '성명'(또는 '이름') 열이 포함되어 있어야 합니다. (현재 열 목록: {list(df.columns)})"
        )
    else:
        # 입력 영역
        student_id = st.text_input(
            "학번", placeholder="예: 202412345", key="id_input"
        )
        name = st.text_input("이름 / 성명", placeholder="예: 홍길동", key="name_input")

        # 버튼을 중앙 정렬하고 좌우로 2배 넓히기 위한 컬럼 배치
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_btn = st.button("인증하기")

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
                        <div class="result-desc">2026학년도 2학기 중앙동아리 <b>회원</b>으로 등록되어 있습니다.</div>
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
                        <div class="result-desc">입력하신 학번(<b>{student_id.strip()}</b>)과 이름(<b>{name.strip()}</b>)을 다시 확인해 주세요.</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
