#!/usr/bin/python -tt
# coding=utf-8

# 此脚本用于生成shadowsocks可使用的IP配置
# 可在windows/linux/mac中使用
# 兼容python 2 和 python 3
# 推荐使用 Mirror1 和 Mirror2
# Mirror3 和 Mirror4为https网址，使用时可能会出现证书问题导致程序异常
# US - 美国地区的IP可能时常断流或不能正常连接，可以使用其他冷门地区的IP

# mac os shadowsocksX-NG 含导入/导出配置功能
# 下载地址 https://www.yunssr.org/ss-6-1-1.html

# print兼容 python 2 和 python 3
from __future__ import print_function

import json
import os
import platform
import sys
import time
import traceback

__tips_prefix = '\n---> '

__urls = [
    # 'http://mirror.rohankdd.com//ss.php',
    'http://mirror.weirch.com//ss.php',
    # 'https://ss.rohankdd.com/ss.php',
    'https://ss.weirch.com/ss.php',
]

# https 网站证书
__crts = [
    '''
        -----BEGIN CERTIFICATE-----
    MIIGyjCCBnGgAwIBAgIRAN6nvY3zGoMq6V1y0DpCjMIwCgYIKoZIzj0EAwIwgZIx
    CzAJBgNVBAYTAkdCMRswGQYDVQQIExJHcmVhdGVyIE1hbmNoZXN0ZXIxEDAOBgNV
    BAcTB1NhbGZvcmQxGjAYBgNVBAoTEUNPTU9ETyBDQSBMaW1pdGVkMTgwNgYDVQQD
    Ey9DT01PRE8gRUNDIERvbWFpbiBWYWxpZGF0aW9uIFNlY3VyZSBTZXJ2ZXIgQ0Eg
    MjAeFw0xNzEwMTAwMDAwMDBaFw0xODA0MTgyMzU5NTlaMGwxITAfBgNVBAsTGERv
    bWFpbiBDb250cm9sIFZhbGlkYXRlZDEhMB8GA1UECxMYUG9zaXRpdmVTU0wgTXVs
    dGktRG9tYWluMSQwIgYDVQQDExtzbmkxODY3ODEuY2xvdWRmbGFyZXNzbC5jb20w
    WTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAQTdELB57NRa2jKYvvftEsNQBfY+S1x
    kWp67LeCIhHW2PDLt5CKiFEedhFTZq0YCFgq4p0/6Vjyo4R4SMhS5xQGo4IEyzCC
    BMcwHwYDVR0jBBgwFoAUQAlhZ/C8g3FP3hIILG/U1Ct2PZYwHQYDVR0OBBYEFNl9
    eulk+++F0TihdrOuKlRd9RWQMA4GA1UdDwEB/wQEAwIHgDAMBgNVHRMBAf8EAjAA
    MB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjBPBgNVHSAESDBGMDoGCysG
    AQQBsjEBAgIHMCswKQYIKwYBBQUHAgEWHWh0dHBzOi8vc2VjdXJlLmNvbW9kby5j
    b20vQ1BTMAgGBmeBDAECATBWBgNVHR8ETzBNMEugSaBHhkVodHRwOi8vY3JsLmNv
    bW9kb2NhNC5jb20vQ09NT0RPRUNDRG9tYWluVmFsaWRhdGlvblNlY3VyZVNlcnZl
    ckNBMi5jcmwwgYgGCCsGAQUFBwEBBHwwejBRBggrBgEFBQcwAoZFaHR0cDovL2Ny
    dC5jb21vZG9jYTQuY29tL0NPTU9ET0VDQ0RvbWFpblZhbGlkYXRpb25TZWN1cmVT
    ZXJ2ZXJDQTIuY3J0MCUGCCsGAQUFBzABhhlodHRwOi8vb2NzcC5jb21vZG9jYTQu
    Y29tMIIDEgYDVR0RBIIDCTCCAwWCG3NuaTE4Njc4MS5jbG91ZGZsYXJlc3NsLmNv
    bYIMKi5hcHB0aWMubmV0gg8qLmRlYWRtZXRydTkudGuCDyouZGlncmh5bWVzLnh5
    eoIVKi5kaWtvbS1nZXNjaGVua2VuLm5sggwqLmV0cGJvb2suY2aCHCouZmFudGFz
    dGljdm9yc2ljaHRpZy5zdHJlYW2CDCouZmFzdGdmLmNvbYIQKi5nZW9yZ2lhd2F5
    LndpboIUKi5pbmZvcm1hdGlvbmFzLmxvYW6CFSoubWVmdS5hbHRlcnZpc3RhLm9y
    Z4INKi5tb25kZW96LmNvbYIRKi5vbmJvb2tuZXh0LmluZm+CDSoub3dlY29ya2Yu
    Y2aCDioucm9oYW5rZGQuY29tghAqLnNlbGwtcWNtZHpxLm1sgg0qLnNreXJvZ3Vl
    LmdhghIqLnNvbGFyZHJlYW0uc3BhY2WCEyoudGFya29uZ2JlY2hlcy54eXqCFSou
    dWNyZml1bWVwdGZtYWFmZy5tbIILKi51c2FpbmEudGuCCyoudmNwb3YuY29tggwq
    LndlaXJjaC5jb22CCmFwcHRpYy5uZXSCDWRlYWRtZXRydTkudGuCDWRpZ3JoeW1l
    cy54eXqCE2Rpa29tLWdlc2NoZW5rZW4ubmyCCmV0cGJvb2suY2aCGmZhbnRhc3Rp
    Y3ZvcnNpY2h0aWcuc3RyZWFtggpmYXN0Z2YuY29tgg5nZW9yZ2lhd2F5LndpboIS
    aW5mb3JtYXRpb25hcy5sb2FughNtZWZ1LmFsdGVydmlzdGEub3Jnggttb25kZW96
    LmNvbYIPb25ib29rbmV4dC5pbmZvggtvd2Vjb3JrZi5jZoIMcm9oYW5rZGQuY29t
    gg5zZWxsLXFjbWR6cS5tbIILc2t5cm9ndWUuZ2GCEHNvbGFyZHJlYW0uc3BhY2WC
    EXRhcmtvbmdiZWNoZXMueHl6ghN1Y3JmaXVtZXB0Zm1hYWZnLm1sggl1c2FpbmEu
    dGuCCXZjcG92LmNvbYIKd2VpcmNoLmNvbTAKBggqhkjOPQQDAgNHADBEAiAA75Zd
    bA8Cq+hYw5a0KxCBKBJLpbdJt8NG7eld/+r6MAIgKNuBnrZVD5QbupoxFGDsTxFF
    jJ/DRkPxpc2B564fCIc=
    -----END CERTIFICATE-----
    '''
]

