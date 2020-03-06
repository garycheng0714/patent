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


def main():

    patent_numbers = get_patent_numbers_from_excel() if args.file else [args.number]

    for number in patent_numbers:
        PatentTw(number).download_all_image()


def get_patent_numbers_from_excel():
    df = pd.read_excel(args.file)
    return df.iloc[:, 0]


class PatentTw:
    base_url = 'https://twpat7.tipo.gov.tw'

    def __init__(self, number):
        self.number = number
        self.download_urls = self.__get_all_image_download_url()

    def __get_all_image_download_url(self):
        detail_url = self.base_url + f'/tipotwoc/tipotwkm?!!FR_{self.number}'

        with urlopen(detail_url) as response:
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.find_all('img', {'src': re.compile(r'/tipotwousr/.*/.*\?')})

        return [self.base_url + tag['src'] for tag in tags]

    def download_all_image(self):
        # download url: 'https://twpat7.tipo.gov.tw/tipotwousr/00050/TWG2090224492_000.png?1037045170'
        # file name: TWG2090224492_000.png
        for download_url in self.download_urls:

            file_name = os.path.basename(download_url).split("?")[0]

            folder_path = os.path.join(os.getcwd(), 'image', self.number)

            if not os.path.isdir(folder_path):
                os.makedirs(folder_path, exist_ok=True)

            print(f'Download {file_name}')

            urlretrieve(download_url, folder_path + '/' + str(file_name))


if __name__ == "__main__":
    main()
