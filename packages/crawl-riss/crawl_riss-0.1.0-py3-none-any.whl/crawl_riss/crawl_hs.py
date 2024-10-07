import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_total_papers_count(search_keyword, start_count=0):
    """전체 검색된 논문 수를 가져오는 함수"""
    base_url = f"https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query={search_keyword}\
&queryText=&iStartCount={start_count}&iGroupView=5&icate=all&colName=re_a_kor&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=100\
&orderBy=&fsearchMethod=&isFDetailSearch=N&sflag=1&searchQuery={search_keyword}&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=\
&facetList=&facetListText=&fsearchDB=&resultKeyword=&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=\
&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&db_type=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 전체 검색된 논문 수 추출
    total_papers_tag = soup.find('span', class_='num')
    if total_papers_tag:
        total_papers = int(total_papers_tag.text.replace(',', ''))  # 숫자에 있는 콤마 제거 후 int 변환
        return total_papers
    else:
        return 0

def crawl_papers_hs(search_keyword, max_papers=1000):
    """논문 정보를 크롤링하는 함수 (최대 max_papers 수집)"""
    # 논문 수 확인
    total_papers = get_total_papers_count(search_keyword)
    print(f"전체 검색된 논문 수: {total_papers}개")

    # 수집할 논문 수 결정 (최대 1000개 혹은 검색된 논문 수)
    papers_to_collect = min(max_papers, total_papers)
    print(f"수집할 논문 수: {papers_to_collect}개")

    # 수집할 데이터 저장 리스트 초기화
    title, writer, publisher, year, journal, link, abstracts = [], [], [], [], [], [], []

    # 페이지별로 논문 데이터 수집
    for start_count in range(0, papers_to_collect, 10):
        # 각 페이지의 URL
        page_url = f"https://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query={search_keyword}\
&queryText=&iStartCount={start_count}&iGroupView=5&icate=all&colName=re_a_kor&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale=100\
&orderBy=&fsearchMethod=&isFDetailSearch=N&sflag=1&searchQuery={search_keyword}&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=\
&facetList=&facetListText=&fsearchDB=&resultKeyword=&pageNumber=1&p_year1=&p_year2=&dorg_storage=&mat_type=&mat_subtype=&fulltext_kind=\
&t_gubun=&learning_type=&language_code=&ccl_code=&language=&inside_outside=&fric_yn=&db_type=&image_yn=&regnm=&gubun=&kdc=&ttsUseYn="
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 논문 정보가 담긴 컨테이너 가져오기
        contents = soup.find_all('div', class_='cont ml60')

        for cont in contents:
            title.append(cont.find('p', class_='title').text.strip())
            writer.append(cont.find('span', class_='writer').text.strip())
            publisher.append(cont.find('p', class_="etc").find_all('span')[1].text.strip())
            year.append(cont.find('p', class_="etc").find_all('span')[2].text.strip())
            journal.append(cont.find('p', class_="etc").find_all('span')[3].text.strip())
            link.append('https://www.riss.kr' + cont.find('p', class_='title').find('a')['href'].strip())

            # 초록이 있을 경우와 없을 경우 처리
            if cont.find('p', class_='preAbstract'):
                abstracts.append(cont.find('p', class_='preAbstract').text.strip())
            else:
                abstracts.append('초록이 없습니다.')

        time.sleep(1)

        # 수집된 논문 수가 목표치에 도달하면 중단
        if len(title) >= papers_to_collect:
            break

    # pandas DataFrame으로 변환
    df = pd.DataFrame({
        'Title': title[:papers_to_collect],
        'Writer': writer[:papers_to_collect],
        'Publisher': publisher[:papers_to_collect],
        'Year': year[:papers_to_collect],
        'Journal': journal[:papers_to_collect],
        'Link': link[:papers_to_collect],
        'Abstract': abstracts[:papers_to_collect]
    })

    # 현재 작업 디렉토리
    current_path = os.getcwd()

    # 검색어로 폴더 생성 (폴더가 없으면 생성)
    folder_name = search_keyword.replace(" ", "_")+"_학술논문"
    folder_path = os.path.join(current_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # CSV 파일과 Excel 파일로 저장
    csv_file = os.path.join(folder_path, f"{folder_name}.csv")
    excel_file = os.path.join(folder_path, f"{folder_name}.xlsx")

    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"CSV 파일이 {csv_file}에 저장되었습니다.")
    print(f"Excel 파일이 {excel_file}에 저장되었습니다.")