# 国家简称
__geo_zh = {
    'AD': u'安道尔共和国',
    'AE': u'阿拉伯联合酋长国',
    'AF': u'阿富汗',
    'AG': u'安提瓜和巴布达',
    'AI': u'安圭拉岛',
    'AL': u'阿尔巴尼亚',
    'AM': u'亚美尼亚',
    'AO': u'安哥拉',
    'AR': u'阿根廷',
    'AT': u'奥地利',
    'AU': u'澳大利亚',
    'AZ': u'阿塞拜疆',
    'BB': u'巴巴多斯',
    'BD': u'孟加拉国',
    'BE': u'比利时',
    'BF': u'布基纳法索',
    'BG': u'保加利亚',
    'BH': u'巴林',
    'BI': u'布隆迪',
    'BJ': u'贝宁',
    'BL': u'巴勒斯坦',
    'BM': u'百慕大群岛',
    'BN': u'文莱',
    'BO': u'玻利维亚',
    'BR': u'巴西',
    'BS': u'巴哈马',
    'BW': u'博茨瓦纳',
    'BY': u'白俄罗斯',
    'BZ': u'伯利兹',
    'CA': u'加拿大',
    'CF': u'中非共和国',
    'CG': u'刚果',
    'CH': u'瑞士',
    'CK': u'库克群岛',
    'CL': u'智利',
    'CM': u'喀麦隆',
    'CN': u'中国',
    'CO': u'哥伦比亚',
    'CR': u'哥斯达黎加',
    'CS': u'捷克',
    'CU': u'古巴',
    'CY': u'塞浦路斯',
    'CZ': u'捷克',
    'DE': u'德国',
    'DJ': u'吉布提',
    'DK': u'丹麦',
    'DO': u'多米尼加共和国',
    'DZ': u'阿尔及利亚',
    'EC': u'厄瓜多尔',
    'EE': u'爱沙尼亚',
    'EG': u'埃及',
    'ES': u'西班牙',
    'ET': u'埃塞俄比亚',
    'FI': u'芬兰',
    'FJ': u'斐济',
    'FR': u'法国',
    'GA': u'加蓬',
    'GB': u'英国',
    'UK': u'英国',
    'GD': u'格林纳达',
    'GE': u'格鲁吉亚',
    'GF': u'法属圭亚那',
    'GH': u'加纳',
    'GI': u'直布罗陀',
    'GM': u'冈比亚',
    'GN': u'几内亚',
    'GR': u'希腊',
    'GT': u'危地马拉',
    'GU': u'关岛',
    'GY': u'圭亚那',
    'HK': u'香港特别行政区',
    'HN': u'洪都拉斯',
    'HT': u'海地',
    'HU': u'匈牙利',
    'ID': u'印度尼西亚',
    'IE': u'爱尔兰',
    'IL': u'以色列',
    'IN': u'印度',
    'IQ': u'伊拉克',
    'IR': u'伊朗',
    'IS': u'冰岛',
    'IT': u'意大利',
    'JM': u'牙买加',
    'JO': u'约旦',
    'JP': u'日本',
    'KE': u'肯尼亚',
    'KG': u'吉尔吉斯坦',
    'KH': u'柬埔寨',
    'KP': u'朝鲜',
    'KR': u'韩国',
    'KT': u'科特迪瓦共和国',
    'KW': u'科威特',
    'KZ': u'哈萨克斯坦',
    'LA': u'老挝',
    'LB': u'黎巴嫩',
    'LC': u'圣卢西亚',
    'LI': u'列支敦士登',
    'LK': u'斯里兰卡',
    'LR': u'利比里亚',
    'LS': u'莱索托',
    'LT': u'立陶宛',
    'LU': u'卢森堡',
    'LV': u'拉脱维亚',
    'LY': u'利比亚',
    'MA': u'摩洛哥',
    'MC': u'摩纳哥',
    'MD': u'摩尔多瓦',
    'MG': u'马达加斯加',
    'ML': u'马里',
    'MM': u'缅甸',
    'MN': u'蒙古',
    'MO': u'澳门',
    'MS': u'蒙特塞拉特岛',
    'MT': u'马耳他',
    'MU': u'毛里求斯',
    'MV': u'马尔代夫',
    'MW': u'马拉维',
    'MX': u'墨西哥',
    'MY': u'马来西亚',
    'MZ': u'莫桑比克',
    'NA': u'纳米比亚',
    'NE': u'尼日尔',
    'NG': u'尼日利亚',
    'NI': u'尼加拉瓜',
    'NL': u'荷兰',
    'NO': u'挪威',
    'NP': u'尼泊尔',
    'NR': u'瑙鲁',
    'NZ': u'新西兰',
    'OM': u'阿曼',
    'PA': u'巴拿马',
    'PE': u'秘鲁',
    'PF': u'法属玻利尼西亚',
    'PG': u'巴布亚新几内亚',
    'PH': u'菲律宾',
    'PK': u'巴基斯坦',
    'PL': u'波兰',
    'PR': u'波多黎各',
    'PT': u'葡萄牙',
    'PY': u'巴拉圭',
    'QA': u'卡塔尔',
    'RO': u'罗马尼亚',
    'RU': u'俄罗斯',
    'SA': u'沙特阿拉伯',
    'SB': u'所罗门群岛',
    'SC': u'塞舌尔',
    'SD': u'苏丹',
    'SE': u'瑞典',
    'SG': u'新加坡',
    'SI': u'斯洛文尼亚',
    'SK': u'斯洛伐克',
    'SL': u'塞拉利昂',
    'SM': u'圣马力诺',
    'SN': u'塞内加尔',
    'SO': u'索马里',
    'SR': u'苏里南',
    'ST': u'圣多美和普林西比',
    'SV': u'萨尔瓦多',
    'SY': u'叙利亚',
    'SZ': u'斯威士兰',
    'TD': u'乍得',
    'TG': u'多哥',
    'TH': u'泰国',
    'TJ': u'塔吉克斯坦',
    'TM': u'土库曼斯坦',
    'TN': u'突尼斯',
    'TO': u'汤加',
    'TR': u'土耳其',
    'TT': u'特立尼达和多巴哥',
    'TW': u'台湾省',
    'TZ': u'坦桑尼亚',
    'UA': u'乌克兰',
    'UG': u'乌干达',
    'US': u'美国',
    'UY': u'乌拉圭',
    'UZ': u'乌兹别克斯坦',
    'VC': u'圣文森特岛',
    'VE': u'委内瑞拉',
    'VN': u'越南',
    'YE': u'也门',
    'YU': u'南斯拉夫',
    'ZA': u'南非',
    'ZM': u'赞比亚',
    'ZR': u'扎伊尔',
    'ZW': u'津巴布韦',
}


