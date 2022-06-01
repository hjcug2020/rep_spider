'''
edit by 洪晶 2022.05.28
用途：爬虫程序，试讲用
'''
import requests
import datetime
from bs4 import BeautifulSoup

#方法一：使用字符串转化方式清洗数据，存入二维列表中去 ，使用split,replace等函数
def get_item_by_str(text):
    text=text.split('<tr>',1)[1]
    #规范为用纯<td>替换掉修饰的<td>
    for tag in ['<td width="8%">','<td colspan="5">','<td colspan="2">','<td width="31%" rowspan="16">','<td width="31%" rowspan="10">','<td width="8%" rowspan="2">','<td width="11%">','<td width="31%">','<td width="42%">']:
        text=text.replace(tag,'<td>')
    # 去除不需要的标签等
    for tag in ['<tr class="background">','<p align="center">','<p align="left">','</strong>','<strong>','</td>', '</p>', '<br />','</tr>','&nbsp;','\n','\r',' ']:
        text = text.replace(tag, '')

    text=text.replace('<td>','\t')
    text=text.replace('<tr>','\n')

    return text
# 方法二：使用BeautifulSoup类较方便的获取标记数据
def get_item_by_bs(text):
    bs = BeautifulSoup(text,features='lxml')# 创建BeautifulSoup实例
    tag_tr = bs.find_all('tr')# 查找所有标签为tr的内容
    txt_result=''#存储爬取的表格数据
    #将bs发现的数据存入一个二维列表lst_result中去
    #<tr>变为换行符
    for tr in tag_tr:
        lst_td=[]#存储表格一行数据
        all_td=tr.find_all('td')
        #<td>变为TAB
        for i in all_td:
            i=i.get_text().strip()#去除空格
            i=i.replace('\n','')#去除换行符
            txt_result=txt_result+i+'\t'#区隔单元格
        txt_result+='\n'#换行
    return txt_result


#0.变量初始化
url='http://www.gaoxiaojob.com/zhaopin/zhuanti/shdzxxzyjsxy2019/index.html'#指定要爬取的网页
content=''#存放要解析的网页内容
output_text=''#存放解析后的文本内容

#1.读取目标网页内容
response = requests.get(url)
response.encoding = response.apparent_encoding
content=response.text
# #方便调试，暂从临时文件中读取网页内容
# with open('request_html.txt','r',encoding='utf-8') as f:
#     content=f.read()
# f.close()
# 1.1缩小页面范围到要爬取的部分
#1.1缩小要解析html内容的范围
content = content.split('<table border="1" cellspacing="0" cellpadding="0" class="td">')[2]
content = content.replace('<tr class="background">', '<tr>')
content = content.split('</table>')[0]

#2.解析-清洗-替换 网页内容，获取目标格式的数据
output_txt=get_item_by_str(content)#方法一：处理字符串，原理通透
#output_txt=get_item_by_bs(content)#方法二：使用beautifulsoap类，节省体力
#print(item_list)

#3.将目标数据转存到txt文件中
date_now=datetime.datetime.now()
day_now=date_now.strftime('%Y%m%d%H%M')
with open(day_now+'result.txt','w') as f:
    f.write(output_txt)
f.close()

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }   # 添加请求头
# r = requests.get('http://httpbin.org/get',params=data, headers = headers)   # params:参数
