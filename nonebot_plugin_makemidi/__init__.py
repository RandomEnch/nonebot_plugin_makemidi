from nonebot import on_command
from nonebot.params import Command, CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot, MessageSegment

from .data_source import make_midi

__plugin_meta__ = PluginMetadata(
    name="在线编曲",
    description="在线编曲",
    usage="""
    usage：
    在线编曲
    仅支持简谱表达，升八度用+，降八度用-，延音用~，短音用_，可叠加，空格分隔，规范为：音符+八度+延音
    乐器代号参照midi乐器列表，不是所有乐器都可用，0为大钢琴
    BPM一般为120，调号一般为C，小调加m，例子：C C# C#m Cb Cm
    指令：
        #编曲 [乐器代号] [BPM] [调号] [简谱]
        #编曲 0 120 C 3 5 6 1+ 2+~ 1+ 2+ 3+~ 1+ 6 5 3 1+ 2+ 6~   
        """.strip(),
    extra={
        "unique_name": "make_music",
        "author": "RandomEnch <randomench@foxmail.com>",
    },
)

make_music = on_command("#编曲", priority=5, block=True)


@make_music.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    if not arg:
        await make_music.finish("未输入参数")
    qq = str(event.user_id)
    arg = arg.extract_plain_text().split()
    program = int(arg[0])
    bpm = int(arg[1])
    key_signature = arg[2]
    notes = arg[3:]
    try:
        result = make_midi(qq, notes, program=program, bpm=bpm, key_signature=key_signature)
    except Exception as e:
        result = f"编曲失败，参数错误：{e}"
    await make_music.finish(result)
