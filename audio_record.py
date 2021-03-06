import pyaudio
import wave
import math
import struct
import audioop
import config as c
from scipy.io import wavfile

class AudioRecorder:

    def __init__(self, logger):
        self.logger = logger

    def get_decibel_level(self, wav_file_path):
        _, data = wavfile.read(wav_file_path)
        rms = audioop.rms(data,2)
        return 20*math.log10( rms )


    def record_audio(self, duration):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = duration

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

        frames = []
        total_decibel_volume = 0;
        max_decibel_volume = -100;

        self.logger.write('info', "starting recording audio... ")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            temp_rms = audioop.rms(data, 2)
            if(temp_rms > 0):
                temp_decibel_volume = 20 * math.log10(temp_rms)
                max_decibel_volume = max(max_decibel_volume, temp_decibel_volume)
                total_decibel_volume += temp_decibel_volume
        
        self.logger.write('info', "done recording audio...")
    
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(c.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        

if __name__ == '__main__':
    AudioRecorder().record_audio(5)