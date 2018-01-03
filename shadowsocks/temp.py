# -*- coding: utf-8 -*-
import urllib2
import cookielib
import httplib
import urllib
import execjs


def get_browser_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Referer': 'https://free-ss.site/',
        'Connection': 'keep-alive',
        'Method': 'GET'
    }


headers = get_browser_headers()


# try:
# cj = cookielib.CookieJar()
# # req = urllib2.Request(url, headers=headers)
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# print([(key, headers[key]) for key in headers.keys()])
# opener.addheaders = [(key, headers[key]) for key in headers.keys()]
# http_connect = opener.open("https://free-ss.site/")
# print(http_connect.read())
# req = urllib2.Request('https://free-ss.site/', headers=headers)
# http_connect = urllib2.urlopen(req, timeout=2)
# except urllib2.HTTPError as e:
#     print(e.headers.dict['set-cookie'])
#     print(e.code)
#     print(e.reason)
# except urllib2.URLError as e:
#     print(e.reason)

# def get_check_param():
def get_html_context():
    conn = httplib.HTTPSConnection("free-ss.site")
    conn.request('GET', '/', headers=headers)
    res = conn.getresponse()
    # 503页面的内容
    resText = res.read()
    # 带回的cookie
    cfdguid = res.msg.dict['set-cookie']
    return [resText, cfdguid]


# function getExpression(str){
# 	var empty = /\[\]/g;
# 	var one = [/\!\+\[\]/g, /\!\!\[\]/g];
# 	var zero = /\!\[\]/g;
# 	// var mark3to1 = '!!!'
# 	return str.replace(one[0], 1).replace(one[1], 1).replace(zero, 0).replace(empty, "\'\'");
# }


def get_expression(str):
    empty = '[]'
    one = ['!+[]', '!![]']
    zero = '![]'
    return str.replace(one[0], '1').replace(one[1], '1').replace(zero, '0').replace(empty, "\'\'")


def main():
    context = get_html_context()
    body = context[0]
    guid = context[1]
    strInit = 'var s,t,o,p,b,r,e,a,k,i,n,g,f, '
    strInitIndex = body.index(strInit)

    # 拿到对象名称
    objName = body[strInitIndex + len(strInit): body.find('=', strInitIndex)]
    # 拿到属性名称
    propName = body[body.find('{"', strInitIndex) + 2: body.find('":', strInitIndex)]

    varName = objName + "." + propName

    # start -> body.find(":", str1Index) + 1
    # end -> body.find("}", str1Index)
    initExpression = body[body.find(":", strInitIndex) + 1: body.find("}", strInitIndex)]

    # 记录验证码的值
    sum = execjs.eval(initExpression)

    # 截取验证码表达式字符串
    str1Start = "('challenge-form');"
    str1End = "a.value"
    otherExpression = body[body.index(str1Start) + len(str1Start) + 1: body.index(str1End)].strip()[1:]
    # sum+=!+[]+!![]+!![]+!![]+!![]+!![]+!![];
    # sum+=+((!+[]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]));
    # sum+=!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![];
    # sum+=+((!+[]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));
    print otherExpression


if __name__ == '__main__':
    main()
