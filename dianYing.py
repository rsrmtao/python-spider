import json
import re
import requests
import pymysql
import time

startUrl = 'https://www.dy2018.com/html/gndy/dyzz/index.html'
proxy = {'HTTPS': '117.85.105.170:808'}
def get_url(startUrl):
    try:
        response = requests.get(startUrl, proxies=proxy, timeout = 2)
        if response.status_code == 200:
            # print(response.apparent_encoding)
            response.encoding = response.apparent_encoding
            html = response.text
            # print(html)
            reg = r'<a href="(.*?)" .*? title="(.*?)">.*?</a>'
            patten = re.compile(reg)   #re.S。它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
            items = re.findall(patten, html)
            for item in items:
                # print(item)
                yield {'url': item[0],
                       'title': item[1]}
        else:
            print("connection error")
    except Exception as e:
        print("request failed")
        print(e)
        return False

def write_file(content):
    with open('dianying.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n') #写入字典
        f.close()

def parse_url(url):
    dict_movie = {}
    try:
        response = requests.get(url, proxies=proxy)
    except:
        print("request error")
        return False
    if response.status_code == 200:
        print(response.apparent_encoding)
        # response.encoding = response.apparent_encoding
        response.encoding = 'GBK'
        html = response.text
        # 根据正则表达式获取详细信息
        reg = r'class="title_all".*?h1>(.*?)</'
        patten = re.compile(reg, re.S)
        items = re.findall(patten, html)
        if items:
            dict_movie['title_all'] = items[0]

        reg = r'>◎译　　名　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['译名'] = items[0]

        reg = r'>◎片　　名　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['片名'] = items[0]
        reg = r'>◎年　　代　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['年代'] = items[0]

        reg = r'>◎产　　地　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['产地'] = items[0]

        reg = r'>◎类　　别　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['类别'] = items[0]

        reg = r'>◎语　　言　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['语言'] = items[0]

        reg = r'>◎字　　幕　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['字幕'] = items[0]

        reg = r'>◎上映日期　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['上映时间'] = items[0]

        reg = r'>◎豆瓣评分　(.*?)</'
        patten = re.compile(reg, re.S | re.M)
        items = re.findall(patten, html)
        if items:
            dict_movie['豆瓣评分'] = items[0]

        reg = r'>◎IMDb评分　(.*?)</'
        patten = re.compile(reg, re.S)
        items = re.findall(patten, html)
        if items:
            dict_movie['imdb评分'] = items[0]

        reg = r'>◎文件格式　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['文件格式'] = items[0]

        reg = r'>◎视频尺寸　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['视频尺寸'] = items[0]

        reg = r'>◎文件大小　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['文件大小'] = items[0]

        reg = r'>◎片　　长　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['片长'] = items[0]

        reg = r'>◎导　　演　(.*?)</'
        patten = re.compile(reg)
        items = re.findall(patten, html)
        if items:
            dict_movie['导演'] = items[0]

        reg = r'>◎主　　演(.*?)◎简　　介</'
        patten = re.compile(reg, re.S | re.M)
        items = re.findall(patten, html)
        reg = r'\u3000(.*?)</'
        patten = re.compile(reg, re.S | re.M)
        if items:
            items = re.findall(patten, items[0])
            if items:
                names = ''
                for i in items:
                    i = i.replace('\u3000', '')
                    names = names + i + ';'
                dict_movie['主演'] = names
        return dict_movie

def sql_word(dict_movie):
    strs1 = ''
    strs2 = ''
    strs3 = ''
    for i in dict_movie.keys():
        if i != '主演':
            strs1 = strs1 + i + ' ' + 'VARCHAR(200),'
        else:
            strs1 = strs1 + i + ' ' + 'VARCHAR(2000),'
        strs2 = strs2 + i + ','
        st = dict_movie.get(i).replace('\'', '\\')     # 处理字符串中的'号
        # strs3 = strs3 + '\'%s\'' % dict_movie.get(i) + ','
        strs3 = strs3 + '\'%s\'' % st +","
    return strs1,strs2,strs3

if __name__ == "__main__":
    # 打开数据库连接
    try:
        db = pymysql.connect("localhost", "root", "123456")
    except Exception:
        print('connect failed')
        exit()
    cursor = db.cursor()
    try:
        cursor.execute("create database movies DEFAULT CHARACTER SET GBK")
    except:
        print('failed')
    cursor.execute("use movies;")
    for i in range(1, 3):
        time.sleep(5)
        if i==1:
            urls =  'https://www.dy2018.com/html/gndy/dyzz/index.html'
        else:
            urls = "https://www.dy2018.com/html/gndy/dyzz/index_%d.html" % i
        for i in get_url(urls):
            write_file(i)
            # print(i.get('url'))
            detail_url = 'https://www.dy2018.com'+ i.get('url')
            dict_movie = parse_url(detail_url)
            print(dict_movie)
            strs1,strs2,strs3 = sql_word(dict_movie)
            try:
                sqlword = "CREATE TABLE IF NOT EXISTS dy2018com (%s PRIMARY KEY (title_all))" % strs1
                cursor.execute(sqlword)
            except:
                print("error")
            sqlword = "INSERT INTO dy2018com (%s) VALUES(%s)" % (strs2[:-1], strs3[:-1])  #去除末尾逗号
            # print(sqlword)
            try:
                cursor.execute(sqlword)
                db.commit()  # 提交之后才会保存记录
            except Exception as e:
                print(e)
                db.rollback()  # 回滚
    db.close()
