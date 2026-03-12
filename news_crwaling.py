# selenium 
from selenium import webdriver                                      # 웹 브라우저 제어 핵심 객체
from selenium.webdriver.common.by import By                         # 요소 찾기 기준
from selenium.webdriver.chrome.options import Options               # 크롬 옵션 설정
from selenium.webdriver.support.ui import WebDriverWait             # 명시적 대기
from selenium.webdriver.support import expected_conditions as EC    # 대기 조건
import time                                                         # 시간 관련 함수 (필요시)
import os                                                           # 운영체제 관련 함수
from tqdm import tqdm                                               # 진행 상황 표시
import pandas as pd                                                 # 데이터 처리
from datetime import datetime                                       # 날짜/시간 처리

# 현재 날짜 구하기 (파일명 및 폴더 생성에 사용)
today = datetime.now().strftime("%Y-%m-%d")

# 저장할 기본 경로와 서브 폴더 이름 지정
base_dir = r"C:\Users\campus1N012\Desktop\뉴스 크롤링"
folder_name = "Today_News"

# 최종 저장 경로 조합 (폴더가 없으면 생성)
save_path = os.path.join(base_dir, folder_name)
os.makedirs(save_path, exist_ok=True)

# 저장할 CSV 파일명 및 전체 경로 생성
filename = f"news_data_{today}.csv"
filepath = os.path.join(save_path, filename)

# 크롬 드라이버 실행 옵션 설정
options = Options()
# options.add_argument("--headless")  # 창 없이 백그라운드 실행 시 활성화
options.add_argument("--no-sandbox")  # 리눅스 샌드박스 관련 설정
options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 부족 문제 방지
options.add_argument("window-size=1920x1080")  # 브라우저 크기 지정
options.add_argument("--disable-gpu")  # GPU 비활성화 (headless 모드에서 필요)
options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시
options.add_argument("--disable-popup-blocking")  # 팝업 차단 해제
options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
options.add_argument("--disable-notifications")  # 웹 알림 비활성화
options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 탐지 우회
options.add_argument("--incognito")  # 시크릿 모드 실행
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36")  # 사용자 에이전트 설정
options.add_argument("--start-maximized")  # 최대화 상태로 시작
options.add_argument("--window-position=0,0")  # 창 위치 지정
options.add_argument("--disable-infobars")  # 'Chrome이 자동화 소프트웨어로 제어 중' 메시지 숨김
options.add_argument("--no-first-run")  # 첫 실행 화면 건너뜀
options.add_argument("--no-default-browser-check")  # 기본 브라우저 체크 안 함
options.add_argument("--enable-automation")  # 자동화 모드 활성화
options.add_argument("--password-store=basic")  # 비밀번호 저장 기본값 설정
options.add_argument("--disable-features=VizDisplayCompositor")  # 디스플레이 컴포지터 비활성화
options.add_argument("--disable-extensions-http-throttling")  # 확장 프로그램 HTTP 제한 해제
options.add_argument("--disable-breakpad")  # 크래시 리포터 비활성화
options.add_argument("--disable-component-update")  # 구성 요소 업데이트 중지
options.add_argument("--disable-domain-reliability")  # 도메인 신뢰성 보고 중지
options.add_argument("--disable-ipc-flooding-protection")  # IPC 플러딩 보호 끔
options.add_argument("--disable-backgrounding-occluded-windows")  # 가려진 창 백그라운드 중지 비활성화
options.add_argument("--disable-renderer-backgrounding")  # 렌더러 백그라운드 제한 해제
options.add_argument("--disable-features=site-per-process,TranslateUI")  # 사이트 격리 및 번역 UI 비활성화
options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")  # 네트워크 서비스 기능 활성화
options.add_argument("--enable-blink-features=IdleDetection")  # Blink Idle Detection 기능 활성화
options.add_argument("--no-proxy-server")  # 프록시 서버 사용 안 함 (직접 연결)
options.add_argument("--disable-site-isolation-trials")  # 사이트 격리 테스트 비활성화
options.add_argument("--disable-background-networking")  # 백그라운드 네트워크 요청 중지
options.add_argument("--hide-scrollbars")  # 스크롤바 숨김 (화면 깔끔하게 유지)
# options.add_argument("--mute-audio")  # 오디오 음소거 (필요시 활성화)

try:
    # 크롬 드라이버 실행 및 네이버 뉴스 경제 섹션 접속
    driver = webdriver.Chrome(options=options)
    driver.get("https://news.naver.com/section/101")
    
    # 기본 암묵적 대기 설정 (요소 찾기 시 최대 대기시간)
    driver.implicitly_wait(30)

    # 명시적 대기 객체 생성 (최대 10초 대기)
    wait = WebDriverWait(driver, 10)

    # '헤드라인 더보기' 버튼이 클릭 가능해질 때까지 대기 후 클릭
    element = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.section_more_inner._SECTION_HEADLINE_MORE_BUTTON._NLOG_IMPRESSION_TRIGGER")
    ))
    element.click()

    # 뉴스 아이템 10개가 로드될 때까지 대기
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sa_item_inner")))
    
    # 링크만 먼저 수집 (Stale Element 문제 해결)
    items = driver.find_elements(By.CSS_SELECTOR, "div.sa_item_inner")[:10]
    news_links = []
    
    for item in items:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, "a.sa_text_title > strong.sa_text_strong")
            title = title_elem.text
            link = item.find_element(By.CSS_SELECTOR, "a.sa_text_title").get_attribute("href")
            news_links.append({"title": title, "link": link})
        except Exception as e:
            print(f"링크 수집 중 오류: {e}")
            continue

    print(f"총 {len(news_links)}개의 뉴스 링크 수집 완료")
    
    news_data = []  # 크롤링 결과 저장 리스트 초기화

    # 수집한 링크로 각 기사 페이지 방문
    for i, news_item in enumerate(tqdm(news_links)):
        try:
            title = news_item["title"]
            link = news_item["link"]
            
            print(f"제목: {title}")
            print(f"링크: {link}")

            # 기사 페이지로 이동
            driver.get(link)
            
            # 썸네일(대표 이미지) URL 크롤링 (og:image 메타 태그 활용)
            try:
                og_image = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]')
                thumbnail_url = og_image.get_attribute("content")
            except Exception:
                thumbnail_url = "썸네일 없음"

            # 본문 영역이 로드될 때까지 최대 10초 대기
            try:
                content_elem = wait.until(EC.presence_of_element_located((By.ID, "dic_area")))
                content = content_elem.text
            except:
                content = "본문을 찾을 수 없습니다."

            # 수집한 데이터 리스트에 저장
            news_data.append({
                "제목": title,
                "링크": link,
                "본문": content,
                "썸네일": thumbnail_url
            })
            
            # 요청 간 딜레이 추가 (서버 부하 방지)
            time.sleep(10)
            
        except Exception as e:
            print(f"기사 {i+1} 처리 중 오류: {e}")
            continue

    # DataFrame으로 변환 후 CSV 저장 (UTF-8 BOM 포함)
    df = pd.DataFrame(news_data)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"CSV 파일로 저장 완료: {filepath}")
    print(f"총 {len(news_data)}개의 뉴스 기사 수집 완료")

    print("5초 후 브라우저를 종료합니다...")
    time.sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")  # 오류 출력

except KeyboardInterrupt:
    print("사용자에 의해 종료됨.")

finally:
    if 'driver' in locals():
        driver.quit()  # 브라우저 종료
    print("Browser closed successfully.")