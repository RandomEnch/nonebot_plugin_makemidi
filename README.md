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
  > 在安装完插件本体后，您还需要安装fluidsynth才能正常使用
  >
  > 下载fluidsynth后解压到合适位置，将其bin文件夹的路径添加到环境变量path中
  >
  > 为使适配器能发送音频，你还需要安装ffmpeg，方法与fluidsynth相同
  >
  > 详见 [go-cqhttp文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)


+ 方式一 使用 pip
  > 1.pip 安装库
  > ```
  > pip install nonebot_plugin_makemidi
  > ```
  > 2.安装fluidsynth
  > ```
  > https://pan.baidu.com/s/1fHljXONT_uGQnW28Ity9Rg?psw=1145
  > 提取密码：1145
  > ```

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
  > 3.安装fluidsynth
  > ```
  > https://pan.baidu.com/s/1fHljXONT_uGQnW28Ity9Rg?psw=1145
  > 提取密码：1145
  > ```
  > 4.复制插件本体到 Nonebot 插件文件夹中


## 使用

仅支持简谱表达，升八度用`+`，降八度用`-`，延音用`~`，短音用`_`，附点`.`，可叠加，空格分隔

升半音用`#`，降半音用`b`，休止符用`0`，不可叠加，空格分隔，顺序不影响

乐器代号参照midi乐器列表，不是所有乐器都可用，0为大钢琴

支持多音轨，用 `>` 表示新的音轨，轨道范围为0-15

BPM一般为120，调号一般为C，小调加m，例子：`C C# C#m Cb Cm`

- 以下命令需要加命令前缀 (默认为`/`)，可自行设置，也可为空

```
编曲 [乐器] [BPM] [调号] [简谱]

编曲 [BPM] [调号] > [乐器] [简谱] > [乐器] [简谱]
```
- 例子
```
编曲 0 120 C 3 5 6 1+ 2+~ 1+ 2+ 3+~ 1+ 6 5 3 1+ 2+ 6~  
编曲 0 170 C 6~ 1+~ 2+# 3+ 0 5# 6 1+ 2+ 1+ 2+_ 2+ 3+ 0 5+ 4+# 4+ 2+# 2+ 1+ 7 6 7 1+ 2+ 2+#~ 3~ 6~ 1+~ 2+# 3+ 0 5# 6 1+ 2+ 1+ 2+_ 2+ 3+ 0 5+ 4+# 4+ 2+# 3+ 4+ 4+# 5+ 5+# 5+# 6+ 6+ 7+~~
```
- 多轨
```
编曲 170 C 
> 0 0 6~ 1+~ 2+# 3+~ 0 5# 6 1+ 2+ 1+ 2+_ 2+ 3+~ 0 5+ 4+# 4+ 2+# 2+ 1+ 7 6 7 1+ 2+ 2+#~ 3~ 6~ 1+~ 2+# 3+~ 0 5# 6 1+ 2+ 1+ 2+_ 2+ 3+~ 0 5+ 4+# 4+ 2+# 3+ 4+ 4+# 5+ 5+# 5+# 6+ 6+ 7+~~
> 1 0 6 6- 6 6- 6 6- 6 6- 1+ 1 1+ 1 1+ 1 1+ 1 4 4- 4 4- 4 4- 4 4- 3 3- 3 3- 3 3- 3 3- 6 6- 6 6- 6 6- 6 6- 1+ 1 1+ 1 1+ 1 1+ 1 4 4- 4 4- 4 4- 4 4- 3 3- 3 3- 3 3- 3 3-
```

[![sX2zp.png](https://s1.328888.xyz/2022/09/28/sX2zp.png)](https://imgloc.com/i/sX2zp)