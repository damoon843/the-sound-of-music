import librosa 
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
from scipy.io.wavfile import write
from skimage import io

# number of samples per second (length of wav file = len(y)/sr)
sr = 22050
# number of samples between successive frames (between columns of spectogram)
hop_length = 512 
# sample the input with window size 2048 = 1 frame
n_fft = 2048
# partition entire frequency spectrum into 128 evenly spaced frequencies to the human ear (ie mel scale, not absolute) 
n_mels = 128

# scale spectogram to pixel 
def minmax_imagescaling(S,):
    s_min = S.min()
    s_max = S.max()
    S_std = (S - s_min) / (s_max - s_min)
    return (S_std * 255).astype(np.uint8)

def wav_to_spectogram(filename):
    y, sr = librosa.load(filename)

    S = librosa.feature.melspectrogram(y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    # log scale
    S = np.log(S + 1e-9)
    return S

def spectogram_img(S, name):
    img = 255 - np.flip(minmax_imagescaling(S), axis=0)
    io.imsave(name, img)

def visualize_specto(S):
    fig = plt.figure(figsize = (10, 6))
    librosa.display.specshow(S, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
    plt.show()

def main():
    spectogram = wav_to_spectogram("data/pop.00058.wav")
    img = spectogram_img(spectogram, "test.png")
    # wav = librosa.feature.inverse.mel_to_audio(spectogram)
    # write('test.wav', sr, wav)
    # playsound('test.wav')


if __name__ == '__main__':
    main()