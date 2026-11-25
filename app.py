import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="3일 서바이벌 주식 모의투자", page_icon="📈")

# 2. 데이터 풀 정의 (거시경제 테마 + 종목별 뉴스 풀)
macro_events_pool = [
    {"title": "🇺🇸 미국 연준(Fed), 깜짝 기준금리 인하 단행!", "desc": "시중에 유동성이 풀리며 주식 시장 전체에 훈풍이 붑니다. (전 종목 +5% 보너스)", "bonus": 0.05},
    {"title": "🛢️ 중동 지정학적 위기로 국제 유가 및 환율 급등!", "desc": "시장 전반에 투자 심리가 위축되며 하방 압력이 커집니다. (전 종목 -5% 페널티)", "bonus": -0.05},
    {"title": "⚖️ 글로벌 증시, 주요 경제 지표 발표 앞두고 관망세", "desc": "시장 전체 변동은 없으며, 철저히 종목별 개별 뉴스에 따라 주가가 움직입니다. (시장 보정 0%)", "bonus": 0.00},
    {"title": "🚀 정부, 국내 증시 밸류업 프로그램 및 세제 혜택 발표!", "desc": "외국인 매수세가 유입되며 전체 시장이 활기를 띱니다. (전 종목 +3% 보너스)", "bonus": 0.03},
    {"title": "❄️ 글로벌 경기 침체(R의 공포) 경고등 점등", "desc": "안전자산 선호 심리가 강해지며 증시 전반이 흔들립니다. (전 종목 -3% 페널티)", "bonus": -0.03}
]

