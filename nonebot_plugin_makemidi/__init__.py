from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import Command, CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot, MessageSegment

from .utils import create_midi, parse_arg, midi_path

__plugin_meta__ = PluginMetadata(
    name="在线编曲",
    description="在线编曲",
    usage="""
    usage：
    在线编曲
    仅支持简谱表达，升八度用+，降八度用-，长音用~，半音用_，附点.，可叠加，空格分隔
    例如八分音符为`1_`，十六分音符为`1__`，三十二分音符为`1___`
    二分音符为`1~`，全音符为`1~~~`，倍全音符为`1~~~~~~~`
    升半音用#，降半音用b，休止符用0，不可叠加，空格分隔，顺序不影响
    乐器代号参照midi乐器列表，不是所有乐器都可用，0为大钢琴
    支持多音轨，用 `>` 表示新的音轨，轨道范围为0-15，力度为0-1的小数
    BPM一般为120，调号一般为C，小调加m，例子：C C# C#m Cb Cm
    指令：
        编曲 [乐器代号] [BPM] [调号] [简谱]
        编曲 [BPM] [调号] > [轨道] [乐器] [力度] [简谱] > [轨道] [乐器] [力度] [简谱]
        编曲 0 120 C 3 5 6 1+ 2+~ 1+ 2+ 3+~ 1+ 6 5 3 1+ 2+ 6~
        """.strip(),
    extra={
        "unique_name": "make_midi",
        "author": "RandomEnch <randomench@foxmail.com>",
    },
)

make_music = on_command("编曲", priority=5, block=True)


@make_music.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    if not arg:
        await make_music.finish("未输入参数")
    qq = str(event.user_id)
    arg = arg.extract_plain_text()
    result = parse_arg(arg, qq)
    if result:
        await make_music.finish(result)
    else:
        await make_music.finish(MessageSegment.record(midi_path / f'{qq}.wav'))


