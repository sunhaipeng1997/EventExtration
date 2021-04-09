''' 创建stanfordnlp服务，并且对文本计算ner结果 '''
# usage: import
# author: luohuagang
# version: 0.0.1
# init: 7/11/2019
# last: 7/11/2019

from stanfordcorenlp import StanfordCoreNLP
import settings


class StanfordNER():
    ''' 调用stanfordnlp工具做ner
    '''
    def __init__(self, text):
        # # 创建stanfordnlp工具，做ner
        # nlp = StanfordCoreNLP(path_or_host=settings.HOST,
        #                       lang=settings.LANG,
        #                       port=settings.PORT)

        nlp = StanfordCoreNLP(r'C:\Users\sun\Desktop\EventExtraction-master\stanford-corenlp-4.2.0', lang='zh')


        self.ner_result = nlp.ner(text)
        nlp.close()


if __name__ == "__main__":
    pass
