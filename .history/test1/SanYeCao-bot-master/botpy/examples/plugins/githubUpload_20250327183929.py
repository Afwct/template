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
        return 1
    else:
        print("文件上传失败:", response.json())
        return 0


def getImage(args):
    file_name = args

    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/JMComic/{file_name}"

    # 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v4+raw",
    }

    try:
        # 发送请求
        response = requests.get(url, headers=headers)
        # 检查HTTP错误
        response.raise_for_status()

        # 如果是二进制文件，直接返回原始内容
        # if response.headers['Content-Type'].startswith('application/octet-stream'):
        #     # 直接返回原始内容URL
        #     return response.url

        # 如果是文本文件，需要解析JSON获取下载链接
        data = response.json()
        return data.get("download_url", data.get("html_url"))

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


# geturl = getImage("[狗野叉漢化] [AREA188] 嫌がる妻を説得して初めて他人棒に貸し出しました結果たった一晩でイクイクセフレ人形に墮とされました.pdf")
# geturl = getImage("00003.jpg")
# print(geturl)


def getCX():
    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/JMComic/cx.jpg"

    # 请求头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v4+raw",
    }

    try:
        # 发送请求
        response = requests.get(url, headers=headers)
        # 检查HTTP错误
        response.raise_for_status()

        # 如果是二进制文件，直接返回原始内容
        # if response.headers['Content-Type'].startswith('application/octet-stream'):
        #     # 直接返回原始内容URL
        #     return response.url

        # 如果是文本文件，需要解析JSON获取下载链接
        data = response.json()
        return data.get("download_url", data.get("html_url"))

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
a = getCX()
print(a)