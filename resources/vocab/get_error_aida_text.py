import requests
import time
import os
import pickle

# 输出目录
output_dir = 'extracted_texts'
os.makedirs(output_dir, exist_ok=True)

start_entity_id = 2
entries = dict()
errors = []
entity_titles = []
cnt = 0 

def fetch_page(title):
    global entries
    global errors
    global cnt
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles=Frankfurt&explaintext=1"
    print('get text from ', title)
    cnt += 1
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('got response!')
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if ('extract' in set(page_info.keys())):
                text = page_info['extract']
                entries[title] = text[:128]    
                print(title, ':', entries[title])
                print("Saving pkl.....")
                with open(os.path.join(output_dir, "entities_desc_567.pkl"), 'wb') as f:
                    pickle.dump(entries, f)
                entries = dict()
    except Exception as e:
        print('Error occurred, resend now...')
        print(e)
        n_response = requests.get(url)
        if n_response.status_code == 200:
            print('got response!')
        data = n_response.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if ('extract' in set(page_info.keys())):
                text = page_info['extract']
                entries[title] = text[:128]    
                print(title, ':', entries[title])
                print("Saving pkl.....")
                with open(os.path.join(output_dir, "entities_desc_567.pkl"), 'wb') as f:
                    pickle.dump(entries, f)
                entries = dict()
        
if __name__ == '__main__':
    fetch_page('Frankfurt_am_Main')
