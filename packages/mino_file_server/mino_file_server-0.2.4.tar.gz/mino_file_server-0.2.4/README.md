# File Service

## POST 文件列表

POST /file/list

> Body 请求参数

```json
{
  "path": "/3ludd/2022/02/12",
  "page": 0,
  "page_size": 2
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» path|body|string| 是 |none|
|» page|body|integer| 是 |从0开始|
|» page_size|body|integer| 是 |none|

> 返回示例

> 200 Response

```json
{
    "path": "/",
    "data": [{"file_path": "/", "file_name": "test.txt", "size": 123, "is_file": True}, ... ]
}
```

## GET 通过 文件地址 下载文件

GET /file/download:path

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|file_path|query|string| 是 |none|
|file_name|query|string| 否 |none|

> 返回示例

> 200 Response


## PUT 上传文件

PUT /file/upload

> Body 请求参数

```yaml
file: ""
file_path: ""
file_name: 123.pdf
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» file|body|string(binary)| 否 |none|
|» file_path|body|string| 否 |none|
|» file_name|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

# 数据模型

