import os
from pathlib import Path
from pydub import AudioSegment
from midi2audio import FluidSynth
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from nonebot.adapters.onebot.v11 import MessageSegment

current_path = Path(__file__).resolve().parent / "resources"
midi_path = current_path / 'midi'


# 调号转换
def signature(key_signature, note, tone_change=0):
    if note == 0:
        return note, tone_change
    src_note = note
    if key_signature == 'C' or key_signature == 'Am':
        pass
    elif key_signature == 'G' or key_signature == 'Em':
        tones = [5, 6, 7, 1, 2, 3, 4]
        note = tones[note - 1]
        if note == 4:
            tone_change += 1
    elif key_signature == 'F' or key_signature == 'Dm':
        tones = [4, 5, 6, 7, 1, 2, 3]
        note = tones[note - 1]
        if note == 7:
            tone_change -= 1
    elif key_signature == 'D' or key_signature == 'Bm':
        tones = [2, 3, 4, 5, 6, 7, 1]
        note = tones[note - 1]
        if note == 1 or note == 4:
            tone_change += 1
    elif key_signature == 'Bb' or key_signature == 'Gm':
        tones = [7, 1, 2, 3, 4, 5, 6]
        note = tones[note - 1]
        if note == 7 or note == 3:
            tone_change -= 1
    elif key_signature == 'A' or key_signature == 'F#m':
        tones = [6, 7, 1, 2, 3, 4, 5]
        note = tones[note - 1]
        if note == 1 or note == 4 or note == 5:
            tone_change += 1
    elif key_signature == 'Eb' or key_signature == 'Cm':
        tones = [3, 4, 5, 6, 7, 1, 2]
        note = tones[note - 1]
        if note == 7 or note == 3 or note == 6:
            tone_change -= 1
    elif key_signature == 'E' or key_signature == 'C#m':
        tones = [3, 4, 5, 6, 7, 1, 2]
        note = tones[note - 1]
        if note == 1 or note == 4 or note == 5 or note == 2:
            tone_change += 1
    elif key_signature == 'Ab' or key_signature == 'Fm':
        tones = [6, 7, 1, 2, 3, 4, 5]
        note = tones[note - 1]
        if note == 7 or note == 3 or note == 6 or note == 2:
            tone_change -= 1
    elif key_signature == 'B' or key_signature == 'G#m' or key_signature == 'Cb':
        tones = [7, 1, 2, 3, 4, 5, 6]
        note = tones[note - 1]
        if note == 1 or note == 4 or note == 5 or note == 2 or note == 6:
            tone_change += 1
    elif key_signature == 'C#' or key_signature == 'Db' or key_signature == 'A#m' or key_signature == 'Bbm':
        tones = [1, 2, 3, 4, 5, 6, 7]
        note = tones[note - 1]
        tone_change += 1
    elif key_signature == 'F#' or key_signature == 'D#m' or key_signature == 'Gb':
        tones = [4, 5, 6, 7, 1, 2, 3]
        note = tones[note - 1]
        if note != 7:
            tone_change += 1
    else:
        pass
    if note < src_note:
        tone_change += 12
    return note, tone_change


def parser_notes(note, key_signature):
    # 延音
    if '~' in note:
        length = 1 + int(str(note).count('~'))
        note = note.replace('~', '')
    # 半音
    elif '_' in note:
        length = 1 * 0.5 ** int(str(note).count('_'))
        note = note.replace('_', '')
    # 附点
    elif '.' in note:
        length = 1 + 0.5 * int(str(note).count('.'))
        note = note.replace('.', '')
    else:
        length = 1
    # 升半调
    if '#' in note:
        tone_change = 1
        note = note.replace('#', '')
    # 降半调
    elif 'b' in note:
        tone_change = -1
        note = note.replace('b', '')
    else:
        tone_change = 0
    # 升八度
    if '+' in note:
        base_sum = int(str(note).count('+'))
        note = int(note.replace('+', ''))
    # 降八度
    elif '-' in note:
        base_sum = -int(str(note).count('-'))
        note = int(note.replace('-', ''))
    else:
        note = int(note)
        base_sum = 0
    # 小调
    if 'm' in key_signature:
        if note == 3 or note == 6 or note == 7:
            tone_change -= 1

    return note, length, tone_change, base_sum


