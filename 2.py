import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from datetime import datetime

# === 설정 ===
FILE_NAME = '골마켓_실시간_시세.xlsx'
CHECK_INTERVAL = 60  # 60초마다 확인 (너무 빠르면 차단됨)

def get_post_details(post_url):
    """ 상세 페이지에서 정보 추출 (이전 코드와 동일) """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(post_url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # 제목 추출
        title_tag = soup.select_one('.view_title .view_lefttit01') or soup.select_one('.view_tit') or soup.select_one('.subject')
        title = title_tag.get_text(strip=True) if title_tag else "제목못찾음"

        # 가격 추출
        price_tag = soup.select_one('.price') or soup.select_one('.view_price') or soup.select_one('.cost')
        if not price_tag:
             target_th = soup.find(string=lambda t: t and ('가격' in t or '금액' in t))
             if target_th:
                 next_td = target_th.parent.parent.find_next_sibling('td') if target_th.parent.name != 'td' else target_th.parent.find_next_sibling('td')
                 if next_td: price_tag = next_td

        price = price_tag.get_text(strip=True) if price_tag else "가격정보없음"

        return {'수집시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '물품명': title, '가격': price, 'URL': post_url}
    except:
        return None

def load_collected_urls():
    """ 기존 엑셀 파일이 있으면 이미 수집한 URL 목록을 가져옴 """
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            # URL 컬럼의 값들을 집합(Set)으로 반환 (중복 제거 및 빠른 검색)
            return set(df['URL'].tolist())
        except Exception as e:
            print(f"기존 파일 읽기 실패: {e}")
            return set()
    return set()

def monitor_golmarket():
    print(f"=== 골마켓 실시간 모니터링 시작 ===")
    print(f"파일명: {FILE_NAME}, 확인 주기: {CHECK_INTERVAL}초")

    # 1. 기존 데이터 로드 (중복 수집 방지)
    collected_urls = load_collected_urls()
    print(f"현재 수집된 게시글 수: {len(collected_urls)}개")

    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{current_time}] 신규 게시글 확인 중...")

            # 2. 목록 페이지(1페이지만) 접속
            url = 
