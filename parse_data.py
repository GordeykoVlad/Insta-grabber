import json
import glob
import csv
from get_data import get_user_by_id, get_user_id
import time


def parse_by_user_id (user_id):
    files_user = glob.glob(f'json/tempdata/{user_id}/*.json')
    user = get_user_by_id(user_id)
    for file in files_user:
        with open(file, 'r') as f:
            data = json.load(f)
            try:
                media = data['data']['user']['edge_owner_to_timeline_media']
                for post in media['edges']:
                    post = post['node']
                    if not post['is_video']:
                        owner = post['owner']
                        dimensions = post['dimensions']
                        try:

                            caption = post['edge_media_to_caption']['edges'][0]['node']['text']
                            # print(caption)
                        except:
                            caption = None
                        comments = post['edge_media_to_comment']['count']
                        photo_url = post['thumbnail_resources'][3]['src']
                        try:
                            location = post['location']['slug']
                        except:
                            location = None
                        try:
                            tagged = post['edge_media_to_tagged_user']['edges']
                            tagged = len(tagged)
                        except:
                            tagged = 0
                        likes = post['edge_media_preview_like']['count']
                        writer.writerow(
                            {'id': owner['id'], 'username': owner['username'], 'is_verified': user['is_verified'],
                             'posts': media['count'], 'height': dimensions['height'], 'width': dimensions['width'],
                             'caption': caption, 'comments': comments,
                             'photo_url': photo_url, 'is_comments_disabled': post['comments_disabled'],
                             'timestamp': post['taken_at_timestamp'], 'location': location, 'tagged': tagged,
                             'short_code': post['shortcode'], 'likes': likes})
                        # time.sleep(0.02)
            except:
                print('error')


if __name__ == '__main__':
    # user_ids = get_user_id()
    with open('csv/data_beyza.csv', mode='w') as csv_file:
        fieldnames = ['id', 'username', 'is_verified', 'posts', 'height', 'width', 'caption', 'comments',
                      'photo_url', 'is_comments_disabled', 'timestamp', 'location', 'tagged', 'short_code', 'likes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        # for user_id in user_ids:
        #     parse_by_user_id(user_id)
        parse_by_user_id(192454188)