stock_news_pool = {
    "K-반도체": [
        {"headline": "글로벌 빅테크 기업들, 차세대 AI 서버 구축 위해 한국산 메모리 확보 총력전", "news_type": "진짜 호재", "hint": "빅테크들의 실제 발주 계약서가 확인된 100% 팩트 호재입니다.", "explanation": "AI 서버용 반도체 수요 급증이 실적 개선으로 직결된 정석적인 호재였습니다."},
        {"headline": "반도체 장비 반입 지연 및 단기 공급 과잉 우려 제기", "news_type": "진짜 악재", "hint": "주요 증권사 리포트에서도 이번 분기 실적 하향을 경고하고 있습니다.", "explanation": "일시적인 공급 과잉과 장비 지연 우려로 주가가 하방 압력을 받았습니다."},
        {"headline": "구형 메모리 감산 선언… 단기 매출 감소 우려에도 재고 소진 및 가격 반등 기대", "news_type": "역발상 호재", "hint": "과거 반도체 사이클에서도 '감산 발표' 직후가 항상 주가 바닥이었습니다!", "explanation": "감산 발표는 당장 매출이 줄어 악재처럼 보이지만, 공급 조절로 반도체 가격 반등을 이끄는 대표적 '역발상 호재'였습니다."}
    ],
    "친환경 배터리": [
        {"headline": "정부, 전기차 보조금 예산 삭감 검토… 대신 내연기관차 도심 진입 강력 규제 발표!", "news_type": "역발상 호재", "hint": "보조금보다 '내연기관 진입 금지'가 완성차 업체들에 훨씬 강력한 압박입니다.", "explanation": "보조금 삭감만 보고 팔았다면 손해! 내연기관 규제 강화가 장기적으로 배터리 수요 폭증을 부르는 '역발상 호재'였습니다."},
        {"headline": "주요 배터리 셀 제조사 화재 사고 여파로 대규모 리콜 사태 발생", "news_type": "진짜 악재", "hint": "실제 리콜 충당금 규모가 영업이익의 절반을 넘어설 전망입니다.", "explanation": "품질 이슈와 리콜 비용 발생으로 단기 실적 악화가 불가피해졌습니다."},
        {"headline": "차세대 전고체 배터리 핵심 특허 등록 및 글로벌 완성차 업체와 대규모 공급 계약", "news_type": "진짜 호재", "hint": "공시로 확정된 대규모 장기 공급 계약입니다.", "explanation": "차세대 기술 선점과 장기 수주 확보가 동시에 이루어진 강력한 호재였습니다."}
    ],
    "바이오제약": [
        {"headline": "바이오제약 대표 해외 도피설 및 회계 부정 루머 SNS 확산 (진위 불명)", "news_type": "가짜 찌라시", "hint": "취재 결과 대표는 현재 국내 연구소에서 정상 근무 중입니다. 공매도 세력의 루머입니다!", "explanation": "전형적인 공포 조장용 가짜 찌라시였습니다! 근거 없는 소문에 패닉셀한 투자자들만 손실을 보았습니다."},
        {"headline": "개발 중인 혁신 신약이 글로벌 임상 3상에서 뛰어난 효능 입증", "news_type": "진짜 호재", "hint": "글로벌 학회에서 데이터가 공식 검증되었습니다.", "explanation": "신약 가치가 급상승하며 대규모 기술 수출 기대감이 증폭되었습니다."},
        {"headline": "주력 파이프라인 신약, 해외 보건당국으로부터 품목 허가 보완 요구(CRL) 통보", "news_type": "진짜 악재", "hint": "단순 서류 보완이 아니라 추가 임상 시험이 요구되는 심각한 상황입니다.", "explanation": "출시 지연과 추가 임상 비용 발생이 불가피해지며 투자 심리가 크게 위축되었습니다."}
    ],
    "종합 상사": [
        {"headline": "국제 원자재 가격 급등 및 해상 물류비 상승으로 수출 기업 채산성 악화 우려", "news_type": "진짜 악재", "hint": "운임 지수 폭등으로 실제 마진율이 크게 훼손되고 있습니다.", "explanation": "물류비와 원자재 부담이 커지면서 종합 상사의 단기 수익성이 크게 악화되었습니다."},
        {"headline": "자원 개발 유전에서 초대형 원유 매장지 발견 및 독점 계약 체결", "news_type": "진짜 호재", "hint": "실제 시추 탐사 결과 상업성이 매우 높은 대형 유전으로 확인되었습니다.", "explanation": "자원 개발 가치가 폭등하며 안정적인 현금 창출원이 확보되었습니다."},
        {"headline": "익명 커뮤니티에 '종합 상사 대규모 파생상품 손실 발생' 출처 불명 글 게시", "news_type": "가짜 찌라시", "hint": "회사 측의 파생상품 한도 조회 결과 특이사항이 전혀 없는 헛소문입니다!", "explanation": "공시나 공식 확인이 전혀 없는 익명 커뮤니티발 찌라시로, 단기 흔들기 후 진정되는 패턴이었습니다."}
    ],
    "🔥 퀀텀 AI 벤처": [
        {"headline": "양자컴퓨팅 기반 초거대 AI 상용화 세계 최초 성공! 글로벌 빅테크 인수 제안설", "news_type": "대박 호재", "hint": "실제 시연회가 성공적으로 끝났으며 글로벌 기업들의 비밀유지계약(NDA)이 확인되었습니다!", "explanation": "게임 체인저 기술 입증으로 주가가 하루 만에 +50% 폭등하는 초대박을 터뜨렸습니다!"},
        {"headline": "외부 회계법인 '감사의견 거절' 및 경영진 횡령 혐의 포착, 거래소 실질심사 돌입", "news_type": "상장폐지", "hint": "⚠️ 경고! 거래소 공식 공시로 확인된 치명적 사유입니다. 즉시 전량 매도하지 않으면 휴지조각이 됩니다!", "explanation": "치명적인 회계 부정과 감사의견 거절로 거래소에서 즉시 '상장폐지' 처리되어 주식이 0원이 되었습니다."},
        {"headline": "핵심 개발진 전원 퇴사 및 AI 서버 해킹 피해 소문 온라인 급속 확산", "news_type": "가짜 찌라시", "hint": "개발진 전원 정상 출근 중이며 서버 보안 점검 결과 이상 무! 경쟁사의 악의적 루머입니다.", "explanation": "테마주 특성을 노린 공포 조장용 가짜 찌라시였습니다. 소문에 속아 팔았다면 아까운 손실을 보았습니다."}
    ]
}

