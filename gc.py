import requests,re,bs4
maxn = 100
inf = input('국민청원 댓글읽기 프로그램\n제작 : 이현록\n깃허브 아이디 : Eos0510\n국민청원 링크 입력 : ')
thn = int(input('쓰레드 수 입력 : '))
if 'Temp' in inf:
    if 'page' in inf : inf = inf[0:50]
    while(True):
        rp = requests.get(inf+'?page='+str(cnt)).text
        a = re.compile('href="(.*)";').search(rp)
        if a != None: rp = requests.get(a.group(1)).text
        cnt += 1
        for i in bs4.BeautifulSoup(rp, 'html.parser').findAll('div', {'class':'R_R_contents_txt'}):
            t = i.text.strip()
            if t == '동의합니다' or t == '동의합니다.': continue
            else : print(t)
else:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import threading, fixlr
    gp = fixlr.getpath()
    class Dom(threading.Thread):
        def __init__(self, inf, thn, maxn):
            threading.Thread.__init__(self)
            self.inf = inf
            self.thn = thn
            self.maxn = maxn
        def run(self):
            cnt = 1
            driver = webdriver.Chrome()
            driver.get(self.inf)
            while(True):
                driver.execute_script('agreement_list('+str(cnt+(self.thn*self.maxn))+')')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "R_R_contents_txt")))
                cnt += 1
                for i in bs4.BeautifulSoup(driver.page_source, 'html.parser').findAll('div', {'class':'R_R_contents_txt'}):
                    t = i.text.strip()
                    if t == '동의합니다' or t == '동의합니다.': continue
                    else : print(t)
    for i in range(thn):
        d = Dom(inf, i, maxn)
        d.start()