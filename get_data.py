import json
import subprocess
import time
import urllib.parse
import os

url_base = 'https://www.instagram.com/graphql/query/?'

command_template = """curl '{url}' -H 'sec-fetch-mode: cors' -H 'x-ig-www-claim: hmac.AR3y_rRswmP-dPWkhNfVNioXkaghJlLtKhEtaeDBTj1SbVqb' -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: mid=XXlKRAAEAAHak9itdB9b1RrHQ32j; fbm_124024574287414=base_domain=.instagram.com; ig_cb=1; ig_did=08BE8403-04FB-4A09-B1B6-22925270CFC3; csrftoken=lJWcytKpzySFZ4KXOgDxA7z63HYciy88; ds_user_id=1907936395; sessionid=1907936395%3AYzxUmwbqVmS5SE%3A25; fbsr_124024574287414=xmNq7xXXKlQUwFBKNgKW-jmlwkb98R3obIoopQhiyy0.eyJ1c2VyX2lkIjoiMTAwMDAyOTQ5NDM0MzI0IiwiY29kZSI6IkFRQVhfUzZlNVpRM2ZtcFQ0ZHIwWHFhN01NUkU1WXZwZEtyTVQ3Y09rcDhCN2padlYzdDVWbVlMMWVxUWdUMFZFUGhnT0pSWUdTdVBCdHJWX3BfamUzVjNyNkE0QW9qNkl3MmlHS1VIclJsMTA2RFlpbjM1MU9BNzBIYmh4dFRDYWpRRXN3TnhwVzlRSENiQlk1ZmxkYWZTXzloVjBnbEpNMFhwTEdPMTFBUVNJRmRYMFpHeGdLbkY4VGo2a1JIc0Q5ZFdTaEVKbnZpbWx5aElFdWM1cmxEMXNTNW5Bd0Z2S1lIV25TSEo2SVkxbFQ2MWFaOFVmWXJZZ01BdG9OazU3Rmdqa1dkX3hPRTU5c1VyLVpXTUhGUk1kTmlxRWFpQkVROG1ySXN6WWtSeW02Nlg4OEZOajQ3SjBWWmhNMnVJdDZqRGw1ZEdsVDhfaEZicHBvM3pUdXZ1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUptMm9MaGtEOW16MlpBTnRZZE9rajJPUzNRblNtWkNWcmtNVTFTbTN1VkpTNEp3UGxlZWxPYzVYWkNYV1V1SEJ2MHhjWkMySWJFZmw1Z3R6M0Nob2dHRzUzUTBGa3Qxc0RYUlBUTUo5U2JjYVdnbXZ0UVhhc2RiQ3RJSThBVHpoME5KYm1JU2RtOVF4RExCdGJKeVh2ekc0TGNCbkJ2blFhbE13SXplIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NzUyMzU1MzJ9; fbsr_124024574287414=xmNq7xXXKlQUwFBKNgKW-jmlwkb98R3obIoopQhiyy0.eyJ1c2VyX2lkIjoiMTAwMDAyOTQ5NDM0MzI0IiwiY29kZSI6IkFRQVhfUzZlNVpRM2ZtcFQ0ZHIwWHFhN01NUkU1WXZwZEtyTVQ3Y09rcDhCN2padlYzdDVWbVlMMWVxUWdUMFZFUGhnT0pSWUdTdVBCdHJWX3BfamUzVjNyNkE0QW9qNkl3MmlHS1VIclJsMTA2RFlpbjM1MU9BNzBIYmh4dFRDYWpRRXN3TnhwVzlRSENiQlk1ZmxkYWZTXzloVjBnbEpNMFhwTEdPMTFBUVNJRmRYMFpHeGdLbkY4VGo2a1JIc0Q5ZFdTaEVKbnZpbWx5aElFdWM1cmxEMXNTNW5Bd0Z2S1lIV25TSEo2SVkxbFQ2MWFaOFVmWXJZZ01BdG9OazU3Rmdqa1dkX3hPRTU5c1VyLVpXTUhGUk1kTmlxRWFpQkVROG1ySXN6WWtSeW02Nlg4OEZOajQ3SjBWWmhNMnVJdDZqRGw1ZEdsVDhfaEZicHBvM3pUdXZ1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUptMm9MaGtEOW16MlpBTnRZZE9rajJPUzNRblNtWkNWcmtNVTFTbTN1VkpTNEp3UGxlZWxPYzVYWkNYV1V1SEJ2MHhjWkMySWJFZmw1Z3R6M0Nob2dHRzUzUTBGa3Qxc0RYUlBUTUo5U2JjYVdnbXZ0UVhhc2RiQ3RJSThBVHpoME5KYm1JU2RtOVF4RExCdGJKeVh2ekc0TGNCbkJ2blFhbE13SXplIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NzUyMzU1MzJ9; shbid=3453; rur=FTW; shbts=1579454183.0496051; urlgen="{{\"94.180.175.51\": 41668\054 \"193.105.65.70\": 50483}}:1itrxs:TPczcsbHifaUOsKYKqr1hkZRCtc"' -H 'x-csrftoken: lJWcytKpzySFZ4KXOgDxA7z63HYciy88' -H 'x-ig-app-id: 936619743392459' -H 'accept-encoding: gzip, deflate, br' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'accept: */*' -H 'referer: https://www.instagram.com/raj_sury1shi/' -H 'authority: www.instagram.com' -H 'sec-fetch-site: same-origin' --compressed  > json/{dir}/{user_id}/posts{index}.json"""


def get_post_by_user(user_id):
    index = 1
    after = None
    posts_in_progress = 0

    while True:
        user_id = user_id
        after_value = f',"after":"{after}"' if after else ''
        variables = f'{{"id":"{user_id}","first":100{after_value}}}'
        get_params = {
            'query_hash': 'e769aa130647d2354c40ea6a439bfc08',
            'variables': variables
        }
        ws_url = url_base + urllib.parse.urlencode(get_params)
        dirname = f'json/tempdata/{user_id}'
        try:
            os.mkdir(dirname)
        except:
            pass
        result = subprocess.run(command_template.format(url=ws_url, dir='tempdata', user_id=user_id, index=index), shell=True)
        if result.returncode != 0:
            exit('Произошло зло, убиваемся')

        with open(f'json/tempdata/{user_id}/posts{index}.json', 'r') as f:
            data = json.load(f)

        if not data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
            break

        after = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        all_posts = data['data']['user']['edge_owner_to_timeline_media']['count']
        in_current_batch = len(data['data']['user']['edge_owner_to_timeline_media']['edges'])
        posts_in_progress += in_current_batch
        print(f'Обработано {posts_in_progress}/{all_posts}')

        time.sleep(3 if index % 10 != 0 else 20)
        index += 1


def get_user_id():
    user_ids = []
    with open('json/users/users.json', 'r') as f:
        data = json.load(f)
        for user in data['users']:
            if not user['is_private']:
                user_ids.append(user['id'])
    return user_ids


def get_user_by_id(user_id):
    with open('json/users/users.json', 'r') as f:
        data = json.load(f)
        for user in data['users']:
            if str(user_id) == user['id']:
                return user


if __name__ == '__main__':
    get_post_by_user(192454188)
    # user_ids = get_user_by_id()
    # index = 1
    # print(len(user_ids))
    # for user_id in user_ids[117:]:
    #     print(f'User id {user_id}')
    #     try:
    #         get_post_by_user(user_id)
    #     except:
    #         print('error')
    #         continue
    #     time.sleep(2 if index % 10 != 0 else 20)
    #     index += 1
    #
    # print("сосеро")
