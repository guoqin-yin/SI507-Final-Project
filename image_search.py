import json
import requests
from PIL import Image
from io import BytesIO
from apiclient.discovery import build

API_KEY = "AIzaSyBKF-XX2mCZylqX7ZZDpGvO9mC8wYgJc_Q"
SEARCH_ENGINE_ID = "531157d8783b2a26d"
CACHE_FILENAME = "project2_cache.json"
CACHE_DICT = {} 

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current search result of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def make_request(param):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    resource = build("customsearch", 'v1', developerKey=API_KEY).cse()
    print(param)
    result = resource.list(q=param, cx=SEARCH_ENGINE_ID,searchType='image').execute()

    return result

def make_request_with_cache(param={}):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    

    key_to_find = param
    
    if key_to_find in CACHE_DICT:
        print('using cache')
        return CACHE_DICT[key_to_find]
    else: 
        print('feching')
        search_return = make_request(param)
        CACHE_DICT[key_to_find] = search_return
        save_cache(CACHE_DICT)
        return CACHE_DICT[key_to_find]



if __name__ == "__main__":
    CACHE_DICT = open_cache()
    while True:

        first_input = input('Enter a search term (e.g. Michigan, michigan) or "exit": ').lower()
        # first access, print national sites
        if first_input == 'exit':
            break
        else:
            search_results = make_request_with_cache(first_input)
            count = 0
            for item in search_results['items']:
                count += 1
                info = f"[{count}] {item['title']} {item['link']} {item['image']['height']}*{item['image']['width']}"
                print(info)
            # second access, print selected picture
            while True:
                second_input = input('Choose a number for showing picture or "exit" or "back": ')
                if second_input.isnumeric() and int(second_input) < 11 and int(second_input) > 0:
                    response = requests.get(search_results['items'][int(second_input)-1]['link'])
                    img = Image.open(BytesIO(response.content))
                    img.show()
                elif second_input == 'back':
                    break
                elif second_input == 'exit':
                    exit()
                else: 
                    print('Invalid input')
            
