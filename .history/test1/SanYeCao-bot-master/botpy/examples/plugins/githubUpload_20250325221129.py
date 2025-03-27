import requests, base64

# GitHub仓库信息
repo_owner = "Afwct"
repo_name = "image"
file_name = ""
branch = "main"  # 或你使用的分支名称

# GitHub Token
token = "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"


def upload(args):
    file_path = args
    # 读取图片文件并编码为Base64
    with open(file_path, "rb") as file:
        file_name = file_path.split("/")[-1]
        file_content = base64.b64encode(file.read()).decode("utf-8")

    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/JMComic/{file_name}"

    # 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 请求体
    data = {"message": "上传图片", "content": file_content, "branch": branch}

    # 发送请求
    response = requests.put(url, headers=headers, json=data)

    # 检查响应
    if response.status_code == 201:
        print("文件上传成功！")
    else:
        print("文件上传失败:", response.json())


def getImage(args):
    file_name = args
    # 读取图片文件并编码为Base64

    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/JMComic/{file_name}"

    # 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 发送请求
    response = requests.get(url, headers=headers)

    # 检查响应
    if response.status_code == 200:
        file_info = response.json()
        download_url = file_info["download_url"]
        return download_url
    else:
        return "文件获取失败"
