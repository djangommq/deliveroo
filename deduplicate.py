import csv
import os
from utils import WEB_NAME, VERSION, fields


def deduplicate_csv():
    # city_names = [
    #     'au',
    #     'ae',
    #     'be',
    #     'de',
    #     'es',
    #     'fr',
    #     'hk',
    #     'ie',
    #     'it',
    #     'nl',
    #     'sg',
    #     'uk',
    # ]
    data_dir = '../crawlerOutput/{}/{}'.format(VERSION, WEB_NAME)
    files = os.listdir(data_dir)
    for file in files:
        if not file.endswith('csv'):
            continue
        new_dir = os.path.join(data_dir, 'deduplicate')
        raw_path = os.path.join(data_dir, file)
        new_path = os.path.join(new_dir, file)
        result_date = {}
        with open(raw_path, 'r', newline='', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f, fieldnames=fields)
            for r in csv_reader:
                if csv_reader.line_num == 1:
                    continue
                resto_id = r.get('resto_id')
                result_date[resto_id] = r

        with open(new_path, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fields)
            if not os.path.getsize(new_path):
                csv_writer.writeheader()
            csv_writer.writerows(result_date.values())


if __name__ == "__main__":
    deduplicate_csv()