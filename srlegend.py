import streamlit as st
import streamlit.components.v1 as components
import json
import random
import time
from gemini_utils import analyze_experience, DEMO_MODE

# 페이지 기본 설정
st.set_page_config(
    page_title="편견 테스트 | 일상 속 시선 체험",
    page_icon="🌱",
    layout="centered"
)

# [고대비 & 선명한 폰트 색상] 다크/라이트 모드 상관없이 100% 뚜렷하게 보이는 CSS
st.markdown("""
<style>
    /* 🌟 애니메이션 정의 */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-18px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(225, 29, 72, 0); }
        100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }

    /* 전체 배경과 기본 본문 글자색 */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif;
    }

    /* 메인 카드 (선명한 흰색 배경과 진한 텍스트) */
    .scenario-card {
        background: #ffffff !important;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        border: 2px solid #cbd5e1;
        margin-bottom: 20px;
        animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        color: #0f172a !important;
    }

    /* NPC 말풍선 (선명한 다크 네이비 배경과 흰 글씨로 대비 극대화) */
    .npc-bubble {
        background: #1e293b !important;
        border-left: 6px solid #38bdf8;
        padding: 18px 20px;
        border-radius: 4px 16px 16px 4px;
        font-size: 1.1rem;
        font-weight: 600;
        color: #f8fafc !important;
        margin: 16px 0;
        animation: slideInLeft 0.5s ease-out forwards;
        line-height: 1.6;
    }
    .npc-bubble b, .npc-bubble span {
        color: #38bdf8 !important;
    }

    /* 속마음 독백 박스 (진한 와인색 텍스트와 뚜렷한 배경) */
    .inner-monologue {
        background: #fff1f2 !important;
        border-radius: 14px;
        padding: 18px 22px;
        color: #881337 !important;
        font-size: 1.02rem;
        font-weight: 600;
        margin-top: 16px;
        border: 2px dashed #f43f5e;
        animation: fadeInUp 0.5s ease-out forwards, pulseGlow 2.5s infinite;
        line-height: 1.6;
    }
    .inner-monologue b {
        color: #be123c !important;
    }

    /* 사이다 클라이맥스 배너 */
    .climax-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        color: #ffffff !important;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        font-size: 1.22rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.3);
        animation: fadeInUp 0.4s ease-out forwards;
        border: 2px solid #6366f1;
    }

    /* 아바타 프로필 뱃지 */
    .avatar-badge {
        display: inline-block;
        background: #0284c7 !important;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    /* 버튼 기본 스타일: 글자 짤림 방지 및 모바일 줄바꿈 최적화 */
    div.stButton > button {
        border-radius: 12px !important;
        font-size: 1.02rem !important;
        font-weight: 700 !important;
        padding: 12px 18px !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 2px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        white-space: normal !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
        height: auto !important;
        min-height: 48px !important;
        line-height: 1.5 !important;
    }
    div.stButton > button div,
    div.stButton > button p,
    div.stButton > button span {
        color: #0f172a !important;
        white-space: normal !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
        line-height: 1.5 !important;
    }

    /* 🔥 마우스 호버(Hover) 시: 배경을 블루(#0284c7)로 채우고 글자를 순백색(#ffffff)으로 반전시켜 선명하게 표시 */
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.28) !important;
    }
    div.stButton > button:hover p,
    div.stButton > button:hover span,
    div.stButton > button:hover div {
        color: #ffffff !important;
    }

    /* 클릭 시(Active) */
    div.stButton > button:active {
        background-color: #0369a1 !important;
        border-color: #0369a1 !important;
        color: #ffffff !important;
        transform: translateY(0) !important;
    }
    div.stButton > button:active p,
    div.stButton > button:active span {
        color: #ffffff !important;
    }

    /* 비활성화 버튼 (정원 초과 등) */
    div.stButton > button:disabled {
        background-color: #f1f5f9 !important;
        border-color: #e2e8f0 !important;
        color: #94a3b8 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    div.stButton > button:disabled p,
    div.stButton > button:disabled span {
        color: #94a3b8 !important;
    }

    /* Primary 버튼 (체험 시작 등 강조 버튼) */
    div.stButton > button[kind="primary"] {
        background: #0284c7 !important;
        border: 2px solid #0284c7 !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #0369a1 !important;
        border-color: #0369a1 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(3, 105, 161, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover p,
    div.stButton > button[kind="primary"]:hover span {
        color: #ffffff !important;
    }

    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 1rem;
        color: #0f172a !important;
    }

    /* ⏱️ 5초 딜레마 타이머 바 애니메이션 */
    @keyframes dilemmaCountdown {
        0% { width: 100%; background: #0284c7; }
        50% { width: 50%; background: #f59e0b; }
        100% { width: 0%; background: #ef4444; }
    }
    .timer-container {
        width: 100%;
        background-color: #e2e8f0;
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
        margin: 8px 0 16px 0;
    }
    .timer-bar {
        height: 100%;
        animation: dilemmaCountdown 5s linear forwards;
        border-radius: 999px;
    }

    /* 🎮 듀얼 게이지 (멘탈/스트레스 & 사이다) */
    .gauge-card {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        animation: fadeInUp 0.3s ease-out forwards;
    }
    .gauge-bar-bg {
        background: #f1f5f9;
        border-radius: 8px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
    }
    .gauge-fill-fire {
        height: 100%;
        background: linear-gradient(90deg, #fb923c, #ef4444);
        transition: width 0.4s ease;
        border-radius: 8px;
    }
    .gauge-fill-lightning {
        height: 100%;
        background: linear-gradient(90deg, #38bdf8, #6366f1);
        transition: width 0.4s ease;
        border-radius: 8px;
    }

    /* 🏆 BTI 결과 인증서 카드 */
    .bti-certificate {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 3px double #0284c7;
        border-radius: 20px;
        padding: 28px 24px;
        text-align: center;
        box-shadow: 0 12px 32px rgba(2, 132, 199, 0.12);
        margin: 20px 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .bti-title {
        font-size: 1.65rem;
        font-weight: 900;
        color: #0f172a;
        margin: 12px 0 8px 0;
    }
    .bti-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0284c7, #2563eb);
        color: #ffffff !important;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
    }
    .bti-tag {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1 !important;
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 4px 3px;
    }

    /* 🛠️ 개발자용 건너뛰기 & 📱 모바일 QR 생성 expander & popover: 기본 흰색 글씨, 호버 시 노란색(#facc15) */
    button[data-dev-skip="true"],
    .dev-skip-custom,
    div[data-testid="stExpander"] div.stButton > button,
    div[data-testid="stPopover"] > button,
    div[data-testid="stExpander"] {
        background-color: #1e293b !important;
        border: 2px solid #475569 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[data-dev-skip="true"] p,
    button[data-dev-skip="true"] span,
    button[data-dev-skip="true"] div,
    .dev-skip-custom p,
    .dev-skip-custom span,
    .dev-skip-custom div,
    div[data-testid="stExpander"] div.stButton > button p,
    div[data-testid="stExpander"] div.stButton > button span,
    div[data-testid="stExpander"] div.stButton > button div,
    div[data-testid="stPopover"] > button p,
    div[data-testid="stPopover"] > button span,
    div[data-testid="stPopover"] > button div,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span {
        color: #ffffff !important;
        font-weight: 700 !important;
        transition: color 0.2s ease !important;
    }
    div[data-testid="stExpander"] summary svg {
        fill: #ffffff !important;
        color: #ffffff !important;
        transition: all 0.2s ease !important;
    }

    /* 마우스 호버(Hover) 시: 선명한 노란색(#facc15)으로 글자색과 테두리 반전 */
    button[data-dev-skip="true"]:hover,
    .dev-skip-custom:hover,
    div[data-testid="stExpander"] div.stButton > button:hover,
    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stExpander"]:hover,
    div[data-testid="stExpander"] summary:hover {
        background-color: #0f172a !important;
        border-color: #facc15 !important;
        color: #facc15 !important;
        box-shadow: 0 4px 16px rgba(250, 204, 21, 0.35) !important;
    }
    button[data-dev-skip="true"]:hover p,
    button[data-dev-skip="true"]:hover span,
    button[data-dev-skip="true"]:hover div,
    .dev-skip-custom:hover p,
    .dev-skip-custom:hover span,
    .dev-skip-custom:hover div,
    div[data-testid="stExpander"] div.stButton > button:hover p,
    div[data-testid="stExpander"] div.stButton > button:hover span,
    div[data-testid="stExpander"] div.stButton > button:hover div,
    div[data-testid="stPopover"] > button:hover p,
    div[data-testid="stPopover"] > button:hover span,
    div[data-testid="stPopover"] > button:hover div,
    div[data-testid="stExpander"] summary:hover p,
    div[data-testid="stExpander"] summary:hover span,
    div[data-testid="stExpander"]:hover summary p,
    div[data-testid="stExpander"]:hover summary span {
        color: #facc15 !important;
    }
    div[data-testid="stExpander"] summary:hover svg,
    div[data-testid="stExpander"]:hover summary svg {
        fill: #facc15 !important;
        color: #facc15 !important;
    }

    /* Expander 내부 레이블 및 캡션 글씨 색상 */
    div[data-testid="stExpander"] label p,
    div[data-testid="stExpander"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] .stCaption,
    div[data-testid="stExpander"] [data-testid="stCaptionContainer"] p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }

    /* 📱💻 기기 선택 카드 hover: 노란 테두리 */
    .device-card {
        background: #ffffff;
        border: 3px solid #cbd5e1;
        border-radius: 18px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
        margin-bottom: 12px;
        transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
        cursor: pointer;
    }
    .device-card:hover {
        border-color: #facc15 !important;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(250, 204, 21, 0.35);
    }
    .device-card:hover h3 {
        color: #ca8a04 !important;
    }
</style>
""", unsafe_allow_html=True)

