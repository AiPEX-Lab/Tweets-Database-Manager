# py3
import argparse
import logging
import os
import re
import glob
import csv
import emoji  
from collections import Counter
import nltk
from nltk.tokenize import TweetTokenizer
# from nltk.book import FreqDist
# required pip == 0.5.1 
# required nltk


def _command_line_parsing():
    parser = argparse.ArgumentParser(description='Accept different paths input.')
    parser.add_argument('--source-dir-data', '-a',
        dest='source_dir_data',
        help='Directory where the tweets\' files are stored.')
    parser.add_argument('--dest-dir', '-b',
                        dest='dest_dir',
                        required=True,
                        help='Directory where the output files will be written.')
    
    parser.add_argument('--debug', '-d',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='Print debug information.')
    return parser.parse_args()

# check ok
def dat2csv(path=''):
    # q: one new line in the end of csv

    # required exist path 
    input_path = '../data/fixed_raw_data_dat/'
    output_path = '../data/fixed_raw_data_csv/'
    source = glob.glob(input_path+'*.dat')
    user_ids = map(lambda x: x.split('/')[-1][:-4], source)
    for user_id in user_ids:
        csv_file = open(output_path + user_id + '.csv', 'w+')
        logging.info('Files is created under %s%s.csv' % (output_path, user_id))
        writer = csv.writer(csv_file)
        with open(input_path+user_id+'.dat') as f:
            content = f.read()
            sentences = re.finditer("{\n(.*\n[^}])*.*\n#POS", content)
            for i in sentences:
                sentence = i.group()[2:-5]  # get rid of {\n and \n#POS
                writer.writerow([id]+[sentence])
    print("BOOM")

# generator check ok
def read_csv(path='', switch=-1):
    # if switch == 1:
    #     input_path = '../data/fixed_raw_data_csv/'  # step1: to Xemoji
    # else:
    # dct = {}
    input_path = '../data/fixed_data_Xemoji_csv/'  # step2: to Xfewwords
    input_path = '../data/fixed_data_Xfewwords_csv/'  # step3: to Xemoticon
    input_path = '../data/fixed_data_Xemoticon_csv/'  # step4: to Xmultipunc

    source = glob.glob(input_path+'*.csv')
    for csv_file_path in source:
        yield csv_file_path

# check ok
def files_emoji_filter():
    output_path = '../data/fixed_data_Xemoji_csv/'
    for input_file_csv in read_csv(switch=1):
        with open(input_file_csv, 'r') as f:
            user_id = input_file_csv.split('/')[-1][:-4]
            csv_file = open(output_path + user_id + '.csv', 'w+')
            logging.info('Output path -> %s%s.csv' % (output_path, user_id))
            writer = csv.writer(csv_file)
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                ori_sentence = row[1]
                ret = emoji_filter(ori_sentence)
                writer.writerow([user_id]+[ret])

# check ok?
def emoji_filter(ori_sentence=''):
    ret = re.sub(r':([a-zA-Z_-]+):', r' emj_\1 ', emoji.demojize(ori_sentence))
    return ret

# check ok
def files_fewwords_filter():
    output_path = '../data/fixed_data_Xfewwords_csv/'
    for input_file_csv in read_csv():
        with open(input_file_csv, 'r') as f:
            user_id = input_file_csv.split('/')[-1][:-4]
            csv_file = open(output_path + user_id + '.csv', 'w+')
            logging.info('Output path -> %s%s.csv' % (output_path, user_id))
            writer = csv.writer(csv_file)
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                ori_sentence = row[1]
                signal, ret = fewwords_filter(ori_sentence)
                if signal:
                    writer.writerow([user_id]+[ret])

# check ok
"""
Return a signal sign and the sentence
"""
def fewwords_filter(ori_sentence='', words_min_limit=2):
    # to-do complete!!!
    if len(ori_sentence.split()) < words_min_limit:
        return (False, '')
    else:
        return (True, ori_sentence)

# step3
# check ok
def files_emoticon_filter():
    output_path = '../data/fixed_data_Xemoticon_csv/'
    for input_file_csv in read_csv():
        with open(input_file_csv, 'r') as f:
            user_id = input_file_csv.split('/')[-1][:-4]
            csv_file = open(output_path + user_id + '.csv', 'w+')
            logging.info('Output path -> %s%s.csv' % (output_path, user_id))
            writer = csv.writer(csv_file)
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                ori_sentence = row[1]
                ret = emoticon_filter(ori_sentence)
                writer.writerow([user_id]+[ret])

# check ok
def emoticon_filter(ori_sentence=''):
    
    # substring_list = [':)', ':(', ':p', ':D', ':-)']
    s = ori_sentence
    s = re.sub(r':\)', r' emtc_happy_face_a ', s)
    s = re.sub(r':\(', r' emtc_sad_face_a ', s)
    s = re.sub(r':p', r' emtc_tongue_out_a ', s)
    s = re.sub(r':D', r' emtc_happy_face_b ', s)
    s = re.sub(r':-\)', r' emtc_happy_face_c ', s)

    return s



