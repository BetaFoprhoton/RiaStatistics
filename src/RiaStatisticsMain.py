from bs4 import BeautifulSoup
import re, random
import urllib.request, urllib.error
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 显示中文标签,处理中文乱码问题
plt.rcParams['axes.unicode_minus'] = False  # 坐标轴负号的处理
#plt.axes(aspect='equal')  # 将横、纵坐标轴标准化处理，确保饼图是一个正圆，否则为椭圆

find_test_result = r'<td>([OR/-])\n</td>'
labels = ["通过", "重试", "未通过", "无效"]
colors = ['#3cdc3c', '#ffc864', '#ff2700', '#686868']
op_list = ['鱼', '星', '灯', '御', '桶', '阿', '影', '冰', '鲈']

def generate_random_color():
    """生成一个随机的颜色字符串，格式为 #RRGGBB"""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def ria_test_pie():
    baseurl = "https://wiki.ria.red/wiki/%E5%AE%A1%E6%A0%B8%E8%AE%B0%E5%BD%95%E9%A1%B5"
    passed_number, retry_number, fail_number, invalid_number = 0, 0, 0, 0
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('table', class_="wikitable"):
        item = str(item)
        results = re.findall(find_test_result, item)
        for result in results:
            match result:
                case "O":
                    passed_number += 1
                case "R":
                    retry_number += 1
                case "/":
                    fail_number += 1
                case "-":
                    invalid_number += 1
    data = [passed_number, retry_number, fail_number, invalid_number]
    plt.pie(x=data,  # 绘图数据
            labels=labels,
            colors=colors,
            autopct='%.2f%%',  # 设置百分比的格式，这里保留两位小数
            pctdistance=0.8,  # 设置百分比标签与圆心的距离
            labeldistance=1.1,  # 设置标签与圆心的距离
            startangle=120,  # 设置饼图的初始角度
            radius=1.2,  # 设置饼图的半径
            counterclock=False,  # 是否逆时针，这里设置为顺时针方向
            wedgeprops={'linewidth': 1, 'edgecolor': 'black'},  # 设置饼图内外边界的属性值
            textprops={'fontsize': 10, 'color': 'black'},  # 设置文本标签的属性值
            )

    # 添加图标题
    plt.title('Ria审核结果统计')
    # 显示图形
    plt.show()

def ria_test_info_pie():
    baseurl = "https://wiki.ria.red/wiki/%E5%AE%A1%E6%A0%B8%E8%AE%B0%E5%BD%95%E9%A1%B5"
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    all_results = []
    for item in soup.find_all('table', class_="wikitable"):  # 查找符合要求的字符串
        item = str(item)
        all_results += re.findall(r'<th>检票员：(.+?)\n</th>', item)  # 通过正则表达式查找

    op_dict = {}
    for char in op_list:
        count = 0
        for result in all_results:
            count += result.count(char)
        op_dict[char] = count

    op_dict = dict(sorted(op_dict.items(), key=lambda item: item[1], reverse=True))

    plt.pie(x=op_dict.values(),  # 绘图数据
            labels=op_dict.keys(),  # 添加标签
            #colors=[generate_random_color() for _ in op_list],
            autopct='%.2f%%',  # 设置百分比的格式，这里保留两位小数
            pctdistance=0.8,  # 设置百分比标签与圆心的距离
            labeldistance=1.1,  # 设置标签与圆心的距离
            startangle=120,  # 设置饼图的初始角度
            radius=1.2,  # 设置饼图的半径
            counterclock=False,  # 是否逆时针，这里设置为顺时针方向
            wedgeprops={'linewidth': 1, 'edgecolor': 'black'},  # 设置饼图内外边界的属性值
            textprops={'fontsize': 10, 'color': 'black'},  # 设置文本标签的属性值
            )

    # 添加图标题
    plt.title('Ria检票员审核频率统计')
    # 显示图形
    plt.show()


def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

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

ria_test_info_pie()
ria_test_pie()

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