import json, yaml, os, logging, datetime, time

from kafka import KafkaProducer

# 解析yaml
cur_path = os.path.dirname(os.path.realpath(__file__))
x = yaml.load(open('%s/config.yml' % cur_path))
kafka_con = x['QUEUES']['KAFKA']['HOST']
kafka_topic = x['QUEUES']['KAFKA']['topic']


# 时间戳转换为时间
def cur_time():
    now = datetime.datetime.now()
    cur_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return cur_time


class NoticePipeline(object):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=kafka_con, api_version=(0, 10, 1),
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
   
    def process_item(self, item, spider):
        up_keywords = ['上币', '上线', '上市', '币种', '新币', '상장일시', '开启', '上架', '换币', 'add', 'New quote currency',
                       '首发', '开放', '开通', '登陆']
        down_keywords = ['下线', '下币', '下架', '关闭', 'delist']
        dic = dict(item)
        if "title" in dic.keys():
            dic['noticeType'] = 1
            for _ in up_keywords:
                if _ in dic['title']:
                    dic['noticeType'] = 2
                    break
            for d in down_keywords:
                if d in dic['title']:
                    dic['noticeType'] = 3
                    break
            time.sleep(1)
            self.producer.send(kafka_topic, dic)
            self.producer.flush()
            logging.info('success to kafka--%s' % spider.name)
            print('success to kafka--%s' % spider.name)
        else:
            logging.error("msg is null --%s" % spider.name)

    def on_close(self, spider):
        self.producer.close()
        logging.info('%s----kafka already close' % spider.name)
