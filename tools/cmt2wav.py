#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

import wave

#==============================================================================
def dump_bytes(bytes):
    idx = 0
    for ch in bytes:
        if (idx & 15) == 15:
            print('0x{:02X}'.format(ch))
        else:
            print('0x{:02X}'.format(ch), end=' ')
        idx += 1
    print()

#==============================================================================
def read_header(fp):
    ch = fp.read(1)
    if ch == b'':
        return None
    elif ch == b'\x3a':
        chunk = ch + fp.read(3)
    elif ch == b'\x3d':
        chunk = ch + fp.read(8+6)
    else:
        raise Exception("unknown header")

    return chunk

#==============================================================================
def extract_chunk(fp):
    chunk = read_header(fp)
    if chunk is None:
        return None

    if chunk[0] == 0x3a:
        while True:
            work = fp.read(2)
            if work[0] != 0x3a:
                raise Exception("not 0x3A")
            if work[1] == 0:
                chunk += work + fp.read(1)
                return chunk
            chunk += work + fp.read(work[1] + 1)
    else:
        print('BASIC')
        last0 = b'AAAAAAAAA'	# dummy
        while True:
            ch = fp.read(1)
            chunk += ch
            last0 = last0[1:] + ch
            if last0 == b'\x00' * 9:
                return chunk

#==============================================================================
def extract_files(cmt_file):
    files = []
    with open(cmt_file, 'rb') as fp:
        while True:
            chunk = extract_chunk(fp)
            if chunk is None:
                break
            files.append(chunk)

    return files

#==============================================================================
def add_blank(wav, sec):
    wav.writeframes(b'\x80' * int(sec * 24000))

def add_space(wav, sec):
    pulses = b'\x1c' * 9 + b'\x80' + b'\xe4' * 9 + b'\x80'
    num = int(sec * 24000 / len(pulses))
    wav.writeframes(pulses * num)

def add_mark(wav, sec):
    pulses = b'\x1c' * 4 + b'\x80' + b'\xe4' * 4 + b'\x80'
    pulses *= 2
    num = int(sec * 24000 / len(pulses))
    wav.writeframes(pulses * num)

pulse_space = b'\x1c' * 9 + b'\x80' + b'\xe4' * 9 + b'\x80'
pulse_space *= 2
pulse_mark = b'\x1c' * 4 + b'\x80' + b'\xe4' * 4 + b'\x80'
pulse_mark *= 4

def char_pulses(ch):
    data = b''
    data += pulse_space
    for bit in range(8):
        if (ch & 1) == 0:
            data += pulse_space
        else:
            data += pulse_mark
        ch >>= 1
    data += pulse_mark
    data += pulse_mark
    return data

def add_data(wav, chunk):
    for ch in chunk:
        wav.writeframes(char_pulses(ch))

#==============================================================================
def main(opts, args):
    if len(args) != 2:
        return False

    files = extract_files(args[0])

    with wave.open(args[1], 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(24000)

        add_blank(wav, 1.0)

        for chunk in files:
            add_space(wav, 1.0)
            add_mark(wav, 2.5)
            add_data(wav, chunk)
            add_mark(wav, 1.3)
            add_space(wav, 2.5)
            add_blank(wav, opts.blank)

    return True

#==============================================================================
if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog ([options]) [cmt file] [wav file]')

    parser.add_option('-b', '--blank', type='float', dest='blank', default=3.4,
                      help='select blank seconds between files with BLANK (default 3.4sec)', metavar='BLANK')

    opts, args = parser.parse_args()

    if not main(opts, args):
        print()
        parser.print_help()
