import requests

username = 'Afwct'
token = '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'
repo_name = 'image'
file_path = 'path_to_your_image.pdf'
 
# GitHub API的URL
url = f'https://api.github.com/repos/{username}/{repo_name}/contents/images'
 
# 读取文件内容
with open(file_path, 'rb') as f:
    file_content = f.read()
    file_name = file_path.split('/')[-1]
    file_size = len(file_content)
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'message': f'Uploading {file_name}',
        'content': file_content.encode('utf-8').hex(),
        'branch': 'main'  # 或者你使用的分支名
    }
    response = requests.put(url, json=data, headers=headers)
    print(response.json())