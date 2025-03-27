import requests, base64

# from github import Github
# from github import InputGitAuthor, InputGitTreeElement

username = "Afwct"
token = "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"
repo_name = "image"
file_path = "D:/pythonProject/JMComic/18comic_dow/books/00001.jpg"
# 请求头
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# GitHub API的URL
url = f"https://api.github.com/repos/Afwct/image/contents/images"


# 读取文件内容
def upload():
    # 发送请求
    response = requests.put(url, headers=headers, json=data)
    # 检查响应
    if response.status_code == 201:
        print("文件上传成功！")
    else:
        print("文件上传失败:", response.json())

    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

    # 请求体
    data = {"message": "上传图片", "content": file_content, "branch": branch}

    with open(file_path, "rb") as f:
        file_content = f.read()
        print(file_content)
        file_name = file_path.split("/")[-1]
        file_size = len(file_content)
        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
        }
        data = {
            "message": f"Uploading {file_name}",
            "content": file_content.encode("utf-8").hex(),
            "branch": "main",  # 或者你使用的分支名
        }
        response = requests.put(url, json=data, headers=headers)
        print(response.json())


def identify(path):
    file_path = path
    if file_path is not "":
        # 读取图片文件并编码为Base64
        with open(file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode("utf-8")
        upload()


identify()
