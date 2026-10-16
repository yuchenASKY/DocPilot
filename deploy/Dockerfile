# DocPilot 应用镜像（第 13 步 ④）
#
# 构建（在**项目根目录**跑，不是 deploy/ 里）：
#     docker build -f deploy/Dockerfile -t docpilot:0.1.0 .
# 或者直接用 compose（推荐，见 deploy/docker-compose.yml）：
#     docker compose -f deploy/docker-compose.yml up -d --build

# ★ 基础镜像用 3.12 而不是文档原版的 3.11：
#   本地 `.venv` 就是 Python 3.12，镜像对齐开发环境能避免大量
#   「本机能跑、容器里报错」的差异（pyproject 里 requires-python 是 >=3.10，都满足）。
FROM python:3.12-slim

# TZ：让容器里的日志时间是本地时间（默认 UTC，排查问题时容易看错十几个小时）
# PYTHONUNBUFFERED：日志实时输出。不设的话 Python 会缓冲 stdout，
#   docker logs 看起来像「卡住了」，SSE 也会延迟 —— 这个坑很常见。
# PYTHONDONTWRITEBYTECODE：不写 .pyc，镜像/卷更干净。
ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ---------------------------------------------------------------------------
# ① 先只拷「依赖声明」，再装依赖 —— 这是分层缓存的关键。
#    Docker 每一条指令是一层；只要 pyproject.toml 没变，这一层永远命中缓存。
#    效果：改代码后重新构建是**秒级**；如果反过来（先 COPY 全部代码再装依赖），
#    每次改一行代码都要重装一遍全部依赖，构建从 10 秒变成几分钟。
# ---------------------------------------------------------------------------
COPY pyproject.toml ./

# 为什么要先造一个占位的 app/ 包：
#   `pip install -e .` 会按 `[tool.setuptools.packages.find] include=["app*"]` 去找包，
#   此刻 app/ 还不存在 ⇒ 找不到任何包，安装出来的东西是残的（甚至构建失败）。
#   先放一个空的 `app/__init__.py`，装完依赖后下面再 `COPY app ./app` 用真代码覆盖；
#   editable 安装是按**路径**生效的，覆盖文件不影响它。
RUN mkdir -p app && touch app/__init__.py \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -e ".[all]"

# ---------------------------------------------------------------------------
# ② 再拷代码
# ---------------------------------------------------------------------------
COPY app ./app
COPY scripts ./scripts
COPY data ./data

# ---------------------------------------------------------------------------
# ③ 把已经建好的向量索引一起打进去
#    ★ 顺序不能反：VOLUME 会用一个**空的**匿名卷挂在 /app/.data 上，
#      如果先声明 VOLUME 再 COPY，索引会「被卷挡在外面」——
#      容器起来了、/health 也通，但检索永远返回空，而且不报错。
#      正确顺序是「先 COPY 内容，再声明 VOLUME」：Docker 首次运行时会用
#      镜像里该目录的内容去**初始化**这个卷。
#    另外索引是从 .env 里的服务商花钱建的（3409 个片段），复制进镜像比
#    容器里重建划算得多。
# ---------------------------------------------------------------------------
COPY .data ./.data
VOLUME ["/app/.data"]

EXPOSE 8000

# 健康检查：让 `docker ps` 能显示 healthy/unhealthy，
# compose 的 depends_on: condition: service_healthy 也靠它。
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

# 注意：这里刻意**不加非 root 用户**。
# 想加固的话加这三行（`--chown` 让卷的属主也对得上）：
#     RUN useradd -m -u 1000 app && chown -R app /app
#     COPY --chown=app:app .data ./.data
#     USER app
# 之所以默认不写：命名卷的属主继承自镜像层，一旦和你之前建过的旧卷对不上，
# 表现是「容器一启动就崩、日志说 .data 没权限」——排查起来比加固本身麻烦。

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
