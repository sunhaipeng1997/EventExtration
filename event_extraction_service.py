# coding:utf-8
"""
# 搭建rest服务
# author: luohuagang
# version: 0.0.3
# date: 6/25/2019
# last: 7/11/2019
"""
# coding:utf-8
import time
from flask import Flask, jsonify, request

import settings
from event_extraction import EventExtraction
from data_to_graph import DataToGraph
from ner import NER
from stanfordnlp_ner import StanfordNER

SERVICE = Flask(__name__)


@SERVICE.route('/mas/rest/fire/v1', methods=['POST'])
def eventextraction_v1():
    ''' 事件提取
    '''
    result = {}

    result['code'] = 'OK'
    result['msg'] = '调用成功'
    result['timestamp'] = str(int(time.time()))

    json_data = request.get_json()
    news = json_data['text']
    news_test = '11月6日凌晨0时28分，湖南省株洲市天元区神龙小区发生火灾，支队接到报警后，立即调集天元消防中队3台消防车赶赴现场扑救。0时35分，天元中队到达现场，经过侦查发现起火建筑有15层，起火位置在底部一层门面，过火面积约30多平方米，经过初步侦查现场无人员被困和死亡。指挥员立即下令出两支水枪从东面控制火势蔓延，并组织破拆小组对防盗窗进行破拆。0时56分，支队调集栗雨中队3台消防车赶赴增援，栗雨中队于1时08分到达现场，在现场负责进行供水，此时现场已经可以达到不间断供水，天元中队再增设一组人员从西面架设拉梯派遣攻坚组进行内攻。2点20分火灾被完全扑灭，栗雨中队撤离了火灾现场，天元中队在现场留了一台消防车留守现场，防止火灾复燃。目前，起火原因尚在调查中。'
    nlp = StanfordNER(news)
    event = EventExtraction(news, nlp)

    result['body'] = {}
    result['body']['graph'] = DataToGraph(event).graph
    result['body']['event_extraction'] = event.event
    result = event.event
    # print(result)
    print(event.event)
    return jsonify(result)



@SERVICE.route('/mas/rest/fire/v1_2', methods=['POST'])
def eventextraction_v1_2():
    ''' 火灾事件提取v1.2版服务
    '''
    json_data = request.get_json()
    result = {}

    # 处理入参
    if 'app_key' in json_data:
        if json_data['app_key'] != 'masweb_demo':
            result['code'] = settings.CODE_ERROR
            result['msg'] = settings.MSG_ERROR_PARSE + \
                            ': app_key is {}.'.format(json_data['app_key'])
            result['time'] = str(int(time.time()))
            return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': app_key'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    if 'func' in json_data:
        for func in json_data['func']:
            if func not in settings.FUNC_LIST:
                result['code'] = settings.CODE_ERROR
                result['msg'] = settings.MSG_ERROR_PARSE + \
                                ': {} in func'.format(func)
                result['time'] = str(int(time.time()))
                return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': func'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    news = json_data['body']['text']

    # 参数检测通过，则调用成功
    result['code'] = settings.CODE_SUCCESS
    result['msg'] = settings.MSG_SUCCESS
    result['timestamp'] = str(int(time.time()))

    result['body'] = {}

    nlp = StanfordNER(news)
    # 根据func定义返回内容
    if 'ner' in json_data['func']:
        result['body']['ner'] = NER(nlp).ner

    if 'event' in json_data['func']:
        event = EventExtraction(news, nlp)
        result['body']['event_extraction'] = event.event
        if 'graph' in json_data['func']:
            result['body']['graph'] = DataToGraph(event).graph

    # return jsonify(result)


@SERVICE.route('/mas/rest/finance/v1', methods=['POST'])
def eventextraction_finance_v1():
    ''' 火灾事件提取v1.2版服务
    '''
    json_data = request.get_json()
    result = {}

    # 处理入参
    if 'app_key' in json_data:
        if json_data['app_key'] != 'masweb_demo':
            result['code'] = settings.CODE_ERROR
            result['msg'] = settings.MSG_ERROR_PARSE + \
                            ': app_key is {}.'.format(json_data['app_key'])
            result['time'] = str(int(time.time()))
            return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': app_key'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    if 'func' in json_data:
        for func in json_data['func']:
            if func not in settings.FUNC_LIST:
                result['code'] = settings.CODE_ERROR
                result['msg'] = settings.MSG_ERROR_PARSE + \
                                ': {} in func'.format(func)
                result['time'] = str(int(time.time()))
                return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': func'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    news = json_data['body']['text']

    # 参数检测通过，则调用成功
    result['code'] = settings.CODE_SUCCESS
    result['msg'] = settings.MSG_SUCCESS
    result['timestamp'] = str(int(time.time()))

    result['body'] = {}

    nlp = StanfordNER(news)
    # 根据func定义返回内容
    if 'ner' in json_data['func']:
        result['body']['ner'] = NER(nlp).ner

    if 'event' in json_data['func']:
        event = EventExtraction(news, nlp)
        result['body']['event_extraction'] = event.event
        if 'graph' in json_data['func']:
            result['body']['graph'] = DataToGraph(event).graph

    return jsonify(result)


def main():
    ''' main 函数
    '''

    SERVICE.config['JSON_AS_ASCII'] = False
    SERVICE.run(
        host='0.0.0.0',
        port=5003,
        debug=True
    )


if __name__ == '__main__':
    main()
    # eventextraction_v1()
    from stanfordcorenlp import StanfordCoreNLP

    ##指明安装路径和语言类型(中文)
    # nlp = StanfordCoreNLP(r'E:\stanford-corenlp-4.2.0', lang='zh')
    # sentence = '2020吉祥文化金银币正式发行。'
    # print(nlp.word_tokenize(sentence))
    # print(nlp.pos_tag(sentence))
    # print(nlp.ner(sentence))
    # print(nlp.parse(sentence))
    # print(nlp.dependency_parse(sentence))
    # nlp.close()