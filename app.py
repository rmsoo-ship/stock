import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="3일 서바이벌 주식 모의투자", page_icon="📈")
st.title("📈 행간을 읽어라! 3일 서바이벌 주식 모의투자")
st.write("100만 원의 시드머니로 시작해, 총 3일 동안 종목별 뉴스를 분석하고 부분 매도 및 맞춤 매수를 통해 최고 수익률에 도전하세요!")

# 2. 세션 상태 초기화
if "day" not in st.session_state:
    st.session_state.day = 1
    st.session_state.current_money = 1000000  # 초기 현금 100만 원
    st.session_state.portfolio = {}           # 보유 종목 {"종목명": 투자금액}
    st.session_state.stock_prices = {         # 종목별 현재 주가
        "K-반도체": 50000,
        "친환경 배터리": 40000,
        "바이오제약": 30000,
        "종합 상사": 20000
    }
    st.session_state.is_settled = False       # 당일 정산 완료 여부 상태 추가
    st.session_state.last_report = None       # 정산 리포트 저장용

stock_names = list(st.session_state.stock_prices.keys())

# 3. 종목별 뉴스 풀
stock_news_pool = {
    "K-반도체": [
        {"headline": "글로벌 빅테크 기업들, 차세대 AI 서버 구축 위해 한국산 메모리 확보 총력전", "news_type": "진짜 호재", "explanation": "AI 서버용 반도체 수요 급증이 실적 개선으로 직결된 정석적인 호재였습니다."},
        {"headline": "반도체 장비 반입 지연 및 단기 공급 과잉 우려 제기", "news_type": "진짜 악재", "explanation": "일시적인 공급 과잉과 장비 지연 우려로 주가가 하방 압력을 받았습니다."}
    ],
    "친환경 배터리": [
        {"headline": "정부, 전기차 보조금 예산 삭감 검토… 대신 내연기관차 도심 진입 강력 규제 발표!", "news_type": "역발상 호재", "explanation": "보조금 삭감만 보고 팔았다면 손해! 내연기관 규제 강화가 장기적으로 배터리 수요 폭증을 부르는 '역발상 호재'였습니다."},
        {"headline": "주요 배터리 셀 제조사 화재 사고 여파로 대규모 리콜 사태 발생", "news_type": "진짜 악재", "explanation": "품질 이슈와 리콜 비용 발생으로 단기 실적 악화가 불가피해졌습니다."}
    ],
    "바이오제약": [
        {"headline": "바이오제약 대표 해외 도피설 및 회계 부정 루머 SNS 확산 (진위 불명)", "news_type": "가짜 찌라시", "explanation": "전형적인 공포 조장용 가짜 찌라시였습니다! 근거 없는 소문에 패닉셀한 투자자들만 손실을 보았습니다."},
        {"headline": "개발 중인 혁신 신약이 글로벌 임상 3상에서 뛰어난 효능 입증", "news_type": "진짜 호재", "explanation": "신약 가치가 급상승하며 대규모 기술 수출 기대감이 증폭되었습니다."}
    ],
    "종합 상사": [
        {"headline": "국제 원자재 가격 급등 및 해상 물류비 상승으로 수출 기업 채산성 악화 우려", "news_type": "진짜 악재", "explanation": "물류비와 원자재 부담이 커지면서 종합 상사의 단기 수익성이 크게 악화되었습니다."},
        {"headline": "자원 개발 유전에서 초대형 원유 매장지 발견 및 독점 계약 체결", "news_type": "진짜 호재", "explanation": "자원 개발 가치가 폭등하며 안정적인 현금 창출원이 확보되었습니다."}
    ]
}

if "daily_news" not in st.session_state:
    st.session_state.daily_news = {
        stock: random.choice(stock_news_pool[stock]) for stock in stock_names
    }

