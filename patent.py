from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import pandas as pd
import re
import os

parser = ArgumentParser()
parser.add_argument("-n", "--number", help="The number of patent")
parser.add_argument("-f", "--file", help="Get all images of the patent in the excel file")
args = parser.parse_args()

image_domain = 'https://twpat7.tipo.gov.tw'


def main():

    patent_numbers = get_patent_numbers_from_excel() if args.file else [args.number]

    for number in patent_numbers:
        response = urlopen('https://twpat7.tipo.gov.tw/tipotwoc/tipotwkm?!!FR_{}'.format(number))

        html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        image_tags = soup.find_all('img', {'src': re.compile(r'/tipotwousr/.*/.*\?')})

        create_image_folder(number)

        download_all_image(number, image_tags)


def get_patent_numbers_from_excel():
    df = pd.read_excel(args.file)
    return df.iloc[:, 0]


def create_image_folder(number):
    image_folder_path = os.path.join(os.getcwd(), 'image', number)

    if not os.path.isdir(image_folder_path):
        os.makedirs(image_folder_path, exist_ok=True)


def download_all_image(number, tags):
    image_folder_path = os.path.join(os.getcwd(), 'image', number)

    for tag in tags:
        image_download_url = image_domain + tag["src"]

        image_name = os.path.basename(image_download_url).split("?")[0]

        print('Download: ' + str(image_name))

        urlretrieve(image_download_url, image_folder_path + '/' + image_name)


if __name__ == "__main__":
    main()
