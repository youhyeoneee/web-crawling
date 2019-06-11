from bs4 import BeautifulSoup
from selenium import webdriver
import time

#찾고자 하는 키워드
keyword = "암+건강"
BASE_URL = 'http://nsearch.chosun.com/search/'
PAGE_LIMIT = 24
SAVE_FILE_NAME = "조선일보.txt"

if __name__ == "__main__":
    # 브라우저 제어
    browser = webdriver.Chrome('./chromedriver')
    # browser.maximize_window()

    browser.get('http://www.chosun.com/')
    time.sleep(5)
    # 검색
    while True:
        try:
            browser.find_element_by_xpath('//*[@id="csh_search_id"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="query"]').send_keys(keyword, '\n')
            break
        except:
            time.sleep(0.5)
    # 검색
    browser.switch_to.window(browser.window_handles[-1])

    time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

    # 검색 설정
    browser.find_element_by_xpath('//*[@id="btn_set_id"]/a').click()
    # 기간 입력하기
    browser.find_element_by_xpath('//*[@id="set_box_id"]/li[1]/a').click()
    browser.find_element_by_xpath('//*[@id="date_start"]').send_keys('20090101')
    browser.find_element_by_xpath('//*[@id="date_end"]').send_keys('20181231')
    browser.find_element_by_xpath('//*[@id="set_box_id"]/li[1]/ul/li[6]/span/a').click()

    time.sleep(2)  # 페이지 글 로딩되는거 기다려주기
    # 검색 설정
    browser.find_element_by_xpath('//*[@id="btn_set_id"]/a').click()
    # 매체 선택하기
    browser.find_element_by_xpath('//*[@id="set_box_id"]/li[2]/a').click()
    browser.find_element_by_xpath('//*[@id="set_box_id"]/li[2]/ul/li[4]/div/label').click()
    browser.find_element_by_xpath('//*[@id="set_box_id"]/li[2]/ul/li[15]/span/a').click()
    time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

    # parsing
    outF = open(SAVE_FILE_NAME, 'w',encoding='utf8')
    bs = BeautifulSoup(browser.page_source, 'lxml')
    # 첫 페이지(_1) 링크 추출하기
    articles = bs.find_all('dt', attrs={'discription': "기사 제목"})
    for article in articles:
        link = article.find('a')['href'].strip()
        outF.write(link + '\n')
        print(">> ", link)

    while True:
        bs = BeautifulSoup(browser.page_source, 'lxml')
        if 'pn=' + str(PAGE_LIMIT) in browser.current_url:  # 찾고자 하는 페이지까지 도달하면 종료
            #print("link : ", browser.current_url)
            #print("종료합니다.")
            break
        # Paging
        pages = bs.find('ul', class_='paginate_num').find_all('a')
        for page in pages[2:]:  # 두번째부터 열번째 페이지 (_2 ~_0) 링크 추출하기
            nextLink = BASE_URL + page['href']
            print(page['href'])
            browser.get(nextLink)
            bs = BeautifulSoup(browser.page_source, 'lxml')

            if 'pn=' + str(PAGE_LIMIT) in browser.current_url:  # 찾고자 하는 페이지까지 도달하면 종료
                #print("link : ", browser.current_url)
                #print("종료합니다.")
                outF.close()
                browser.quit()
                exit(-1)
            else:  # 아니면 계속 찾는다
                articles = bs.find_all('dt', attrs={'discription': "기사 제목"})
                for article in articles:
                    link = article.find('a')['href'].strip()
                    outF.write(link + '\n')
                    print(">> ", link)
            if page.get_text().strip() == "다음":  # 다음 페이지(_1) 넘어가기
                nextLink = BASE_URL + page['href']
                browser.get(nextLink)
                break

        time.sleep(2)

    outF.close()
    browser.quit()
