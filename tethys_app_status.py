#!/usr/local/bin/python

import sys
import os
import time
import json
import requests

# colors
end_style = '\033[0m'
red_style = '\033[0;31m'
green_style = '\033[0;32m'
orange_style = '\033[0;33m'
blue_style = '\033[0;34m'

# variables
success = True
check_count = 0
base_url = sys.argv[1]
install_id = sys.argv[2]
auth_token = sys.argv[3]


# print colors
def c_print(msg, style) -> str:
    return print(f'{style}{msg}{end_style}')


# call api a total of 10 times in the space of 10 minutes
def status_check() -> str:
    global check_count

    request_params = dict(install_id=install_id)
    request_headers = dict(Authorization=f'Token {auth_token}')
    res = requests.get(base_url, params=request_params, headers=request_headers)

    data = json.loads(res.content)

    if check_count == 0:
        c_print(f'Install Start Time: {data["installStartTime"]}', blue_style)

    if not data['installComplete'] and check_count <= 12:  # first 4 minutes
        time.sleep(20)
        check_count += 1
        c_print(data['status'], blue_style)
        status_check()
    elif not data['installComplete'] and 12 < check_count <= 15:  # next 3 minutes
        c_print('App installation is taking longer than expected.', blue_style)
        time.sleep(60)
        check_count += 1
        c_print(data['status'], blue_style)
        status_check()
    elif not data['installComplete'] and 15 < check_count == 16:  # next 3 minutes
        c_print('App installation is taking longer than expected.', blue_style)
        time.sleep(120)
        check_count += 1
        c_print(data['status'], blue_style)
        status_check()
    elif not data['installComplete'] and check_count > 16:  # print logs
        c_print('App installation took too long. See logs below.', orange_style)
        logs_base_url = os.path.join(os.path.dirname(base_url), "logs")
        logs_res = requests.get(logs_base_url, params=request_params, headers=request_headers)

        log_data = logs_res.content
        c_print(log_data, orange_style)
        c_print('\nRESULT: Failed', orange_style)
    elif data['installComplete']:  # successful installation
        c_print(data['status'], green_style)
        c_print(f'Install Completed Time: {data["installCompletedTime"]}', green_style)
        c_print('\nRESULT: Success', green_style)
    else:  # installation failed
        c_print('\nRESULT: Failed', red_style)


def main() -> str:
    status_check()


if __name__ == "__main__":
    main()
