"""工具（Function Calling）注册表。

Function Calling 的本质：
模型不执行任何代码，它只是输出一段 JSON，告诉你「我想调用哪个函数、参数是什么」；
真正的执行、结果回传，都是你的程序做的。
这一点面试里被反复问，务必能自己讲清楚。
"""

from __future__ import annotations

import ast
import json
import logging
import operator
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from . import retriever, tracing

# 每个模块用自己名字的 logger（__name__ 就是模块名）——
# 日志里能看出是哪个文件打的，第 12 步接 Langfuse 也靠它做分组。
logger = logging.getLogger(__name__)


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    func: Callable[..., Any]

    def to_openai_schema(self) -> dict:
        """转成 OpenAI tools 字段要求的 JSON Schema 结构。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


async def search_documents(query: str, top_k: int = 5) -> str:
    """检索本地知识库。"""
    hits = await retriever.retrieve(query, top_k=top_k, use_hybrid=True)
    if not hits:
        return "知识库为空或没有命中任何片段。请先执行 build_index.py 建立索引。"
    lines = []
    for i, h in enumerate(hits, start=1):
        loc = f"{h.source}" + (f" 第 {h.page} 页" if h.page else "")
        lines.append(f"[{i}] {loc}（相关度 {h.score:.4f}）\n{h.text[:400]}")
    return "\n\n".join(lines)


async def calculator(expression: str) -> str:
    """安全的四则运算

    ⚠️ 先看这个反面教材：最省事的写法是 `return str(eval(expression))`。
    但模型传进来的参数属于不可信输入 —— 它可以传
    `__import__('os').system('calc')`，那就是一个远程命令执行漏洞。
    所以本函数的要求是：代码里不许出现 `eval(` / `exec(`。

    规格（做到这四条就算过）：
      1. 支持 + - * / ** % 和一元负号，能正确处理括号与运算优先级；
      2. 危险表达式（含函数调用、属性访问、import 等）必须拒绝，
         返回以「计算失败」开头的中文说明，或者抛异常 —— 但绝不能执行；
      3. 除零、语法错误等异常不能把 Agent 打挂，要返回可读的错误文本；
      4. 正常表达式返回结果的字符串形式（如 `(12+34)*5` → `"230.0"`）。

    提示：
      - 思路是「解析成语法树，然后只放行白名单节点」：
        `ast.parse(expression, mode="eval")` 拿到树，递归遍历，
        只允许 `Expression` / `Constant`（数字）/ `BinOp`（运算符在白名单里）
        / `UnaryOp`（正负号），其余一切节点直接拒绝；
      - 具体哪个运算符对应 `operator` 模块里的哪个函数，去查 Python 官方文档的
        `operator` 章节 —— 别猜，猜错了会静默算错；
      - `ast` 和 `operator` 文件顶部已经 import 好了。
    """
    # 白名单：只放行这些运算符，其余 AST 节点一律拒绝
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.operand))
        # 走到这里说明出现了白名单外的节点（函数调用、属性访问、import …）
        raise ValueError("表达式含有不被允许的运算")

    try:
        return str(_eval(ast.parse(expression, mode="eval")))
    except Exception as exc:  # noqa: BLE001
        # 除零、语法错误都不能把 Agent 打挂，转成可读文本返回
        return f"计算失败：{exc}"


async def current_time(timezone: str = "Asia/Shanghai") -> str:
    """返回当前时间。真实项目里换成 zoneinfo 处理时区。"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


async def web_search(query: str) -> str:
    """联网搜索

    文档问答只能回答「文档里写了什么」，涉及最新信息就得靠联网。

    规格：
      - 返回 str（要转述给模型看的文本结果，不是原始 JSON）；
      - 没配置搜索服务时要优雅降级 —— 返回一句「未配置联网搜索服务」的说明，
        而不是抛异常。原因：工具报错会打断整条 Agent 链路，
        而「这个工具暂时不可用」是完全正常的状态。

    实现路线（选一条）：
      A. 接搜索 API：Tavily / Bocha / SerpAPI，注册后拿 Key 调 HTTP 接口
      B. 自己写一个 MCP Server 把搜索能力暴露出去 —— 这条能让你把
         「MCP 解决 agent-to-tool 的什么问题」从概念讲到动手

    提示：Key 记得走 `settings`（放 .env），别硬编码。
    """
    # 没配置搜索服务时的优雅降级：返回说明而不是抛异常 ——
    # 工具报错会打断整条 Agent 链路，而「这个工具暂时不可用」是完全正常的状态。
    return (
        f"[未启用] 没有配置联网搜索服务，无法查询：{query}。"
        "如需联网：在 app/tools.py 的 web_search() 里接入 Tavily / Bocha 等搜索 API，"
        "或参考说明文档第 9 步，把它做成一个 MCP Server。"
    )


# ---------- 工具注册表 ----------
# 四个工具都定义完之后再建这张表（它要引用上面那几个函数），
# description 写清「什么时候用」—— 模型就是靠这句话决定要不要调你的工具。
TOOLS: dict[str, Tool] = {
    "search_documents": Tool(
        name="search_documents",
        description="当问题涉及本地已上传的技术文档内容时，用它检索相关片段。",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "检索用的查询语句"},
                "top_k": {"type": "integer", "description": "返回片段条数，默认 5"},
            },
            "required": ["query"],
        },
        func=search_documents,
    ),
    "calculator": Tool(
        name="calculator",
        description="做精确的四则运算、乘方、取模，避免模型算错数。",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "要计算的表达式，如 (12+34)*5",
                },
            },
            "required": ["expression"],
        },
        func=calculator,
    ),
    "current_time": Tool(
        name="current_time",
        description="获取当前日期时间，用于回答涉及时间的问题。",
        parameters={
            "type": "object",
            "properties": {
                "timezone": {"type": "string", "description": "时区，默认 Asia/Shanghai"},
            },
        },
        func=current_time,
    ),
    "web_search": Tool(
        name="web_search",
        description="当问题需要文档之外的最新信息时，用它在互联网上检索。",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "要在互联网上搜索的内容"},
            },
            "required": ["query"],
        },
        func=web_search,
    ),
}


def openai_tool_schemas() -> list[dict]:
    return [t.to_openai_schema() for t in TOOLS.values()]


@tracing.observe(name="tool.execute", as_type="tool")
async def execute(name: str, arguments: str | dict) -> str:
    # 入口打一条：模型让调哪个工具、参数是什么
    logger.info("tool_call name=%s args=%s", name, arguments)

    tool = TOOLS.get(name)
    if tool is None:
        return f"未知工具：{name}"
    args = json.loads(arguments) if isinstance(arguments, str) else arguments
    try:
        result = tool.func(**args)
        if hasattr(result, "__await__"):
            result = await result
        out = str(result)
        # 出口再打一条：和上面那条配对，就是一次完整的工具调用链
        logger.info("tool_result name=%s len=%d", name, len(out))
        return out
    except TypeError as exc:
        return f"参数不匹配：{exc}"  # 让模型看到错误后自己纠正
    except Exception as exc:
        return f"工具执行失败：{exc}"
