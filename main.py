import aiohttp
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("cwg", "jinshiqwq", "查询2b2t.biz群违规记录", "1.0.0", "")
class CwgPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("cwg")
    async def cwg_command(self, event: AstrMessageEvent):
        """查询2b2t.biz群违规记录"""
        args = event.message_str.split()
        if len(args) != 2:          # 第一个是指令本身，第二个是 QQ 号
            yield event.plain_result("用法：cwg <QQ号>")
            return

        qq = args[1].strip()
        url = f"http://wg.2b2t.biz/cx.php?qq={qq}"

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        yield event.plain_result(f"请求失败，HTTP 状态码：{resp.status}")
                        return
                    text = await resp.text(encoding="utf-8")
                    yield event.plain_result(text.strip())
        except Exception as e:
            logger.exception("cwg 查询异常")
            yield event.plain_result(f"查询出错：{e}")

    async def terminate(self):
        """插件卸载时调用（可选）"""
        pass
