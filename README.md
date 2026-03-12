## 네이버 경제 뉴스 크롤러 (`news_crwaling.py`)

이 프로젝트는 **네이버 뉴스 경제 섹션(섹션 101)의 헤드라인 기사 10개를 크롤링**하여,
제목·링크·본문·썸네일 정보를 CSV 파일로 저장하는 스크립트를 포함합니다.

- **수집 대상**: 네이버 뉴스 경제 섹션 헤드라인 기사 10개  
- **저장 형식**: `news_data_YYYY-MM-DD.csv`  
- **저장 위치 예시**: `Today_News` 폴더 아래

### 1. 사전 준비

- Python 3.x
- Google Chrome 브라우저
- ChromeDriver (Chrome 버전에 맞는 드라이버)
- 필수 패키지:
  - `selenium`
  - `pandas`
  - `tqdm`

2. 스크립트 주요 동작
https://news.naver.com/section/101 페이지 접속
"헤드라인 더보기" 버튼 클릭 후 기사 리스트 로드
각 기사에 대해 다음 정보를 수집:
제목
기사 링크
본문 내용 (#dic_area)
썸네일 이미지 URL (meta[property="og:image"])
수집 결과를 하나의 CSV 파일로 저장

3. 실행 방법
news_crwaling.py 파일의 저장 경로(base_dir) 를 자신의 PC 환경에 맞게 수정합니다.
터미널(또는 PowerShell)에서 프로젝트 폴더로 이동합니다.
cd "c:\Users\Roy_Koh\OneDrive\바탕 화면\News_Crawling"
아래 명령으로 스크립트를 실행합니다.
python news_crwaling.py
실행이 완료되면 지정한 폴더에 오늘 날짜를 포함한 CSV 파일이 생성됩니다.

4. 참고 사항
사이트 구조 변경, 요소 선택자 변경 등으로 인해 크롤링이 실패할 수 있습니다.
과도한 요청은 서비스 정책에 위반될 수 있으므로, 코드 내 time.sleep() 과 같은 대기 시간을 적절히 유지하는 것이 좋습니다.
