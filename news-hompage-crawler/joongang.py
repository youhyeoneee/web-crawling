from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


#pattern = re.compile(r'page=\d+')
#찾고자 하는 키워드
keyword = "암+건강"
BASE_URL = 'https://search.joins.com/'
PAGE_LIMIT = 13
SAVE_FILE_NAME= "중앙일보.txt"

if __name__ == "__main__":
    # 브라우저 제어
    browser = webdriver.Chrome('./chromedriver')
    browser.get('https://joongang.joins.com/?cloc=joongang|section|bi')

    #time.sleep(5)
    # 검색
    while True:
        try:
            browser.find_element_by_xpath('//*[@id="btnOpenSearch"]').click()
            browser.find_element_by_xpath('//*[@id="searchKeyword"]').send_keys(keyword, '\n')
            break
        except:
            time.sleep(0.5)

    #
    time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
    # 뉴스 탭 선택하기
    browser.find_element_by_xpath('//*[@id="gnb_menu"]/ul/li[2]/a').click()
    time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

    # 기간 입력하기
    browser.find_element_by_xpath('//*[@id="btnPreriodTypeDirectInput"]').click()

    browser.find_element_by_xpath('//*[@id="filterStartDate"]').clear()
    browser.find_element_by_xpath('//*[@id="filterStartDate"]').send_keys('2009.01.01')

    browser.find_element_by_xpath('//*[@id="filterEndDate"]').clear()
    browser.find_element_by_xpath('//*[@id="filterEndDate"]').send_keys('2018.12.31')
    browser.find_element_by_xpath('//*[@id="btnSubmitForFilterDirectInput"]').click()

    # 매체 선택하기
    browser.find_element_by_xpath('//*[@id="sourceGroupTypeCheck"]').click()
    browser.find_element_by_xpath('//*[@id="sourceGroupType01"]').click()
    browser.find_element_by_xpath('//*[@id="btnSourceGroupType"]').click()
    time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

    # parsing
    outF = open(SAVE_FILE_NAME, 'w',encoding='utf8')

    while True:
        bs = BeautifulSoup(browser.page_source, 'lxml')
        if 'page=' + str(PAGE_LIMIT) in browser.current_url:  # 찾고자 하는 페이지까지 도달
            print("link : ", browser.current_url)
            print("종료합니다.")
            break
        # 첫 페이지(_1) 링크 추출하기
        articles = bs.find_all('strong', attrs={'class': 'headline mg'})
        for article in articles:
            link = article.find('a')['href'].strip()
            outF.write(link + '\n')
            print(">> ", link)

        # Paging
        pages = bs.find_all('a', class_='link_page')
        pageLastA = bs.find('div', class_='paging_comm').find_all('a')[-1]

        for page in pages:  # 두번째부터 열번째 페이지 (_2 ~_0) 링크 추출하기
            nextLink = BASE_URL + page['href']
            browser.get(nextLink)
            if 'page=' + str(PAGE_LIMIT) in browser.current_url:  # 찾고자 하는 페이지까지 도달하면 종료
                print("link : ", browser.current_url)
                print("종료합니다.")
                outF.close()
                browser.quit()
                exit(-1)
            else:  # 아니면 계속 찾는다
                articles = bs.find_all('strong', attrs={'class': 'headline mg'})
                for article in articles:
                    link = article.find('a')['href'].strip()
                    outF.write(link + '\n')
                    print(">> ", link)

        if pageLastA.get_text().strip() == "다음페이지":  # 다음 페이지(_1) 넘어가기
            nextLink = BASE_URL + pageLastA['href']
            browser.get(nextLink)

        time.sleep(2)

    outF.close()
    browser.quit()
