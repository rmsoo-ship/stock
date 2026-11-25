import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="3일 서바이벌 주식 모의투자", page_icon="📈")

# 2. 종목별 뉴스 풀 (3일 동안 중복 없이 나오도록 종목당 3개 이상 구성)
stock_news_pool = {
    "K-반도체": [
        {"headline": "글로벌 빅테크 기업들, 차세대 AI 서버 구축 위해 한국산 메모리 확보 총력전", "news_type": "진짜 호재", "explanation": "AI 서버용 반도체 수요 급증이 실적 개선으로 직결된 정석적인 호재였습니다."},
        {"headline": "반도체 장비 반입 지연 및 단기 공급 과잉 우려 제기", "news_type": "진짜 악재", "explanation": "일시적인 공급 과잉과 장비 지연 우려로 주가가 하방 압력을 받았습니다."},
        {"headline": "구형 메모리 감산 선언… 단기 매출 감소 우려에도 재고 소진 및 가격 반등 기대", "news_type": "역발상 호재", "explanation": "감산 발표는 당장 매출이 줄어 악재처럼 보이지만, 공급 조절로 반도체 가격 반등을 이끄는 대표적 '역발상 호재'였습니다."}
    ],
    "친환경 배터리": [
        {"headline": "정부, 전기차 보조금 예산 삭감 검토… 대신 내연기관차 도심 진입 강력 규제 발표!", "news_type": "역발상 호재", "explanation": "보조금 삭감만 보고 팔았다면 손해! 내연기관 규제 강화가 장기적으로 배터리 수요 폭증을 부르는 '역발상 호재'였습니다."},
        {"headline": "주요 배터리 셀 제조사 화재 사고 여파로 대규모 리콜 사태 발생", "news_type": "진짜 악재", "explanation": "품질 이슈와 리콜 비용 발생으로 단기 실적 악화가 불가피해졌습니다."},
        {"headline": "차세대 전고체 배터리 핵심 특허 등록 및 글로벌 완성차 업체와 대규모 공급 계약", "news_type": "진짜 호재", "explanation": "차세대 기술 선점과 장기 수주 확보가 동시에 이루어진 강력한 호재였습니다."}
    ],
    "바이오제약": [
        {"headline": "바이오제약 대표 해외 도피설 및 회계 부정 루머 SNS 확산 (진위 불명)", "news_type": "가짜 찌라시", "explanation": "전형적인 공포 조장용 가짜 찌라시였습니다! 근거 없는 소문에 패닉셀한 투자자들만 손실을 보았습니다."},
        {"headline": "개발 중인 혁신 신약이 글로벌 임상 3상에서 뛰어난 효능 입증", "news_type": "진짜 호재", "explanation": "신약 가치가 급상승하며 대규모 기술 수출 기대감이 증폭되었습니다."},
        {"headline": "주력 파이프라인 신약, 해외 보건당국으로부터 품목 허가 보완 요구(CRL) 통보", "news_type": "진짜 악재", "explanation": "출시 지연과 추가 임상 비용 발생이 불가피해지며 투자 심리가 크게 위축되었습니다."}
    ],
    "종합 상사": [
        {"headline": "국제 원자재 가격 급등 및 해상 물류비 상승으로 수출 기업 채산성 악화 우려", "news_type": "진짜 악재", "explanation": "물류비와 원자재 부담이 커지면서 종합 상사의 단기 수익성이 크게 악화되었습니다."},
        {"headline": "자원 개발 유전에서 초대형 원유 매장지 발견 및 독점 계약 체결", "news_type": "진짜 호재", "explanation": "자원 개발 가치가 폭등하며 안정적인 현금 창출원이 확보되었습니다."},
        {"headline": "익명 커뮤니티에 '종합 상사 대규모 파생상품 손실 발생' 출처 불명 글 게시", "news_type": "가짜 찌라시", "explanation": "공시나 공식 확인이 전혀 없는 익명 커뮤니티발 찌라시로, 단기 흔들기 후 진정되는 패턴이었습니다."}
    ]
}

# 중복 없는 3일 치 뉴스 덱 초기화 함수
def init_news_deck(names):
    deck = {}
    daily = {}
    for s in names:
        items = stock_news_pool[s].copy()
        random.shuffle(items)
        daily[s] = items.pop()
        deck[s] = items
    return deck, daily

# 새 게임 상태 초기화 함수
def reset_game_state():
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
    st.session_state.score_recorded = False  # 랭킹 중복 등록 방지 플래그
    names = list(st.session_state.stock_prices.keys())
    st.session_state.remaining_news, st.session_state.daily_news = init_news_deck(names)

