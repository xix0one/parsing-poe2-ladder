import requests

CLASSES = {
    'Ranger1': 'Deadeye',
    'Ranger2': 'Ranger2',
    'Ranger3': 'The Pathfinder',
    'Huntress1': 'Amazon',
    'Huntress2': 'Huntress2',
    'Huntress3': 'Ritualist',
    'Warrior1': 'The Titan',
    'Warrior2': 'The Warbringer',
    'Warrior3': 'Smith of Kitava',
    'Mercenary1': 'The Tactician',
    'Mercenary2': 'The Witchhunter',
    'Mercenary3': 'Gemling Legionnaire',
    'Monk1': 'The Acolyte of Chayula',
    'Monk2': 'The Invoker', 
    'Monk3': 'Monk3',
    'Witch1': 'The Infernalist',
    'Witch2': 'The Blood Mage',
    'Witch3': 'The Lich',
    'Sorceress1': 'The Stormweaver',
    'Sorceress2': 'The Chronomancer',
    'Sorceress3': 'Sorceress3'
}

current_chars_url = "https://pathofexile2.com/internal-api/content/game-ladders"
current_league_url = "https://pathofexile2.com/internal-api/content.json"

headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
}

def get_league():
    try:
        league_response = requests.get(current_league_url, headers=headers, timeout=10)
        league_response.raise_for_status()
        league_data = league_response.json()
    except Exception as e:
        print(f"error: {e}")

    return league_data['data']['league-announcement']['label']['en_US']

def get_chars():
    try:
        chars_response = requests.get(current_chars_url, headers=headers, timeout=10)
        chars_response.raise_for_status()
        chars_data = chars_response.json()
    except Exception as e:
        print(f"error: {e}")

    return chars_data['context']['ladders']

def get_top_10():
    current_league_name = get_league()

    chars_data = get_chars()
    target_league = None
    for ladder in chars_data:
        if ladder['league']['name'] == current_league_name:
            target_league = ladder
            break

    if not target_league:
        print(f"\tleague '{current_league_name}' not found in ladder data")
    else:
        print(f"\ttop 10 ({current_league_name}):")
        for player in target_league['entries'][:10]:
            char = player['character']
            class_name = CLASSES.get(char['class'], char['class'])
            print(f"\t\t{char['level']} | {class_name}")

    

def get_all():
    chars_data = get_chars()

    for ladder in chars_data:
        print(f"\t{ladder['league']['name']}:")
        for chars in ladder['entries']:
            char = chars['character']
            class_name = CLASSES.get(char['class'], char['class'])
            if chars['dead']:
                print(f"\t\t{char['level']} | {class_name} dead")
            else:
                print(f"\t\t{char['level']} | {class_name}")
        print()

choose = 0
while (1):
    print("write all or top 10? -> 1 or 2 -> ", end="")
    choose = int(input())
    if choose == 1:
        get_all()
    elif choose == 2:
        get_top_10()
    else:
        print("enter 1 or 2")