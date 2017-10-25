# -*- coding: utf-8 -*-
import translate
import pytesseract
from PIL import Image
import cv2, re
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
# import enchant


def ocr(cv_image):
	# image = Image.open(image_path)
	# image = Image.fromstring("RGB", cv.GetSize(cv_image), cv_image.tostring())

    image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(image)
    # print('--{}--'.format(text))
    # text = text.replace('\n', ' &dog1# ')
    # print('OCR text:\n--{}--'.format(text))

    return text


def trans(text):

	# https://cloud.google.com/translate/docs/languages
	# en,zh,hr,cs,da,nl,fr,de,el,iw,hu,ga,it,ja,ko,pt,ro,ru,sr,es,th,vi
	translator= translate.Translator(to_lang="zh")
	translation = translator.translate(text)

	# print('translation result:', translation)

	return translation


def trans_list_text(text_list):
    # break_string = ' #rocket& '
    split_mark = '*@.'
    text = ''
    for i in range(len(text_list)):
        text += ' #rocket& {}'.format(text_list[i])

    # print('tran: ', text)
    text = trans(text)
    # print('tran: ', text)
    text = re.sub(r' *# *rocket *& *', split_mark, text)
    # print('tran: ', text)
    text = text.split(split_mark)
    # print('tran: ', text)
    new_list = []
    for line in text:
        line = line.strip(' ')
        if line != '':
            new_list.append(line)
    # print('tran list:', new_list)
    # todo
    if len(new_list) != len(text_list):
        print('trans_list_text: error')
        pass
    return new_list


def text_correction(text):
    '''
    words should be splited by ';', which brings high quality !!!
    the shorter string the better quality.
    sometimes it return nothing(is often caused by words connected with blanks), try it again.
    :param text: a string like 'pzza; fo0d; beof; fr1ed; chip5'
    :return: a list of words
    '''

    if isinstance(text, list):
        new_text = ''
        for t in text:
            t = t.strip(' ')
            new_text += "{}; ".format(t)
        # print(new_text)
    else:
        new_text = text

    params = {'mkt': 'en-US', 'mode': 'proof', 'text': new_text}
    key = '5910225ffd544b948c4d83bbae52f076'

    host = 'api.cognitive.microsoft.com'
    path = '/bing/v7.0/spellcheck'

    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-Type': 'application/x-www-form-urlencoded'}

    conn = http.client.HTTPSConnection(host)
    params = urllib.parse.urlencode(params)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    result = response.read()
    print('text_correction:', response.status, response.reason)
    print('text_correction:', result)
    result = get_suggestion(result)

    if isinstance(text, list):
        # todo
        if len(text) != len(result):
            print('text_correction: len(old) != len(new)')
            pass

    return result

def get_suggestion(http_result):
    # print('get_suggestion:', http_result)
    http_str = http_result.decode()
    # print('get_suggestion:', http_str)
    mjson = json.loads(http_str)
    flagged_tokens_list = mjson['flaggedTokens']
    if len(flagged_tokens_list) == 0:
        # todo
        print('http error')
        pass

    # print('flagged_tokens_list:', flagged_tokens_list)
    result = []
    for s in flagged_tokens_list:
        suggestion = s['suggestions'][0]['suggestion']
        result.append(suggestion)

    # print(result)
    return result


def get_food_dict():
    with open('food.txt', encoding='utf-8') as file:
        raw_words = file.readlines()
    words = []
    for w in raw_words:
        w = w.strip('\n')
        words.append(w)
    words = set(words)
    return words


# def local_correction(word):
#     words = get_food_dict()
#     d = enchant.Dict("en_US")
#     if not d.check(word):
#         suggestion = d.suggest(word)
#         sg = set(suggestion)
#         common = words & sg
#         if len(common) > 0:
#             # print('common', common)
#             common = list(common)
#             return common[0]
#         else:
#             # print(suggestion)
#             return suggestion[0]
#     else:
#         # print(word)
#         return word


def filter_words(file_name):
    words = []
    # name = 'food-dict.txt'
    name = file_name

    with open(name, encoding='utf-8') as file:
        lines = file.read()
        lines = lines.lower()

    words = re.findall(r'[za-zA-Z]+', lines)
    words = set(words)
    words = list(words)

    for i in range(len(words)):
        w = words[i]
        words[i] = '{}\n'.format(w)

    with open('food.txt', 'w') as file:
        file.writelines(words)


if __name__ == '__main__':
    #testimg = cv2.imread('testfiles/menu5.jpg')
    # testimg = cv2.imread('/Users/raopengyan/Documents/2017S2/9517/project/stage2/m2.png')
    #
    # text = ocr(testimg)
    # print('OCR text:\n--{}--'.format(text))
    # translation = trans(text)
    # print('translation result:', translation)
    text_list = trans_list_text(['curry chicken', 'fried chips', 'beef with potato'])
    print('tran list:', text_list)
    result = text_correction('pzza fo0d frled chip5')
    print('text_correction A:', result)
    result = text_correction(['pzza', 'fo0d', 'frled', 'chip5'])
    print('text_correction B:', result)
    result = text_correction('Te mo5t de1ici0us fo0d in the w0rld!')
    print('text_correction C:', result)

    # print('test words:', ['pzza', 'fo0d', 'frled', 'chip5'])
    # for t in ['pzza', 'fo0d', 'frled', 'chip5']:
    #     print(local_correction(t))
