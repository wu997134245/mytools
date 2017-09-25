# coding=utf-8
import tornado.ioloop
import tornado.web
import torndb
import json

''' url检测方式数据源'''



op = torndb.Connection(host='127.0.0.1',database='o',
                           user='root', password='123456')

def conn_db():
    '''获取停用状态的应用 '''
    sql = '''SELECT
      `app_name`,
      `admin_env`.`env_name`
    FROM
      `app_pools`
      LEFT JOIN `admin_env`
        ON `app_pools`.`env_id` = `admin_env`.`env_id`
        WHERE
        `app_pools`.`status` = 0'''

    data = op.query(sql)
    return data



def available_data():
    '''获取启用状态的应用 '''
    sql = '''SELECT
      `app_name`,
      `admin_env`.`env_name`
    FROM
      `app_pools`
      LEFT JOIN `admin_env`
        ON `app_pools`.`env_id` = `admin_env`.`env_id`
        WHERE
        `app_pools`.`status` = 1'''

    data = op.query(sql)
    return data


def contrast_data():
    '''当一个环境存在两个相同应用时，有停用与启用两个状态，以启用为准'''
    unav_data = pr_data(conn_db())
    an_data = pr_data(available_data())
    for i in unav_data:
        try:
            interc_data = set(an_data[i]) & set(unav_data[i])
        except KeyError:
            continue
        for y in interc_data:
            unav_data[i].remove(y)
    return unav_data





def pr_data(data):
    ''' 数据处理'''
    adcit = {}
    for i in data:
        if adcit.get(i['env_name']):
            adcit[i['env_name']].append(i['app_name'])
        else:
            adcit[i['env_name']] = [i['app_name']]
    return adcit


def get_data():
    adict = contrast_data()
    jsdata = json.dumps(adict)
    return jsdata


class MainHandler(tornado.web.RequestHandler):
    '''添加跨域请求处理'''
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write(get_data())

    options = get



application = tornado.web.Application(handlers = [
    (r"/", MainHandler)], debug= True)



if __name__ == "__main__":
    application.listen(8888)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        op.close()
