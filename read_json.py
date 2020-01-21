import json
import glob
import collections

files_users = glob.glob("json/users/*.json")
# files_following = glob.glob("json/following/*.json")


def parse_json(argument, jsons):
    user_data = []
    for file in jsons:
        with open(file, 'r') as f:
            data = json.load(f)
            for user in data['data']['user'][f'{argument}']['edges']:
                user_info = user['node']
                user_data.append({
                    'id': user_info['id'],
                    'username': user_info['username'],
                    'full_name': user_info['full_name'],
                    'is_private': user_info['is_private'],
                    'is_verified': user_info['is_verified'],
                    'followed_by_viewer': user_info['followed_by_viewer'],
                })
    users = {'users': user_data}

    return users


def unfollowers (list_1, list_2):
    for following in list_2:
        if following in list_1:
            i =1
            # print(f'{following} Is follow back')
        else:
            print(f'{following} - этот черт не подписан на тебя!')

def sort_list(list,list_2):
    followers_array = []
    following_array =[]
    for key in sorted(list.keys()):
        if list[key]['followed_by_viewer']:
            # print(key, "I followed", list[key]['followed_by_viewer'])
            followers_array.append(key)
    for key in sorted(list_2.keys()):
        # print(key)
        following_array.append(key)
    return followers_array, following_array


users = parse_json('edge_followed_by', files_users)


with open(f'json/users/users.json', 'w') as f:
    json.dump(users, f)


