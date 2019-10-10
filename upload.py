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
