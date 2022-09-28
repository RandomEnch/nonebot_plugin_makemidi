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
在安装完插件本体后，您还需要安装fluidsynth才能正常使用

克隆仓库后，将其中的fluidsynth文件夹放到合适位置并将其bin文件夹添加到path

- 使用 nb-cli

```
nb plugin install nonebot_plugin_makemidi
```

- 使用 pip

```
pip install nonebot_plugin_makemidi
```

- 安装fluidsynth

```
git clone https://github.com/RandomEnch/nonebot_plugin_makemidi.git
```

## 使用

仅支持简谱表达，升八度用+，降八度用-，延音用~，短音用_，可叠加，空格分隔，支持升降号

乐器代号参照midi乐器列表，不是所有乐器都可用，0为大钢琴

BPM一般为120，调号一般为C，小调加m，例子：`C C# C#m Cb Cm`

- 以下命令需要加命令前缀 (默认为/)，可自行设置，也可为空

```
编曲 [乐器代号] [BPM] [调号] [简谱]
编曲 0 120 C 3 5 6 1+ 2+~ 1+ 2+ 3+~ 1+ 6 5 3 1+ 2+ 6~  
```

[![sX2zp.png](https://s1.328888.xyz/2022/09/28/sX2zp.png)](https://imgloc.com/i/sX2zp)