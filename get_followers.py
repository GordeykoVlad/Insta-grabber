import json
import subprocess
import time
import urllib.parse

url_base = 'https://www.instagram.com/graphql/query/?'

command_template = """curl '{url}' -H 'sec-fetch-mode: cors' -H 'x-ig-www-claim: hmac.AR3y_rRswmP-dPWkhNfVNioXkaghJlLtKhEtaeDBTj1SbSEn' -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: mid=XXlKRAAEAAHak9itdB9b1RrHQ32j; rur=FTW; fbm_124024574287414=base_domain=.instagram.com; ig_cb=1; ig_did=08BE8403-04FB-4A09-B1B6-22925270CFC3; shbid=3453; csrftoken=lJWcytKpzySFZ4KXOgDxA7z63HYciy88; ds_user_id=1907936395; sessionid=1907936395%3AYzxUmwbqVmS5SE%3A25; fbsr_124024574287414=xmNq7xXXKlQUwFBKNgKW-jmlwkb98R3obIoopQhiyy0.eyJ1c2VyX2lkIjoiMTAwMDAyOTQ5NDM0MzI0IiwiY29kZSI6IkFRQVhfUzZlNVpRM2ZtcFQ0ZHIwWHFhN01NUkU1WXZwZEtyTVQ3Y09rcDhCN2padlYzdDVWbVlMMWVxUWdUMFZFUGhnT0pSWUdTdVBCdHJWX3BfamUzVjNyNkE0QW9qNkl3MmlHS1VIclJsMTA2RFlpbjM1MU9BNzBIYmh4dFRDYWpRRXN3TnhwVzlRSENiQlk1ZmxkYWZTXzloVjBnbEpNMFhwTEdPMTFBUVNJRmRYMFpHeGdLbkY4VGo2a1JIc0Q5ZFdTaEVKbnZpbWx5aElFdWM1cmxEMXNTNW5Bd0Z2S1lIV25TSEo2SVkxbFQ2MWFaOFVmWXJZZ01BdG9OazU3Rmdqa1dkX3hPRTU5c1VyLVpXTUhGUk1kTmlxRWFpQkVROG1ySXN6WWtSeW02Nlg4OEZOajQ3SjBWWmhNMnVJdDZqRGw1ZEdsVDhfaEZicHBvM3pUdXZ1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUptMm9MaGtEOW16MlpBTnRZZE9rajJPUzNRblNtWkNWcmtNVTFTbTN1VkpTNEp3UGxlZWxPYzVYWkNYV1V1SEJ2MHhjWkMySWJFZmw1Z3R6M0Nob2dHRzUzUTBGa3Qxc0RYUlBUTUo5U2JjYVdnbXZ0UVhhc2RiQ3RJSThBVHpoME5KYm1JU2RtOVF4RExCdGJKeVh2ekc0TGNCbkJ2blFhbE13SXplIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NzUyMzU1MzJ9; shbts=1576011036.0554223; urlgen="{{\"94.180.161.158\": 41668}}:1ienaw:xozDT3FzKMBQfHFAyVW5-nWPyM0"' -H 'x-csrftoken: lJWcytKpzySFZ4KXOgDxA7z63HYciy88' -H 'x-ig-app-id: 936619743392459' -H 'accept-encoding: gzip, deflate, br' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'accept: */*' -H 'referer: https://www.instagram.com/vladgordeyko/followers/' -H 'authority: www.instagram.com' -H 'sec-fetch-site: same-origin' --compressed > json/followers_{index}.json"""
# command_template = """curl '{url}' -H 'sec-fetch-mode: cors' -H 'x-ig-www-claim: hmac.AR3y_rRswmP-dPWkhNfVNioXkaghJlLtKhEtaeDBTj1SbSEn' -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: mid=XXlKRAAEAAHak9itdB9b1RrHQ32j; rur=FTW; fbm_124024574287414=base_domain=.instagram.com; ig_cb=1; ig_did=08BE8403-04FB-4A09-B1B6-22925270CFC3; shbid=3453; csrftoken=lJWcytKpzySFZ4KXOgDxA7z63HYciy88; ds_user_id=1907936395; sessionid=1907936395%3AYzxUmwbqVmS5SE%3A25; fbsr_124024574287414=xmNq7xXXKlQUwFBKNgKW-jmlwkb98R3obIoopQhiyy0.eyJ1c2VyX2lkIjoiMTAwMDAyOTQ5NDM0MzI0IiwiY29kZSI6IkFRQVhfUzZlNVpRM2ZtcFQ0ZHIwWHFhN01NUkU1WXZwZEtyTVQ3Y09rcDhCN2padlYzdDVWbVlMMWVxUWdUMFZFUGhnT0pSWUdTdVBCdHJWX3BfamUzVjNyNkE0QW9qNkl3MmlHS1VIclJsMTA2RFlpbjM1MU9BNzBIYmh4dFRDYWpRRXN3TnhwVzlRSENiQlk1ZmxkYWZTXzloVjBnbEpNMFhwTEdPMTFBUVNJRmRYMFpHeGdLbkY4VGo2a1JIc0Q5ZFdTaEVKbnZpbWx5aElFdWM1cmxEMXNTNW5Bd0Z2S1lIV25TSEo2SVkxbFQ2MWFaOFVmWXJZZ01BdG9OazU3Rmdqa1dkX3hPRTU5c1VyLVpXTUhGUk1kTmlxRWFpQkVROG1ySXN6WWtSeW02Nlg4OEZOajQ3SjBWWmhNMnVJdDZqRGw1ZEdsVDhfaEZicHBvM3pUdXZ1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUptMm9MaGtEOW16MlpBTnRZZE9rajJPUzNRblNtWkNWcmtNVTFTbTN1VkpTNEp3UGxlZWxPYzVYWkNYV1V1SEJ2MHhjWkMySWJFZmw1Z3R6M0Nob2dHRzUzUTBGa3Qxc0RYUlBUTUo5U2JjYVdnbXZ0UVhhc2RiQ3RJSThBVHpoME5KYm1JU2RtOVF4RExCdGJKeVh2ekc0TGNCbkJ2blFhbE13SXplIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NzUyMzU1MzJ9; shbts=1576011036.0554223; urlgen="{{\"94.180.161.158\": 41668\054 \"89.232.116.66\": 28840}}:1if3NH:wR7e_c7hy0zS_1M02hOZ_V1dcxY"' -H 'x-csrftoken: lJWcytKpzySFZ4KXOgDxA7z63HYciy88' -H 'x-ig-app-id: 936619743392459' -H 'accept-encoding: gzip, deflate, br' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'accept: */*' -H 'referer: https://www.instagram.com/vladgordeyko/following/' -H 'authority: www.instagram.com' -H 'sec-fetch-site: same-origin' --compressed"""
# after = '"after":"QVFDeTcxTnNoeFl1T053bjM5S1RvNnYtelBNOEFkQzVNaHJMSy1OVko4M3VTNlJEc1VtcEdBNDROVFNZZjRWLWZpYm5HSl9Pdmp4RmZEU0UxSHNiMUNLQQ=="'

index = 1
after = None
followers_in_progress = 0
while True:
    after_value = f',"after":"{after}"' if after else ''
    variables = f'{{"id":"1907936395","include_reel":true,"fetch_mutual":false,"first":80{after_value}}}'
    get_params = {
            'query_hash': 'c76146de99bb02f6415203be841dd25a',
            'variables': variables
    }
    ws_url = url_base + urllib.parse.urlencode(get_params)
    result = subprocess.run(command_template.format(url=ws_url, index=index), shell=True)
    if result.returncode != 0:
        exit('Произошло зло, убиваемся')

    with open(f'json/followers_{index}.json', 'r') as f:
        data = json.load(f)

    if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
        break

    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    all_followers = data['data']['user']['edge_followed_by']['count']
    in_current_batch = len(data['data']['user']['edge_followed_by']['edges'])
    followers_in_progress += in_current_batch
    print(f'Обработано {followers_in_progress}/{all_followers}')

    time.sleep(5 if index % 10 != 0 else 20)
    index += 1

print("сосеро")




