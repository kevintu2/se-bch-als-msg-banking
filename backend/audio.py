# audio.py - contains audio processing functions
# code in file partially pulled from: https://github.com/wiseman/py-webrtcvad/blob/master/example.py

import collections
import contextlib
import sys
import wave

import vadfuncs
from pydub import AudioSegment


def backgNoise(args):
    return


def deadSpace(filePath):
    # "Takes .wav file path, and returns voiced audio segment from file."
    print("in deadspace function", flush=True)

    # if len(args) != 2:
    #     sys.stderr.write(
    #         'Usage: example.py <aggressiveness> <path to wav file>\n')
    #     sys.exit(1)
    
    sample_rate = 48000

    # # Preparation of wav file for vad function
    pySeg = AudioSegment.from_wav(filePath).set_channels(1).set_frame_rate(sample_rate).export('/tmp/editedFile.WAV', format='wav')

    audio = vadfuncs.read_wave('/tmp/editedFile.WAV')

    vad = vadfuncs.webrtcvad.Vad(3)
    frames = vadfuncs.frame_generator(30, audio[0], sample_rate)
    frames = list(frames)
    segments = vadfuncs.vad_collector(sample_rate, 30, 300, vad, frames)

    chunkPaths = []

    # Writes voice audio chunks
    for i, segment in enumerate(segments):
        path = '/tmp/chunk-%002d.WAV' % (i)
        chunkPaths.append(path)
        print(' Writing %s' % (path))
        vadfuncs.write_wave(path, segment, sample_rate)
    
    onlyVoice = AudioSegment.from_wav(chunkPaths[0])

    # Merges chunks into single file
    if len(chunkPaths) > 1:
        for n in range(1, len(chunkPaths)):
            onlyVoice = onlyVoice + AudioSegment.from_wav(chunkPaths[n])

    chunkedFile = '/tmp/chunksTogether.WAV'

    onlyVoice.export(chunkedFile, format='wav')

    return chunkedFile


def processAudio(filePath):
    "Takes .wav file path, runs file through audio processors, and returns processed file path"
    print(filePath, flush = True)
    voiceAudio = deadSpace(filePath)

    return voiceAudio

if __name__ == '__main__':
    processAudio(sys.argv[1:])