# 중복 없는 3일 치 뉴스 & 거시경제 덱 초기화 함수
def init_game_decks(names):
    news_deck = {}
    daily_news = {}
    for s in names:
        items = stock_news_pool[s].copy()
        random.shuffle(items)
        daily_news[s] = items.pop()
        news_deck[s] = items
        
    macro_items = macro_events_pool.copy()
    random.shuffle(macro_items)
    today_macro = macro_items.pop()
    
    return news_deck, daily_news, macro_items, today_macro

# 새 게임 상태 초기화 함수
def reset_game_state():
    st.session_state.day = 1
    st.session_state.current_money = 1000000
    st.session_state.portfolio = {}
    st.session_state.stock_prices = {
        "K-반도체": 50000,
        "친환경 배터리": 40000,
        "바이오제약": 30000,
        "종합 상사": 20000,
        "🔥 퀀텀 AI 벤처": 10000
    }
    st.session_state.delisted_stocks = []    # 상장폐지된 종목 리스트
    st.session_state.is_settled = False
    st.session_state.last_report = None
    st.session_state.score_recorded = False
    
    # 특수 아이템 상태
    st.session_state.hint_used = False
    st.session_state.hint_target = None
    
    names = list(st.session_state.stock_prices.keys())
    (
        st.session_state.remaining_news,
        st.session_state.daily_news,
        st.session_state.remaining_macros,
        st.session_state.today_macro
    ) = init_game_decks(names)

# 3. 세션 상태 최초 초기화
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "intro"
    st.session_state.player_name = ""
    st.session_state.leaderboard = []
    reset_game_state()

all_stock_names = list(st.session_state.stock_prices.keys())
active_stock_names = [s for s in all_stock_names if s not in st.session_state.delisted_stocks]