# 3. 세션 상태 최초 초기화
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "intro"    # "intro" -> "playing" -> "finished"
    st.session_state.player_name = ""
    st.session_state.leaderboard = []        # [{"이름": ..., "최종 자산": ..., "수익률": ..., "등급": ...}]
    reset_game_state()

stock_names = list(st.session_state.stock_prices.keys())

# 4. 포트폴리오 정산 및 매매 처리 함수
def process_day_end(current_money, portfolio, user_sell_amounts, user_buy_amounts, daily_news, stock_prices):
    market_table = []
    stock_new_prices = {}
    stock_change_rates = {}
    
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
        
    temp_portfolio = portfolio.copy()
    cash_from_sell = 0
    
    for stock_name, sell_amt in user_sell_amounts.items():
        if stock_name in temp_portfolio and sell_amt > 0:
            current_holding_val = temp_portfolio[stock_name]
            actual_sell = min(sell_amt, current_holding_val)
            cash_from_sell += actual_sell
            
            temp_portfolio[stock_name] -= actual_sell
            if temp_portfolio[stock_name] <= 10:
                del temp_portfolio[stock_name]

    updated_portfolio = {}
    for stock_name, remaining_amt in temp_portfolio.items():
        rate = stock_change_rates[stock_name]
        updated_portfolio[stock_name] = int(remaining_amt * (1 + rate))

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


# ==========================================
# 화면 1: 시작하기 화면 (Intro)
# ==========================================
if st.session_state.game_stage == "intro":
    st.title("📈 행간을 읽어라! 3일 서바이벌 주식 모의투자")
    st.markdown("""
    ### 🎯 게임 규칙 안내
    * **시드머니:** **100만 원**으로 시작하여 총 **3일** 동안 투자를 진행합니다.
    * **매매 방식:** 매일 발표되는 종목별 뉴스를 읽고, **부분/전량 매도** 및 **맞춤 매수**로 포트폴리오를 구성하세요.
    * **뉴스의 4가지 함정과 기회:**
      * 🟢 **진짜 호재 (+20%):** 실적과 기업 가치 상승으로 이어지는 정석 호재
      * 🔵 **역발상 호재 (+15%):** 겉보기엔 악재 같지만 행간을 읽으면 기회인 뉴스
      * 🟡 **가짜 찌라시 (-10%):** 공포를 조장하는 근거 없는 루머 (패닉셀 주의!)
      * 🔴 **진짜 악재 (-20%):** 실제 기업 가치와 수익성이 훼손되는 악재
    """)
    
    st.divider()
    
    with st.form("start_game_form"):
        name_input = st.text_input("👤 참가자 이름(또는 닉네임)을 입력하세요:", placeholder="예: 김투자")
        submitted = st.form_submit_button("🚀 모의투자 시작하기", use_container_width=True)
        
        if submitted:
            if name_input.strip() == "":
                st.warning("⚠️ 시작하기 전에 이름을 입력해 주세요!")
            else:
                st.session_state.player_name = name_input.strip()
                reset_game_state()
                st.session_state.game_stage = "playing"
                st.rerun()

    # 이전 참가자 기록이 있다면 시작 화면 하단에도 명예의 전당 표시
    if st.session_state.leaderboard:
        st.divider()
        st.subheader("🏆 현재 명예의 전당 (실시간 랭킹)")
        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["raw_wealth"], reverse=True)
        display_board = [
            {
                "순위": f"{idx + 1}위",
                "이름": row["이름"],
                "최종 자산": f"{row['raw_wealth']:,}원",
                "수익률": f"{row['return_rate']:+.2f}%",
                "등급": row["등급"]
            }
            for idx, row in enumerate(sorted_board)
        ]
        st.table(display_board)


