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
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles={title}&explaintext=1"
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
                if cnt % 100 == 0:
                    print("Saving pkl.....")
                    with open(os.path.join(output_dir, "entities_desc_{}.pkl".format(int(cnt / 10))), 'wb') as f:
                        pickle.dump(entries, f)
                    entries = dict()
    except Exception as e:
        print('Error occurred, resend now...')
        print(e)
        n_response = requests.get(url)
        if n_response.status_code == 200:
            print('got response!')
        cnt += 1
        data = n_response.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if ('extract' in set(page_info.keys())):
                text = page_info['extract']
                entries[title] = text[:128]    
                print(title, ':', entries[title])
                if cnt % 100 == 0:
                    print("Saving pkl.....")
                    with open(os.path.join(output_dir, "entities_desc_{}.pkl".format(int(cnt / 10))), 'wb') as f:
                        pickle.dump(entries, f)
                    entries = dict()
        

if __name__ == '__main__':
    # AIDA 数据集中的实体标题列表
    with open('aida.txt', 'r', encoding='utf-8') as f:
        entity_titles = [line.strip() for line in f]
    # error_entries = dict()
    # with open('error_items.pkl', 'r') as f:
    #     pickle.load(error_entries, f)

    for title in entity_titles:
        try:
            fetch_page(title)
            print(f"Fetched {title}")
            print('===========\n')
        except Exception as e:
            print(f"Failed to fetch {title}: {e}")
            errors.append(title)
            print('Error item ', title, ' appended!')

        time.sleep(1)  # 避免触发API速率限制

    with open(os.path.join(output_dir, "entities_desc_{}.pkl".format(int(cnt / 10))), 'wb') as f:
        pickle.dump(entries, f)

    print(errors)
    if len(errors) > 0:
        with open(os.path.join(output_dir, 'errors_items.pkl'), 'wb') as f:
            pickle.dump(errors, f)
    print('cnt pt: ', cnt)