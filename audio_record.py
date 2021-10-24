
import pyaudio
import wave
import math
import struct
import audioop

# def rms( data ):   # root mean square
#     count = len(data)/2
#     format = "%dh"%(count)
#     shorts = struct.unpack( format, data )
#     sum_squares = 0.0
#     for sample in shorts:
#         n = sample * (1.0/32768)
#         sum_squares += n*n
#     return math.sqrt( sum_squares / count )

# def get_decibel(data):
#     result = rms(data)
#     if result == 0:
#         return float('-inf')
#     return 20 * math.log10(rms(data))

def record_audio(duration, output_name):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration
    WAVE_OUTPUT_FILENAME = "audio_output.wav"

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

    frames = []
    total_decibel_volume = 0;
    max_decibel_volume = -100;

    print("Starting recording audio... ")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        temp_rms = audioop.rms(data, 2)
        if(temp_rms > 0):
            temp_decibel_volume = 20 * math.log10(temp_rms)
            max_decibel_volume = max(max_decibel_volume, temp_decibel_volume)
            total_decibel_volume += temp_decibel_volume
    
    print("Done recording audio...")
    mean_decibel_volume = total_decibel_volume/int(RATE / CHUNK * RECORD_SECONDS)

    print('max_decibel_level: ', max_decibel_volume)
    print('mean_decibel_level: ', mean_decibel_volume)    
    with open('log_file.txt', 'a') as f:
        f.write(output_name + ': ' + str(mean_decibel_volume) + '\n')
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    record_audio(5)