# step4
# check ok
def files_multipunc_filter():
    output_path = '../data/fixed_data_Xmultipunc_csv/'
    for input_file_csv in read_csv():
        with open(input_file_csv, 'r') as f:
            user_id = input_file_csv.split('/')[-1][:-4]
            csv_file = open(output_path + user_id + '.csv', 'w+')
            logging.info('Output path -> %s%s.csv' % (output_path, user_id))
            writer = csv.writer(csv_file)
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                ori_sentence = row[1]
                ret = multipunc_filter(ori_sentence)
                writer.writerow([user_id]+[ret])

# check ok
def multipunc_filter(ori_sentence=''):
    ret = re.sub(r'[!\?\.][!\?\.]+', r' MULTI_PUNC ', ori_sentence)
    return ret

# assume all in one file
# log write to files
def files_ngram_counter():
    container = ''
    for input_file_csv in read_csv():
        with open(input_file_csv, 'r') as f:
            # user_id = input_file_csv.split('/')[-1][:-4]
            logging.info('Input path <- %s' % (input_file_csv))
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                container += row[1] + '\n'
                print(row[1])
                break

    n1 = ngram_counter(container, 1)
    n2 = ngram_counter(container, 2)
    n3 = ngram_counter(container, 3)
    print(n1)
    print(n2)
    print(n3)
    return True    

# self
def ngram_counter(instring, mlen):
    tknzr = TweetTokenizer()
    lst = tknzr.tokenize(instring)
    return Counter(map(' '.join, zip(*[lst[i:] for i in range(mlen)])))

# others
def bigram_counter(instring):
    tknzr = TweetTokenizer()
    lst = tknzr.tokenize(instring)
    gnt = nltk.bigrams(lst)
    fdist1 = FreqDist(list(gnt))
    ret = []
    for k, v in fdist1.items():
        ret.append((k,v))
    # return fdist1.most_common(0)
    return ret


# lower?? chars
# backup holding
def at_remover(text):
    sentence = re.sub(r"@\S+", "", text)
    return sentence
def link_remover(text):
    sentence = re.sub(r"http\S+", "", text)
    return sentence


if __name__ == '__main__':
    # $ python3 super_preprocessor.py --source-dir-data ../data/fixed_raw_data/ --dest-dir ../data/test_data
    # args = _command_line_parsing()
    # logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
    # logging.info(''.join(['Starting filtering out data ...',
    #                    '\n\tsource directory data = ', str(args.source_dir_data),
    #                    '\n\tdestination directory = ', str(args.dest_dir),
    #                    '\n\tdebug = ', str(args.debug),
    #                  ]))
    # logging.info('Creating output directories ...')
    # if os.path.exists(args.dest_dir):
    #     logging.error(''.join(['Destination directory ', args.dest_dir, ' already exists. Quitting ...']))
    #     sys.exit(1)
    # else:
    #     os.makedirs(args.dest_dir)
    logging.basicConfig(level=logging.DEBUG if False else logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
    
    # step0
    # dat2csv()

    # step1
    # print(emoji_filter('Middle school was so fun😂😂'))
    assert emoji_filter('Middle school was so fun😂😂') == 'Middle school was so fun emj_face_with_tears_of_joy  emj_face_with_tears_of_joy '
    # files_emoji_filter()

    # step2
    # print(fewwords_filter(' Middle  '))
    assert fewwords_filter(' Middle  ') == (False, '')
    # print(fewwords_filter(' Middle school  '))
    assert fewwords_filter(' Middle school  ') == (True, ' Middle school  ')

    # files_fewwords_filter()

    # step3
    # print(emoticon_filter(":D is:p it? :) TAG:) URL :-) "))
    assert emoticon_filter(":D is:p it? :) TAG:) URL :-) ") == ' emtc_happy_face_b  is emtc_tongue_out_a  it?  emtc_happy_face_a  TAG emtc_happy_face_a  URL  emtc_happy_face_c  '
    # files_emoticon_filter()

    # step4
    # to-do: multi-punc
    # print(multipunc_filter("hi!? hi .?. !?!hi !"))
    assert multipunc_filter("hi!? hi .?. !?!hi !") == 'hi MULTI_PUNC  hi  MULTI_PUNC   MULTI_PUNC hi !'
    # files_multipunc_filter()

    # step5
    # ngram
    s = 'NUMst place in culinary and management what what MULTI_PUNC  URL emtc_happy_face_a '
    # print(ngram_counter(s, 3))
    assert ngram_counter(s, 1) == Counter({'what': 2, 'emtc_happy_face_a': 1, 'and': 1, 'management': 1, 'place': 1, 'in': 1, 'NUMst': 1, 'culinary': 1, 'MULTI_PUNC': 1, 'URL': 1})
    assert ngram_counter(s, 3) == Counter({'MULTI_PUNC URL emtc_happy_face_a': 1, 'in culinary and': 1, 'management what what': 1, 'what MULTI_PUNC URL': 1, 'place in culinary': 1, 'NUMst place in': 1, 'and management what': 1, 'culinary and management': 1, 'what what MULTI_PUNC': 1})
    files_ngram_counter()
    # print(bigram_counter(s))