def play_note(note, length, track, bpm=120, base_num=0, delay=0, velocity=1.0, channel=0, tone_change=0):
    meta_time = 60 * 60 * 10 / bpm
    major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
    base_note = 60
    if note != 0 and 1 <= note <= 7:
        if tone_change == 0:
            note = base_note + base_num * 12 + sum(major_notes[0:note])
        elif tone_change != 0:
            note = base_note + base_num * 12 + sum(major_notes[0:note]) + tone_change
        track.append(
            Message('note_on', note=note, velocity=round(64 * velocity),
                    time=round(delay * meta_time), channel=channel))
        track.append(
            Message('note_off', note=note, velocity=round(64 * velocity),
                    time=round(meta_time * length), channel=channel))
    # 休止符
    elif note == 0:
        track.append(
            Message('note_on', note=note, velocity=round(64 * velocity),
                    time=round(delay * meta_time), channel=channel))
        track.append(
            Message('note_off', note=note, velocity=round(64 * velocity),
                    time=round(meta_time * length), channel=channel))


def make_midi(qq, notes, bpm=120, program=0, key_signature='C'):
    if os.path.exists(midi_path):
        pass
    else:
        os.mkdir(midi_path)
    try:
        os.remove(midi_path / f'{qq}.mid')
        os.remove(midi_path / f'{qq}.wav')
    except:
        pass
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    tempo = bpm2tempo(bpm)
    track.append(Message('program_change', channel=0, program=program, time=0))
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    track.append(MetaMessage('key_signature', key=key_signature))
    for note in notes:
        note, length, tone_change, base_sum = parser_notes(note, key_signature)
        note, tone_change = signature(key_signature, note, tone_change)
        play_note(note, length, track, bpm, base_sum, tone_change=tone_change)

    mid.save(midi_path / f'{qq}.mid')
    midi2wav(qq)
    high_volume(qq)
    return MessageSegment.record(midi_path / f'{qq}.wav')


def multi_tracks(qq, tracks, bpm=120, key_signature='C'):
    if os.path.exists(midi_path):
        pass
    else:
        os.mkdir(midi_path)
    try:
        os.remove(midi_path / f'{qq}.mid')
        os.remove(midi_path / f'{qq}.wav')
    except:
        pass
    mid = MidiFile(type=1)
    tempo = bpm2tempo(bpm)
    for simple in tracks:
        if simple[0] == ' ':
            simple = simple[1:]
        channel = int(simple.split()[0])
        program = int(simple.split()[1])
        velocity = float(simple.split()[2])
        notes = simple.split()[3:]
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        track.append(MetaMessage('key_signature', key=key_signature))
        track.append(Message('program_change', channel=channel, program=program, time=0))
        for note in notes:
            note, length, tone_change, base_sum = parser_notes(note, key_signature)
            note, tone_change = signature(key_signature, note, tone_change)
            play_note(note, length, track, bpm, base_sum, tone_change=tone_change, channel=channel, velocity=velocity)

    mid.save(midi_path / f'{qq}.mid')
    midi2wav(qq)
    high_volume(qq)
    return MessageSegment.record(midi_path / f'{qq}.wav')


# MIDI转WAV
def midi2wav(qq):
    sf_path = current_path / 'gm.sf2'
    s = FluidSynth(sound_font=sf_path)
    s.midi_to_audio(midi_path / f'{qq}.mid', midi_path / f'{qq}.wav')


# 增加音量
def high_volume(qq):
    song = AudioSegment.from_wav(midi_path / f'{qq}.wav')
    song = song + 20
    song.export(midi_path / f'{qq}.wav', format="wav")
