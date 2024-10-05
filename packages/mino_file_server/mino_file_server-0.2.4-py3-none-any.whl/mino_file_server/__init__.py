import os
import requests

URL_BASE = os.environ.get("MINO_FILE_SERVER_URL_BASE")
assert URL_BASE is not None, "MINO_FILE_SERVER_URL_BASE environment variable is not set"


def move_file(file_path, new_path):
    """
    移动文件到mino文件服务器

    :param file_path: 文件路径
    :param new_path: 新路径
    """
    url = f"{URL_BASE}/file/move-file"
    data = {"file_path": file_path, "new_path": new_path}

    res = requests.get(url, params=data)
    if res.status_code != 200:
        raise Exception(f"移动文件失败, {res.status_code}, {res.text[:100]}")
    return res.json()["data"]

def delete_file(file_path):
    """
    删除文件

    :param file_path: 文件路径
    """
    url = f"{URL_BASE}/file/delete-file"
    data = {"file_path": file_path}

    res = requests.delete(url, params=data)
    if res.status_code != 200:
        raise Exception(f"删除文件失败, {res.status_code}, {res.text[:100]}")
    return res.json()["data"]

def get_file_info(file_path):
    """
    获取文件信息

    :param file_path: 文件路径
    :return: 文件信息

    :example:
    >>> get_file_info("/test.txt")
    >>> {"file_path": "/", "file_name": "test.txt", "size": 123, "is_file": True}
    """
    url = f"{URL_BASE}/file/info"
    data = {"path": file_path}

    res = requests.get(url, params=data)
    if res.status_code != 200:
        raise Exception(f"文件信息获取失败, {res.status_code}, {res.text[:100]}")
    return res.json()["data"]

def get_file_list(root_path, page=1, page_size=1000):
    """
    获取文件列表

    :param root_path: 根路径
    :param page: 页码 (从1开始)
    :param page_size: 每页大小
    :return: 文件列表

    :example:
    >>> get_file_list("/")
    >>> [{"file_path": "/", "file_name": "test.txt", "size": 123, "is_file": True}, ... ]
    """
    url = f"{URL_BASE}/file/list"
    data = {"path": root_path, "page_size": page_size, "page": page - 1}

    res = requests.post(url, json=data)
    if res.status_code != 200:
        raise Exception(f"文件列表获取失败, {res.status_code}, {res.text[:100]}")
    return res.json()["data"]


def upload_file(file_path, save_path):
    """
    上传文件到mino文件服务器

    :param file_path: 文件路径
    :param save_path: 保存路径
    """
    url = f"{URL_BASE}/file/upload"
    payload = {
        "file_path": save_path,
    }
    files = {
        "file": open(file_path, "rb"),
    }
    res = requests.put(url, data=payload, files=files)
    if res.status_code != 200:
        raise Exception(f"上传文件失败, {res.status_code}, {res.text[:100]}")


def download_file_path(file_path, save_path=None):
    """
    从mino文件服务器下载文件

    :param file_path: 文件路径
    :param save_path: 保存路径
    :return: 文件内容
    """
    url = f"{URL_BASE}/file/download:path"
    params = {
        "file_path": file_path,
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"文件下载失败, {res.status_code}, {res.text[:100]}")
    if save_path is not None:
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        with open(save_path, "wb") as f:
            f.write(res.content)
    return res
