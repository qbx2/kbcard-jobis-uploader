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

    def upload(self, image, notes='', ext='.jpg'):
        response = requests.post('https://apis.jobis.co/v2.03/upload', files={
            'receipts': (f'Receipts{ext}', image, 'image/jpeg'),
            'notes': (None, notes),
            'r_type': (None, 'R'),
            'u_idx': (None, self.user_index),
            'user_token': (None, self.user_token),
        })
        return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('receipts_dir')
    args = parser.parse_args()

    api = JobisAPI(os.environ['JOBIS_API_USER_INDEX'], os.environ['JOBIS_API_USER_TOKEN'])
    receipt_timeline = api.receipt_timeline()
    last_pay_datetime = max(
        datetime.datetime.strptime(pay_time, '%Y-%m-%d %H:%M:%S')
        for pay_time in [
            receipt['pay_time'] for receipt in sum([
                day['receipts'] for day in sum([
                    data['days'] for data in receipt_timeline['data']
                ], [])
            ], [])
        ]
        if pay_time
    )
    print(f'last_pay_datetime: {last_pay_datetime}')

    for receipt in sorted(os.listdir(args.receipts_dir)):
        root, ext = os.path.splitext(receipt)
        assert ext.lower() in ['.jpg', '.png']

        datetime_str, basename = os.path.basename(receipt).split('_', maxsplit=2)
        receipt_datetime = datetime.datetime.strptime(datetime_str, '%Y%m%dT%H%M%S')
        assert receipt_datetime > last_pay_datetime, f'{receipt_datetime} is too old'

        image = open(f'{args.receipts_dir}/{receipt}', 'rb')
        print(api.upload(image, notes='야근식대' if basename[0] == 'D' else '', ext=ext))


if __name__ == '__main__':
    main()
