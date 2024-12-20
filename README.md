<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">
  
# Nonebot_Plugin_Makemidi
  
_✨ 基于OneBot适配器的[NoneBot2](https://v2.nonebot.dev/)在线编曲插件 ✨_
  
</div>

## 功能

- 通过发送简谱实现简单的在线编曲

## 安装

+ 注意：
  > 在安装完插件本体后，您还需要安装ffmpeg和fluidsynth才能正常使用
  >
  > 为使适配器能发送音频，你需要安装ffmpeg，详见 [go-cqhttp文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)

+ 方式一 使用 pip
  > 1.pip 安装库
  > ```
  > pip install nonebot_plugin_makemidi
  > ```
  > 2.安装ffmpeg和fluidsynth

+ 方式二 手动安装
  > 1.克隆本仓库
  > ```
  > git clone https://github.com/RandomEnch/nonebot_plugin_makemidi.git
  > ```
  > 2.安装依赖 requirements.txt
  > ```
  > cd nonebot_plugin_makemidi
  > pip install -r requirements.txt
  > ```
  > 3.安装ffmpeg和fluidsynth
  > 
  > 4.复制插件本体到 Nonebot 插件文件夹中

+ 安装fluidsynth
  > 1.Windows安装
  > 
  > 按照[go-cqhttp文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)安装ffmpeg
  > 
  > 下载fluidsynth后解压到合适位置，将其bin文件夹的路径添加到环境变量path中
  > 
  > 这里提供我使用的版本的[下载地址](https://pan.baidu.com/s/1fHljXONT_uGQnW28Ity9Rg?psw=1145)
  > 
  > 你也可以直接去[fluidsynth项目页](https://github.com/FluidSynth/fluidsynth)下载
  > 
  > 2.Linux安装
  > 
  > 此处以Ubuntu/Debian为例，其他发行版请自行搜索安装方法
  > ```
  > sudo apt update
  > sudo apt install -y ffmpeg fluidsynth
  > ```


## 使用

仅支持简谱表达，升八度用`+`，降八度用`-`，长音用`~`，半音用`_`，附点`.`，可叠加，空格分隔，顺序不影响

升半音用`#`，降半音用`b`，休止符用`0`，不可叠加，空格分隔

乐器代号参照 [MIDI乐器编号](https://blog.csdn.net/snail8384/article/details/8102730)，可用乐器具体取决于你的SF2文件，一般0为大钢琴

支持多音轨，用 `>` 表示新的音轨，轨道范围为0-15，力度范围为0-1的小数

支持和弦，用 `|` 表示和弦，`2+#~|4+#`表示同时按下2+#和4+#，但2+#的持续时间更长

BPM一般为120，调号一般为C，小调加m，例子：`C C# C#m Cb Cm`

提供了一个将MIDI文件转为编曲指令的脚本，可以将MIDI文件转换为简谱指令，详见[midi2jianpu.py](https://github.com/RandomEnch/nonebot_plugin_makemidi/blob/master/midi2jianpu.py)(使用前先安装 pretty_midi 和 mido 库)

> 注意：
> 
> - 因为未编写音符间隔的判断，上一个音符的末尾和下一个音符的开头是连续的，可能会导致音长听起来过短，可以通过延长上一个音符的时间来解决
> 
> - 和弦只用于两个音符同时发声的情况（长短可以不一样），不支持一个音符发声到中途时另一个音符发声的情况，可以通过减短当前音符的持续时间来实现

## 指令

- 以下命令需要加命令前缀 (默认为`/`)，可自行设置，也可为空

```
编曲 [乐器] [BPM] [调号] [简谱]

编曲 [BPM] [调号] > [轨道] [乐器] [力度] [简谱] > [轨道] [乐器] [力度] [简谱]
```

## 音长修饰符

| 拍值   | 符号     | 说明     |
|--------|--------|--------|
| 0.9375 | `_...` | 15/16拍 |
| 0.875  | `_..`  | 7/8拍   |
| 0.75   | `_.`   | 3/4拍   |
| 0.5    | `_`    | 八分音符   |
| 0.4375 | `__..` | 7/16拍  |
| 0.375  | `__.`  | 3/8拍   |
| 0.25   | `__`   | 十六分音符  |
| 0.21875| `___..` | 7/32拍  |
| 0.1875 | `___.` | 3/16拍 |
| 0.125  | `___`  | 三十二分音符 |
| 0.109375| `____..` | 7/64拍  |
| 0.09375 | `____.` | 3/32拍 |
| 0.0625 | `____` | 六十四分音符 |
| 1      |        | 四分音符   |
| 1.5    | `.`    | 附点音符   |
| 1.75   | `..`   | 双附点    |
| 1.875  | `...`  | 三附点    |
| 2      | `~`    | 二分音符   |
| 2.5    | `~.`   | 2.5拍   |
| 2.75   | `~..`  | 2.75拍  |
| 3      | `~~`   | 3拍     |
| 3.5    | `~~.`  | 3.5拍   |
| 3.75   | `~~..` | 3.75拍  |
| 3.875  | `~~...` | 3.875拍 |
| 4      | `~~~`  | 全音符    |
| 4.5    | `~~~.` | 4.5拍   |
| 4.75   | `~~~..` | 4.75拍  |
| 4.875  | `~~~...` | 4.875拍 |
| 5      | `~~~~` | 5拍     |
| 5.5    | `~~~~.` | 5.5拍   |
| 5.75   | `~~~~..` | 5.75拍  |
| 5.875  | `~~~~...` | 5.875拍 |
| 6      | `~~~~~` | 6拍     |
| 6.5    | `~~~~~.` | 6.5拍   |
| 6.75   | `~~~~~..` | 6.75拍  |
| 6.875  | `~~~~~...`| 6.875拍 |
| 7      | `~~~~~~` | 7拍     |
| 7.5    | `~~~~~~.` | 7.5拍   |
| 7.75   | `~~~~~~..`| 7.75拍  |
| 7.875  | `~~~~~~...` | 7.875拍 |
| 8      | `~~~~~~~` | 倍全音符   |

## 示例
### 单轨

My Soul, your Beats!
```
编曲 0 145 C 3+_ 2+ 1+ 6 5~~~ 3+_ 2+ 1+ 6 5~~~ 3+_ 2+ 1+ 2+ 5+ 6+~~ 3+_ 2+ 1+ 5 6~~~
```
砕月
```
编曲 0 240 C 3 5 6 1+ 2+~ 1+ 2+ 3+~ 1+ 6 5 3 1+ 2+ 6~ 6 1+ 2+~ 1+ 2+ 3+~ 5+ 6+ 1++ 7+ 6+__ 7+__ 6+__ 5+ 6+~ 5+ 3+ 2+~ 3+ 1+ 2+~ 1+ 2+ 3+. 6_ 1+_ 2+_ 1+ 6~ 6 5 6 5_ 6_ 1+ 2+ 3+ 2+ 5~ 6~~~ 3 5 6 2+ 5+ 6+ 3+ 2+ 3+~ 1+ 2+ 7 1+ 7__ 1+__ 7* 5 6~ 3 5 6 1+ 2+ 1+ 2+. 1+_ 2+_ 3+_ 1+ 2+. 1+_ 2+ 5+ 3+~ 3+ 5+ 6+~ 5+ 6+ 3+.~ 1+ 2+ 3+ 2+_ 3+_ 1+ 6~ 6 5 6 5_ 6_ 1+ 2+ 3+ 2+ 5+~ 6+~~~
```
Lemon
```
编曲 0 86 C 1#+__. 2#+___. 1#+__ 7__ 5#__ 7_. 2#+__ 4#+_. 1#+__ 7_. 1#+__. 2#+___. 1#+__ 7__ 5#__ 7_. 2#+__ 4#+_. 1#+__ 7_. 1#+__. 2#+___. 1#+__ 7__ 5#__ 7_. 2#+__ 4#+_. 5#+__ 4#+_. 4#+__ 7+_. 6#+__ 4#+_. 2#+__ 4#+_. 1#+ 1#+__. 2#+___. 1#+__ 7__ 5#__ 7_. 2#+__ 4#+_. 1#+__ 7_. 7__. 7___. 1#+__ 2#+__ 3+__ 2#+_. 1#+__ 6#_. 7. 7__ 6#__ 5#_ 6#_ 7_ 1#+_ 7__ 4#_. 2#__ 4#_. 5#__ 1#+_. 6#__ 7_. 7. 7__ 6#__ 5#_ 6#_ 7_ 1#+_ 7__ 4#_. 7__ 1#+_. 2#+__ 3+_. 1#+__ 7_. 7~
```

### 多轨

Unwelcome School
```
编曲 180 C 
> 0 0 1 6- 1 2#._ 3 5-#_ 6-_ 1_ 2_ 1_ 2#_ 2#__ 3 5_ 4#_ 4_ 3_ 2_ 1_ 7-_ 6#-_ 7-_ 1_ 2_ 2#_ 3 3- 6- 1 2#._ 3 5-#_ 6-_ 1_ 2_ 1_ 2#_ 2#__ 3 5_ 4#_ 4_ 3_ 2#_ 3_ 4#_ 5_ 5#_ 5#_ 6_ 6_ 7
> 1 0 0.7 3- 3- 3- 3- 3- 3- 3- 3- 1- 1- 1- 1- 7-- 7-- 7-- 7-- 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 3-_ 4-_ 1-_ 1-_ 4-_ 1-_ 1-_ 1-_ 4-_ 1-_ 7--_ 7-_ 7--_ 7--_ 7--_
```
Unknown · Mother Goose
```
编曲 110 C
> 0 0 0.63 1#+_.|3_.|1#_. 3+_.|3_. 4#+|6|4# 4#+_|6_|4#_ 3+_|5#_|3_ 1#+_|1#_ 7_.|3_.|7-_. 1#+_.|3_.|1#_. 7_|3_|7-_ 1#+_|3_|1#_ 7__|7-__ 1#+__|1#__ 4#|4#- 1#+_.|3_.|1#_. 3+_.|3_. 4#+|6|4# 4#+_|6_|4#_ 3+_|5#_|3_ 1#+_|1#_ 6+_.|1#+_.|6_. 5#+_.|5#_. 3+_|3_ 4#+_|6_|4#_ 3+_|3_ 1#+|1# 1#+_.|3_.|1#_. 3+_.|3_. 4#+|6|4# 4#+_|6_|4#_ 3+_|5#_|3_ 1#+_|1#_ 7_.|3_.|7-_. 1#+_.|3_.|1#_. 7_|3_|7-_ 1#+_|3_|1#_ 7__|7-__ 1#+__|1#__ 4#|4#- 1#+_.|3_.|1#_. 3+_.|3_. 4#+|6|4# 4#+_|6_|4#_ 3+_|5#_|3_ 1#+_|1#_ 6+_.|1#+_.|6_. 5#+_.|5#_. 3+_|3_ 4#+_|6_|4#_ 3+_|3_ 1#+_...|1#_...
> 1 0 0.63 6--_.|2-_.|2--_. 2--__ 6--_ 2- 2--_ 7--|3-|3-- 3--_. 7--_. 3-_ 1#-_.|4#-_.|4#--_. 4#-_. 1#-_ 6--_.|2-_.|2--_. 2--__ 6--_ 2- 2--_ 7--|3-|3-- 3--_. 7--_. 3-_ 1#-_.|4#-_.|4#--_. 4#-_. 1#-_ 6--_.|2-_.|2--_. 2--__ 6--_ 2- 2--_ 7--|3-|3-- 3--_. 7--_. 3-_ 1#-_.|4#-_.|4#--_. 4#-_. 1#-_ 6--_.|2-_.|2--_. 2--__ 6--_ 2- 2--_ 7--|3-|3-- 3--_. 7--_. 3-_ 1#-_.|4#-_.|4#--_. 4#-_.
```

### 和弦

大吉猫咪
```
编曲 0 170 C 7_ 2+_ 7_ 3+_.. 2#+___ 3+ 7_ 6_ 5_ 4#_ 3 2+ 3+ 2#+___ 2+___ 1#+_ 3+_. 6+___ 6#+___ 7+ 6+_ 5+_ 4#+_ 2#+_ 7_. 1#+___ 2+___. 2#+ 3+ 2#+___ 2+___ 1#+_ 3+_. 2+___ 2#+___ 3+ 7_ 6_ 5_ 4#_ 3_ 7___ 1+___ 1#+___. 2+ 3+ 4#+ 5+_ 6+_ 7+___ 6+__. 5+_ 3+_ 2+_ 7_ 2+_ 3+~. 3+_ 4#+_ 5+_ 3+|7+ 3+|7+ 6+_ 7+_ 2++_ 6+_ 5+ 5+_ 4#+. 3+_ 2#+____.. 2+____. 1#+____.. 1+____.. 7_ 3+_ 4#+_ 5+_ 6+_ 7+_ 6+_ 4#+_ 3+|5+ 2#+|4#+ 3+|5+ 4#+|6+ 3+|7+ 3+|7+ 6+_ 7+_ 2++_ 6+_ 5+ 4#+_ 5+ 4#+_ 4+____.. 3+____. 2#+____.. 2#+_ 3+_ 7_ 6+_ 4#+_ 7+_ 5+_ 6+_ 3+_ 5+_|7+_ 4#+_|6+_ 2#+_|4#+_ 5+_|7+_ 5+|3+ 4#+____..|2#+____.. 3+____.|2+____. 2#+____..|1#+____.. 2+_|1+_ 3+|7+ 3+|7+ 6+_ 7+_ 2++_ 6+_ 5+ 5+_ 4#+. 3+_ 2#+____.. 2+____. 1#+____.. 1+____.. 7_ 3+_ 4#+_ 5+_ 6+_ 7+_ 6+_ 4#+_ 3+|5+ 2#+|4#+ 3+|5+ 4#+|6+ 3+|7+ 3+|7+ 6+_ 7+_ 2++_ 6+_ 5+ 4#+_ 5+ 4#+_ 4+____.. 3+____. 2#+____.. 2#+_ 3+_ 7_ 6+_ 4#+_ 7+_ 5+_ 6+_ 3+__ 4#+__ 7|7+ 2#+|2#++ 3+~~~|3++~~~
```
PANDORA PARADOXXX
```
编曲 0 150 C 6#+_|2#_|6#_|6#-_ 6#+_|2#_|6#_|6#-_ 5#_|5#+_|1#_|5#-_ 5#_|5#+_|1#_|5#-_ 6#+_|2#_|6#_|6#-_ 6#_|6#+_|2#_|6#-_ 5#+_|1#_|5#_|5#-_ 5#_|5#+_|1#_|5#-_ 6#+_|2#_|6#_|6#-_ 6#+_|2#_|6#_|6#-_ 6#-_|2#_|2#+_|2#-_ 2#+_|2#_|6#-_|2#-_ 4#+_|4#_|1#_|4#-_ 4#+_|4#_|1#_|4#-_ 1#_|4+_|4_|4-_ 4+_|4_|1#_|4-_ 2#_|6#+_|6#_|6#-_ 2#_|6#+_|6#_|6#-_ 1#_|5#+_|5#_|5#-_ 1#_|5#+_|5#_|5#-_ 6#_|2#_|6#+_|6#-_ 6#_|2#_|6#+_|6#-_ 5#_|1#_|5#+_|5#-_ 5#_|1#_|5#+_|5#-_ 2#_|6#+_|6#_|6#-_ 2#_|6#+_|6#_|6#-_ 4#+_|4#++_|4#_|6#_ 4#++_|4#_|4#+_|6#_ 4_|4+_|4++_|5#_ 4_|4+_|4++_|5#_ 1#_|1#+_|1#++_|4_ 1#_|1#+_|1#++_|4_ 2#_.|2#+_.|6#_.|2#++_. 1#_.|1#+_.|5#_.|1#++_. 2#_.|2#+_.|6#_.|2#++_. 1#_.|1#+_.|5#_.|1#++_. 2#_.|2#+_.|2#++_.|6#_. 1#_.|1#+_.|5#_.|1#++_. 2#_.|2#+_.|2#++_.|6#_. 1#_.|1#+_.|1#++_.|5#_. 2#_.|2#+_.|2#++_.|6#_. 4#++_.|4#+_.|4#_.|1#+_. 4++_.|4+_.|4_.|1+_. 5#_.|1#_.|1#+_.|1#++_. 6#++__.|4+__.|6#__.|6#+__. 5#+__.|5#++__.|2#+__.|5#__. 6#+__.|6#++__.|4+__.|6#__. 5#+__.|5#__.|2#+__.|5#++__. 4#+__.|4#++__.|1#+__.|4#__. 5#+__.|5#__.|2#+__.|5#++__. 4#+__.|4#__.|1#+__.|4#++__. 1#+__.|1#__.|1#++__.|6#__. 4#+__.|4#__.|4#++__.|1#+__. 1#+__.|6#__.|1#__.|1#++__. 6#__.|4#__.|6#+__.|6#-__. 5#__.|4__.|5#+__.|5#-__.
```
雑踏、僕らの街
```
编曲 0 120 C 3__. 5__. 6__. 7_ 6__. 5___. 5_ 2__. 3___.. 2__. 7-__. 3_ 7_ 7_. 3__. 5__. 6__. 3+_|7_ 7+____ 6__. 6___. 6+____ 5__. 5___. 3__.|7+__. 3___. 2__.|4#+__. 2+__.|7-__. 3+_|3_ 2+_|7+_ 5+_.|7_. 6__.|3+__. 7__.|5+__. 2+__.|6+__. 7+____ 3+_ 7+__.|3+__. 2+___.|6+___. 7+____ 3+__. 6+____ 2+___. 7+____ 3+__. 2+___.|6+___. 7+____ 3+_. 7+____ 3+__. 6+____ 2+___. 3+__.|7+__. 6+___.|2+___. 7+__.|3+__. 3+__.|7+__. 6+__. 5+__.|7__. 2++__. 2+_.|6+_.|5+_. 6+____ 2+__. 7-____|7+____ 3+__. 5___. 4#___. 3___. 7-_.. 3__. 3___. 3__. 2___. 3_ 2___. 3___. 2___. 3__. 7_. 6__. 6__. 5__. 7_. 3_. 5+___. 4#+___. 2+___. 7___. 6___. 2+___. 6___. 7__ 5+___. 4#+___. 2+___. 7___. 6___ 2+___. 6___ 7___. 3+___. 2+___. 3+___. 4#+___. 5+___. 6+___. 4#+___. 5+___. 7+___. 5+___. 6+___. 2++___. 1++___. 7+___. 6+___. 5+___. 3++___. 2++___. 3++___. 4#++___. 5++___. 4#++___. 5++___. 6++___. 7++___. 6++___. 7++___. 2+++___. 2#+++___. 7++___. 6++___. 5++___. 3++___. 6++___. 7++___. 3++___. 6++___. 7++___. 3++___. 2+++___. 3+++___. 7++___. 2+++___. 3+++___. 3++___. 6++___ 7++.
```
