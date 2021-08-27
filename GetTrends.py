import time
from concurrent.futures import ThreadPoolExecutor

from TikTokApi import TikTokApi
api = TikTokApi.get_instance()


def get_trending(results: int = 10) -> dict:
    """
    Gets trends of tiktok
    :param results: Amount of results that will be getting
    :return: dict of trends
    """
    return api.by_trending(count=results, custom_verifyFp="")


def get_nicknames_from_trending(trending: dict) -> set:
    """
    Gets nicknames for each author from trends
    :param trending: dict of trends
    :return: set of nicknames
    """
    return set([tiktok['author']['nickname'] for tiktok in trending])


def get_user_stat(author_unique_id: int) -> dict:
    return api.get_user(author_unique_id)['userInfo']['stats']


def get_stat_in_threads(trending: dict, threads: int = None) -> None:
    """
    Gets statistics for each author from trends
    :param trending: dict of trends
    :param threads: the maximum amount of threads
    """
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for trend_video in trending:
            print('\nStat for ', trend_video['author']['nickname'])
            stat_print(get_user_stat(trend_video['author']['uniqueId']))


def stat_print(stat: dict) -> None:
    """
    For pretty printing stat of user
    :param stat: dict type with stat of the user
    :return: None
    """
    for key in stat:
        print(key, ': ', stat[key])


if __name__ == '__main__':
    print('Please input amount of threads')
    try:
        threads = int(input())
    except:
        print('Wrong input, amount of threads must be int')
        threads = None
    trending = get_trending()
    nicknames = get_nicknames_from_trending(trending)
    print('Nicknames:', nicknames)  # If in this line prints only one nickname(TikTok), => something wrong with api
    get_stat_in_threads(trending, threads)

    print('\nSleep 1m...')
    time.sleep(60)
    trending = get_trending()
    nicknames.update(get_nicknames_from_trending(trending))
    get_stat_in_threads(trending, threads)
    exit()

