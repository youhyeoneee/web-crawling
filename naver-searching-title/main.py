from bs4 import BeautifulSoup
from selenium import webdriver
import time


#찾고자 하는 키워드 추가
keyword = "단기간살빼기"

#브라우저 제어
browser = webdriver.Chrome('./chromedriver')
browser.maximize_window()

browser.get('https://www.naver.com/')

#검색
browser.find_element_by_xpath('//*[@id="query"]').send_keys(keyword)
browser.find_element_by_xpath('//*[@id="search_btn"]/span[2]').click()

print(">>> 블로그")
#블로그 탭 클릭
browser.find_element_by_xpath('//*[@id="lnb"]/div/div[1]/ul/li[2]/a/span').click()

time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

#페이지 소스 얻어오기
bs4 = BeautifulSoup(browser.page_source, 'lxml')

#제목 가져오기
blogs = bs4.find_all('a', attrs={'class':'sh_blog_title _sp_each_url _sp_each_title'})
for blog in blogs:
  print(blog['title'])

print(">>> 지식인")
#지식인 탭 클릭
browser.find_element_by_xpath('//*[@id="lnb"]/div/div[1]/ul/li[5]/a').click()

time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

#페이지 소스 얻어오기
bs4 = BeautifulSoup(browser.page_source, 'lxml')

titles = bs4.find_all("dt", "question")
for title in titles:
    t = title.get_text()
    new_t = t.replace("질문", "")
    print(new_t.lstrip())

print(">>> 카페")
#카페 탭 클릭
browser.find_element_by_xpath('//*[@id="lnb"]/div/div[1]/ul/li[7]/a/span').click()

time.sleep(5)  # 페이지 글 로딩되는거 기다려주기

#페이지 소스 얻어오기
bs4 = BeautifulSoup(browser.page_source, 'lxml')

#제목 가져오기
cafes = bs4.find_all('a', attrs={'class':'sh_cafe_title'})
for cafe in cafes:
  print(cafe.get_text())

browser.quit()

