import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

from TikTokApi import TikTokApi
api = TikTokApi.get_instance()


def get_trending(results: int = 10) -> dict:
    # Since TikTok changed their API you need to use the custom_verifyFp option.
    # In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
    return api.by_trending(count=results, custom_verifyFp="")


def get_nicknames_from_trending(trending: dict) -> set:
    return set([tiktok['author']['nickname'] for tiktok in trending])


def get_user_stat(author_unique_id: int):
    print(author_unique_id, '... in process')
    return api.get_user(author_unique_id)['userInfo']['stats']


if __name__ == '__main__':
    max_workers = None
    trending = get_trending()
    print("Running without threads:")
    without_threads_start = time.time()
    tictok_nicknames = get_nicknames_from_trending(trending)
    print(tictok_nicknames)
    for tictok in trending:
        get_user_stat(tictok['author']['uniqueId'])
    print("Without threads time:", time.time() - without_threads_start)

    print("Running threaded:")
    threaded_start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for tictok in trending:
            get_user_stat(tictok['author']['uniqueId'])
    print("Threaded time:", time.time() - threaded_start)