# 4. 포트폴리오 정산 및 매매 처리 함수
def process_day_end(current_money, portfolio, user_sell_amounts, user_buy_amounts, daily_news, stock_prices):
    market_table = []
    stock_new_prices = {}
    stock_change_rates = {}
    
    # 1단계: 각 종목별 주가 변동률 계산
    for name in stock_names:
        base_price = stock_prices[name]
        n_type = daily_news[name]["news_type"]
        
        if n_type == "진짜 호재":
            change_rate = 0.20
        elif n_type == "역발상 호재":
            change_rate = 0.15
        elif n_type == "가짜 찌라시":
            change_rate = -0.10
        else: # 진짜 악재
            change_rate = -0.20
            
        stock_change_rates[name] = change_rate
        stock_new_prices[name] = int(base_price * (1 + change_rate))
        
    # 2단계: 보유 종목 매도 처리 (장 시작 전 기준가로 현금 회수)
    temp_portfolio = portfolio.copy()
    cash_from_sell = 0
    
    for stock_name, sell_amt in user_sell_amounts.items():
        if stock_name in temp_portfolio and sell_amt > 0:
            current_holding_val = temp_portfolio[stock_name]
            actual_sell = min(sell_amt, current_holding_val)
            
            # 매도 금액 그대로 현금 확보 (악재 회피 및 익절 가능)
            cash_from_sell += actual_sell
            
            temp_portfolio[stock_name] -= actual_sell
            if temp_portfolio[stock_name] <= 10:
                del temp_portfolio[stock_name]

    # 3단계: 남은 보유 주식들에 오늘의 주가 변동 반영
    updated_portfolio = {}
    for stock_name, remaining_amt in temp_portfolio.items():
        rate = stock_change_rates[stock_name]
        updated_portfolio[stock_name] = int(remaining_amt * (1 + rate))

    # 4단계: 확보한 현금 + 기존 현금으로 신규 맞춤 매수 진행
    total_available_cash = int(current_money + cash_from_sell)
    total_requested_buy = sum(user_buy_amounts.values())
    
    if total_requested_buy > total_available_cash:
        return "ERROR_EXCEED_CASH", 0, 0, {}, {}, []
        
    final_cash = int(total_available_cash - total_requested_buy)
    
    for stock_name, buy_amt in user_buy_amounts.items():
        if buy_amt > 0:
            rate = stock_change_rates[stock_name]
            valued_buy = int(buy_amt * (1 + rate))
            
            if stock_name in updated_portfolio:
                updated_portfolio[stock_name] += valued_buy
            else:
                updated_portfolio[stock_name] = valued_buy

    # 5단계: 결과 테이블 데이터 생성
    for name in stock_names:
        b_price = stock_prices[name]
        n_price = stock_new_prices[name]
        c_rate = stock_change_rates[name]
        
        status_str = "미보유"
        if name in updated_portfolio:
            status_str = f"보유 중 ({updated_portfolio[name]:,}원)"
            
        market_table.append({
            "종목명": name,
            "오늘의 뉴스": daily_news[name]["headline"][:24] + "...",
            "뉴스 성격": daily_news[name]["news_type"],
            "기초 주가": f"{b_price:,}원",
            "변동 후 주가": f"{n_price:,}원",
            "등락률": f"{c_rate * 100:+.1f}%",
            "내 포트폴리오": status_str
        })
        
    total_portfolio_value = sum(updated_portfolio.values())
    total_assets = int(final_cash + total_portfolio_value)
    
    return "SUCCESS", total_assets, final_cash, updated_portfolio, stock_new_prices, market_table


# --- 5. Streamlit UI 화면 구성 ---

# 사이드바 계좌 정보
st.sidebar.header("📊 내 계좌 정보")
display_day = min(st.session_state.day, 3)
st.sidebar.metric("현재 진행 일차", f"{display_day}일차 / 총 3일")
total_wealth = int(st.session_state.current_money + sum(st.session_state.portfolio.values()))
st.sidebar.metric("현재 총 자산", f"{total_wealth:,}원")
st.sidebar.write(f"💵 보유 현금: {st.session_state.current_money:,}원")

if st.session_state.portfolio:
    st.sidebar.write("📌 **보유 중인 종목:**")
    for s_name, s_val in st.session_state.portfolio.items():
        st.sidebar.write(f"- {s_name}: {s_val:,}원")
else:
    st.sidebar.info("보유 중인 주식 없음 (현금 100%)")


