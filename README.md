# OSS 文件托管

## 开始

本项目使用流式传输上传和下载 OSS 对象储存的文件，目前实现的功能：

- [x] 下载文件
- [ ] 上传文件

使用前请参考 `.env.example` 文件创建 `.env` 文件，然后修改其中的配置。

开发：

```bash
sanic server.app --host=0.0.0.0 --port=8000 --dev
```

生产：

```bash
sanic server.app --host=0.0.0.0 --port=8000 --fast
```

Docker 部署：

```bash
docker build -t oss-host .
```
