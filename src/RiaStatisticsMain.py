import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 显示中文标签,处理中文乱码问题
plt.rcParams['axes.unicode_minus'] = False  # 坐标轴负号的处理
plt.axes(aspect='equal')  # 将横、纵坐标轴标准化处理，确保饼图是一个正圆，否则为椭圆

labels = ["通过", "重试", "未通过", "无效"]
colors = ['#3cdc3c', '#ffc864', '#ff2700', '#686868']
op_list = ['鱼', '星', '灯', '御', '桶', '阿', '影', '冰', '鲈']

baseurl = "https://wiki.ria.red/wiki/%E5%AE%A1%E6%A0%B8%E8%AE%B0%E5%BD%95%E9%A1%B5"
def askURL(url):
    head = {"User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"}
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def get_results_list():
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    all_results = []
    for item in soup.find_all('table', class_="wikitable"):
        item = str(item)
        item = ''.join(re.findall(r'[^\n]', item))
        player_results = re.findall(r'<tr>(.*?)</tr>', item)
        for results_string in player_results:
            results = re.findall(r'<td>(.*?)</td>', results_string)
            if not results:
                continue
            all_results.append(results)
    return all_results


def test_st(results_list=None) -> dict:
    if results_list is None:
        results_list = get_results_list()
    results_dict = {"通过": 0, "重试": 0, "未通过": 0, "无效": 0}
    for result in results_list:
        try:
            result[2]
        except IndexError:
            continue
        match result[2]:
            case 'O': results_dict["通过"] += 1
            case 'R': results_dict["重试"] += 1
            case '/': results_dict["未通过"] += 1
            case '-': results_dict["无效"] += 1
    return results_dict

def info_st(results_list = get_results_list()) -> dict:
    results_dict = {}
    for result in results_list:
        try:
            result[3]
        except:
            continue
        sub = re.findall(r'(<sub>(.*?)</sub>)', result[3])

        if sub != []:
            sub = ''.join(sub[0][0])
            name = result[3].replace(sub, "")
        else: name = result[3]
        try:
            results_dict[name] += 1
        except:
            results_dict[name] = 1
    return dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))

def op_st() -> dict:
    baseurl = "https://wiki.ria.red/wiki/%E5%AE%A1%E6%A0%B8%E8%AE%B0%E5%BD%95%E9%A1%B5"
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    all_results = []
    for item in soup.find_all('table', class_="wikitable"):  # 查找符合要求的字符串
        item = str(item)
        item = ''.join(re.findall(r'[^\n]', item))
        all_results += re.findall(r'<th>检票员：(.+?)</th>', item)  # 通过正则表达式查找
        op_dict = {}
        for char in op_list:
            count = 0
            for result in all_results:
                count += result.count(char)
            op_dict[char] = count

    return dict(sorted(op_dict.items(), key=lambda item: item[1], reverse=True))

def sub_st(results_list = get_results_list()) -> dict:
    results_dict = {}
    for result in results_list:
        try:
            result[3]
        except:
            continue
        sub = re.findall(r'(<sub>(.*?)</sub>)', result[3])

        if sub != []:
            sub = ''.join(sub[0][1])
        else:
            continue
        try:
            results_dict[sub] += 1
        except:
            results_dict[sub] = 1
    return dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))


def show_pie(results_dict: dict, title = "统计"):
    plt.pie(x=results_dict.values(),  # 绘图数据
            labels=results_dict.keys(),  #标签
            autopct='%.2f%%',  # 设置百分比的格式，保留两位小数
            pctdistance=0.8,  # 设置百分比标签与圆心的距离
            labeldistance=1.2,  # 设置标签与圆心的距离
            startangle=120,  # 设置饼图的初始角度
            radius=1.2,  # 设置饼图的半径
            counterclock=False,  # 是否逆时针，这里设置为顺时针方向
            wedgeprops={'linewidth': 1, 'edgecolor': 'black'},  # 设置饼图内外边界的属性值
            textprops={'fontsize': 10, 'color': 'black'},  # 设置文本标签的属性值
            )

    # 添加图标题
    plt.title(title)
    # 显示图形
    plt.show()


show_pie(op_st(), "Ria检票员活跃数统计")
show_pie(test_st(), "Ria测试数统计")
show_pie(info_st(), "Ria备注信息统计")
show_pie(sub_st(), "Ria未通过者小标题原因统计")


'''
鱼	鳕鱼	Codusk
星	佛祖	Accelerant
灯	火嗷	Huoao_Buao
御	鱼板	Misaka10087th
桶	安格	AngliaAnest
阿	老A	AiuRFAR
影	431	Code_C431
冰	冻菜	LettuceIce
鲈	鲈鱼	liziluyu
鱼星灯御桶阿影冰鲈
'''