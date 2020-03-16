import json
from parsers.parser_mebelshara import get_mebelshara_offices
from parsers.parser_tui import get_tui_offices

##### Creating json file #####

if __name__ == '__main__':
    filename = 'offices.json'
    with open(filename, 'w', encoding='utf-8') as f:
        offices = get_mebelshara_offices() + get_tui_offices()
        json.dump(offices, f, ensure_ascii=False, sort_keys=False, indent=4)