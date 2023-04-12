import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import xlrd
import re
import xlwt
import pandas as pd
from pyecharts import Bar
# 配置Selenium
browser = webdriver.Chrome(executable_path=r'C:\Users\hp\AppData\Local\Programs\Python\Python38\Scripts\chromedriver')
wait = WebDriverWait(browser, 2)

book = xlrd.open_workbook('D:\python\zhihu爬取\任务link.xlsx')
sheet = book.sheet_by_name('Sheet2')
rows = sheet.nrows
cols = sheet.ncols
print('该工作表有%d行，%d列.'%(rows,cols))

#title = ['知乎昵称', '主页链接', '粉丝数', '认证', '公众号', '标签', '地区']  # 表格title


def get_goods(i):
    """
    获取用户数据
    :return:
    """

    try:
        if i < 1:
            login = browser.find_element_by_css_selector('#root .AppHeader-inner .AppHeader-login').text #查看是否有登录两字，有就登入，没有跳过
            if "登录" in login:
                browser.find_element_by_css_selector('#root .AppHeader-inner .AppHeader-login').click() #太懒，二维码登入
                time.sleep(15)
                # browser.find_element_by_css_selector('.Modal-inner .SignFlow-tabs .SignFlow-tab').click()
                # browser.find_elements_by_css_selector('.Input')[0].sendKeys("13049397009")
                # browser.find_elements_by_css_selector('.Input')[1].sendKeys("Power163")
                # browser.find_element_by_css_selector('.Modal-backdrop .Login-options .SignFlow-submitButton').click()

        nickname = browser.find_element_by_css_selector("#root .Card span.ProfileHeader-name").text #爬取知乎昵称
        print(nickname)

        print(url)

        fans = browser.find_elements_by_css_selector("#root .NumberBoard-itemInner strong")[1].text #爬取粉丝数
        fans = fans.replace(',','') #去除数字中的逗号
        if fans is not None:
            print(fans)
        else:
            fans = 0
            print(fans)

        try:
            agree = browser.find_elements_by_css_selector('#root .Card  .css-vurnku')[0].text #爬取认同的人数
            if "赞" in agree:
                head, sep, tail = agree.partition('\n')
                agree = head
                print(agree)
            else:
                agree = browser.find_elements_by_css_selector('#root .Card  .css-vurnku')[1].text
                if "赞" in agree:
                    head, sep, tail = agree.partition('\n')
                    agree = head
                    print(agree)
                else:
                    agree = browser.find_elements_by_css_selector('#root .Card  .css-vurnku')[2].text
                    if "赞" in agree:
                        head, sep, tail = agree.partition('\n')
                        agree = head
                        print(agree)
                    else:
                        agree = browser.find_elements_by_css_selector('#root .Card  .css-vurnku')[3].text
                        if "赞" in agree:
                            head, sep, tail = agree.partition('\n')
                            agree = head
                            print(agree)
        except:
            agree = ""
            print(agree)

        official= browser.find_elements_by_css_selector("#root .Card span")[1].text #爬取公众号
        if "公众" in official:
            print(official)
        else:
            official = ""
            print(official)

        try:
            button = browser.find_elements_by_css_selector(".Profile-lightItem")[0].text #爬取兴趣前四项
            if "话题" in button:
                browser.find_elements_by_css_selector("[class='Profile-lightItem']")[0].click()
            else:
                button = browser.find_elements_by_css_selector(".Profile-lightItem")[1].text
                if "话题" in button:
                    browser.find_elements_by_css_selector("[class='Profile-lightItem']")[1].click()
                else:
                    button = browser.find_elements_by_css_selector(".Profile-lightItem")[2].text
                    if "话题" in button:
                        browser.find_elements_by_css_selector("[class='Profile-lightItem']")[2].click()
            time.sleep(1)
            like1 = browser.find_elements_by_css_selector("div[aria-haspopup='true']")[1].text
            like2 = browser.find_elements_by_css_selector("div[aria-haspopup='true']")[2].text
            like3 = browser.find_elements_by_css_selector("div[aria-haspopup='true']")[3].text
            like4 = browser.find_elements_by_css_selector("div[aria-haspopup='true']")[4].text
            hobby = (like1,like2,like3,like4)
            print(hobby)
        except:
            hobby = ""
            print(hobby)

        js = "var q=document.documentElement.scrollTop=0"  #js完成上拉，但好像不用也行
        browser.execute_script(js)
        browser.find_element_by_css_selector("#root .Card .ProfileHeader-expandButton span").click()  #点击查看详细资料
        time.sleep(1)
        live = browser.find_elements_by_css_selector("#root .Card span")[3].text  #居住地
        if "居" in live:
            head, sep, tail = live.partition('居')
            live = tail
            print(live)
        else:
            live = ""
            print(live)

        # excelpath = r'D:\python\zhihu爬取\123.xls'
        # wtbook = xlwt.Workbook()
        # # 新增一个sheet工作表
        # sheet = wtbook.get_sheet(1)
        # # 写入数据头
        # headlist = [u'知乎昵称', u'主页链接', u'粉丝数', u'认证', u'公众号', u'标签', u'地区']
        #
        #
        # # 循环写
        # if i < 1:
        #     sheet.write(i, j, headlist)
        # for data in data:
        #     j = j + 1
        #     sheet.write(i, j, data)
        #     print("OK")
        # # 保存
        # wtbook.save(excelpath)
        # sheets是要写入的excel工作簿名称列表


        #pandas

        # mysql
        # 保存writer中的数据至excel
        # 如果省略该语句，则数据不会写入到上边创建的excel文件中
        # db = pymysql.connect(host='localhost', user='root', password='1', port=3306, db='mysql', charset='utf8')
        # cursor = db.cursor()
        # sql = '''insert into zhihu(nickname,url,fans,agree,official,like,live) values(%s,%s,%s,%s,%s,%s,%s)'''
        # value = (nickname, url, fans, agree, official, hobby, live)
        # # try:
        # #     cursor.execute(sql, value)
        # #     print('ok')
        # #     db.commit()
        # # except:
        # #     # 发生错误时回滚
        # #     db.rollback()
        # cursor.execute(sql, value)
        # print('ok')
        # db.commit()
    except:  #当网页404时，赋值
        nickname=""
        fans = 0
        agree=""
        official=""
        hobby=""
        live=""
        print(nickname)
        print(url)
        print(fans)
        print(agree)
        print(official)
        print(hobby)
        print(live)


    list_0.append(nickname) #list_0 取 知乎昵称
    print(list_0)

    list_1.append(fans) #list_1 取 粉丝数
    print(list_1)

    list_2.append(agree) #list_2 取 认同数
    print(list_2)

    list_3.append(official) #list_3 取 公众号
    print(list_3)

    list_4.append(hobby) #list_4 取 兴趣
    print(list_4)

    list_5.append(live) #list_3 取 居住
    print(list_5)
    if i == 69:
        # (新)写入文件
        # dataframe = pd.DataFrame({'知乎昵称':list_0, '主页链接': line,'粉丝数':list_2, '认证': list_3,'公众号':list_4, '标签': list_5, '地区': list_6})
        # # 将DataFrame存储为csv,index表示是否显示行名，default=True
        # dataframe.to_csv("D:\\python\\zhihu爬取\\123.csv", index=False, sep=',',encoding="GBK")
        # print("ok")

        # 可视化数据
        list_6 = list(map(float, list_1)) #转float的形式，但好像现在不用了
        bar = Bar("爬取粉丝数目")
        bar.add("粉丝数", list_0, list_6)
        bar.show_config()
        bar.render()

        #xlwt
        # excelpath = r'D:\python\zhihu爬取\123.xls'
        # wtbook = xlwt.Workbook()
        # # 新增一个sheet工作表
        # sheet = wtbook.get_sheet(1)
        # col = 0
        # # 循环写
        # for data in data:
        #     j = j + 1
        #     sheet.write(i, j, data)
        #     print("OK")
        # # 保存
        # wtbook.save(excelpath)
        # 保存


        #mysql
        # db = pymysql.connect(host='localhost', user='root', password='1', port=3306, db='mysql', charset='utf8')
        # cursor = db.cursor()
        # sql = '''insert into zhihu(nickname,url,fans,agree,official,like,live) values(%s,%s,%s,%s,%s,%s,%s)'''
        # value = (nickname, url, fans, agree, official, hobby, live)
        # # try:
        # #     cursor.execute(sql, value)
        # #     print('ok')
        # #     db.commit()
        # # except:
        # #     # 发生错误时回滚
        # #     db.rollback()
        # cursor.execute(sql, value)
        # print('ok')
        # db.commit()


    #旧pandas一行一行写入,可行但标题也会一行一行写入
    # data = [nickname, url,  fans, agree, official,  hobby, live]
    # print(data)
    # df = pd.DataFrame(data)
    # try:
    #     df.to_csv(r'D:\python\zhihu爬取\123.csv', line_terminator="\n", index=False,mode='a',encoding="gb2312")
    # except:
    #     print("bug")
    #     nickname = ""
    #     fans = ""
    #     agree = ""
    #     official = ""
    #     hobby = ""
    #     live = ""
    #     data = [nickname, url,  fans, agree, official,  hobby, live]
    #     df = pd.DataFrame(data)
    #     df.to_csv(r'D:\python\zhihu爬取\123.csv', line_terminator="\n", index=False, mode='a', encoding="gb2312")




if __name__ == '__main__':
    time.sleep(1)
    list_0 = []
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    for i in range(0,1):
        line = sheet.col_values(0)
        print(line)
        for url in line:
            browser.get(url)
            get_goods(i)
            i = i + 1






