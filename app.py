import streamlit as st
import datetime
import time

# 1. 페이지 기본 설정 및 타이틀
st.title("⏳ 인생 타임라인 계산기")
st.write("당신의 생년월일을 입력하면, 지나온 시간과 남은 기회가 실시간으로 카운트됩니다.")

# 2. 사용자 입력 구역 (생년월일 및 시간 입력)
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input(
        "생년월일을 선택하세요",
        value=datetime.date(2000, 1, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date.today()
    )
with col2:
    birth_time = st.time_input("태어난 시간 (모르면 00:00)", datetime.time(0, 0))

# 대한민국 평균 수명 기준 설정 (예: 83세)
AVERAGE_LIFESPAN = 83

# 3. 계산 및 실시간 렌더링 구역
if birth_date:
    # 태어난 시각을 datetime 객체로 병합
    birth_datetime = datetime.datetime.combine(birth_date, birth_time)
    
    # 예상 사망일 계산 (생일 + 83년)
    try:
        expiry_date = birth_datetime.replace(year=birth_datetime.year + AVERAGE_LIFESPAN)
    except ValueError:
        # 윤년(2월 29일) 예외 처리
        expiry_date = birth_datetime.replace(year=birth_datetime.year + AVERAGE_LIFESPAN, day=28)

    st.write("---")
    st.subheader("📊 당신의 시간은 흐르고 있습니다")
    
    # 실시간 숫자가 업데이트될 빈 공간(Container) 생성
    live_container = st.empty()

    # 무한 루프를 돌며 0.1초마다 화면을 갱신 (실시간 카운터 효과)
    while True:
        now = datetime.datetime.now()
        
        # 지나온 시간 계산 (현재 - 태어난 시간)
        time_passed = now - birth_datetime
        seconds_passed = time_passed.total_seconds()
        
        # 남은 시간 계산 (예상 사망일 - 현재)
        time_left = expiry_date - now
        days_left = time_left.days
        weeks_left = days_left // 7 # 남은 주말의 수와 대략 일치
        
        # 가정치 기반 재미있는 수치 계산
        # 1) 평균 호흡 수: 분당 약 16회 -> 초당 16/60회
        breaths = seconds_passed * (16 / 60)
        # 2) 평균 심장 박동 수: 분당 약 70회 -> 초당 70/60회
        heartbeats = seconds_passed * (70 / 60)

        # 영수증 테마와 어울리는 미니멀하고 웅장한 감성 CSS 스타일링
        html_content = f"""
        <div style="font-family: 'Courier New', Courier, monospace; background-color: white; padding: 25px; border-radius: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); color: black;">
            
            <p style="font-size: 14px; color: #666; margin-bottom: 5px;">[지나온 발자국]</p>
            <h3 style="margin: 5px 0;">지구에 머문 시간: <span style="color: #000; font-weight: bold;">{int(seconds_passed):,} 초</span></h3>
            <p style="margin: 5px 0; font-size: 16px;">지나간 일수: <b>{time_passed.days:,} 일</b></p>
            <p style="margin: 5px 0; font-size: 16px;">그동안의 호흡: <b>{int(breaths):,} 번</b></p>
            <p style="margin: 5px 0; font-size: 16px;">심장 박동 수: <b>{int(heartbeats):,} 번</b></p>
            
            <hr style="border-top: 1px dashed #ccc; margin: 20px 0;">
            
            <p style="font-size: 14px; color: #666; margin-bottom: 5px;">[앞으로 남은 기회 (평균 수명 {AVERAGE_LIFESPAN}세 기준)]</p>
            <h3 style="margin: 5px 0; color: #ff4b4b;">남은 주말 (토/일): <span style="font-weight: bold;">{weeks_left:,} 번</span></h3>
            <p style="margin: 5px 0; font-size: 16px;">남은 일수: <b>{days_left:,} 일</b></p>
            
            <p style="font-size: 12px; color: #999; text-align: center; margin-top: 25px;">"시간은 우리에게 가장 공평하고도 한정된 자원입니다."</p>
        </div>
        """
        
        # 빈 공간에 준비된 HTML 코드를 밀어 넣어 화면을 전환
        live_container.markdown(html_content, unsafe_allow_html=True)
        
        # 0.1초 대기 후 루프 다시 실행 (너무 빠르면 과부하가 걸릴 수 있음)
        time.sleep(0.1)
