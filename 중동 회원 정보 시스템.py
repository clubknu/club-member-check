import base64
import mimetypes
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정 (가장 상단에 위치해야 합니다)
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
bg_image_path = os.path.join(BASE_DIR, "bg.png")  # bg.png 로 변경

if os.path.exists(bg_image_path):
    bg_img_base64 = get_base64_of_bin_file(bg_image_path)
    mime_type, _ = mimetypes.guess_type(bg_image_path)
    mime_type = mime_type or "image/png"

    # 이미지 배경 스타일
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:{mime_type};base64,{bg_img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* 내부 컨테이너 투명화 */
    [data-testid="stAppViewContainer"] {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}
    </style>
    """
else:
    # bg.png 파일이 없을 때 적용될 기본 단색 배경
    bg_css = """
    <style>
    .stApp {
        background-color: #f0f6ff;
    }
    </style>
    """

# 배경 스타일 적용
st.markdown(bg_css, unsafe_allow_html=True)

# 4. 공통 커스텀 UI CSS
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
    
    /* 전체 폰트 설정 */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 메인 타이틀 영역 */
    .main-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
    }
    .main-header h1 {
        color: #1e293b;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .main-header p {
        color: #64748b;
        font-size: 1.05rem;
    }
    
    /* 카드 컨테이너 스타일 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.92); /* 배경 이미지가 살짝 비치도록 약간의 투명도 부여 */
        backdrop-filter: blur(10px); /* 글래스모피즘 효과 */
        padding: 1.5rem;
        border-radius: 16px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        margin-bottom: 1.5rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
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
        with st.container(border=True):
            student_id = st.text_input(
                "학번", placeholder="예: 202412345", key="id_input"
            )
            name = st.text_input(
                "이름 / 성명", placeholder="예: 홍길동", key="name_input"
            )
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
