from core.plugin import BasePlugin, logger, register_tool
from core.chat.message_utils import KiraMessageBatchEvent

class LogicHelperPlugin(BasePlugin):
    def __init__(self, ctx, cfg: dict):
        super().__init__(ctx, cfg)

    async def initialize(self):
        logger.info("LogicHelperPlugin initialized")

    async def terminate(self):
        logger.info("LogicHelperPlugin terminated")

    @register_tool(
        name="compare_numbers",
        description="比较两个数字的大小，支持整数和浮点数（例如 '3.10' 会被正确解析为 3.1）。返回较大的那个数字并说明比较结果。",
        params={
            "type": "object",
            "properties": {
                "a": {"type": "string", "description": "第一个数字，如 '3.10'"},
                "b": {"type": "string", "description": "第二个数字，如 '3.9'"}
            },
            "required": ["a", "b"]
        }
    )
    async def compare_numbers(self, event: KiraMessageBatchEvent, a: str, b: str) -> str:
        try:
            fa = float(a)
            fb = float(b)
            if fa > fb:
                return f"{a} 大于 {b}，因为数值比较 {fa} > {fb}"
            elif fa < fb:
                return f"{a} 小于 {b}，因为数值比较 {fa} < {fb}"
            else:
                return f"{a} 等于 {b}"
        except ValueError:
            return f"无法将 '{a}' 或 '{b}' 转换为数字，请确保输入的是有效的数字字符串。"

    @register_tool(
        name="count_digits",
        description="统计一个数字字符串中指定数字的出现次数。",
        params={
            "type": "object",
            "properties": {
                "number_str": {"type": "string", "description": "数字字符串，如 '3369305352'"},
                "digits": {
                    "type": "array",
                    "items": {"type": "string", "pattern": "^[0-9]$"},
                    "description": "要统计的数字列表，如 ['3', '5']"
                }
            },
            "required": ["number_str", "digits"]
        }
    )
    async def count_digits(self, event: KiraMessageBatchEvent, number_str: str, digits: list) -> str:
        counts = {}
        for d in digits:
            counts[d] = number_str.count(d)
        result = ", ".join([f"{d} 出现了 {counts[d]} 次" for d in digits])
        return f"在数字串 {number_str} 中，{result}。"