# 시나리오 데이터 로드
@st.cache_data
def load_data():
    with open("data/scenarios.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# 🏆 BTI 성향 프로필 계산 함수
def get_bti_profile(patience_count, action_count):
    total = patience_count + action_count
    action_pct = int((action_count / total) * 100) if total > 0 else 50
    patience_pct = 100 - action_pct

    if action_count >= 8:
        return {
            "title": "🌶️ 마라맛 사이다 전사",
            "badge": "전국 사이다 협회 특등급 회원",
            "tags": ["#할말은_한다", "#부당함_철벽방어", "#정의구현_사이다", "#단호한_직진"],
            "desc": "어떤 편견과 무례한 시선 앞에서도 기죽지 않고, 자신의 권리와 존엄을 똑 부러지게 지켜내는 당찬 직진형 해결사입니다!",
            "action_pct": action_pct,
            "patience_pct": patience_pct
        }
    elif action_count > patience_count:
        return {
            "title": "⚡ 눈치 100단 스마트 팩트폭격기",
            "badge": "이성적 논리 방어사",
            "tags": ["#차분한_일침", "#논리정연", "#선넘으면_경고", "#전략적_대응"],
            "desc": "감정에 휘둘리기보다 핵심을 정확히 짚어내며, 상대방의 편견 어린 논리를 조용히 무너뜨리는 지혜로운 현실 전략가입니다!",
            "action_pct": action_pct,
            "patience_pct": patience_pct
        }
    elif patience_count >= 8:
        return {
            "title": "🧘 생불(生佛)급 해탈의 인내 보살",
            "badge": "인내심 올림픽 금메달리스트",
            "tags": ["#보살의_경지", "#속앓이_마스터", "#평화주의", "#안전제일"],
            "desc": "어떤 억울한 편견 속에서도 스스로를 다스리며 갈등을 원만히 피해 가는, 바다처럼 넓은 마음을 가진 평화주의자입니다!",
            "action_pct": action_pct,
            "patience_pct": patience_pct
        }
    elif patience_count > action_count:
        return {
            "title": "🛡️ 조용한 품격의 외유내강 수호자",
            "badge": "남모를 배려의 달인",
            "tags": ["#묵묵한_인내", "#마음속_내공", "#성숙한_어른", "#상황_배려"],
            "desc": "불필요한 마찰을 줄이기 위해 한 발 물러서면서도, 속으로는 상황의 부당함을 날카롭게 응시하는 깊은 내공의 소유자입니다!",
            "action_pct": action_pct,
            "patience_pct": patience_pct
        }
    else:
        return {
            "title": "⚖️ 밀당의 달인 황금 밸런서",
            "badge": "사회생활 만렙 전략가",
            "tags": ["#유연한_대처", "#황금_밸런스", "#상황판단력_갑", "#융통성_만렙"],
            "desc": "참아야 할 순간과 목소리를 내야 할 타이밍을 기가 막히게 조율하는, 유연하고 노련한 균형 감각의 대가입니다!",
            "action_pct": action_pct,
            "patience_pct": patience_pct
        }

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "DEVICE_SELECT"
if "selected_avatar_ids" not in st.session_state:
    st.session_state.selected_avatar_ids = set()
if "selected_avatars" not in st.session_state:
    st.session_state.selected_avatars = []
if "current_avatar_idx" not in st.session_state:
    st.session_state.current_avatar_idx = 0
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "show_step_result" not in st.session_state:
    st.session_state.show_step_result = False
if "last_result" not in st.session_state:
    st.session_state.last_result = {}
if "timer_enabled" not in st.session_state:
    st.session_state.timer_enabled = True
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = DEMO_MODE
if "dev_skip_used" not in st.session_state:
    st.session_state.dev_skip_used = False
if "device_mode" not in st.session_state:
    st.session_state.device_mode = None

# ⚙️ 전역 사이드바 (게임 & 시연 설정 + 개발자 건너뛰기 도구)
with st.sidebar:
    st.subheader("⚙️ 게임 & 시연 설정")
    timer_toggle = st.toggle("⏱️ 20초 딜레마 타이머 모드", value=st.session_state.timer_enabled)
    st.session_state.timer_enabled = timer_toggle
    st.caption("켜두면 질문마다 20초 카운트다운이 진행되며, 시간 초과 시 침묵 속에 상황을 받아들이는 선택으로 자동 진행됩니다.")
    st.divider()
    demo_toggle = st.toggle("발표용 초고속 데모 모드 (Fallback)", value=st.session_state.demo_mode)
    st.caption("체크 시 0.5초 만에 사전 검증된 결과가 표시되며, 체크 해제 시 제공해주신 Gemini API로 실시간 분석합니다.")
    st.session_state.demo_mode = demo_toggle

    st.divider()
    with st.expander("🛠️ 개발자용 건너뛰기 도구", expanded=True):
        st.caption("개발 및 시연 중 질문을 일일이 풀지 않고 원하는 화면으로 즉시 점프합니다.")
        
        # 1. 최종 결과 화면으로 직행
        if st.button("🏁 최종 결과 리포트로 직행", use_container_width=True, type="primary"):
            st.session_state.dev_skip_used = True
            if len(st.session_state.get("selected_avatars", [])) < 3:
                st.session_state.selected_avatars = data["avatars"][:3]
                st.session_state.selected_avatar_ids = {a["id"] for a in st.session_state.selected_avatars}
            if len(st.session_state.get("answers", [])) < 12:
                sample_types = ["참기", "맞서기", "참기", "맞서기", "참기", "맞서기", "맞서기", "참기", "맞서기", "참기", "맞서기", "참기"]
                st.session_state.answers = []
                for idx, c_type in enumerate(sample_types):
                    av = st.session_state.selected_avatars[idx // 4]
                    st.session_state.answers.append({
                        "avatar": av["desc"],
                        "category": c_type,
                        "type": c_type
                    })
            st.session_state.page = "RESULT"
            st.rerun()

        # 2. 엔딩 시네마틱으로 직행
        if st.button("🎬 엔딩 시네마틱 화면으로 직행", use_container_width=True):
            st.session_state.dev_skip_used = True
            st.session_state.page = "CINEMATIC"
            st.rerun()

        # 3. 플레이 화면 중 건너뛰기 옵션들
        if st.session_state.page == "PLAY":
            col_skip1, col_skip2 = st.columns(2)
            with col_skip1:
                if st.button("⏩ 질문 1개 건너뛰기", use_container_width=True):
                    st.session_state.dev_skip_used = True
                    curr_av = st.session_state.selected_avatars[st.session_state.current_avatar_idx]
                    st.session_state.answers.append({
                        "avatar": curr_av["desc"],
                        "category": "맞서기" if st.session_state.current_q_idx % 2 == 0 else "참기",
                        "type": "개발자 건너뛰기"
                    })
                    st.session_state.q_start_time = None
                    if st.session_state.current_q_idx < 4:
                        st.session_state.current_q_idx += 1
                        st.session_state.show_step_result = False
                    else:
                        if st.session_state.current_avatar_idx < 2:
                            st.session_state.current_avatar_idx += 1
                            st.session_state.current_q_idx = 0
                            st.session_state.show_step_result = False
                            st.session_state.page = "AVATAR_INTRO"
                        else:
                            st.session_state.page = "RESULT"
                    st.rerun()
            with col_skip2:
                if st.button("🔥 Q5 클라이맥스로", use_container_width=True):
                    st.session_state.dev_skip_used = True
                    st.session_state.current_q_idx = 4
                    st.session_state.show_step_result = False
                    st.session_state.q_start_time = None
                    st.rerun()

            if st.button("🎭 다음 아바타로 넘어가기", use_container_width=True):
                st.session_state.dev_skip_used = True
                st.session_state.q_start_time = None
                if st.session_state.current_avatar_idx < 2:
                    st.session_state.current_avatar_idx += 1
                    st.session_state.current_q_idx = 0
                    st.session_state.show_step_result = False
                    st.session_state.page = "AVATAR_INTRO"
                else:
                    st.session_state.page = "RESULT"
                st.rerun()

        # 5. 처음으로 리셋
        if st.button("🔄 처음으로 완전 초기화", use_container_width=True):
            st.session_state.device_mode = None
            st.session_state.page = "DEVICE_SELECT"
            st.session_state.selected_avatar_ids = set()
            st.session_state.selected_avatars = []
            st.session_state.current_avatar_idx = 0
            st.session_state.current_q_idx = 0
            st.session_state.answers = []
            st.session_state.show_step_result = False
            st.session_state.last_result = {}
            st.session_state.dev_skip_used = False
            st.rerun()

is_mobile = (st.session_state.get("device_mode") == "MOBILE")

# 📱 모바일 모드 전용 반응형 CSS 주입 (여백 최적화 및 폰트 스케일링)
if is_mobile:
    st.markdown("""
    <style>
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            max-width: 100% !important;
        }
        .scenario-card {
            padding: 16px 14px !important;
            border-radius: 14px !important;
            margin-bottom: 14px !important;
        }
        .npc-bubble {
            padding: 13px 15px !important;
            font-size: 0.98rem !important;
            margin: 12px 0 !important;
            line-height: 1.55 !important;
        }
        .inner-monologue {
            padding: 13px 15px !important;
            font-size: 0.95rem !important;
            margin-top: 12px !important;
            line-height: 1.55 !important;
        }
        .climax-banner {
            font-size: 1.05rem !important;
            padding: 16px 12px !important;
        }
        div.stButton > button {
            font-size: 0.96rem !important;
            padding: 12px 14px !important;
            min-height: 48px !important;
            line-height: 1.45 !important;
        }
        .bti-certificate {
            padding: 20px 14px !important;
            margin: 14px 0 !important;
        }
        .bti-title {
            font-size: 1.35rem !important;
        }
        h1 {
            font-size: 1.7rem !important;
        }
        h2 {
            font-size: 1.35rem !important;
        }
        h3 {
            font-size: 1.15rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 0. 기기 환경(모바일 vs PC) 선택 화면 (처음 시작 시)
if st.session_state.page == "DEVICE_SELECT" or st.session_state.device_mode is None:
    st.markdown("""
    <div style="text-align: center; margin: 15px 0 25px 0;">
        <span style="background: #e0f2fe; color: #0284c7; padding: 6px 18px; border-radius: 20px; font-weight: 800; font-size: 0.95rem;">
            🌱 일상 속 편견 공감 프로젝트
        </span>
        <h1 style="color: #0f172a; font-weight: 900; margin: 14px 0 8px 0; font-size: 2.2rem;">편견 테스트</h1>
        <p style="color: #475569; font-size: 1.08rem; font-weight: 600; line-height: 1.6;">
            접속하신 기기 환경을 선택해 주세요.<br/>
            화면 크기에 맞춰 <b>글자 짤림 없는 최적화 화면</b>을 제공합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_dev_m, col_dev_p = st.columns(2)
    with col_dev_m:
        st.markdown("""
        <div class="device-card">
            <div style="font-size: 3.5rem; margin-bottom: 8px;">📱</div>
            <h3 style="color: #0f172a; font-weight: 800; margin-bottom: 8px;">스마트폰 (모바일)</h3>
            <p style="color: #334155; font-size: 0.93rem; font-weight: 600; line-height: 1.7; margin-bottom: 16px;">
                • <b>글자 짤림 방지</b> 1열 세로 맞춤 배치<br/>
                • 터치하기 편한 넓은 선택지 버튼<br/>
                • 스마트폰 화면에 최적화된 카드 크기
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📱 모바일 모드로 시작하기", use_container_width=True, type="primary", key="btn_choose_mode_mobile"):
            st.session_state.device_mode = "MOBILE"
            st.session_state.page = "INTRO"
            st.rerun()

    with col_dev_p:
        st.markdown("""
        <div class="device-card">
            <div style="font-size: 3.5rem; margin-bottom: 8px;">💻</div>
            <h3 style="color: #0f172a; font-weight: 800; margin-bottom: 8px;">PC / 노트북 / 태블릿</h3>
            <p style="color: #334155; font-size: 0.93rem; font-weight: 600; line-height: 1.7; margin-bottom: 16px;">
                • 넓은 모니터를 위한 2열 와이드 배치<br/>
                • 여유롭고 쾌적한 화면 구성<br/>
                • 마우스 조작에 맞춘 인터페이스
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💻 PC 모드로 시작하기", use_container_width=True, key="btn_choose_mode_pc"):
            st.session_state.device_mode = "PC"
            st.session_state.page = "INTRO"
            st.rerun()

# 1. 인트로 화면
elif st.session_state.page == "INTRO":
    col_intro_title, col_intro_qr = st.columns([3, 1])
    with col_intro_title:
        st.title("🌱 편견 테스트")
        st.caption("일상 속 타인의 시선을 직접 입어보는 공감 프로젝트")
    with col_intro_qr:
        with st.popover("📱 모바일 QR"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=http://172.30.10.158:8501", caption="스마트폰으로 스캔", use_container_width=True)
            st.caption("http://172.30.10.158:8501")
    
    st.markdown("""
    <div class="scenario-card">
        <h3 style="color: #0f172a; margin-top: 0;">당신은 잠시 동안 우리 곁에 실재하는 3명의 이웃이 됩니다.</h3>
        <p style="color: #334155; font-size: 1.05rem; line-height: 1.7; font-weight: 500;">
            우리는 누군가를 차별할 생각이 없더라도 익숙한 편견으로 상처를 주곤 합니다.<br/>
            이곳에는 <b style="color: #0284c7;">정답도, 당신을 평가하는 점수도 없습니다.</b><br/>
            세 사람의 일상 속에 들어가 그들의 호흡과 속마음을 느껴보세요.
        </p>
        <hr style="border: none; border-top: 2px solid #e2e8f0; margin: 18px 0;"/>
        <p style="font-size: 0.9rem; color: #64748b; font-weight: 600;">
            🔒 개인정보와 선택 기록은 서버에 절대 저장되지 않으며 세션 종료 시 파기됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("👥 체험할 아바타 3명을 직접 선택해 주세요")
    st.caption("카드를 클릭해 3명을 선택하세요. 3명이 채워지면 다른 아바타는 자동으로 잠깁니다.")

    avatars = data["avatars"]
    selected_set = st.session_state.selected_avatar_ids
    
    if is_mobile:
        # 📱 모바일 모드: 1열 세로 전체 너비로 글자 짤림 방지
        for av in avatars:
            is_selected = av["id"] in selected_set
            can_select = is_selected or (len(selected_set) < 3)
            card_border = "#0284c7" if is_selected else "#cbd5e1"
            card_bg = "#f0f9ff" if is_selected else "#ffffff"
            
            st.markdown(f"""
            <div style="background:{card_bg}; border:2.5px solid {card_border}; border-radius:14px; padding:15px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-weight:800; font-size:1.02rem; color:#0f172a;">#{av['id']} {av['desc']}</span>
                    <span style="background:#0284c7; color:#ffffff; padding:3px 10px; border-radius:12px; font-size:0.78rem; font-weight:700;">{av['tag']}</span>
                </div>
                <p style="color:#334155; font-size:0.92rem; margin:0 0 10px 0; line-height:1.55; font-weight:500;">{av['appearance']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            btn_label = "선택 해제 ❌" if is_selected else ("선택하기 ➕" if can_select else "정원 초과 (3명 완료)")
            if st.button(btn_label, key=f"btn_av_{av['id']}", disabled=(not can_select and not is_selected), use_container_width=True):
                if is_selected:
                    selected_set.remove(av["id"])
                else:
                    selected_set.add(av["id"])
                st.session_state.selected_avatar_ids = selected_set
                st.rerun()
    else:
        # 💻 PC 모드: 2열 가로 분할
        col_left, col_right = st.columns(2)
        for i, av in enumerate(avatars):
            target_col = col_left if i % 2 == 0 else col_right
            with target_col:
                is_selected = av["id"] in selected_set
                can_select = is_selected or (len(selected_set) < 3)
                card_border = "#0284c7" if is_selected else "#cbd5e1"
                card_bg = "#f0f9ff" if is_selected else "#ffffff"
                
                st.markdown(f"""
                <div style="background:{card_bg}; border:2.5px solid {card_border}; border-radius:14px; padding:16px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:800; font-size:1.05rem; color:#0f172a;">#{av['id']} {av['desc']}</span>
                        <span style="background:#0284c7; color:#ffffff; padding:3px 10px; border-radius:12px; font-size:0.8rem; font-weight:700;">{av['tag']}</span>
                    </div>
                    <p style="color:#334155; font-size:0.92rem; margin:0 0 10px 0; line-height:1.5; font-weight:500;">{av['appearance']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                btn_label = "선택 해제 ❌" if is_selected else ("선택하기 ➕" if can_select else "정원 초과 (3명 완료)")
                if st.button(btn_label, key=f"btn_av_{av['id']}", disabled=(not can_select and not is_selected), use_container_width=True):
                    if is_selected:
                        selected_set.remove(av["id"])
                    else:
                        selected_set.add(av["id"])
                    st.session_state.selected_avatar_ids = selected_set
                    st.rerun()

    st.markdown(f"<div style='margin: 18px 0; font-weight: 800; font-size: 1.15rem; color: #0284c7;'>현재 선택된 아바타: {len(selected_set)} / 3 명</div>", unsafe_allow_html=True)

    def start_with_avatars(selected_list):
        st.session_state.selected_avatars = selected_list
        st.session_state.selected_avatar_ids = {av["id"] for av in selected_list}
        st.session_state.current_avatar_idx = 0
        st.session_state.current_q_idx = 0
        st.session_state.answers = []
        st.session_state.show_step_result = False
        st.session_state.page = "AVATAR_INTRO"
        st.session_state.demo_mode = demo_toggle
        st.rerun()

    if is_mobile:
        if st.button("선택한 3명으로 체험 시작하기 ➔", use_container_width=True, type="primary", key="btn_start_mobile"):
            if len(selected_set) != 3:
                st.error("반드시 아바타를 정확히 3명 선택해 주세요!")
            else:
                start_with_avatars([av for av in avatars if av["id"] in selected_set])
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🎲 3명 랜덤 선택", use_container_width=True, key="btn_random_mobile"):
            start_with_avatars(random.sample(avatars, 3))
    else:
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button("선택한 3명으로 체험 시작하기 ➔", use_container_width=True, type="primary", key="btn_start_pc"):
                if len(selected_set) != 3:
                    st.error("반드시 아바타를 정확히 3명 선택해 주세요!")
                else:
                    start_with_avatars([av for av in avatars if av["id"] in selected_set])
        with col_btn2:
            if st.button("🎲 3명 랜덤 선택", use_container_width=True, key="btn_random_pc"):
                start_with_avatars(random.sample(avatars, 3))

# 2. 아바타 소개/빙의 화면
elif st.session_state.page == "AVATAR_INTRO":
    avatar = st.session_state.selected_avatars[st.session_state.current_avatar_idx]
    order_num = st.session_state.current_avatar_idx + 1

    st.markdown(f'<span class="avatar-badge">🎭 이번에 빙의할 아바타 {order_num}/3</span>', unsafe_allow_html=True)
    st.title(f"#{avatar['id']} {avatar['desc']}")
    
    st.markdown(f"""
    <div class="scenario-card" style="border-top: 8px solid #0284c7; padding: 28px;">
        <div style="font-size: 1.2rem; font-weight: 800; color: #0284c7; margin-bottom: 14px;">
            🏷️ 유형: {avatar['tag']}
        </div>
        <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin: 16px 0; border: 2px solid #cbd5e1;">
            <p style="color: #475569; font-weight: 700; margin-bottom: 8px; font-size: 0.95rem;">👀 세상이 바라보는 당신의 겉모습:</p>
            <div style="font-size: 1.15rem; color: #0f172a; font-weight: 700; line-height: 1.6;">"{avatar['appearance']}"</div>
        </div>
        <p style="color: #334155; font-size: 1rem; line-height: 1.7; margin-top: 18px; font-weight: 500;">
            당신은 지금부터 이 사람의 입장이 되어, 편의점·대중교통·식당 등 일상 속에서 마주치는 사람들의 시선과 편견을 직접 겪게 됩니다.<br/>
            준비가 되셨다면 아래 <b>[체험 시작하기]</b> 버튼을 눌러주세요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"👉 #{avatar['id']} {avatar['desc']}의 시선으로 시작하기", use_container_width=True, type="primary"):
        st.session_state.page = "PLAY"
        st.rerun()

# 3. 플레이 화면 (Q1 ~ Q5)
elif st.session_state.page == "PLAY":
    avatar = st.session_state.selected_avatars[st.session_state.current_avatar_idx]
    
    flat_questions = []
    for place in avatar["places"]:
        for q in place["questions"]:
            q_copy = dict(q)
            q_copy["place_name"] = place["place"]
            flat_questions.append(q_copy)
    
    current_q = flat_questions[st.session_state.current_q_idx]
    
    total_progress = (st.session_state.current_avatar_idx * 5 + st.session_state.current_q_idx + 1) / 15
    st.progress(total_progress)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<span class="avatar-badge">👤 {avatar["tag"]} | 아바타 {st.session_state.current_avatar_idx + 1}/3</span>', unsafe_allow_html=True)
        st.subheader(avatar["desc"])
    with col2:
        st.markdown(f"<div style='text-align: right; color: #0f172a; font-size: 0.95rem; font-weight: 700; padding-top: 10px;'>장소: <b>{current_q['place_name']}</b><br/>문항 {st.session_state.current_q_idx + 1} / 5</div>", unsafe_allow_html=True)

    # 🎮 실시간 멘탈 & 스트레스 / 사이다 게이지
    p_count = sum(1 for a in st.session_state.answers if a["category"] == "참기")
    a_count = sum(1 for a in st.session_state.answers if a["category"] == "맞서기")
    fire_pct = int((p_count / 12) * 100)
    lightning_pct = int((a_count / 12) * 100)

    if p_count > a_count:
        status_text = "속으로 삭히며 참아내는 중... (내적 스트레스 축적 중 🔥)"
        status_color = "#e11d48"
    elif a_count > p_count:
        status_text = "할 말은 똑부러지게 하는 중! (당당한 사이다 충전 ⚡)"
        status_color = "#0284c7"
    else:
        status_text = "상황에 맞춰 유연하게 반응하는 중 🧘"
        status_color = "#475569"

    st.markdown(f"""
    <div class="gauge-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 800; font-size: 0.95rem; color: #0f172a;">🎮 실시간 멘탈 게이지</span>
            <span style="font-size: 0.85rem; font-weight: 700; color: {status_color};">{status_text}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700;">
                    <span style="color: #e11d48;">🔥 내적 분노·참기 ({p_count}/12)</span>
                    <span style="color: #e11d48;">{fire_pct}%</span>
                </div>
                <div class="gauge-bar-bg">
                    <div class="gauge-fill-fire" style="width: {min(fire_pct, 100)}%;"></div>
                </div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700;">
                    <span style="color: #0284c7;">⚡ 사이다·맞서기 ({a_count}/12)</span>
                    <span style="color: #0284c7;">{lightning_pct}%</span>
                </div>
                <div class="gauge-bar-bg">
                    <div class="gauge-fill-lightning" style="width: {min(lightning_pct, 100)}%;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="scenario-card">
        <p style="color: #0284c7; font-size: 1rem; font-weight: 800; margin-bottom: 8px;">📍 상황</p>
        <div style="font-size: 1.12rem; font-weight: 700; color: #0f172a; line-height: 1.6;">{current_q['situation']}</div>
        <div class="npc-bubble">
            💬 <b>상대방:</b> "{current_q['npc']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not current_q.get("is_ending", False):
        if not st.session_state.show_step_result:
            if st.session_state.get("timer_enabled", True):
                timer_html = f"""
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 2px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; margin-bottom: 5px;">
                        <span style="color: #475569;">⏱️ <b>20초 딜레마</b> (생각할 시간 20초, 초과 시 침묵으로 받아들입니다)</span>
                        <span id="timer-text" style="color: #0284c7; font-weight: 800;">남은 시간: 20초</span>
                    </div>
                    <div style="width: 100%; background-color: #e2e8f0; border-radius: 999px; height: 9px; overflow: hidden;">
                        <div id="timer-bar" style="height: 100%; width: 100%; background: #0284c7; border-radius: 999px; transition: width 0.1s linear, background-color 0.3s ease;"></div>
                    </div>
                </div>
                <script>
                    let timeLeft = 20.0;
                    const totalTime = 20.0;
                    const textEl = document.getElementById('timer-text');
                    const barEl = document.getElementById('timer-bar');
                    let triggered = false;

                    const hideTimeoutBtn = () => {{
                        try {{
                            const buttons = window.parent.document.querySelectorAll("button");
                            for (const b of buttons) {{
                                if (b.innerText && b.innerText.includes("시간 초과 시 자동 수용")) {{
                                    const container = b.closest('div[data-testid="stButton"]') || b.parentElement;
                                    if (container) {{
                                        container.style.position = 'absolute';
                                        container.style.opacity = '0';
                                        container.style.pointerEvents = 'none';
                                        container.style.height = '0px';
                                        container.style.overflow = 'hidden';
                                    }}
                                    return b;
                                }}
                            }}
                        }} catch(e) {{}}
                        return null;
                    }};
                    hideTimeoutBtn();
                    setTimeout(hideTimeoutBtn, 50);
                    setTimeout(hideTimeoutBtn, 200);

                    const tagDevSkipButtons = () => {{
                        try {{
                            const buttons = window.parent.document.querySelectorAll("button");
                            for (const b of buttons) {{
                                if (b.innerText && (b.innerText.includes("개발자") || b.innerText.includes("건너뛰기"))) {{
                                    b.setAttribute("data-dev-skip", "true");
                                    b.classList.add("dev-skip-custom");
                                    b.style.setProperty("background-color", "#1e293b", "important");
                                    b.style.setProperty("border", "2px solid #475569", "important");
                                    b.style.setProperty("color", "#ffffff", "important");
                                    
                                    const p = b.querySelector("p") || b.querySelector("span") || b;
                                    p.style.setProperty("color", "#ffffff", "important");

                                    b.onmouseenter = () => {{
                                        b.style.setProperty("background-color", "#0f172a", "important");
                                        b.style.setProperty("border-color", "#facc15", "important");
                                        b.style.setProperty("color", "#facc15", "important");
                                        p.style.setProperty("color", "#facc15", "important");
                                        b.style.setProperty("box-shadow", "0 4px 16px rgba(250, 204, 21, 0.35)", "important");
                                    }};
                                    b.onmouseleave = () => {{
                                        b.style.setProperty("background-color", "#1e293b", "important");
                                        b.style.setProperty("border-color", "#475569", "important");
                                        b.style.setProperty("color", "#ffffff", "important");
                                        p.style.setProperty("color", "#ffffff", "important");
                                        b.style.removeProperty("box-shadow");
                                    }};
                                }}
                            }}
                        }} catch(e) {{}}
                    }};
                    tagDevSkipButtons();
                    setTimeout(tagDevSkipButtons, 50);
                    setTimeout(tagDevSkipButtons, 150);
                    setTimeout(tagDevSkipButtons, 350);
                    setTimeout(tagDevSkipButtons, 800);

                    const interval = setInterval(() => {{
                        timeLeft -= 0.1;
                        if (timeLeft <= 0) {{
                            timeLeft = 0;
                            clearInterval(interval);
                            if (!triggered) {{
                                triggered = true;
                                if (textEl) {{
                                    textEl.innerText = "⌛ 20초 초과! 침묵 속에 상황을 받아들입니다...";
                                    textEl.style.color = "#ef4444";
                                }}
                                if (barEl) barEl.style.width = "0%";
                                
                                setTimeout(() => {{
                                    try {{
                                        const buttons = window.parent.document.querySelectorAll("button");
                                        for (const b of buttons) {{
                                            if (b.innerText && b.innerText.includes("시간 초과 시 자동 수용")) {{
                                                b.click();
                                                break;
                                            }}
                                        }}
                                    }} catch(e) {{
                                        console.error("Auto timeout error:", e);
                                    }}
                                }}, 300);
                            }}
                        }} else {{
                            const sec = Math.ceil(timeLeft);
                            const pct = (timeLeft / totalTime) * 100;
                            if (textEl) textEl.innerText = "남은 시간: " + sec + "초";
                            if (barEl) barEl.style.width = pct + "%";
                            
                            if (timeLeft <= 5) {{
                                if (barEl) barEl.style.background = "#ef4444";
                                if (textEl) textEl.style.color = "#ef4444";
                            }} else if (timeLeft <= 10) {{
                                if (barEl) barEl.style.background = "#f59e0b";
                                if (textEl) textEl.style.color = "#d97706";
                            }} else {{
                                if (barEl) barEl.style.background = "#0284c7";
                                if (textEl) textEl.style.color = "#0284c7";
                            }}
                        }}
                    }}, 100);
                </script>
                """
                components.html(timer_html, height=45)

                # 시간 초과 시 자바스크립트가 자동으로 누르는 트리거
                if st.button("⏰ 시간 초과 시 자동 수용", key=f"btn_timeout_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}"):
                    timeout_res = {
                        "type": "체념과 수용",
                        "category": "참기",
                        "result": "20초 동안 당황한 마음에 아무 말도 하지 못하고, 씁쓸한 표정으로 상황을 묵묵히 받아들였습니다.",
                        "inner": "찰나의 순간에 머릿속이 하얘져 말문이 턱 막혔다... 어차피 따져봤자 나만 이상한 사람 취급받겠지. 이번에도 그냥 내가 참고 넘기는 게 편하겠다."
                    }
                    st.session_state.answers.append({
                        "avatar": avatar["desc"],
                        "category": "참기",
                        "type": "체념과 수용 (시간 초과)"
                    })
                    st.session_state.last_result = timeout_res
                    st.session_state.show_step_result = True
                    st.rerun()

            st.markdown("<p style='font-size: 1.1rem; font-weight: 800; color: #0f172a; margin-top: 8px;'>당신의 선택은?</p>", unsafe_allow_html=True)
            c1, c2 = current_q["choices"][0], current_q["choices"][1]
            c1_icon = "🛡️" if c1["category"] == "참기" else "⚡"
            c2_icon = "⚡" if c2["category"] == "맞서기" else "🛡️"

            def handle_choice_action(choice):
                st.session_state.answers.append({
                    "avatar": avatar["desc"],
                    "category": choice["category"],
                    "type": choice["type"]
                })
                st.session_state.last_result = choice
                st.session_state.show_step_result = True
                st.rerun()

            if is_mobile:
                # 📱 모바일 모드: 1열 세로 배치로 글자 짤림 방지 및 넓은 터치 영역 제공
                if st.button(f"{c1_icon} [{c1['type']}]\n{c1['text']}", key=f"c1_btn_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}", use_container_width=True):
                    handle_choice_action(c1)
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                if st.button(f"{c2_icon} [{c2['type']}]\n{c2['text']}", key=f"c2_btn_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}", use_container_width=True):
                    handle_choice_action(c2)
            else:
                # 💻 PC 모드: 2열 가로 분할
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"{c1_icon} [{c1['type']}]\n{c1['text']}", key=f"c1_btn_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}", use_container_width=True):
                        handle_choice_action(c1)
                with col_b:
                    if st.button(f"{c2_icon} [{c2['type']}]\n{c2['text']}", key=f"c2_btn_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}", use_container_width=True):
                        handle_choice_action(c2)

            # 🛠️ 개발자용 인라인 건너뛰기
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button("⏩ [개발자] 이 질문 바로 건너뛰기", key=f"inline_skip_{st.session_state.current_avatar_idx}_{st.session_state.current_q_idx}", help="테스트용: 질문을 풀지 않고 즉시 다음 장면으로 이동합니다"):
                st.session_state.dev_skip_used = True
                st.session_state.answers.append({
                    "avatar": avatar["desc"],
                    "category": "맞서기" if st.session_state.current_q_idx % 2 == 0 else "참기",
                    "type": "개발자 건너뛰기"
                })
                st.session_state.current_q_idx += 1
                st.session_state.show_step_result = False
                st.rerun()
        else:
            res = st.session_state.last_result
            st.markdown(f"""
            <div class="scenario-card" style="border-left: 8px solid #0284c7;">
                <p style="color: #0284c7; font-weight: 800; font-size: 1.05rem;">⚡ 결과</p>
                <div style="font-size: 1.08rem; color: #0f172a; font-weight: 600; line-height: 1.7;">{res['result']}</div>
                <div class="inner-monologue">
                    💭 <b>나의 속마음:</b><br/>{res['inner']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("다음 장면으로 ➔", use_container_width=True, type="primary"):
                st.session_state.current_q_idx += 1
                st.session_state.show_step_result = False
                st.rerun()

    else:
        st.balloons()
        
        st.markdown(f"""
        <div class="climax-banner">
            🔥 {current_q['climax_quote']}
        </div>
        """, unsafe_allow_html=True)
        
        tab_action, tab_truth = st.tabs(["📢 사이다 당당한 맞서기 & 사과", "🌱 이 아바타의 숨은 진실"])
        
        with tab_action:
            st.markdown(f"""
            <div class="scenario-card" style="border: 3px solid #0f172a; margin-top: 10px;">
                <p style="color: #0f172a; font-weight: 800; font-size: 1.05rem;">📢 나의 당당한 한마디:</p>
                <div style="font-size: 1.15rem; color: #0284c7; font-weight: 800; line-height: 1.6; padding: 6px 0;">
                    "{current_q['action_text']}"
                </div>
                <hr style="border: none; border-top: 2px solid #e2e8f0; margin: 12px 0;"/>
                <p style="color: #059669; font-weight: 800; font-size: 1.05rem;">✨ 상대방의 반응 (사과와 양보):</p>
                <div style="font-size: 1.05rem; color: #0f172a; font-weight: 600; line-height: 1.7;">
                    {current_q['result']}
                </div>
                <div class="inner-monologue" style="background: #f0fdf4 !important; border-color: #22c55e !important; color: #14532d !important;">
                    💭 <b>속마음:</b> {current_q['inner']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with tab_truth:
            st.markdown(f"""
            <div class="scenario-card" style="background: #f0fdf4 !important; border: 2.5px solid #22c55e; margin-top: 10px;">
                <h4 style="color: #15803d; margin-bottom: 12px; font-weight: 800;">🌱 사실 이 사람은요...</h4>
                <div style="color: #0f172a; font-size: 1.1rem; line-height: 1.7; font-weight: 700;">
                    {avatar['truth']}
                </div>
                <hr style="border: none; border-top: 2px solid #bbf7d0; margin: 16px 0;"/>
                <p style="color: #334155; font-size: 0.95rem; margin: 0; font-weight: 600;">
                    특별한 사람이어서가 아니라, 우리 곁에서 묵묵히 삶을 살아가는 평범한 사람이기에 모든 편견 없는 대우를 받을 자격이 있습니다.
                </p>
            </div>
            """, unsafe_allow_html=True)

        btn_label = "다음 아바타 만나기 ➔" if st.session_state.current_avatar_idx < 2 else "최종 성찰 리포트 보기 ✨"
        if st.button(btn_label, use_container_width=True, type="primary"):
            if st.session_state.current_avatar_idx < 2:
                st.session_state.current_avatar_idx += 1
                st.session_state.current_q_idx = 0
                st.session_state.show_step_result = False
                st.session_state.page = "AVATAR_INTRO"
                st.rerun()
            else:
                st.session_state.page = "RESULT"
                st.rerun()

# 4. 최종 결과 화면
elif st.session_state.page == "RESULT":
    st.title("✨ 최종 성찰 리포트")
    st.caption("당신이 걸어온 12번의 선택과 3번의 용기를 돌아봅니다.")

    patience_count = sum(1 for a in st.session_state.answers if a["category"] == "참기")
    action_count = sum(1 for a in st.session_state.answers if a["category"] == "맞서기")
    avatar_names = [a["desc"] for a in st.session_state.selected_avatars]

    profile = get_bti_profile(patience_count, action_count)
    tags_html = " ".join([f'<span class="bti-tag">{t}</span>' for t in profile["tags"]])

    st.markdown(f"""
    <div class="bti-certificate">
        <div style="font-size: 0.85rem; font-weight: 800; color: #0284c7; letter-spacing: 2px;">★ OFFICIAL BTI CERTIFICATE ★</div>
        <div class="bti-title">{profile['title']}</div>
        <div style="margin: 8px 0;"><span class="bti-badge">{profile['badge']}</span></div>
        <div style="margin: 14px 0;">
            {tags_html}
        </div>
        <p style="color: #334155; font-size: 1.05rem; line-height: 1.6; margin: 16px auto; max-width: 540px; font-weight: 600;">
            "{profile['desc']}"
        </p>
        <div style="background: #f1f5f9; border-radius: 12px; padding: 14px; margin-top: 14px; border: 1.5px solid #cbd5e1;">
            <div style="display: flex; justify-content: space-around; font-weight: 800; font-size: 0.95rem;">
                <span style="color: #e11d48;">🔥 인내·참기 성향: {profile['patience_pct']}% ({patience_count}회)</span>
                <span style="color: #0284c7;">⚡ 사이다·맞서기 성향: {profile['action_pct']}% ({action_count}회)</span>
            </div>
        </div>
        <div style="margin-top: 12px; font-size: 0.85rem; color: #64748b; font-weight: 600;">
            📸 화면을 캡처해서 친구들과 편견 대처 유형을 비교해보세요!
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="상황을 유연하게 넘긴 횟수", value=f"{patience_count} 회", help="갈등을 피하고 상황을 지키려는 배려의 선택")
    with col_stat2:
        st.metric(label="내 의견/목소리를 낸 횟수", value=f"{action_count} 회", help="존엄을 지키고 오해를 바로잡으려는 용기의 선택")

    # 📢 우리 곁 실재하는 이웃들의 현실 카드
    st.markdown("""
    <div class="scenario-card" style="border-left: 8px solid #ef4444; background: #fff5f5; margin-top: 20px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
            <span style="font-size: 1.35rem;">📢</span>
            <h3 style="margin: 0; color: #991b1b; font-weight: 800; font-size: 1.2rem;">
                우리 사회에는 실제로 매일 이런 편견을 견뎌내는 이웃들이 살아갑니다
            </h3>
        </div>
        <p style="color: #334155; font-size: 1.02rem; line-height: 1.7; font-weight: 600; margin-bottom: 12px;">
            오늘 12번의 선택에서 느꼈던 답답함과 억울함은 가상의 게임이 아닙니다.<br/>
            우리 주변에는 <b>단지 겉모습, 서툰 말투, 휠체어를 탔다는 이유만으로</b> 편의점에서 도둑 취급을 당하거나 가방 검사를 요구받고, 식당과 거리에서 이유 없는 반말과 무시를 당하며 살아가는 평범한 사람들이 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols_reality = st.columns(3)
    for idx, av in enumerate(st.session_state.selected_avatars):
        with cols_reality[idx]:
            st.markdown(f"""
            <div style="background: #ffffff; border: 2px solid #cbd5e1; border-radius: 14px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                <div style="margin-bottom: 6px;">
                    <span style="background: #0284c7; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700;">#{av['id']} {av['tag']}</span>
                </div>
                <div style="font-weight: 800; font-size: 1rem; color: #0f172a; margin-bottom: 10px;">{av['desc']}</div>
                <div style="background: #f8fafc; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 3.5px solid #ef4444;">
                    <p style="font-size: 0.8rem; font-weight: 700; color: #991b1b; margin: 0 0 4px 0;">👀 세상의 섣부른 편견:</p>
                    <p style="font-size: 0.85rem; color: #334155; margin: 0; line-height: 1.5;">"{av['appearance']}"</p>
                </div>
                <div style="background: #f0fdf4; border-radius: 10px; padding: 10px; border-left: 3.5px solid #16a34a;">
                    <p style="font-size: 0.8rem; font-weight: 700; color: #166534; margin: 0 0 4px 0;">🌱 가려진 진실:</p>
                    <p style="font-size: 0.85rem; color: #1e293b; margin: 0; line-height: 1.5;">{av['truth']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    summary_data = {
        "참기": patience_count,
        "맞서기": action_count,
        "avatars": avatar_names,
        "bti_title": profile["title"]
    }

    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 28px; text-align: center; border: 3px dashed #0284c7; margin: 20px 0; animation: pulseGlow 1.8s infinite;">
            <h3 style="color: #0284c7; margin-bottom: 8px; font-weight: 800;">🤖 AI가 당신의 선택 여정을 깊이 분석하고 있습니다...</h3>
            <p style="color: #334155; font-size: 1rem; font-weight: 600;">누군가를 평가하지 않고, 당신이 마주했던 순간의 마음 결을 온전히 들여다보고 있어요.</p>
        </div>
        """, unsafe_allow_html=True)
        demo_flag = getattr(st.session_state, "demo_mode", False)
        report_text = analyze_experience(summary_data, demo_mode=demo_flag)
    
    loading_placeholder.empty()
    st.snow()

    st.markdown(f"""
    <div class="scenario-card" style="border: 3px solid #0284c7; background: #ffffff;">
        <h3 style="color: #0284c7; margin-bottom: 18px; font-weight: 800;">💬 편견 너머 공감 리포트</h3>
        <div style="font-size: 1.08rem; line-height: 1.9; color: #0f172a; font-weight: 600;">
            {report_text.replace(chr(10), '<br/>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 다음 단계 이동 버튼 (엔딩 시네마틱 전용 화면으로 이동)
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    if is_mobile:
        if st.button("🎬 엔딩 시네마틱(영상 자막) 보러가기 ➔", use_container_width=True, type="primary"):
            st.session_state.page = "CINEMATIC"
            st.rerun()
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("처음으로 돌아가기 (다시 체험하기) 🔄", use_container_width=True):
            st.session_state.page = "DEVICE_SELECT"
            st.session_state.device_mode = None
            st.session_state.selected_avatar_ids = set()
            st.session_state.selected_avatars = []
            st.session_state.current_avatar_idx = 0
            st.session_state.current_q_idx = 0
            st.session_state.answers = []
            st.session_state.show_step_result = False
            st.session_state.last_result = {}
            st.session_state.dev_skip_used = False
            st.rerun()
    else:
        col_res_btn1, col_res_btn2 = st.columns([3, 2])
        with col_res_btn1:
            if st.button("🎬 엔딩 시네마틱(영상 자막) 보러가기 ➔", use_container_width=True, type="primary"):
                st.session_state.page = "CINEMATIC"
                st.rerun()
        with col_res_btn2:
            if st.button("처음으로 돌아가기 (다시 체험하기) 🔄", use_container_width=True):
                st.session_state.page = "DEVICE_SELECT"
                st.session_state.device_mode = None
                st.session_state.selected_avatar_ids = set()
                st.session_state.selected_avatars = []
                st.session_state.current_avatar_idx = 0
                st.session_state.current_q_idx = 0
                st.session_state.answers = []
                st.session_state.show_step_result = False
                st.session_state.last_result = {}
                st.session_state.dev_skip_used = False
                st.rerun()

# 5. 엔딩 시네마틱 전용 전체 화면
elif st.session_state.page == "CINEMATIC":
    st.title("🎬 엔딩 시네마틱 : 편견 너머, 우리의 일상")
    st.caption("한 사람의 이웃으로서 마주하는 공감의 여정 (슬라이드당 약 8초 동안 넉넉히 머뭅니다)")

    cinematic_html = """
    <div style="
        background: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
        border: 2.5px solid #1e293b;
        border-radius: 22px;
        padding: 36px 28px 24px 28px;
        color: #f8fafc;
        box-shadow: 0 20px 48px rgba(0, 0, 0, 0.5);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;
        text-align: center;
        user-select: none;
    ">
        <!-- Top bar -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
            <span style="font-size: 11.5px; letter-spacing: 3px; font-weight: 800; color: #38bdf8;">
                🎬 ENDING CINEMATIC REFLECTION
            </span>
            <span id="scene-counter" style="font-size: 12.5px; font-weight: 700; color: #cbd5e1; background: rgba(255,255,255,0.08); padding: 4px 14px; border-radius: 12px;">
                SCENE 1 / 5
            </span>
        </div>

        <!-- Center Subtitle Display Area -->
        <div style="min-height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div id="scene-tag" style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 10px; transition: all 0.6s ease;">
                [체험의 끝에서]
            </div>
            <div id="scene-title" style="font-size: 22px; font-weight: 800; line-height: 1.5; color: #ffffff; margin-bottom: 10px; transition: all 0.6s ease; text-shadow: 0 2px 12px rgba(0,0,0,0.6);">
                당신이 오늘 잠시 머물렀던 3명의 일상...
            </div>
            <div id="scene-sub" style="font-size: 15.5px; font-weight: 500; color: #94a3b8; line-height: 1.6; transition: all 0.6s ease;">
                그곳에서 마주쳤던 차가운 눈빛과 서글픈 침묵을 기억하시나요?
            </div>
        </div>

        <!-- Progress Bar for Current Scene (8초 게이지) -->
        <div style="width: 100%; background: rgba(255,255,255,0.1); height: 5px; border-radius: 999px; overflow: hidden; margin: 24px 0 16px 0;">
            <div id="timeline-bar" style="height: 100%; width: 0%; background: linear-gradient(90deg, #38bdf8, #818cf8); border-radius: 999px;"></div>
        </div>

        <!-- Bottom Controls -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div id="dots-container" style="display: flex; gap: 7px; align-items: center;"></div>
            <div style="display: flex; gap: 7px;">
                <button id="btn-prev" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #f8fafc; border-radius: 8px; padding: 6px 14px; font-size: 12.5px; font-weight: 600; cursor: pointer;">◀ 이전</button>
                <button id="btn-play" style="background: #0284c7; border: none; color: #ffffff; border-radius: 8px; padding: 6px 16px; font-size: 12.5px; font-weight: 700; cursor: pointer;">⏸️ 일시정지</button>
                <button id="btn-next" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #f8fafc; border-radius: 8px; padding: 6px 14px; font-size: 12.5px; font-weight: 600; cursor: pointer;">다음 ▶</button>
                <button id="btn-replay" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #f8fafc; border-radius: 8px; padding: 6px 12px; font-size: 12.5px; font-weight: 600; cursor: pointer;">🔁 다시보기</button>
            </div>
        </div>
    </div>

    <script>
        const scenes = [
            {
                tag: "[체험의 끝에서]",
                title: "당신이 오늘 잠시 머물렀던 3명의 일상...",
                sub: "그곳에서 마주쳤던 차가운 눈빛과 서글픈 침묵을 기억하시나요?"
            },
            {
                tag: "[보이지 않는 벽]",
                title: "우리 곁에는 단지 겉모습, 말투, 장애가 있다는 이유로",
                sub: "편의점에서 의심받고, 대중교통에서 눈총을 받으며 매일을 견뎌내는 사람들이 실재합니다."
            },
            {
                tag: "[평범함의 자격]",
                title: "그들은 결코 특별한 혜택이나 동정을 바란 것이 아닙니다.",
                sub: "그저 '한 사람의 평범한 이웃'으로 의심 없이 존중받고 싶었을 뿐입니다."
            },
            {
                tag: "[당신의 12번의 선택]",
                title: "가슴 졸이며 삼켰던 순간도, 용기 내어 맞섰던 순간도...",
                sub: "누군가가 매일 24시간 홀로 짊어져야 했던 삶의 무게였습니다."
            },
            {
                tag: "[내일의 우리에게]",
                title: "내일 아침, 당신의 일상에서 마주칠 누군가에게",
                sub: "섣부른 의심 대신, 편견 없는 따뜻한 눈인사를 먼저 건네보는 건 어떨까요? 🌱"
            }
        ];

        let currentIdx = 0;
        let isPlaying = true;
        let elapsedMs = 0;
        const sceneDurationMs = 8000; // 슬라이드당 8초로 넉넉하게 연장
        const tickIntervalMs = 50;

        const tagEl = document.getElementById('scene-tag');
        const titleEl = document.getElementById('scene-title');
        const subEl = document.getElementById('scene-sub');
        const counterEl = document.getElementById('scene-counter');
        const barEl = document.getElementById('timeline-bar');
        const dotsContainer = document.getElementById('dots-container');
        const btnPlay = document.getElementById('btn-play');
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnReplay = document.getElementById('btn-replay');

        function renderDots() {
            dotsContainer.innerHTML = '';
            scenes.forEach((_, i) => {
                const dot = document.createElement('div');
                dot.style.width = i === currentIdx ? '22px' : '8px';
                dot.style.height = '8px';
                dot.style.borderRadius = '999px';
                dot.style.background = i === currentIdx ? '#38bdf8' : 'rgba(255,255,255,0.2)';
                dot.style.transition = 'all 0.3s ease';
                dot.style.cursor = 'pointer';
                dot.onclick = () => { goToScene(i); };
                dotsContainer.appendChild(dot);
            });
        }

        function showScene(idx) {
            const sc = scenes[idx];
            tagEl.style.opacity = '0';
            titleEl.style.opacity = '0';
            subEl.style.opacity = '0';
            tagEl.style.transform = 'translateY(-12px)';
            titleEl.style.transform = 'translateY(-12px)';
            subEl.style.transform = 'translateY(-12px)';

            setTimeout(() => {
                tagEl.innerText = sc.tag;
                titleEl.innerText = sc.title;
                subEl.innerText = sc.sub;
                counterEl.innerText = `SCENE ${idx + 1} / ${scenes.length}`;

                tagEl.style.transform = 'translateY(12px)';
                titleEl.style.transform = 'translateY(12px)';
                subEl.style.transform = 'translateY(12px)';

                setTimeout(() => {
                    tagEl.style.opacity = '1';
                    titleEl.style.opacity = '1';
                    subEl.style.opacity = '1';
                    tagEl.style.transform = 'translateY(0)';
                    titleEl.style.transform = 'translateY(0)';
                    subEl.style.transform = 'translateY(0)';
                }, 40);
            }, 300);

            renderDots();
        }

        function goToScene(idx) {
            currentIdx = (idx + scenes.length) % scenes.length;
            elapsedMs = 0;
            showScene(currentIdx);
        }

        setInterval(() => {
            if (!isPlaying) return;
            elapsedMs += tickIntervalMs;
            const pct = Math.min((elapsedMs / sceneDurationMs) * 100, 100);
            barEl.style.width = pct + '%';

            if (elapsedMs >= sceneDurationMs) {
                elapsedMs = 0;
                goToScene(currentIdx + 1);
            }
        }, tickIntervalMs);

        btnPlay.onclick = () => {
            isPlaying = !isPlaying;
            btnPlay.innerText = isPlaying ? '⏸️ 일시정지' : '▶ 재생';
            btnPlay.style.background = isPlaying ? '#0284c7' : '#10b981';
        };

        btnPrev.onclick = () => { goToScene(currentIdx - 1); };
        btnNext.onclick = () => { goToScene(currentIdx + 1); };
        btnReplay.onclick = () => { goToScene(0); isPlaying = true; btnPlay.innerText = '⏸️ 일시정지'; btnPlay.style.background = '#0284c7'; };

        renderDots();
        showScene(0);
    </script>
    """
    components.html(cinematic_html, height=330 if is_mobile else 290)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if is_mobile:
        if st.button("📊 최종 성찰 리포트로 돌아가기 ↩", use_container_width=True):
            st.session_state.page = "RESULT"
            st.rerun()
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🌱 처음으로 돌아가기 (다시 체험) 🔄", use_container_width=True, type="primary"):
            st.session_state.page = "DEVICE_SELECT"
            st.session_state.device_mode = None
            st.session_state.selected_avatar_ids = set()
            st.session_state.selected_avatars = []
            st.session_state.current_avatar_idx = 0
            st.session_state.current_q_idx = 0
            st.session_state.answers = []
            st.session_state.show_step_result = False
            st.session_state.last_result = {}
            st.session_state.dev_skip_used = False
            st.rerun()
    else:
        col_cine1, col_cine2 = st.columns(2)
        with col_cine1:
            if st.button("📊 최종 성찰 리포트로 돌아가기 ↩", use_container_width=True):
                st.session_state.page = "RESULT"
                st.rerun()
        with col_cine2:
            if st.button("🌱 처음으로 돌아가기 (다시 체험) 🔄", use_container_width=True, type="primary"):
                st.session_state.page = "DEVICE_SELECT"
                st.session_state.device_mode = None
                st.session_state.selected_avatar_ids = set()
                st.session_state.selected_avatars = []
                st.session_state.current_avatar_idx = 0
                st.session_state.current_q_idx = 0
                st.session_state.answers = []
                st.session_state.show_step_result = False
                st.session_state.last_result = {}
                st.session_state.dev_skip_used = False
                st.rerun()