# 메인 화면 (3일차 이하 진행 중)
if st.session_state.day <= 3:
    # [상태 A] 아직 장 마감 전 -> 뉴스 분석 및 매매 입력 화면
    if not st.session_state.is_settled:
        st.subheader(f"📅 [ {st.session_state.day}일차 ] 종목별 경제 뉴스 속보 & 맞춤 매매")
        st.write("뉴스의 행간을 읽고, 보유 주식은 **부분/전량 매도**하거나 확보될 현금으로 **신규/추가 매수**하세요!")
        
        user_sell_amounts = {}
        user_buy_amounts = {}
        
        for stock in stock_names:
            news = st.session_state.daily_news[stock]
            with st.expander(f"📢 [{stock}] 오늘의 뉴스 및 거래 (현재가: {st.session_state.stock_prices[stock]:,}원)", expanded=True):
                st.info(f"**헤드라인:** {news['headline']}")
                # 스포일러 방지를 위해 뉴스 성격 캡션 제거
                
                if stock in st.session_state.portfolio:
                    holding_val = int(st.session_state.portfolio[stock])
                    st.warning(f"현재 이 종목 투자금: {holding_val:,}원")
                    
                    sell_amt = st.number_input(
                        f"{stock} 매도할 금액 입력 (원) [최대 {holding_val:,}원]:",
                        min_value=0,
                        max_value=holding_val,
                        step=10000,
                        value=0,
                        key=f"sell_{stock}_{st.session_state.day}"
                    )
                    if sell_amt > 0:
                        user_sell_amounts[stock] = sell_amt
                
                # 매도 대금으로 당일 재매수가 가능하도록 max_value를 넉넉하게 설정
                buy_amt = st.number_input(
                    f"{stock} 신규/추가 매수할 금액 입력 (원):", 
                    min_value=0, 
                    max_value=100000000, 
                    step=10000, 
                    value=0,
                    key=f"buy_{stock}_{st.session_state.day}"
                )
                if buy_amt > 0:
                    user_buy_amounts[stock] = buy_amt
                        
        st.divider()
        
        if st.button(f"📊 {st.session_state.day}일차 장 마감 및 결과 정산"):
            prev_wealth = total_wealth
            result_code, next_total, next_cash, next_portfolio, updated_prices, result_table = process_day_end(
                st.session_state.current_money,
                st.session_state.portfolio,
                user_sell_amounts,
                user_buy_amounts,
                st.session_state.daily_news,
                st.session_state.stock_prices
            )
            
            if result_code == "ERROR_EXCEED_CASH":
                st.error("⚠️ 보유 현금 + 당일 매도 확보 현금보다 총 매수 신청 금액이 많습니다! 입력 금액을 조정해 주세요.")
            else:
                # 정산 결과 저장 및 상태 전환 후 즉시 화면 갱신
                st.session_state.last_report = {
                    "day": st.session_state.day,
                    "prev_wealth": prev_wealth,
                    "next_total": next_total,
                    "next_cash": next_cash,
                    "result_table": result_table,
                    "news_snapshot": st.session_state.daily_news.copy()
                }
                st.session_state.current_money = next_cash
                st.session_state.portfolio = next_portfolio
                st.session_state.stock_prices = updated_prices
                st.session_state.is_settled = True
                st.rerun()

    # [상태 B] 장 마감 정산 완료 -> 리포트 확인 및 다음 날 이동 화면
    else:
        report = st.session_state.last_report
        st.subheader(f"📋 {report['day']}일차 장 마감 정산 리포트")
        
        r_col1, r_col2 = st.columns(2)
        r_col1.metric("장 마감 총 자산", f"{report['next_total']:,}원", f"{report['next_total'] - report['prev_wealth']:+,}원")
        r_col2.metric("남은 현금 잔고", f"{report['next_cash']:,}원")
        
        st.write("### 🏢 종목별 뉴스 결과 및 주가 변동 현황")
        st.table(report["result_table"])
        
        with st.expander("💡 오늘의 종목별 경제 해설 모음", expanded=True):
            for s in stock_names:
                st.write(f"- **{s}** ({report['news_snapshot'][s]['news_type']}): {report['news_snapshot'][s]['explanation']}")
                
        st.divider()
        
        btn_label = "▶️ 다음 날로 넘어가기" if st.session_state.day < 3 else "🏆 최종 성적표 확인하기"
        if st.button(btn_label):
            st.session_state.day += 1
            st.session_state.is_settled = False
            if st.session_state.day <= 3:
                st.session_state.daily_news = {
                    s: random.choice(stock_news_pool[s]) for s in stock_names
                }
            st.rerun()

# 3일차 종료 후 최종 성적표
else:
    st.balloons()
    st.subheader("🏆 3일 서바이벌 모의투자 최종 성적표")
    
    final_total_wealth = int(st.session_state.current_money + sum(st.session_state.portfolio.values()))
    total_return = ((final_total_wealth - 1000000) / 1000000) * 100
    
    st.metric("최종 총 자산", f"{final_total_wealth:,}원", f"총 누적 수익률: {total_return:+.2f}%")
    
    if final_total_wealth >= 1500000:
        st.success("🏆 **등급: 워런 버핏 급 전설의 투자자!**\n\n유연한 부분 매도와 맞춤 재투자로 자산을 극대화하셨습니다!")
    elif final_total_wealth >= 1000000:
        st.info("📈 **등급: 안정적인 수익을 거둔 스마트 개미!**\n\n원금을 잘 지키며 현명하게 자산을 관리하셨습니다.")
    else:
        st.error("💸 **등급: 찌라시에 흔들린 개미…**\n\n변동성에 아쉽게 자산을 잃었습니다. 다시 도전해 보세요!")
        
    if st.button("🔄 게임 다시 시작하기"):
        st.session_state.day = 1
        st.session_state.current_money = 1000000
        st.session_state.portfolio = {}
        st.session_state.stock_prices = {
            "K-반도체": 50000,
            "친환경 배터리": 40000,
            "바이오제약": 30000,
            "종합 상사": 20000
        }
        st.session_state.is_settled = False
        st.session_state.last_report = None
        st.session_state.daily_news = {
            stock: random.choice(stock_news_pool[stock]) for stock in stock_names
        }
        st.rerun()
