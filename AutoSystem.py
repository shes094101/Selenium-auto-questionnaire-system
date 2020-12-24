from selenium import webdriver
import tkinter as tk
import time


#開啟瀏覽器，並進入登入處
driver = webdriver.Chrome('chromedriver.exe')
url = 'https://webs.asia.edu.tw/stdinfo/login.asp#'
driver.get(url)
classList_url = []
step = 1

#登入帳號
def login():   
    account = str(ac_var.get())
    password = str(pw_var.get())
    try:
        account_input = driver.find_element_by_id('f_id')
        account_input.send_keys(account)
        password_input = driver.find_element_by_id('f_pwd')
        password_input.send_keys(password)
        password_input.submit()
        time.sleep(1)
    except:
        pass
    finally:
        if url != driver.current_url:
            out_area.insert("insert","STEP1.請按下Next進行下一步!\n")
            out_area.see(tk.END)

#讀取表單連結並存入矩陣
def form():
    #在登入後抓取含有金鑰的網址
    goldkey = driver.find_element_by_xpath('//*[@id="teacherchk"]/ul/li[2]/a')
    evaluation_url = goldkey.get_attribute('href')
    driver.get(evaluation_url)
    
    #將網頁上抓取到的連結存入矩陣
    global classList_url
    flag = True
    i = 2
    try:
        while(flag):
            xpath = '/html/body/center[3]/table/tbody/tr[%i]/td[7]/a'%(i)
            classList = driver.find_element_by_xpath(xpath)

            #當連結不等於空就存入矩陣，找不到元件就進入except
            if classList.get_attribute('href') != None:
                classList_url.append(classList.get_attribute('href'))
            i+=1
    except:
        pass
    finally:
        y = str(len(classList_url))
        out_area.insert("insert","STEP2.請按下Next進行下一步!\n")
        out_area.see(tk.END)

#填寫表單
def write():
    for i in range(len(classList_url)):
        out_area.insert("insert","第"+str(i+1)+"頁填完了ヽ(✿ﾟ▽ﾟ)ノ'\n")
        out_area.see(tk.END)
        driver.get(classList_url[i])
        
        #UVW的ASCII
        x = [85,86,87]
        try:
            #1-9
            for i in range(1,10):
                Q = driver.find_element_by_name("Q"+str(i))
                Q.click()
            #A-Z沒有U、V、W
            for i in range(65,91):
                if not i in x:
                    have = chr(i)
                    Q = driver.find_element_by_name("Q"+have)
                    Q.click()
        except:
            pass

        try:
            #AA-AC
            for i in range(65,68):
                have = chr(i)
                Q = driver.find_element_by_name("QA"+have)
                Q.click()
            #U、V、W
            for i in x:
                have = chr(i)
                Q = driver.find_element_by_name("Q"+chr(i))
                Q.click()
        except:
            pass
        submit = driver.find_element_by_name("sent")
        submit.click()
        driver.switch_to_alert().accept()
        
    driver.get('https://webs.asia.edu.tw/stdinfo/main.asp')
    out_area.insert("insert","全部都填完了ヽ(✿ﾟ▽ﾟ)ノ'\n")
    out_area.see(tk.END)

#按下一步執行不同函數
def nextStep():    
    global step
    if step == 1:
        form()
        step += 1
    elif step == 2:
        write()

#搭建視窗->Tkinter

root = tk.Tk() #搭建一個物件，名字叫做root(你也可以隨便取)
root.title('自動填寫系統ヽ(✿ﾟ▽ﾟ)ノ') #設定標題
root.geometry('400x470') #設定視窗大小
root.resizable(0, 0) #設定視窗不可被拉伸

title = tk.Label(root, text="期末教學評鑑表自動填寫系統",font=('Arial',20))
title.pack(pady = 10,side = "top",fill = 'x')

tk.Label(root, text="帳號:",font=('Arial',15)).place(x=60,y=70)

ac_var = tk.StringVar()
ac_var.set("")
ac = tk.Entry(root,show = '*',textvariable = ac_var)
ac.place(x=120,y=75)

tk.Label(root, text="密碼:",font=('Arial',15)).place(x=60,y=110)

pw_var = tk.StringVar()
pw_var.set("")
pw = tk.Entry(root,show = '*',textvariable = pw_var)
pw.place(x=120,y=115)


login = tk.Button(root,text = "Login",command = login)
login.place(x=280,y=70)

nextStep = tk.Button(root,text = "Next",command = nextStep) 
nextStep.place(x=280,y=110)

out_area = tk.Text(root,width = 25, height = 13,font=('Arial',14))
out_area.place(x=60,y=155)

root.wm_attributes('-topmost',1)
root.mainloop() #執行