# 4. 포트폴리오 정산 및 매매 처리 함수
def process_day_end(current_money, portfolio, user_sell_amounts, user_buy_amounts, daily_news, stock_prices, today_macro, active_stocks):
    market_table = []
    stock_new_prices = stock_prices.copy()
    stock_change_rates = {}
    newly_delisted = []
    macro_bonus = today_macro["bonus"]
    
    # 1단계: 활성 종목별 주가 변동률 계산 (상장폐지 판정 포함)
    for name in active_stocks:
        base_price = stock_prices[name]
        n_type = daily_news[name]["news_type"]
        
        if n_type == "상장폐지":
            stock_change_rates[name] = -1.00
            stock_new_prices[name] = 0
            newly_delisted.append(name)
        elif n_type == "대박 호재":
            total_rate = round(0.50 + macro_bonus, 4)
            stock_change_rates[name] = total_rate
            stock_new_prices[name] = int(base_price * (1 + total_rate))
        else:
            if n_type == "진짜 호재":
                base_rate = 0.20
            elif n_type == "역발상 호재":
                base_rate = 0.15
            elif n_type == "가짜 찌라시":
                base_rate = -0.10
            else: # 진짜 악재
                base_rate = -0.20
                
            total_rate = round(base_rate + macro_bonus, 4)
            stock_change_rates[name] = total_rate
            stock_new_prices[name] = int(base_price * (1 + total_rate))
        
    # 2단계: 장 시작 전 매도 처리 (상장폐지 뉴스라도 당일 매도하면 전액 방어 성공)
    temp_portfolio = portfolio.copy()
    cash_from_sell = 0
    for stock_name, sell_amt in user_sell_amounts.items():
        if stock_name in temp_portfolio and sell_amt > 0:
            actual_sell = min(sell_amt, temp_portfolio[stock_name])
            cash_from_sell += actual_sell
            temp_portfolio[stock_name] -= actual_sell
            if temp_portfolio[stock_name] <= 10:
                del temp_portfolio[stock_name]

    # 3단계: 잔여 주식 변동 반영
    updated_portfolio = {}
    for stock_name, remaining_amt in temp_portfolio.items():
        rate = stock_change_rates[stock_name]
        if rate <= -1.00:
            # 상장폐지 -> 투자금 0원 소멸
            continue
        updated_portfolio[stock_name] = int(remaining_amt * (1 + rate))

    # 4단계: 매수 가능 금액 확인 및 신규 매수 반영
    total_available_cash = int(current_money + cash_from_sell)
    total_requested_buy = sum(user_buy_amounts.values())
    
    if total_requested_buy > total_available_cash:
        return "ERROR_EXCEED_CASH", 0, 0, {}, {}, [], [], []
        
    cash_after_buy = int(total_available_cash - total_requested_buy)
    
    invested_principal = temp_portfolio.copy()
    for stock_name, buy_amt in user_buy_amounts.items():
        if buy_amt > 0:
            invested_principal[stock_name] = invested_principal.get(stock_name, 0) + buy_amt
            rate = stock_change_rates[stock_name]
            if rate <= -1.00:
                # 상장폐지 종목 매수 시 0원 소멸
                continue
            valued_buy = int(buy_amt * (1 + rate))
            updated_portfolio[stock_name] = updated_portfolio.get(stock_name, 0) + valued_buy

    # 5단계: 추가 특수 룰 정산 (CMA 현금 이자 & 야수의 심장 보너스 & 상장폐지 알림)
    special_events_log = []
    
    for d_stock in newly_delisted:
        lost_amt = invested_principal.get(d_stock, 0)
        if lost_amt > 0:
            special_events_log.append(f"💀 **[상장폐지 충격!]** [{d_stock}]가 상장폐지되어 투자금 **{lost_amt:,}원**이 전액 소멸되었습니다!")
        else:
            special_events_log.append(f"💀 **[상장폐지 발생]** [{d_stock}]가 상장폐지되어 거래소에서 퇴출되었습니다. (보유 주식 없음)")

    # CMA 파킹통장 이자 (남은 현금의 1%)
    cma_interest = int(cash_after_buy * 0.01)
    if cma_interest > 0:
        cash_after_buy += cma_interest
        special_events_log.append(f"🏦 **CMA 파킹통장 이자 (+1%):** 보유 현금에 대한 이자 **{cma_interest:,}원**이 지급되었습니다.")
        
    # 야수의 심장 집중 투자 보너스
    pre_market_total = cash_after_buy - cma_interest + sum(invested_principal.values())
    if pre_market_total > 0:
        for s_name, principal in invested_principal.items():
            if s_name not in newly_delisted and (principal / pre_market_total) >= 0.70 and stock_change_rates[s_name] > 0:
                beast_bonus = int(principal * 0.05)
                updated_portfolio[s_name] += beast_bonus
                special_events_log.append(f"🔥 **'야수의 심장' 집중 투자 보너스:** [{s_name}]에 70% 이상 승부수를 띄워 **{beast_bonus:,}원**의 추가 수익을 얻었습니다!")

    # 6단계: 결과 테이블 생성
    for name in active_stocks:
        b_price = stock_prices[name]
        n_price = stock_new_prices[name]
        c_rate = stock_change_rates[name]
        
        if name in newly_delisted:
            status_str = "💀 상장폐지 (0원)"
            price_str = "0원 (폐지)"
            rate_str = "-100.0%"
        else:
            status_str = f"보유 중 ({updated_portfolio[name]:,}원)" if name in updated_portfolio else "미보유"
            price_str = f"{n_price:,}원"
            rate_str = f"{c_rate * 100:+.1f}%"
            
        market_table.append({
            "종목명": name,
            "오늘의 뉴스": daily_news[name]["headline"][:22] + "...",
            "뉴스 성격": daily_news[name]["news_type"],
            "기초 주가": f"{b_price:,}원",
            "변동 후 주가": price_str,
            "최종 등락률": rate_str,
            "내 포트폴리오": status_str
        })
        
    total_portfolio_value = sum(updated_portfolio.values())
    total_assets = int(cash_after_buy + total_portfolio_value)
    
    return "SUCCESS", total_assets, cash_after_buy, updated_portfolio, stock_new_prices, market_table, special_events_log, newly_delisted


