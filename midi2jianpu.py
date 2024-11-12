import mido
import pretty_midi
import argparse

from math import isclose


def get_bpm(midi_file_path):
    # 使用 mido 读取 BPM 信息
    mid = mido.MidiFile(midi_file_path)
    bpm = None
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                bpm = mido.tempo2bpm(msg.tempo)
                break
        if bpm:
            break
    if not bpm:
        raise ValueError("BPM未找到")
    return int(bpm)


def get_key_signature(midi_file_path):
    # 使用 mido 读取 MIDI 文件
    mid = mido.MidiFile(midi_file_path)
    key_signature = None
    
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'key_signature':
                key_signature = msg.key
                break
        if key_signature:
            break
    
    if not key_signature:
        raise ValueError("Key Signature未找到")
    
    return key_signature


def get_time_signature(midi_file_path):
    # 使用 mido 读取 MIDI 文件
    mid = mido.MidiFile(midi_file_path)
    time_signature = None
    
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'time_signature':
                # 获取拍子的分子和分母
                numerator = msg.numerator
                denominator = msg.denominator
                time_signature = f"{numerator}/{denominator}"
                break
        if time_signature:
            break
    if not time_signature:
        raise ValueError("Time Signature未找到")
    return time_signature


def pitch_to_jianpu(pitch):
    base_pitch = 60  # 中央C对应的简谱"1"
    octave_shift = (pitch - base_pitch) // 12
    
    note_to_jianpu = {
        0: "1", 1: "1#", 2: "2", 3: "2#", 4: "3", 5: "4", 6: "4#", 
        7: "5", 8: "5#", 9: "6", 10: "6#", 11: "7"
    }
    
    note_index = (pitch - base_pitch) % 12
    jianpu_base = note_to_jianpu.get(note_index, "?")
    
    if octave_shift > 0:
        jianpu_base += "+" * octave_shift
    elif octave_shift < 0:
        jianpu_base += "-" * abs(octave_shift)
    
    return jianpu_base


def duration_to_jianpu(duration, bpm):
    base_duration = 60 / bpm  # 四分音符的基准时长
    target_ratio = duration / base_duration

    # 定义简谱中的时值和修饰符
    duration_map = {
        0.9375: "_...",       # 15/16拍
        0.875: "_..",         # 7/8拍
        0.75: "_.",           # 3/4拍
        0.5: "_",             # 八分音符
        0.4375: "__..",       # 7/16拍
        0.375: "__.",         # 3/8音符
        0.25: "__",           # 十六分音符
        0.21875: "___..",     # 7/32拍
        0.1875: "___.",       # 3/16音符
        0.125: "___",         # 三十二分音符
        0.109375: "____..",   # 7/64拍
        0.09375: "____.",     # 3/32音符
        0.0625: "____",       # 六十四分音符
        1: "",                # 四分音符
        1.5: ".",             # 附点音符
        1.75: "..",           # 双附点
        1.875: "...",         # 三附点
        2: "~",               # 二分音符
        2.5: "~.",            # 2.5拍
        2.75: "~..",          # 2.75拍
        3: "~~",              # 3拍
        3.5: "~~.",           # 3.5拍
        3.75: "~~..",         # 3.75拍
        3.875: "~~...",       # 3.875拍
        4: "~~~",             # 全音符
        4.5: "~~~.",          # 4.5拍
        4.75: "~~~..",        # 4.75拍
        4.875: "~~~...",      # 4.875拍
        5: "~~~~",            # 5拍
        5.5: "~~~~.",         # 5.5拍
        5.75: "~~~~..",       # 5.75拍
        5.875: "~~~~...",     # 5.875拍
        6: "~~~~~",           # 6拍
        6.5: "~~~~~.",        # 6.5拍
        6.75: "~~~~~..",      # 6.75拍
        6.875: "~~~~~...",    # 6.875拍
        7: "~~~~~~",          # 7拍
        7.5: "~~~~~~.",       # 7.5拍
        7.75: "~~~~~~..",     # 7.75拍
        7.875: "~~~~~~...",   # 7.875拍
        8: "~~~~~~~"          # 倍全音符
    }

    # 如果 `target_ratio` 接近 1，则不加修饰符
    if isclose(target_ratio, 1, abs_tol=0.01):
        return ""
    
    # 确定最佳匹配修饰符
    best_match = ""
    min_difference = float("inf")

    # 遍历常规音符时值修饰符，判断是延长还是缩短
    for ratio, symbol in duration_map.items():
        if target_ratio > 1:  # 延长音符
            # 仅选择倍率大于1的符号
            if ratio >= 1:
                difference = abs(target_ratio - ratio)
                if difference < min_difference:
                    min_difference = difference
                    best_match = symbol
        else:  # 缩短音符
            # 仅选择倍率小于1的符号
            if ratio <= 1:
                difference = abs(target_ratio - ratio)
                if difference < min_difference:
                    min_difference = difference
                    best_match = symbol

    # 返回最佳匹配的修饰符
    return best_match
    

