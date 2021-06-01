from scipy.io.wavfile import read, write
import numpy as np
from scipy.signal import butter, lfilter
import soundfile as sf
from functools import reduce

def append_silence(data_new):
    for x in range(int(1000)):
        data_new.insert(0, 0)
    if len(data_new) < 4800:
        for y in range(int(4800-len(data_new))):
            data_new.append(0)
    return data_new

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

path = "D:/process_voice_classify/audio_raw/bat.wav"
file_save = 0
pt = 0
sr, data = read(path)
data_new = []
a = 0
low = 100.0
high = 3900.0
data = butter_bandpass_filter(data, low, high, sr, 6)
data = data.astype(np.int16)

# print("done")
for l in range(int(len(data) / 1024)):
    data1 = data[pt:pt + 1024]
    # data1 = butter_bandpass_filter(data1, low, high, sr, 6)
    # data1 = data1.astype(np.int16)
    pt = pt + 1024
    n = 0
    for m in range(int(len(data1) / 64)):
        data_scan = data1[n:n + 64]
        n = n + 64
        # print(max(data_scan))
        if max(data_scan) > 800:
            y = data_scan
            data_new.extend(y)
            a = 0
        # else:
        #     data_filter = Convert(data_scan)
        #     y = np.add(data_filter, data_scan)
        #     data_new.extend(y)
        elif len(data_new) > 500 and a == 0:
            if max(data_new) < 22000:
                value_thresh = int((22000 / max(data_new)))
                data_new = [i * value_thresh for i in data_new]
                    
            data_new = append_silence(data_new)
            data_new = np.array(data_new)
            data_new = data_new.astype(np.int16)
            sf.write("audio_data/{0}_{1}.wav".format('bat', file_save), data_new, sr, 'PCM_16')
    
            # data_new = data_new.astype(np.int16)
            # sf.write("file_mo_0/file_{0}_{1}.wav".format('bat', file_save), data_new, sr, 'PCM_16')
            data_new = []
            file_save += 1
            print('save done {}'.format(file_save))
            # else:
            #     data_new = append_silence(data_new)
            #     data_new = np.array(data_new)
            #     data_new = data_new.astype(np.int16)
            #     sf.write("audio_data/{0}_{1}.wav".format('bat', file_save), data_new, sr, 'PCM_16')
        
            #     # data_new = data_new.astype(np.int16)
            #     # sf.write("file_mo_0/file_{0}_{1}.wav".format('bat', file_save), data_new, sr, 'PCM_16')
            #     data_new = []
            #     file_save += 1
            #     print('save done {}'.format(file_save))
        else:
            a += 1