# ==========================================
# 화면 2: 게임 진행 화면 (Playing)
# ==========================================
elif st.session_state.game_stage == "playing":
    st.title("📈 행간을 읽어라! 3일 서바이벌 주식 모의투자")
    
    # 사이드바 계좌 정보
    st.sidebar.header(f"👤 {st.session_state.player_name}님의 계좌")
    st.sidebar.metric("현재 진행 일차", f"{st.session_state.day}일차 / 총 3일")
    total_wealth = int(st.session_state.current_money + sum(st.session_state.portfolio.values()))
    st.sidebar.metric("현재 총 자산", f"{total_wealth:,}원")
    st.sidebar.write(f"💵 보유 현금: {st.session_state.current_money:,}원")

    if st.session_state.portfolio:
        st.sidebar.write("📌 **보유 중인 종목:**")
        for s_name, s_val in st.session_state.portfolio.items():
            st.sidebar.write(f"- {s_name}: {s_val:,}원")
    else:
        st.sidebar.info("보유 중인 주식 없음 (현금 100%)")

    # [상태 A] 장 마감 전 -> 뉴스 분석 및 매매 입력
    if not st.session_state.is_settled:
        st.subheader(f"📅 [ {st.session_state.day}일차 ] 종목별 경제 뉴스 속보 & 맞춤 매매")
        st.write("뉴스의 행간을 읽고, 보유 주식은 **부분/전량 매도**하거나 확보될 현금으로 **신규/추가 매수**하세요!")
        
        user_sell_amounts = {}
        user_buy_amounts = {}
        
        for stock in stock_names:
            news = st.session_state.daily_news[stock]
            with st.expander(f"📢 [{stock}] 오늘의 뉴스 및 거래 (현재가: {st.session_state.stock_prices[stock]:,}원)", expanded=True):
                st.info(f"**헤드라인:** {news['headline']}")
                
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
        
        if st.button(f"📊 {st.session_state.day}일차 장 마감 및 결과 정산", use_container_width=True):
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

    # [상태 B] 장 마감 정산 완료 -> 리포트 확인 및 다음 날 이동
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
        
        btn_label = "▶️ 다음 날로 넘어가기" if st.session_state.day < 3 else "🏆 최종 성적표 및 랭킹 확인하기"
        if st.button(btn_label, use_container_width=True):
            if st.session_state.day < 3:
                st.session_state.day += 1
                st.session_state.is_settled = False
                st.session_state.daily_news = {
                    s: st.session_state.remaining_news[s].pop() for s in stock_names
                }
            else:
                st.session_state.game_stage = "finished"
            st.rerun()


# ==========================================
# 화면 3: 최종 성적표 및 명예의 전당 랭킹 (Finished)
# ==========================================
elif st.session_state.game_stage == "finished":
    st.balloons()
    st.title(f"🏆 {st.session_state.player_name}님의 최종 투자 성적표")
    
    final_total_wealth = int(st.session_state.current_money + sum(st.session_state.portfolio.values()))
    total_return = ((final_total_wealth - 1000000) / 1000000) * 100
    
    st.metric("최종 총 자산", f"{final_total_wealth:,}원", f"총 누적 수익률: {total_return:+.2f}%")
    
    if final_total_wealth >= 1500000:
        grade_title = "전설의 투자자"
        st.success("🏆 **등급: 워런 버핏 급 전설의 투자자!**\n\n유연한 부분 매도와 맞춤 재투자로 자산을 극대화하셨습니다!")
    elif final_total_wealth >= 1000000:
        grade_title = "스마트 개미"
        st.info("📈 **등급: 안정적인 수익을 거둔 스마트 개미!**\n\n원금을 잘 지키며 현명하게 자산을 관리하셨습니다.")
    else:
        grade_title = "흔들린 개미"
        st.error("💸 **등급: 찌라시에 흔들린 개미…**\n\n변동성에 아쉽게 자산을 잃었습니다. 다시 도전해 보세요!")

    # 랭킹 보드에 현재 플레이어 결과 자동 저장 (새로고침 시 중복 등록 방지)
    if not st.session_state.score_recorded:
        st.session_state.leaderboard.append({
            "이름": st.session_state.player_name,
            "raw_wealth": final_total_wealth,
            "return_rate": total_return,
            "등급": grade_title
        })
        st.session_state.score_recorded = True

    st.divider()
    st.subheader("🥇 명예의 전당 (실시간 자산 순위)")
    
    # 최종 자산 기준 내림차순 정렬
    sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x["raw_wealth"], reverse=True)
    
    ranking_table = []
    for idx, row in enumerate(sorted_board):
        rank_badge = "🥇 1위" if idx == 0 else ("🥈 2위" if idx == 1 else ("🥉 3위" if idx == 2 else f"{idx + 1}위"))
        ranking_table.append({
            "순위": rank_badge,
            "이름": row["이름"],
            "최종 총 자산": f"{row['raw_wealth']:,}원",
            "누적 수익률": f"{row['return_rate']:+.2f}%",
            "투자 등급": row["등급"]
        })
        
    st.table(ranking_table)
    
    st.divider()
    if st.button("🔄 새 플레이어로 처음부터 다시 하기", use_container_width=True):
        st.session_state.game_stage = "intro"
        st.session_state.player_name = ""
        reset_game_state()
        st.rerun()