def midi_to_jianpu(midi_file_path):
    bpm = get_bpm(midi_file_path)
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    all_tracks_jianpu = []

    for instrument in midi_data.instruments:
        if instrument.is_drum:
            continue

        # 计算音轨的平均力度
        if instrument.notes:
            avg_velocity = sum(note.velocity for note in instrument.notes) / len(instrument.notes) / 127
        else:
            avg_velocity = 0

        jianpu_notes = []
        # 将音符按开始时间分组，便于处理和弦
        notes_by_start = {}
        for note in instrument.notes:
            start_time = note.start
            if start_time not in notes_by_start:
                notes_by_start[start_time] = []
            notes_by_start[start_time].append(note)

        # 获取音符的开始时间列表并排序，方便后续时间计算
        start_times = sorted(notes_by_start.keys())

        for i, start_time in enumerate(start_times):
            notes = notes_by_start[start_time]
            chord_jianpu = []

            for note in notes:
                jianpu = pitch_to_jianpu(note.pitch)

                # 计算音符的持续时间
                if i < len(start_times) - 1:
                    # 如果有下一个音符，获取其开始时间
                    next_start_time = start_times[i + 1]
                    # 如果下一个音符在当前音符结束之前，则使用到下一个音符的时间作为持续时间
                    duration = next_start_time - note.start
                else:
                    # 如果没有下一个音符，使用音符的自身持续时间
                    duration = note.end - note.start

                # 转换为简谱时长修饰符
                duration_modifier = duration_to_jianpu(duration, bpm)
                chord_jianpu.append(jianpu + duration_modifier)

            # 将和弦音符用'|'连接
            jianpu_notes.append('|'.join(chord_jianpu))

        # 保存该音轨的信息到字典
        track_info = {
            "instrument": instrument.program if instrument.program else 0,
            "velocity": avg_velocity,
            "jianpu_notes": jianpu_notes
        }
        
        all_tracks_jianpu.append(track_info)

    return all_tracks_jianpu


def main(midi_file_path):
    bpm = get_bpm(midi_file_path)
    jianpu_notes = midi_to_jianpu(midi_file_path)
    
    if len(jianpu_notes) == 1:
        print(f"编曲 0 {int(bpm)} C {' '.join(jianpu_notes[0]['jianpu_notes'])}")
    else:
        result = f'编曲 {int(bpm)} C\n'
        for i, track in enumerate(jianpu_notes):
            result += f'> {i} {track["instrument"]} {float(track["velocity"]):.2f} {" ".join(track["jianpu_notes"])}\n'
        print(result)


if __name__ == '__main__':
    # 使用前先安装 pretty_midi 和 mido 库
    # python midi2jianpu.py test.mid
    parser = argparse.ArgumentParser(description='MIDI 转简谱')
    parser.add_argument('midi_file_path', type=str, help='Path to the MIDI file')
    args = parser.parse_args()
    
    main(args.midi_file_path)
        
