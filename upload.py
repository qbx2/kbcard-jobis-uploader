import argparse
import datetime
import os

import requests
from declrest import endpoint, GET, json_decode, f, read_decode


@endpoint('https://apis.jobis.co')
class JobisAPI:
    def __init__(self, user_index, user_token):
        self.user_index = user_index
        self.user_token = user_token

    @read_decode()
    @json_decode()
    @GET(f('/v2.03/receipts_timeline?u_idx={self.user_index}&user_token={self.user_token}'))
    def receipt_timeline(self, *, params):
        pass

    def upload(self, image, notes=''):
        response = requests.post('https://apis.jobis.co/v2.03/upload', files={
            'receipts': ('Receipts.jpg', image, 'image/jpeg'),
            'notes': (None, notes),
            'r_type': (None, 'R'),
            'u_idx': (None, self.user_index),
            'user_token': (None, self.user_token),
        })
        return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('receipts_dir')
    parser.add_argument('--user-index')
    parser.add_argument('--user-token')
    args = parser.parse_args()

    api = JobisAPI(args.user_index, args.user_token)
    last_receipt_datetime = datetime.datetime.strptime(
        '%Y-%m-%d %H:%M:%S',
        api.receipt_timeline()['data'][0]['days'][0]['receipts']['pay_time'],
    )

    for receipt in os.listdir(args.receipts_dir):
        root, ext = os.path.splitext(receipt)
        assert ext in ['jpg']
        image = open(receipt, 'rb')
        basename, datetime_str = os.path.basename(receipt).split('_', maxsplit=2)
        receipt_datetime = datetime.datetime.strptime('%Y%m%dT%H%M%S')

        assert receipt_datetime > last_receipt_datetime
        api.upload(image, receipt, '야근식대' if basename[0] == 'D' else '')


if __name__ == '__main__':
    main()
