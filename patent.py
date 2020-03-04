from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import re
import os

parser = ArgumentParser()
parser.add_argument("-n", "--number", help="The number of patent")
args = parser.parse_args()

image_domain = 'https://twpat7.tipo.gov.tw'
image_folder_path = os.path.join(os.getcwd(), args.number)


def main():
    response = urlopen('https://twpat7.tipo.gov.tw/tipotwoc/tipotwkm?!!FR_{}'.format(args.number))

    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')

    image_tags = soup.find_all('img', {'src': re.compile(r'/tipotwousr/.*/.*\?')})

    create_image_folder()

    download_all_image(image_tags)


def create_image_folder():
    if not os.path.isdir(image_folder_path):
        os.mkdir(image_folder_path)


def download_all_image(tags):
    for tag in tags:
        image_download_url = image_domain + tag["src"]

        image_name = os.path.basename(image_download_url).split("?")[0]

        print('Download: ' + str(image_name))

        urlretrieve(image_download_url, image_folder_path + '/' + image_name)


if __name__ == "__main__":
    main()
