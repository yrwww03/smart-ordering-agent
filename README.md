# Smart Ordering Agent

基于 FastAPI、LangChain 和 MySQL 的智能点餐 Agent 项目。后端使用 Python 与 FastAPI，前端使用 Vue 3 与 Vite。

## 项目目录

```text
smart-ordering-agent/
├── agent/              # Agent、Prompt、Redis 与 Milvus 相关代码
├── api/                # FastAPI 接口
├── models/             # 本地嵌入模型
├── tests/              # 后端测试
├── ui/                 # Vue 前端
├── .env                # 本地环境变量，不提交 Git
├── pyproject.toml      # Python 项目与依赖声明
├── run.py              # 后端启动入口
└── uv.lock             # Python 依赖锁文件
```

## 环境要求

- Windows PowerShell
- Python 3.13 或更高版本
- [uv](https://docs.astral.sh/uv/)
- Node.js 与 npm

检查环境：

```powershell
python --version
uv --version
node --version
npm.cmd --version
```

## 首次安装

### 1. 同步后端依赖

在项目根目录执行：

```powershell
cd D:\roway_code\ai\smart-ordering-agent
uv sync
```

`uv sync` 会读取 `pyproject.toml` 和 `uv.lock`，并将依赖安装到项目的 `.venv/`。

### 2. 安装前端依赖

进入 `ui/` 目录：

```powershell
cd D:\roway_code\ai\smart-ordering-agent\ui
npm.cmd install
```

如果官方 npm 源频繁出现 `ECONNRESET`，可以单次使用国内镜像：

```powershell
npm.cmd install `
  --registry=https://registry.npmmirror.com `
  --fetch-retries=5 `
  --fetch-retry-maxtimeout=120000
```

安装成功后确认 Vite 已生成：

```powershell
$LASTEXITCODE
Test-Path .\node_modules\.bin\vite.cmd
```

预期结果：

```text
0
True
```

## 启动项目

前后端需要分别占用一个终端。建议先启动后端，再启动前端。

### 终端一：启动后端

在项目根目录执行：

```powershell
cd D:\roway_code\ai\smart-ordering-agent
uv run python run.py
```

后端默认地址：

```text
http://127.0.0.1:8000
```

健康检查：

```text
http://127.0.0.1:8000/health
```

FastAPI 接口文档：

```text
http://127.0.0.1:8000/docs
```

也可以在 PowerShell 中验证：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

预期结果：

```text
status
------
ok
```

### 终端二：启动前端

在 `ui/` 目录执行：

```powershell
cd D:\roway_code\ai\smart-ordering-agent\ui
npm.cmd run dev
```

前端默认地址：

```text
http://localhost:3000
```

不要在项目根目录运行 `npm.cmd run dev`。项目根目录没有 `package.json`，前端的 `package.json` 位于 `ui/`。

## 前后端连接关系

Vite 开发服务器监听 `3000` 端口，FastAPI 后端监听 `8000` 端口。

前端发送到 `/api/*` 的请求会由 Vite 转发给后端，并去掉 `/api` 前缀：

```text
浏览器请求：http://localhost:3000/api/health
后端收到：http://127.0.0.1:8000/health
```

代理配置位于：

```text
ui/vite.config.js
```

## 停止服务

分别回到前端和后端终端，按：

```text
Ctrl+C
```

## 常见问题

### PowerShell 找不到 `uv`

uv 默认安装位置可能是：

```text
C:\Users\你的用户名\.local\bin\uv.exe
```

可以先使用完整路径：

```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" --version
& "$env:USERPROFILE\.local\bin\uv.exe" run python run.py
```

临时加入当前终端 PATH：

```powershell
$uvBin = "$env:USERPROFILE\.local\bin"
$env:Path = "$uvBin;$env:Path"
```

### PowerShell 禁止运行 `npm.ps1`

使用 `npm.cmd`，不要使用 `npm`：

```powershell
npm.cmd install
npm.cmd run dev
```

### npm 提示找不到 `package.json`

说明当前目录不正确。先进入前端目录：

```powershell
cd D:\roway_code\ai\smart-ordering-agent\ui
Test-Path .\package.json
```

结果应为 `True`。

### 提示找不到 `vite`

说明前端依赖没有完整安装。进入 `ui/` 后重新安装，并且只有安装成功后才启动：

```powershell
cd D:\roway_code\ai\smart-ordering-agent\ui
npm.cmd install --registry=https://registry.npmmirror.com

if ($LASTEXITCODE -ne 0) {
    throw "Frontend dependency installation failed."
}

Test-Path .\node_modules\.bin\vite.cmd
npm.cmd run dev
```

### `start.bat` 输出中文乱码

当前复制的 `ui/start.bat` 使用 UTF-8、LF 换行以及中文和 Emoji，Windows CMD 可能错误解析。开发阶段建议直接执行：

```powershell
cd D:\roway_code\ai\smart-ordering-agent\ui
npm.cmd run dev
```

### Uvicorn 提示找不到 `api.main:app`

确认 `api/main.py` 中存在：

```python
from fastapi import FastAPI

app = FastAPI()
```

并且后端命令从项目根目录执行。

## Git 提交注意事项

以下本地文件和目录不应提交：

```text
.env
.venv/
node_modules/
ui/node_modules/
ui/dist/
.idea/
__pycache__/
```

以下依赖声明文件应提交：

```text
pyproject.toml
uv.lock
ui/package.json
ui/package-lock.json
```

提交前检查：

```powershell
git status
```

不要提交 API Key、数据库密码、模型密钥或其他敏感信息。
