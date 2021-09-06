import cv2
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
            image = image[150:900, 70:600]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
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
    if verbose: logging.info('The image was received correctly') 
    
    # recognizing the text    
    if pdf:
        all_text = []
        for img in image:
            text = image_to_string(img)
            all_text.append(text)
        # save text to file
        with open(output, 'w') as f:
            for text in all_text:
                f.write(text)
        if verbose: logging.info('The image was recognizing and save correctly') 
    else:
        text = image_to_string(image)
        # save text to file
        with open(output, 'w') as f:
            f.write(text)
        if verbose: logging.info('The image was recognizing and save correctly')


if __name__ == '__main__':
    read_doc()
