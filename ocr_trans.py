import translate
import pytesseract
from PIL import Image
import cv2


def ocr(cv_image):
	# image = Image.open(image_path)
	# image = Image.fromstring("RGB", cv.GetSize(cv_image), cv_image.tostring())

    image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(image)
    # print('--{}--'.format(text))
    # text = text.replace('\n', ';')
    # print('OCR text:\n--{}--'.format(text))

    return text


def trans(text):

	# https://cloud.google.com/translate/docs/languages
	# en,zh,hr,cs,da,nl,fr,de,el,iw,hu,ga,it,ja,ko,pt,ro,ru,sr,es,th,vi
	translator= translate.Translator(to_lang="zh")
	translation = translator.translate(text)

	# print('translation result:', translation)

	return translation


if __name__ == '__main__':
    #testimg = cv2.imread('testfiles/menu5.jpg')
    testimg = cv2.imread('test.png')

    text = ocr(testimg)
    print('OCR text:\n--{}--'.format(text))
    translation = trans(text)
    print('translation result:', translation)