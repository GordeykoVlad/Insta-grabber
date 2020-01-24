import pickle
from random import random

import requests
import json
import re
import time
import os

from config import Config

url = 'https://www.instagram.com/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_user_detail = 'https://www.instagram.com/%s/'

username = Config.username
password = Config.password

session_file = 'session_file'


def get_messages_page(s):
    url = 'https://www.instagram.com/'
    s.headers.update()
    try:
        info = s.get(url)
        return info
    except:
        print('error')
        return

def get_user_id_by_username (s, user_name):
    url_info = url_user_detail % user_name
    try:
        info = s.get(url_info)
        json_info = json.loads(re.search(
            "window._sharedData = (.*?);</script>", info.text,
            re.DOTALL).group(1))
        id_user = json_info['entry_data']['ProfilePage'][0]['graphql'][
            'user']['id']
        return id_user, json_info
    except:
        print(f"Could not retrieve information about user "
                            f"{user_name}, url: {url_info}. Status code: "
                            f"{info.status_code}")
        return


def remove_spoiled_session_file(session_file):
    try:
        os.remove(session_file)
        print(f"{session_file} has been successfully deleted")
    except:
        print(f"Could not delete your session file " f"{session_file}. Please delete it manually")


def login(username, password):
    s = requests.Session()
    successful_login = False
    s.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Host": "www.instagram.com",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/",
                "X-Instagram-AJAX": "1",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
            })
    if session_file and os.path.isfile(session_file):
        print("Found session file {session_file}")
        successful_login = True
        with open(session_file, 'rb') as i:
            cookies = pickle.load(i)
            s.cookies.update(cookies)
    else:
        login_post = {
            "username": username,
            "password": password,
        }
        r = s.get(url)
        csrf_token = re.search('(?<="csrf_token":")\\w+', r.text).group(0)
        s.headers.update({"X-CSRFToken": csrf_token})
        time.sleep(2)
        print(csrf_token)
        try:
            login = s.post(url_login, data=login_post, allow_redirects=True)
        except Exception as exc:
            print(exc)
            return

        login_response = login.json()
        try:
            csrftoken = login.cookies['csrftoken']
            s.headers.update({"X-CSRFToken": csrftoken})
        except Exception as exc:
            print("Something wrong with the login")
            print(login.text)
            print(exc)

        if login_response.get('errors'):
            print(f"Something is wrong with Instagram: "
                              f"{login_response['errors']['error']}. Please"
                              f"try to login later.")

        elif login_response.get('message') == 'checkpoint_required':
            try:
                if 'instagram.com' in login_response['checkpoint_url']:
                    challenge_url = login_response['checkpoint_url']
                else:
                    challenge_url = "https://instagram.com" + \
                                    login_response['checkpoint_url']
                print(f"Challenge is required at "
                                 f"{challenge_url}")
                with s as clg:
                    clg.headers.update(
                        {
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Host": "www.instagram.com",
                            "Origin": "https://www.instagram.com",
                            "X-Instagram-AJAX": "1",
                            "Content-Type":
                                "application/x-www-form-urlencoded",
                            "x-requested-with": "XMLHttpRequest",
                        }
                    )
                    # Get challenge page
                    challenge_request_explore = clg.get(challenge_url)

                    # Get CSRF Token from challenge page
                    challenge_csrf_token = re.search(
                        '(?<="csrf_token":")\w+',
                        challenge_request_explore.text).group(0)
                    # Get Rollout Hash from challenge page
                    rollout_hash = re.search(
                        '(?<="rollout_hash":")\w+',
                        challenge_request_explore.text).group(0)

                    # Ask for option 1 from challenge, which is usually
                    # Email or Phone
                    challenge_post = {"choice": 1}

                    # Update headers for challenge submit page
                    clg.headers.update(
                        {"X-CSRFToken": challenge_csrf_token})
                    clg.headers.update({"Referer": challenge_url})

                    # Request Instagram to send a code
                    challenge_request_code = clg.post(
                        challenge_url, data=challenge_post,
                        allow_redirects=True)

                    # User should receive a code soon, ask for it
                    challenge_userinput_code = input(
                        "Challenge is required.\n\nEnter the code which has"
                        " just been sent to your mail/phone: ")
                    challenge_security_post = {
                        "security_code": challenge_userinput_code
                    }

                    complete_challenge = clg.post(
                        challenge_url,
                        data=challenge_security_post,
                        allow_redirects=True,
                    )
                    if complete_challenge.status_code != 200:
                        print("Entered code is not correct, Please try again later")
                        return
                    csrftoken = complete_challenge.cookies["csrftoken"]
                    s.headers.update(
                        {"X-CSRFToken": csrftoken,
                         "X-Instagram-AJAX": "1"}
                    )
                    successful_login = complete_challenge.status_code == 200

            except Exception as err:
                print(f"Login failed. Response: \n\n"
                                  f"{login.text} {err}")
                return False
        elif login_response.get('authenticated') is False:
            print("Could not login into Instagram with user "
                              f"{username}. Make sure you are using"
                              f" correct login and/or password.")
            return
        else:
            rollout_hash = re.search('(?<="rollout_hash":")\\w+',
                                     r.text).group(0)
            s.headers.update({"X-Instagram-AJAX": rollout_hash})
            successful_login = True
        # ig_vw=1536; ig_pr=1.25; ig_vh=772; ig_or=landscape-primary;
        s.cookies['csrftoken'] = csrftoken
        s.cookies['ig_vw'] = '1536'
        s.cookies['ig_pr'] = '1.25'
        s.cookies['ig_vh'] = '772'
        s.cookies['ig_or'] = 'landscape-primary'
        time.sleep(3)

    if successful_login:
        try:
            r = s.get("https://www.instagram.com/")
            csrftoken = re.search('(?<="csrf_token":")\\w+',
                                       r.text).group(0)
            s.cookies['csrftoken'] = csrftoken
            s.headers.update({"X-CSRFToken": csrftoken})
            finder = r.text.find(username)
            if finder != -1:
                user_id = get_user_id_by_username(s,username)
                if user_id:
                    login_status = True
                    print(f"{username} has logged in successfully!")
                else:
                    print(f"Could not login into Instagram with user {username}")
                    if session_file and os.path.isfile(
                            session_file):
                        remove_spoiled_session_file(session_file)
                    return

                if session_file:
                    print(f"Saving cookies to the session file {session_file}")
                    with open(session_file, "wb") as output:
                        pickle.dump(s.cookies, output,
                                    pickle.HIGHEST_PROTOCOL)
                # we need to wait between 3 to 9 seconds just after login
                time.sleep(7)
                return s
            else:
                login_status = False
                print("Login error! Check your login data!")
                if session_file and os.path.isfile(session_file):
                    remove_spoiled_session_file(session_file)

                prog_run = False
        except Exception as exc:
            print(exc)
            return
    else:
        print(f"Could not login to Instagram with user "
                          f"{username}")
        return


s = login(username, password)
# user, json = get_user_id_by_username(s, 'vladgordeyko')
answer = get_messages_page(s)
print(json)