def version():
    version_ = '%d.%d' % sys.version_info[:2]
    return float(version_)


def is_python3():
    return version() >= 3


# 生成13位的时间戳
def timestamp():
    return int(time.time() * 1000)


def get_platform():
    return platform.system()


def is_windows():
    return get_platform() == "Windows"


def is_linux():
    return get_platform() == "Linux"


def is_mac():
    return get_platform() == "Darwin"


def get_connect(url, headers):
    http_connect = None
    if is_python3():

        try:
            import urllib.request
            from urllib.error import HTTPError

            req = urllib.request.Request(url, headers=headers)
            http_connect = urllib.request.urlopen(req)

        except HTTPError:
            print(__tips_prefix + u"地址请求异常，请选择其他镜像或联系开发人员。")
            # traceback.print_exc(e)
            sys.exit(-1)
    else:
        try:
            import urllib2

            req = urllib2.Request(url, headers=headers)
            http_connect = urllib2.urlopen(req)
        except urllib2.HTTPError:
            print(__tips_prefix + u"地址请求异常，请选择其他镜像或联系开发人员。")
            # traceback.print_exc(e)
            sys.exit(-1)

    return http_connect


def wget(url_idx):
    url = __urls[url_idx - 1] + '?_=' + str(timestamp())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Referer': 'https://ss.rohankdd.com/',
        'Connection': 'keep-alive',
        'Method': 'GET'
    }
    # 请求时添加证书（暂不可用）
    # if url_idx - 1 < len(__crts):
    #     headers['X-Mashape-Key'] = __crts[0]
    return get_connect(url, headers).read()


