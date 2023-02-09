from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

#--------------------------------------------------------------------------------------------------------------------
id = ""                                                 # 你的帳號          | Your username
pwd = ""                                                # 你的密碼          | Your password
url = ""                                                # 抽獎貼文網址      | Link to your giveaway post
picks = 2                                               # 抽出人數          | Pick how many people
tags = 2                                                # 至少要tag多少人   | How many people need to be tagged
#--------------------------------------------------------------------------------------------------------------------

# 開網頁    | Open website
browser = webdriver.Firefox()
browser.get('http://instagram.com/')

# 登入      | Log in
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
browser.find_element(By.NAME, "username").send_keys(id)
browser.find_element(By.NAME, "password").send_keys(pwd)
time.sleep(2)
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[3]/button/div')))
browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
print("Logging in...", end = "")
time.sleep(7)

# 開啟目標貼文  | Open target page
browser.get(url)
print("Success!\nOpening target page...", end = "")
time.sleep(5)

# 滾動到最下面  | Scroll to the bottom
print("Success!\nRolling comments...", end = "")
notFound = 0
rolled = 1
while notFound < 2:
    moreComment = browser.find_elements(By.TAG_NAME, 'svg')
    for btns in moreComment:
        if btns.get_attribute('aria-label') == '載入更多留言':
            notFound = -1
            btns.click()
            print(" "+str(rolled), end = "")
            rolled += 1
            break
    time.sleep(0.6)
    notFound += 1

# 抓留言者和留言    | Gather comments
print("\nGathering comments...", end = "")
type = 0
posters = []
count = -1
commentBoxes = browser.find_elements(By.CLASS_NAME, "x1i10hfl")
for commentBox in commentBoxes:
    # 抓留言者      | Gather commentors
    if str(commentBox.get_attribute('href')) and str(commentBox.get_attribute('href')) == 'https://www.instagram.com/'+commentBox.text+'/':
        type = 1
        tmp = []
        tmp.append(commentBox.text)
        posters.append(tmp)
        count = count + 1
    # 抓標記人      | Gather tagged people
    elif type == 1 and str(commentBox.get_attribute('href')):
        if str(commentBox.text) and str(commentBox.text)[0] == "@":
            posters[count].append(commentBox.text)
print(" ", count, "comments")

# 濾掉重複的人&沒標n個人的人 | Filter repeated commentors and not enough taggs
print("Filtering candidates...", end = "  ")
candidates = set()
for i in range(len(posters)):
    if len(posters[i]) >= tags+1:
        candidates.add(posters[i][0])
print(len(candidates), "candidates")

# 抽留言者  | Pink winner
print("Picking winner...\n")
print("winner: ", random.sample(list(candidates), picks))

# 關瀏覽器  | Close browser
browser.close()