# ==========================================
# 화면 1: 시작하기 화면 (Intro)
# ==========================================
if st.session_state.game_stage == "intro":
    st.title("📈 행간을 읽어라! 3일 서바이벌 주식 모의투자")
    st.markdown("""
    ### 🎯 게임 규칙 및 전략 포인트
    * **기본 목표:** 시드머니 **100만 원**으로 **3일** 동안 최고의 수익률을 기록해 명예의 전당 1위에 오르세요!
    * **1️⃣ 거시경제(시장) 테마:** 매일 아침 금리·환율·정책 등 **전 종목에 영향을 주는 시장 변수**가 발표됩니다.
    * **2️⃣ 4대 우량주 뉴스:** 
      * 🟢 **진짜 호재 (+20%)** / 🔴 **진짜 악재 (-20%)**
      * 🔵 **역발상 호재 (+15%):** 겉보기엔 악재 같지만 행간을 읽으면 기회인 반전 뉴스
      * 🟡 **가짜 찌라시 (-10%):** 공포를 조장하는 루머
    * **3️⃣ 하이리스크 테마주 (`🔥 퀀텀 AI 벤처`):**
      * 대박 호재 적중 시 **+50% 폭등**하지만, **💀 치명적 악재(상장폐지)** 뉴스를 피하지 못하면 투자금이 **0원(휴지조각)**이 됩니다!
    * **4️⃣ 히든 전략 요소:**
      * 🔍 **유료 팩트체크 찬스 (게임당 1회):** 정보 이용료 **3만 원**으로 선택한 종목 뉴스의 진위를 미리 파악합니다.
      * 🏦 **CMA 현금 이자 (+1%):** 남은 현금에 매일 이자가 붙습니다.
      * 🔥 **야수의 심장 보너스 (+5%):** 한 종목에 자산의 **70% 이상** 집중 투자 후 상승 시 추가 수익을 얻습니다!
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
    
    # 사이드바 계좌 및 아이템 정보
    st.sidebar.header(f"👤 {st.session_state.player_name}님의 계좌")
    st.sidebar.metric("현재 진행 일차", f"{st.session_state.day}일차 / 총 3일")
    total_wealth = int(st.session_state.current_money + sum(st.session_state.portfolio.values()))
    st.sidebar.metric("현재 총 자산", f"{total_wealth:,}원")
    st.sidebar.write(f"💵 보유 현금: {st.session_state.current_money:,}원")
    
    hint_status = "❌ 사용 완료" if st.session_state.hint_used else "✅ 사용 가능 (1회)"
    st.sidebar.write(f"🔍 팩트체크 찬스: **{hint_status}**")

    if st.session_state.portfolio:
        st.sidebar.write("📌 **보유 중인 종목:**")
        for s_name, s_val in st.session_state.portfolio.items():
            st.sidebar.write(f"- {s_name}: {s_val:,}원")
    else:
        st.sidebar.info("보유 중인 주식 없음 (현금 100%)")

    if st.session_state.delisted_stocks:
        st.sidebar.error(f"💀 상장폐지 퇴출: {', '.join(st.session_state.delisted_stocks)}")

    # [상태 A] 장 마감 전 -> 거시경제 확인, 팩트체크, 매매 입력
    if not st.session_state.is_settled:
        macro = st.session_state.today_macro
        st.warning(f"🌐 **[오늘의 거시경제 특보] {macro['title']}**\n\n{macro['desc']}")
        
        # 유료 팩트체크(내부자 리포트) 찬스 박스
        with st.container(border=True):
            st.markdown("#### 🔍 긴급 팩트체크 찬스 (게임당 단 1회 / 정보 이용료 30,000원)")
            if not st.session_state.hint_used:
                if st.session_state.current_money >= 30000:
                    h_col1, h_col2 = st.columns([3, 1])
                    with h_col1:
                        selected_hint_stock = st.selectbox("진위를 확인할 종목 선택:", active_stock_names, label_visibility="collapsed")
                    with h_col2:
                        if st.button("3만 원 결제 및 확인", use_container_width=True):
                            st.session_state.current_money -= 30000
                            st.session_state.hint_used = True
                            st.session_state.hint_target = (st.session_state.day, selected_hint_stock)
                            st.rerun()
                else:
                    st.caption("보유 현금이 30,000원 미만이어서 팩트체크를 이용할 수 없습니다.")
            else:
                if st.session_state.hint_target and st.session_state.hint_target[0] == st.session_state.day:
                    target_s = st.session_state.hint_target[1]
                    st.success(f"🕵️ **[{target_s}] 팩트체크 리포트:** {st.session_state.daily_news[target_s]['hint']}")
                else:
                    st.caption("이미 이전 일차에 팩트체크 찬스를 사용하셨습니다.")

        st.subheader(f"📅 [ {st.session_state.day}일차 ] 종목별 경제 뉴스 속보 & 맞춤 매매")
        
        user_sell_amounts = {}
        user_buy_amounts = {}
        
        for stock in active_stock_names:
            news = st.session_state.daily_news[stock]
            risk_tag = " [⚠️ 고위험 테마주: +50% 또는 상장폐지]" if stock == "🔥 퀀텀 AI 벤처" else ""
            with st.expander(f"📢 [{stock}] 오늘의 뉴스 (현재가: {st.session_state.stock_prices[stock]:,}원){risk_tag}", expanded=True):
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
            result_code, next_total, next_cash, next_portfolio, updated_prices, result_table, special_logs, newly_delisted = process_day_end(
                st.session_state.current_money,
                st.session_state.portfolio,
                user_sell_amounts,
                user_buy_amounts,
                st.session_state.daily_news,
                st.session_state.stock_prices,
                st.session_state.today_macro,
                active_stock_names
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
                    "news_snapshot": st.session_state.daily_news.copy(),
                    "macro_snapshot": st.session_state.today_macro.copy(),
                    "special_logs": special_logs,
                    "evaluated_stocks": active_stock_names.copy()
                }
                st.session_state.current_money = next_cash
                st.session_state.portfolio = next_portfolio
                st.session_state.stock_prices = updated_prices
                st.session_state.delisted_stocks.extend(newly_delisted)
                st.session_state.is_settled = True
                st.rerun()

    # [상태 B] 장 마감 정산 완료 -> 리포트 확인 및 다음 날 이동
    else:
        report = st.session_state.last_report
        st.subheader(f"📋 {report['day']}일차 장 마감 정산 리포트")
        st.caption(f"적용된 시장 변수: {report['macro_snapshot']['title']} ({report['macro_snapshot']['bonus']*100:+.0f}%)")
        
        r_col1, r_col2 = st.columns(2)
        r_col1.metric("장 마감 총 자산", f"{report['next_total']:,}원", f"{report['next_total'] - report['prev_wealth']:+,}원")
        r_col2.metric("남은 현금 잔고", f"{report['next_cash']:,}원")
        
        if report["special_logs"]:
            for log in report["special_logs"]:
                if "💀" in log:
                    st.error(log)
                else:
                    st.success(log)
        
        st.write("### 🏢 종목별 뉴스 결과 및 주가 변동 현황")
        st.table(report["result_table"])
        
        with st.expander("💡 오늘의 종목별 경제 해설 모음", expanded=True):
            for s in report["evaluated_stocks"]:
                st.write(f"- **{s}** ({report['news_snapshot'][s]['news_type']}): {report['news_snapshot'][s]['explanation']}")
                
        st.divider()
        
        btn_label = "▶️ 다음 날로 넘어가기" if st.session_state.day < 3 else "🏆 최종 성적표 및 랭킹 확인하기"
        if st.button(btn_label, use_container_width=True):
            if st.session_state.day < 3:
                st.session_state.day += 1
                st.session_state.is_settled = False
                # 살아남은 종목들에 대해서만 다음 날 뉴스 꺼내기
                remaining_active = [s for s in all_stock_names if s not in st.session_state.delisted_stocks]
                st.session_state.daily_news = {
                    s: st.session_state.remaining_news[s].pop() for s in remaining_active
                }
                st.session_state.today_macro = st.session_state.remaining_macros.pop()
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
    
    if final_total_wealth >= 1800000:
        grade_title = "전설의 투자자"
        st.success("🏆 **등급: 워런 버핏 급 전설의 투자자!**\n\n거시경제 흐름과 테마주의 폭발력까지 완벽히 지배하셨습니다!")
    elif final_total_wealth >= 1000000:
        grade_title = "스마트 개미"
        st.info("📈 **등급: 안정적인 수익을 거둔 스마트 개미!**\n\n원금을 잘 지키며 현명하게 자산을 불렸습니다.")
    else:
        grade_title = "흔들린 개미"
        st.error("💸 **등급: 찌라시와 상장폐지에 흔들린 개미…**\n\n변동성과 함정에 아쉽게 자산을 잃었습니다.")

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
