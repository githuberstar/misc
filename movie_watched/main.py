import http.client
import re
from urllib import parse
import json
import csv

'''
4. 替换userid
5. writerow 第一行
'''

domain = "frodo.douban.com"
user_agent = "com.douban.frodo"
conn_url = http.client.HTTPSConnection(domain)
headers = {
    'user-agent': user_agent,
    'content-type': "application/x-www-form-urlencoded"
}


def get_access_token():
    payload = "client_id=0ab215a8b1977939201640fa14c66bab&client_secret=22b2cf86ccc81009&grant_type=password&username=zhujihui1991%40gmail.com&password=Zhujihui6578602%25"
    conn_url.request("POST", "/service/auth2/token", payload, headers)
    res = conn_url.getresponse().read().decode()
    access_token = re.search('[0-9a-f]{32}', res).group()
    # user_id = re.search()
    return str(access_token)


def get_all_movies(count, start):
    headers['Authorization'] = 'Bearer ' + get_access_token()
    body = {'count': count,  # 一次返回多少个数据
            'start': start,
            'status': 'done',
            'type': 'movie',
            }
    request_url = '/api/v2/user/51530953/interests?' + parse.urlencode(body)  # 请求参数加密并拼接成url
    conn_url.request("GET", request_url, headers=headers)
    response_data = conn_url.getresponse().read() # read结果是bytes型
    dict_main = json.loads(response_data.decode("utf-8"))  # 先将bytes转为str，再将str转为dict
    total_amount = dict_main['total']
    return dict_main, total_amount


def write_into_csv(count, start):
    csv_file = open("csvData.csv", "a+", newline='', encoding='utf-8')  # a+追加并可读可写
    writer = csv.writer(csv_file)
    # writer.writerow(['电影名称', '豆瓣评分', '我的评分', '我的评语', '评分时间'])
    all_movies = get_all_movies(count, start)
    total_amount = all_movies[1]  # 看过的电影总数
    inn = total_amount%count
    for i in range(1, inn):
        start = (i-1)*50 + 1
        marked_movie_list = get_all_movies(count, start)[0]['interest']  # 看过的所有电影列表
        # number = 0
        for marked_movie in marked_movie_list:  # 从看过的所有电影列表中循环并格式化输出到csv文件
            comment = marked_movie['comment']
            my_rating = marked_movie['rating']['value']
            create_time = marked_movie['create_time']
            title = marked_movie['subject']['title']
            rating = marked_movie['subject']['rating']['value']
            # number += 1
            writer.writerow([title, rating, my_rating, comment, create_time])
    csv_file.close()


if __name__ == "__main__":
    print(get_all_movies(50, 1))
    write_into_csv(50, 1)