# 获取IP
def retrieve_ips(url_idx):
    return json.loads(wget(url_idx))['data']


# shadowsocks 的默认配置
def default_config():
    config_str = '''
    {
      "configs": [
      ],
      "strategy": null,
      "index": 0,
      "global": false,
      "enabled": false,
      "shareOverLan": false,
      "isDefault": false,
      "localPort": 1080,
      "pacUrl": null,
      "useOnlinePac": false,
      "secureLocalPac": true,
      "availabilityStatistics": false,
      "autoCheckUpdate": true,
      "checkPreRelease": false,
      "isVerboseLogging": false,
      "logViewer": {
        "topMost": false,
        "wrapText": false,
        "toolbarShown": false,
        "Font": "Consolas, 8pt",
        "BackgroundColor": "Black",
        "TextColor": "White"
      },
      "proxy": {
        "useProxy": false,
        "proxyType": 0,
        "proxyServer": "",
        "proxyPort": 0,
        "proxyTimeout": 3
      },
      "hotkey": {
        "SwitchSystemProxy": "",
        "SwitchSystemProxyMode": "",
        "SwitchAllowLan": "",
        "ShowLogs": "",
        "ServerMoveUp": "",
        "ServerMoveDown": ""
      }
    }
    '''
    if is_mac():
        config_str = '''
        {
          "random" : false,
          "authPass" : null,
          "useOnlinePac" : false,
          "TTL" : 0,
          "global" : false,
          "reconnectTimes" : 3,
          "index" : 0,
          "proxyType" : 0,
          "proxyHost" : null,
          "authUser" : null,
          "proxyAuthPass" : null,
          "isDefault" : false,
          "pacUrl" : null,
          "configs" : [
          ],
          "proxyPort" : 0,
          "randomAlgorithm" : 0,
          "proxyEnable" : false,
          "enabled" : true,
          "autoban" : false,
          "proxyAuthUser" : null,
          "shareOverLan" : false,
          "localPort" : 1080
        }
        '''
    return json.loads(config_str)


