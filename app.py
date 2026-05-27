import streamlit as st
import datetime
import time
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (브라우저 탭 타이틀 및 레이아웃)
st.set_page_config(
    page_title="인생 타임라인 계산기",
    page_icon="⏳",
    layout="centered"
)

# 2. 상단 타이틀 및 가이드
st.title("⏳ 인생 타임라인 계산기")
st.write("당신의 생년월일을 입력하면, 지나온 시간과 남은 기회가 실시간으로 계측됩니다.")

# 3. 사용자 입력 구역 (생년월일 및 시간)
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input(
        "생년월일 선택",
        value=datetime.date(2000, 1, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date.today()
    )
with col2:
    birth_time = st.time_input("태어난 시간 (모르면 00:00)", datetime.time(0, 0))

# 대한민국 평균 수명 기준 설정
AVERAGE_LIFESPAN = 83

# 4. 실시간 타이머 작동 구역
if birth_date:
    # 입력받은 날짜와 시간을 하나의 datetime 객체로 병합
    birth_datetime = datetime.datetime.combine(birth_date, birth_time)
    
    # 예상 사망일 계산 (윤년 예외 처리 포함)
    try:
        expiry_date = birth_datetime.replace(year=birth_datetime.year + AVERAGE_LIFESPAN)
    except ValueError:
        expiry_date = birth_datetime.replace(year=birth_datetime.year + AVERAGE_LIFESPAN, day=28)

    st.markdown("---")
    
    # 실시간으로 화면이 업데이트될 빈 도화지(Container) 생성
    live_container = st.empty()

    # 무한 루프를 돌며 0.1초마다 내부 HTML만 새로고침 (깜빡임 없음)
    while True:
        now = datetime.datetime.now()
        
        # 지나온 시간 계산
        time_passed = now - birth_datetime
        seconds_passed = time_passed.total_seconds()
        days_passed = time_passed.days
        
        # 남은 시간 계산 (음수 방지를 위해 max 사용)
        time_left = expiry_date - now
        days_left = max(0, time_left.days)
        weeks_left = max(0, days_left // 7)
        
        # 신체 데이터 가상 계산 (평균치 기준)
        breaths = seconds_passed * (16 / 60)      # 분당 16회 호흡
        heartbeats = seconds_passed * (70 / 60)   # 분당 70회 박동

        # B안 테마(.streamlit/config.toml)와 완벽히 동화되는 네온 다크 CSS & HTML
        html_content = f"""
        <div style="
            font-family: 'Courier New', Courier, monospace; 
            background-color: #121212; 
            padding: 30px; 
            border: 1px solid #00ff66; 
            border-radius: 8px; 
            color: #00ff66;
            box-shadow: 0 0 15px rgba(0, 255, 102, 0.15);
        ">
            <p style="font-size: 13px; color: #888888; margin: 0 0 5px 0; letter-spacing: 1px;">[ RECORD: TIME PASSED ]</p>
            <h2 style="margin: 5px 0 15px 0; font-size: 22px; color: #ffffff; border-bottom: 1px dashed #333333; padding-bottom: 12px;">
                지구 체류 기간: <span style="color: #00ff66; font-weight: bold;">{int(seconds_passed):,} 초</span>
            </h2>
            <p style="margin: 8px 0; font-size: 16px; color: #cccccc;">• 지나온 날들: <b style="color: #ffffff;">{days_passed:,} 일</b></p>
            <p style="margin: 8px 0; font-size: 16px; color: #cccccc;">• 누적 호흡 수: <b style="color: #ffffff;">{int(breaths):,} 번</b></p>
            <p style="margin: 8px 0; font-size: 16px; color: #cccccc;">• 심장 박동 수: <b style="color: #ffffff;">{int(heartbeats):,} 번</b></p>
            
            <hr style="border: none; border-top: 1px dashed #333333; margin: 25px 0;">
            
            <p style="font-size: 13px; color: #888888; margin: 0 0 5px 0; letter-spacing: 1px;">[ PREDICTION: TIME REMAINING ]</p>
            <h2 style="margin: 5px 0 15px 0; font-size: 22px; color: #ff4b4b;">
                남은 주말 (토/일): <span style="font-weight: bold;">{weeks_left:,} 번</span>
            </h2>
            <p style="margin: 8px 0; font-size: 16px; color: #cccccc;">• 남은 일수: <b style="color: #ffffff;">{days_left:,} 일</b></p>
            <p style="margin: 8px 0; font-size: 16px; color: #cccccc;">• 기대 수명 기준: <b style="color: #00ff66;">{AVERAGE_LIFESPAN}세</b></p>
            
            <p style="font-size: 12px; color: #555555; text-align: center; margin-top: 35px; letter-spacing: 0.5px; line-height: 1.5;">
                "MEMENTO MORI : 시간은 흐르는 것이 아니라 사라지는 것이다."
            </p>
        </div>
        """
        
        # st.markdown 대신 iframe 컴포넌트를 이용해 코드가 텍스트로 깨지는 현상 방지
        with live_container:
            components.html(html_content, height=460, scrolling=False)
            
        # 0.1초 쉬고 다음 루프 실행 (CPU 과부하 방지)
        time.sleep(0.1)
