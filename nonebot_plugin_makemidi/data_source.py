import os
from pathlib import Path
from midi2audio import FluidSynth
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from nonebot.adapters.onebot.v11 import MessageSegment

current_path = Path(__file__).resolve().parent / "resources"


def play_note(note, length, track, bpm=120, base_num=0, delay=0, velocity=1.0, channel=0, tone_change=0):
    meta_time = 60 * 60 * 10 / bpm
    major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
    base_note = 60
    if tone_change == 0:
        note = base_note + base_num * 12 + sum(major_notes[0:note])
    elif tone_change > 0:
        note = base_note + base_num * 12 + sum(major_notes[0:note]) + tone_change
    elif tone_change < 0:
        note = base_note + base_num * 12 + sum(major_notes[0:note]) + tone_change
    track.append(
        Message('note_on', note=note, velocity=round(64 * velocity),
                time=round(delay * meta_time), channel=channel))
    track.append(
        Message('note_off', note=note, velocity=round(64 * velocity),
                time=round(meta_time * length), channel=channel))


def make_midi(qq, notes, bpm=120, program=0, key_signature='C'):
    try:
        os.remove(current_path / f'{qq}.mid')
        os.remove(current_path / f'{qq}.wav')
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
        if '~' in note:
            length = 1 + 0.5 * int(str(note).count('~'))
            note = note.replace('~', '')
        elif '_' in note:
            length = 1 - 0.25 * int(str(note).count('_'))
            note = note.replace('_', '')
        else:
            length = 1
        if '#' in note:
            tone_change = int(str(note).count('#'))
            note = note.replace('#', '')
        elif 'b' in note:
            tone_change = -int(str(note).count('b'))
            note = note.replace('b', '')
        else:
            tone_change = 0
        if '+' in note:
            base_sum = int(str(note).count('+'))
            note = int(note.replace('+', ''))
        elif '-' in note:
            base_sum = -int(str(note).count('-'))
            note = int(note.replace('-', ''))
        else:
            note = int(note)
            base_sum = 0
        play_note(note, length, track, bpm, base_sum, tone_change=tone_change)

    mid.save(current_path / f'{qq}.mid')
    midi2wav(qq)
    return MessageSegment.record(current_path / f'{qq}.wav')


def midi2wav(qq):
    sf_path = current_path / 'gm.sf2'
    s = FluidSynth(sound_font=sf_path)
    s.midi_to_audio(current_path / f'{qq}.mid', current_path / f'{qq}.wav')