# 获取配置项
def get_config_item(ip_info):
    remarks = ip_info[6]
    item = {
        'server': ip_info[1],
        'server_port': int(ip_info[2]),
        'password': ip_info[3],
        'method': ip_info[4],
        'plugin': '',
        'plugin_opts': '',
        'remarks': remarks,
        'timeout': 5,
    }

    if is_mac():
        item = {
            "enable": True,
            "password": ip_info[3],
            "method": ip_info[4],
            "remarks": remarks,
            "server": ip_info[1],
            "obfs": "plain",
            "protocol": "origin",
            "server_port": int(ip_info[2]),
            "remarks_base64": ""
        }

    return item


# 生成IP配置
def get_ip_configs(ips):
    ip_list = []
    # 以区域分类统计
    ip_dict = {}
    for ip in ips:
        config = get_config_item(ip)
        geo = ip[6]
        if geo in ip_dict:
            ip_dict[geo] = ip_dict[geo] + 1
        else:
            ip_dict[geo] = 1
        ip_list.append(config)
    return [ip_list, ip_dict]


def get_geo_zh_name(code):
    return __geo_zh.get(code)


def print_ip_list(ip_geo_list):
    print(u'序号  地区简称  地区名称  IP数量')

    # 以下是为控制台打印设置的字串宽度
    index_width = 4
    geo_code_width = 7
    geo_name_width = 8
    geo_ip_width = 4

    for item in ip_geo_list:
        index = str(ip_geo_list.index(item) + 1)
        geo_code = item[0]
        geo_name = get_geo_zh_name(item[0])
        if geo_name is None:
            geo_name = u'未知(%s)' % geo_code
            geo_code = '  '
        geo_ip_sum = str(item[1])
        print(index.center(index_width), geo_code.center(geo_code_width),
              geo_name.center(geo_name_width + (index_width - len(geo_name))), geo_ip_sum.center(geo_ip_width))

    print(u'\n输入地区简称选择可用IP配置，多个地区用空格分隔：')


# 根据录入的序号匹配地区简称
def get_geo_by_idx(ip_geo_list, idx):
    if not idx.isdigit():
        return -1
    idx = int(idx) - 1

    if 0 <= idx < len(ip_geo_list):
        return ip_geo_list[idx][0]

    return None


