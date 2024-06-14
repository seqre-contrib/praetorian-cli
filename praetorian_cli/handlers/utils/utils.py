import json

import click


key_set = {'assets': '#asset#', 'seeds': '#seed#', 'jobs': '#job#', 'risks': '#risk#', 'accounts': '#account#',
           'definitions': '#file#definitions/', 'integrations': '#account#', 'attributes': '#attribute#',
           'references': '#ref#', 'files': '#file#', 'threats': '#threat#'}


def my_result(controller, key, filter="", offset="", pages=1):
    resp = controller.my(dict(key=key, offset=offset), pages)
    result = {'data': []}
    for key, value in resp.items():
        if isinstance(value, list):
            result['data'] += value
    if filter != "":  # filter by name or member only for accounts
        result['data'] = [item for item in resp['accounts'] if filter == item['name'] or filter == item['member']]
    if resp.get('offset'):
        result['offset'] = json.dumps(resp['offset'])
    return result


def paginate(controller, key, item_type="", filter="", offset="", details=False, page="no"):
    pages = 100 if page == 'all' else 1
    while True:
        result = my_result(controller, key, filter, offset, pages)
        result = handle_results(result, item_type)
        display_list(result, details)

        if page == 'interactive' and 'offset' in result:
            if 'offset' in result:
                print("Press any key to view next or 'q' to quit")
                if click.getchar() == 'q':
                    break
                offset = result['offset']
        else:
            break

    if 'offset' in result and not details:
        print(f'There are more results. Add the following argument to the command to view them:')
        print(f"--offset '{result['offset']}'")


def handle_results(result, item_type):
    if item_type == 'integrations':
        result['data'] = [item for item in result['data'] if '@' not in item['member'] and item['member'] != 'settings']
    elif item_type == 'accounts':
        result['data'] = [item for item in result['data'] if '@' in item['member']]
    elif item_type == 'definitions':
        for hit in result.get('data', []):
            hit['key'] = hit['key'].split("definitions/")[-1]
    return result


def display_list(result, details):
    if details:
        print(json.dumps(result, indent=4))
    else:
        for hit in result.get('data', []):
            print(f"{hit['key']}")
