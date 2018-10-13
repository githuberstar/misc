import http.client
import json
import csv
from urllib import parse

domain = "frodo.douban.com"
user_agent = "com.douban.frodo"
conn_url = http.client.HTTPSConnection(domain)
headers = {
    'user-agent': user_agent,
    'content-type': "application/x-www-form-urlencoded"
}


def log_in(username, password):
    # 获取登录后的access_token和user_id
    api_url = "/service/auth2/token"
    request_body = {
        "client_id": "0ab215a8b1977939201640fa14c66bab",
        "client_secret": "22b2cf86ccc81009",
        "grant_type": "password",
        "username": username,
        "password": password,

    }
    conn_url.request("POST", api_url, parse.urlencode(request_body), headers)
    response = conn_url.getresponse()
    if response.code == 200:
        response_body = response.read().decode("utf-8")
        access_token_dict = json.loads(response_body)
        return access_token_dict
    elif response.code == 400:
        return 'bad request'
    else:
        return 'others'


def get_all_movies(access_token_str, user_id_no, count, start):
    # 获取所有登录用户的标记过的电影
    headers['Authorization'] = 'Bearer ' + access_token_str
    body = {'count': count,  # 一次返回多少个数据
            'start': start,
            'status': 'done',
            'type': 'movie',
            }
    request_url = '/api/v2/user/' + user_id_no + '/interests?' + parse.urlencode(body)  # 请求参数加密并拼接成url
    conn_url.request("GET", request_url, headers=headers)
    response_data = conn_url.getresponse().read()  # read结果是bytes型
    dict_main = json.loads(response_data.decode("utf-8"))  # 先将bytes转为str，再将str转为dict
    total_amount = dict_main['total']
    return dict_main, total_amount


def write_into_csv(count, start):
    # 把获取的标记过的电影写入CSV文件
    csv_file = open("csvData.csv", "a+", newline='', encoding='utf-8')  # a+追加并可读可写
    writer = csv.writer(csv_file)
    # writer.writerow(['电影名称', '豆瓣评分', '我的评分', '我的评语', '评分时间'])
    all_movies = get_all_movies(access_token, user_id, count, start)
    total_amount = all_movies[1]  # 看过的电影总数
    times = total_amount // count  # /是精确除法，//是向下取整，%是求余
    for i in range(1, times + 2):
        start = (i-1)*50 + 1
        marked_movie_list = get_all_movies(access_token, user_id, count, start)[0]['interests']  # 看过的所有电影列表
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
    user_name = "zhujihui1991@gmail.com"
    pass_word = "Zhujihui6578602"
    log_in_return = log_in(user_name, pass_word)
    access_token = log_in_return['access_token']
    user_id = log_in_return['douban_user_id']
    write_into_csv(50, 1)
