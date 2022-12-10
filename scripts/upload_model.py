import requests
from requests.exceptions import HTTPError
import asyncio
import base64
import json
import argparse
import pprint as pp

b2_bucket_id = '9b5a199b944cf7858d490211'
b2_id = '004ba9b4c75d9210000000001'
b2_key = 'K004x4Qv8pj9InJwj1VFqX5STJwubzE'


def get_parser(**parser_kwargs):
    parser = argparse.ArgumentParser(**parser_kwargs)
    parser.add_argument(
        "--file_name",
        type=str,
        nargs="?",
        const=True,
        default="./laion",
        help="directory with laion parquet files, default is ./laion",
    )


async def authorize_account():
    try:
        keys_bytes = f'{b2_id}{b2_key}'.encode('ascii')
        keys_b64 = base64.b64encode(keys_bytes)
        response = await requests.get('https://api.backblazeb2.com/b2api/v2/b2_authorize_account', headers={'Authorization': f'Basic {keys_b64}'}).json()
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return (response['apiUrl'], response['authorizationToken'])


async def upload_lrg_file(api_url, auth_token):
    try:
        response = await requests.post(
            f'{api_url}/b2api/v2/b2_start_large_file', 
            json.dumps(
                { 'fileName': opt.file_name,
                 'contentType': 'b2/x-auto',
                  'bucketId': b2_bucket_id }),
            headers = { 'Authorization': auth_token })

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return response


async def upload_to_b2():
    pp = pp.PrettyPrinter(indent=2)
    try:
        api_url, auth_token = await authorize_account()
        response = await upload_lrg_file(api_url, auth_token)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        response_data = json.loads(response.read())
        pp.pprint(response_data)


if __name__ == '__main__':

    parser = get_parser()
    opt = parser.parse_args()

    asyncio.run(upload_to_b2())

