import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
import click
from pytesseract.pytesseract import image_to_string 
import sys
import logging

def get_image(input):
    pdf = False
    # determine what format the file has
    try:
        if '.jpg' in input:
            image = cv2.imread(input)
            if image is None:
                logging.error('JPG image is None, Could not open file')
                raise IOError
            image = cv2.resize(image, None, fx=0.3, fy=0.3)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif '.png' in input:
            image = cv2.imread(input)
            if image is None:
                logging.error('PNG image is None, Could not open file')
                raise IOError
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image =  cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 11) # 91, 11
            cv2.imshow('Image', image)
            # cv2.imshow('Binary image', adaptive_th)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif '.pdf' in input:
            pdf = True
            img_pdf = convert_from_path(input)
            image = []
            for img in img_pdf:
                img = np.array(img)
                image.append(img)
        # input format is not correct
        else:
            click.echo('Wrong format! Please, try again!')
    except IOError:
        click.echo('I/O Error: Could not open file'+input+': No such file or directory')
        logging.error('Exit due to an error')
        sys.exit()
    except Exception as e:
        click.echo(e)
        logging.error('Exit due to an error')
        sys.exit()
    return image, pdf


@click.command()
@click.option('--input')
@click.option('--output')
@click.option('--verbose', is_flag=True, help='Print verbose message')
def read_doc(input, output, verbose):
    if verbose:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    # get an image for recognition
    image, pdf = get_image(input)
    logging.info('The image was received correctly') 
    # recognizing the text    
    if pdf:
        all_text = []
        for img in image:
            text = pytesseract.image_to_string(img)
            all_text.append(text)
        # save text to file
        with open(output, 'w') as f:
            for text in all_text:
                f.write(text)
        logging.info('The image was recognizing and save correctly') 
    else:
        text = pytesseract.image_to_string(image)
        # save text to file
        with open(output, 'w') as f:
            f.write(text)
        logging.info('The image was recognizing and save correctly')



if __name__ == '__main__':
    read_doc()

'''
способы улучшения
1) перевести в оттенки серого
2) уменьшить размер
3) применение порога, чтобы убрать фон
'''
# хорошо сработало
# adaptive_th =  cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11)
"""
Оставшиеся задачи
1) улучшить как-то изображение, чтобы улучшить их распознование 
бинаризация сработала плохо, медианный фильтр всё сломал
попробовать фильтрацию и улучшение контрастности
2) возможно задать вопросы
    2.1 про verbose не понял, что он должен делать
    2.2 второе требование про пост обработку, удалить что не распознал ocr 
    т.е. это обработка текста я так понял
3) выложить всё на github и оформить
    3.1 установка доп пакетов
    3.2 инструкции как пользоваться 
4) Проверить что я всё сделал или возможно что-то упустил
Дополнительно
5) сравнить с работой другой ocr
"""
# mkvirtualenv ocr --python=python3.8
# 13.01 -5
# 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