# 获取从控制台录入的序号
def get_input_geo(ip_geo_list):
    idxs = sys.stdin.readline()
    if not idxs.strip():
        return None
    idxs = set(idxs.strip().split(' '))
    geos = []
    for idx in idxs:
        geo = get_geo_by_idx(ip_geo_list, idx)
        if geo:
            geos.append(geo)
    return geos


# 根据地区简称码过滤IP配置
def filter_ip_config(ip_config_list, geos):
    ips = []
    if not geos:
        return ip_config_list

    for geo in geos:
        for config in ip_config_list:
            if geo.upper() == config['remarks'].upper():
                ips.append(config)
    return ips


# 将IP配置写入文件
def write_to_file(ip_config_list):
    # 配置文件名
    config_file_name = 'gui-config.json'
    # 配置文件读取、配置项读取错误的提示信息
    config_or_program_out_of_date = config_file_name + ' or this program is out of date!'
    # 判断配置文件是存在
    config_file_exist = os.path.exists(config_file_name)
    ss_ip_config_file = None
    try:
        if config_file_exist:
            # 第一次，以'读'模式打开配置文件
            ss_ip_config_file = open(config_file_name, 'r')
            # 读取配置信息
            ss_configs = json.load(ss_ip_config_file)
            ss_ip_config_file.close()
        else:
            # 默认配置
            ss_configs = default_config()

        if 'configs' in ss_configs:
            ss_configs['configs'] = ip_config_list

            # 第二次，以'写'模式打开配置文件
            ss_ip_config_file = open(config_file_name, 'w')
            # 将生成的配置信息写入回文件
            json.dump(ss_configs, ss_ip_config_file, sort_keys=True, indent=2, separators=(',', ': '))
        else:
            print(config_or_program_out_of_date)
        # 关闭文件
        ss_ip_config_file.close()
    except ValueError as e:
        traceback.print_exc(e)
    finally:
        if ss_ip_config_file is not None:
            ss_ip_config_file.close()

    print(__tips_prefix, u'共生成', len(ip_config_list), u'条可用IP配置\n')


# 保持控制台不退出
def pause():
    if is_windows():
        os.system('pause')
    else:
        os.system('echo "按任意键继续..." && read')


def select_mirrors():
    print(u'序号    镜像       地址 (PS:https地址可能出现证书错误) \n')
    for url in __urls:
        idx = __urls.index(url) + 1
        print(idx, str('Mirror' + str(idx)).center(15), url.ljust(4), '\n')

    print(u"根据序号选择镜像：")
    idx = sys.stdin.readline().rstrip()
    if idx and idx.isdigit():
        idx = int(idx)
    else:
        # 非https，不会出现证书错误
        idx = 1
        print(__tips_prefix, u'默认使用镜像：Mirror1')
    return idx


def main():
    idx = select_mirrors()
    msg = u'可用IP获取中，请稍等...(PS：使用时请关闭其他代理和shadowsocks程序)\n'
    print(__tips_prefix, msg)

    # 获取IP
    ips = retrieve_ips(idx)

    # 解析IP数据，生成IP配置
    result = get_ip_configs(ips)

    ip_config_list = result[0]
    ip_geo_dict = result[1]
    ip_geo_list = sorted(ip_geo_dict.items(), key=lambda s: s[1], reverse=True)

    # 以地区分类，打印出可选列表
    print_ip_list(ip_geo_list)

    # 获取控制台录入的序号 -> 转换成地区简称码
    geo_args = get_input_geo(ip_geo_list)

    # 按用户录入的地区码过滤出需要的IP配置
    ip_config_list = filter_ip_config(ip_config_list, geo_args)

    # 写入文件
    write_to_file(ip_config_list)

    # 保持控制台不关闭
    pause()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
