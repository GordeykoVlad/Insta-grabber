import json
import glob
import collections

files_followers = glob.glob("json/followers/*.json")
files_following = glob.glob("json/following/*.json")


def parse_json(argument, jsons):
    followers = {}
    for file in jsons:
        with open(file, 'r') as f:
            data = json.load(f)
            for user in data['data']['user'][f'{argument}']['edges']:
                user_info = user['node']
                followers[user_info['username']] = {
                    'id': user_info['id'],
                    'username': user_info['username'],
                    'followed_by_viewer': user_info['followed_by_viewer'],
                    'full_name': user_info['full_name']
                }

    return followers


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

followers = parse_json('edge_followed_by', files_followers)
following = parse_json('edge_follow', files_following)

followers_array, following_array = sort_list(followers, following)
unfollowers(followers_array, following_array)
# sort_list(following)

# sorted_dict = collections.OrderedDict(sorted_x)
# for k,v in followers.items():
#     print(f'{k}, {v["full_name"]}')

# with open('followers.json', 'w') as outfile:
#     json.dump(followers, outfile)
