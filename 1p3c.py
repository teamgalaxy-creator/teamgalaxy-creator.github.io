import requests
import re
import json


# from https://github.com/stevenliuyi/covid19/blob/master/data/1p3a-data/crawler.py
url = 'https://coronavirus.1point3acres.com'
html_txt = requests.get(url=url).text
js_files = re.findall(r'chunks[^"]+\.js', html_txt)

for js_file in set(js_files):
    curr_html_txt = requests.get(url=url + '/_next/static/' + js_file).text
    if ('us-100' in curr_html_txt):
        data = curr_html_txt.split("JSON.parse('")[3]
        data = data.split("')}")[0]

data = data.encode().decode('unicode_escape')
data = json.loads(data)

# check
if (data[0]['id'] != 'us-1'):
    print('Data are not valid!')
    exit(1)

data = json.dumps(
    data,
    indent=2,
    ensure_ascii=False,
)

f = open('assets/1p3c.json', 'w', encoding='utf-8')
f.write(data)
f.close()
print("finished!")