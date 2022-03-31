# code in file pulled from: https://github.com/wiseman/py-webrtcvad/blob/master/example.py

import collections
import contextlib
import sys
import wave

import vadfuncs
from pydub import AudioSegment

def main(args):
    if len(args) != 2:
        sys.stderr.write(
            'Usage: example.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)
    
    sample_rate = 48000

    # Preparation of wav file for vad function
    pySeg = AudioSegment.from_wav(args[1]).set_channels(1).set_frame_rate(sample_rate).export('editedFile.WAV', format='wav')

    audio = vadfuncs.read_wave('editedFile.WAV')

    vad = vadfuncs.webrtcvad.Vad(int(args[0]))
    frames = vadfuncs.frame_generator(30, audio[0], sample_rate)
    frames = list(frames)
    segments = vadfuncs.vad_collector(sample_rate, 30, 300, vad, frames)

    chunkPaths = []

    # Writes voice audio chunks
    for i, segment in enumerate(segments):
        path = 'chunk-%002d.wav' % (i)
        chunkPaths.append(path)
        print(' Writing %s' % (path))
        vadfuncs.write_wave(path, segment, sample_rate)
    
    onlyVoice = AudioSegment.from_wav(chunkPaths[0])

    # Merges chunks into single file
    if len(chunkPaths) > 1:
        for n in range(1, len(chunkPaths)):
            onlyVoice = onlyVoice + AudioSegment.from_wav(chunkPaths[n])

    onlyVoice.export('chunksTogether.wav', format='wav')

if __name__ == '__main__':
    main(sys.argv[1:])