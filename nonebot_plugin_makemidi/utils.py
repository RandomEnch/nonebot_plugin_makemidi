from pathlib import Path
from typing import Union

from pydub import AudioSegment
from midi2audio import FluidSynth
from midiutil import MIDIFile

# 调号到半音偏移量的映射
key_offset_map = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6,
    'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

# 音符到 C 大调的 MIDI 音符基准映射
jianpu_to_midi = {
    '1': 0,  # C
    '2': 2,  # D
    '3': 4,  # E
    '4': 5,  # F
    '5': 7,  # G
    '6': 9,  # A
    '7': 11  # B
}

# 文件保存路径
resources_path = Path(__file__).resolve().parent / "resources"
midi_path = resources_path / 'midi'
if not midi_path.exists():
    midi_path.mkdir()


def jianpu_to_midi_note(jianpu: str, key: str) -> Union[int, None]:
    """
    将简谱音符转换为 MIDI 音符

    :param jianpu: 简谱音符列表
    :param key: 调号
    :return: MIDI 音符(0-127)
    """
    # 基础音符
    base_note = jianpu_to_midi.get(jianpu[0], None)
    if base_note is None:
        return None  # 非法音符

    # 获取调号的偏移量
    key_offset = key_offset_map.get(key.replace('m', ''), 0)

    # 如果是小调，需要调整音符（自然小调）
    if 'm' in key:
        natural_minor_shift = [0, 2, 3, 5, 7, 8, 10]  # 小调音阶的半音偏移
        base_note = natural_minor_shift[int(jianpu[0]) - 1]

    # 计算音符的 MIDI 值
    midi_note = 60 + base_note + key_offset  # 60 为中央 C (C4)

    # 处理升八度 `+` 和降八度 `-`
    octave_shift = jianpu.count('+') * 12 - jianpu.count('-') * 12
    midi_note += octave_shift

    # 处理升半音 `#` 和降半音 `b`
    if '#' in jianpu:
        midi_note += 1
    if 'b' in jianpu:
        midi_note -= 1

    return midi_note


def parse_jianpu(jianpu_str: str) -> list[list[dict[str, Union[str, int]]]]:
    """
    解析简谱字符串

    :param jianpu_str: 简谱字符串
    :return: [[{'note': '1', 'duration': 1}, {'note': '2', 'duration': 1},...], [...],...]
    """
    notes = []
    # 将简谱字符串按空格分割
    jianpu_parts = jianpu_str.split()
    for part in jianpu_parts:
        chords = part.split('|')  # 使用 "|" 分割和弦
        chord_notes = []

        for chord_part in chords:
            note_info = {
                'note': chord_part,  # 单个音符或和弦中的单个音
                'duration': 1  # 默认时值
            }
            # 处理时值符号
            note_info['duration'] *= max(2 * int((chord_part.count('~') + 1) / 2), 1)  # 点划线
            note_info['duration'] *= 1.5 ** chord_part.count('.')  # 附点符
            note_info['duration'] *= 0.5 ** chord_part.count('_')  # 半音符
            note_info['duration'] *= (1 / 3) ** chord_part.count('*')  # 三分符
            note_info['duration'] *= (2 / 3) ** chord_part.count('%')  # 三分之二符
            note_info['duration'] *= 0.75 ** chord_part.count('$')  # 四分之三符
            chord_notes.append(note_info)

        notes.append(chord_notes)  # 添加和弦信息，和弦是一组音符
    return notes


def create_midi(bpm: int, key: str, tracks: list[dict[str, Union[str, int]]], filename: str = 'output.mid') -> None:
    """
    创建 MIDI 文件

    :param bpm: BPM
    :param key: 调号
    :param tracks: 音轨列表
    :param filename: 文件名
    :return: None
    """
    midi = MIDIFile(len(tracks))

    for track_data in tracks:
        track_num = track_data['track']
        instrument = track_data['instrument']
        velocity = int(track_data['velocity'] * 127)
        jianpu = track_data['jianpu']

        time = 0
        midi.addTempo(track_num, time, bpm)
        midi.addProgramChange(track_num, track_num, time, instrument)

        notes = parse_jianpu(jianpu)

        for note_group in notes:
            max_duration = 0

            for note_info in note_group:
                note = note_info['note']
                duration = note_info['duration']
                max_duration = max(max_duration, duration)

                if note == '0':
                    continue  # 跳过休止符

                midi_note = jianpu_to_midi_note(note, key)
                if midi_note is None:
                    continue  # 跳过非法音符

                midi.addNote(track_num, track_num, midi_note, time, duration, velocity)

            time += max_duration  # 根据和弦的最大时值进行时间推进

    # 保存 MIDI 文件
    outfile = midi_path / filename
    with open(outfile, 'wb') as f:
        midi.writeFile(f)
    file_name = filename.split('.')[0]
    midi2wav(file_name)


def midi2wav(filename: str) -> None:
    """将 MIDI 文件转换为 WAV 文件"""
    sf_path = resources_path / 'gm.sf2'
    s = FluidSynth(sound_font=sf_path)
    midi_file = midi_path / f'{filename}.mid'
    audio_file = midi_path / f'{filename}.wav'
    s.midi_to_audio(midi_file, audio_file)
    high_volume(filename)


def high_volume(filename: str) -> None:
    """提高 WAV 文件的音量"""
    song = AudioSegment.from_wav(midi_path / f'{filename}.wav')
    song = song + 10
    song.export(midi_path / f'{filename}.wav', format="wav")


# 解析参数
def parse_arg(arg: str, qq: str) -> Union[None, str]:
    """
    解析参数

    :param arg: 参数字符串
    :param qq: QQ号
    :return: 结果字符串
    """
    result = ''
    # 单音轨
    if '>' not in arg:
        try:
            arg = arg.split(maxsplit=3)
            tracks = [
                {
                    'track': 0,  # 轨道 0
                    'instrument': int(arg[0]),  # 乐器
                    'velocity': 1,  # 力度
                    'jianpu': arg[3]
                },
            ]
            bpm = int(arg[1])  # BPM
            key_signature = arg[2]  # 调号
            create_midi(bpm, key_signature, tracks, f'{qq}.mid')
        except Exception as e:
            result = f"编曲失败，参数错误：{e}"
    # 多音轨
    else:
        try:
            arg = arg.replace('\n', '').split('>')
            bpm = int(arg[0].split()[0])
            key_signature = arg[0].split()[1]
            tracks = []
            for i in range(1, len(arg)):
                track = arg[i].split(maxsplit=3)
                tracks.append({
                    'track': int(track[0]),  # 轨道
                    'instrument': int(track[1]),  # 乐器
                    'velocity': float(track[2]),  # 力度
                    'jianpu': track[3]
                })
            create_midi(bpm, key_signature, tracks, f'{qq}.mid')
        except Exception as e:
            result = f"编曲失败，参数错误：{e}"

    return result
