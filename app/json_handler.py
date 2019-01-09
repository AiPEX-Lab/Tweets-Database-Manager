# import app
from app.db_models import Tweet
import json
# TODO
from app.db_manager import Manager
from sqlalchemy.exc import IntegrityError



class JsonParser(object):
    def __init__(self):
        manager = Manager()
        self.session = manager.Session()

        self.tweets_info_dict_lst = []
        self.flag_read_tweet = 0

        # self.tweets_queue = queue.Queue()

    # todo catch error path 
    def read_json(self, input_path=''):
        with open(input_path, 'r') as f:
            raw_tweets_info_dict_lst = json.load(f)
            self.tweets_info_dict_lst = raw_tweets_info_dict_lst['features']
            self.flag_read_tweet = 1
        # print('-- FINISH READ -- ')

    def model_tweet(self):
        if self.flag_read_tweet == 1:
            for tweet_info_dict in self.tweets_info_dict_lst:
                print(tweet_info_dict)

                t = Tweet(user_name=tweet_info_dict['properties']['user_name'],
                      latitude=tweet_info_dict['geometry']['coordinates'][0],
                      longitude=tweet_info_dict['geometry']['coordinates'][1],
                      tweet=tweet_info_dict['properties']['tweet'],
                      sentiment=tweet_info_dict['properties']['sentiment'],
                      )
                print()
                self.session.add(t)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()

        else:
            print('DAMN')


    def make(self):
        input_path = '/Users/LouisLvvv/Documents/coding_god/python3/Tweets-Database-Manager/data/test_json_valid_clip.json'

        self.read_json(input_path)
        self.model_tweet()
        print('-- DONE --')


if __name__ == '__main__':

    json_parser = JsonParser()
    json_parser.make()


# print('ues')
# input_path = '../data/test_json_valid_clip.json'
# # input_path = '../data/please.json'
# # input_path = '../data/test.json'
# with open(input_path, 'r') as f:
#     raw_tweets_info_dict_lst = json.load(f)
#     # print(a['features'])

#     # print(raw_tweets_info_dict_lst)
#     # print 

#     tweets_info_dict_lst = raw_tweets_info_dict_lst['features']
#     # print(len(tweets_info_dict_lst))
#     for tweet_info_dict in tweets_info_dict_lst:
#         print(tweet_info_dict)
#         # print(tweet_info_dict['properties']['user_name'])
#         # print(tweet_info_dict['geometry']['coordinates'][0])
#         # print(tweet_info_dict['geometry']['coordinates'][1])
#         # print(tweet_info_dict['properties']['tweet'])
#         # print(tweet_info_dict['properties']['sentiment'])


#         t = Tweet(user_name=tweet_info_dict['properties']['user_name'],
#               latitude=tweet_info_dict['geometry']['coordinates'][0],
#               longitude=tweet_info_dict['geometry']['coordinates'][1],
#               tweet=tweet_info_dict['properties']['tweet'],
#               sentiment=tweet_info_dict['properties']['sentiment'],
#               )

#         # check type 

#         print()


#     # print(a)

#     # parser = ijson.parse(f)
#     # objects = ijson.items(f, 'posts')
#     # objects = ijson.items(f, 'features')
#     # print(list(objects)[0])

#     #
#     # t = Tweet(user_name=_name,
#     #           latitude=_la,
#     #           longitude=_lo,
#     #           tweet=_tweet,
#     #           sentiment=_sentiment,
#     #           )

# # to class
