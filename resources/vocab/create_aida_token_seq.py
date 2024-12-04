import requests
import time
import torch
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('roberta-base')
# AIDA 数据集中的实体标题列表
with open('aida.txt', 'r', encoding='utf-8') as f:
    entity_titles = [line.strip() for line in f]

# 输出目录
output_dir = 'extracted_texts'
os.makedirs(output_dir, exist_ok=True)

start_entity_id = 2
entries = dict()
def fetch_page(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles={title}&explaintext=1"
    response = requests.get(url)
    data = response.json()
    
    pages = data.get('query', {}).get('pages', {})
    for page_id, page_info in pages.items():
        if 'extract' in page_info:
            text = page_info['extract']
            encode_seq = tokenizer(title, text[:32], return_tensors='pt', padding=True, truncation=True)
            entries[start_entity_id] = encode_seq
            # with open(os.path.join(output_dir, f'{title.replace(" ", "_")}.txt'), 'w', encoding='utf-8') as out_file:
            #     out_file.write(text[:32])
    with open(os.path.join(output_dir, "entities_desc.pt", 'wb')) as f:
        torch.save(entries, f)

for title in entity_titles:
    try:
        fetch_page(title)
        print(f"Fetched {title}")
    except Exception as e:
        print(f"Failed to fetch {title}: {e}")
    time.sleep(3)  # 避免触发API速率限制