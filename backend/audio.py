# audio.py - contains audio processing functions
# code in file partially pulled from: https://github.com/wiseman/py-webrtcvad/blob/master/example.py

# Required imports
import collections
import contextlib
import sys
import wave
import re

import vadfuncs
from pydub import AudioSegment


def backgNoise(args):
    return


def deadSpace(filePath):
    "Takes .wav file path, and returns file paths of voiced audio segments from original file."
    
    sample_rate = 48000

    prepPath = '/tmp/' + re.split('.wav|.WAV', (filePath.split('/tmp/')[1]))[0] + 'Edited.WAV'

    # Preparation of wav file for vad function
    pySeg = AudioSegment.from_wav(filePath).set_channels(1).set_frame_rate(sample_rate).export(prepPath, format='wav')

    audio = vadfuncs.read_wave(prepPath)

    # finds voiced audio segments
    vad = vadfuncs.webrtcvad.Vad(3)
    frames = vadfuncs.frame_generator(30, audio[0], sample_rate)
    frames = list(frames)
    segments = vadfuncs.vad_collector(sample_rate, 30, 720, vad, frames)

    chunkPaths = []

    # Writes voice audio chunks + appends valid files
    for i, segment in enumerate(segments):
        path = prepPath.split('.WAV')[0] + 'chunk-'+ str(i) + '.WAV'
        print(' Writing %s' % (path))
        vadfuncs.write_wave(path, segment, sample_rate)

        currSeg = AudioSegment.from_wav(path).set_channels(2)

        if currSeg.duration_seconds >= 4:
            currSeg.export(path, format='wav')
            chunkPaths.append(path)

    return chunkPaths


def modifyVol(filePaths):
    "Takes .wav file paths, and changes average amplitude of files to -20dBFS (loudness)"

    for path in filePaths:
        pathSeg = AudioSegment.from_wav(path)

        change_dBFS = -20 - pathSeg.dBFS  
        pathSeg = pathSeg.apply_gain(change_dBFS)

        pathSeg.export(path, format='wav')
    
    return filePaths


def processAudio(filePath):
    "Takes .wav file path, runs file through audio processors, and returns processed file path(s)"

    voicedAudioPaths = deadSpace(filePath)
    finalAudioPaths = modifyVol(voicedAudioPaths)

    return finalAudioPaths


if __name__ == '__main__':
    processAudio(sys.argv[1])