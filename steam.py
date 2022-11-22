from fake_useragent import UserAgent
import requests


ua = UserAgent()


def get_inventory_list(steam_id, game_id):
    response = requests.get(
        url=f'https://steamcommunity.com/inventory/{steam_id}/{game_id}/2?count=25',
        headers={
        	'User-Agent': f'{ua.random}'},
        	'Referer': f'https://steamcommunity.com/profiles/{steam_id}/inventory/')

    data = response.json()
    items = [item['assetid'] for item in data.get('assets')]

    return items
