import numpy as np
import librosa
from librosa import piptrack
from librosa.feature import chroma_cqt
from scipy.fftpack import fft
from scipy.interpolate import PchipInterpolator
from numpy.random import default_rng

flow_size = 0

class val_curve:
    def __init__(self, value, value2 = None, knots = None, bten = None, ften = None):
        global flow_size
        if not isinstance(value, np.ndarray):
            self.value = np.full(flow_size, value)
        else:
            self.value = value
        self.value2 = value2 #cannot construct w/ one value
        if knots is None:
            knots = np.arange(0, flow_size, 1) / 30
        if bten is None:
            bten = np.full(flow_size, 1)
        if ften is None:
            ften = np.full(flow_size, 1)

        self.knots = knots
        self.bten = bten
        self.ften = ften

    @classmethod
    def as2d(cls, val):
        if val.value2 is not None:
            return val
        return cls(val.value, val.value, val.knots, val.bten, val.ften)

    @classmethod
    def _boperatorimpl(cls, self, other, f):
        value2 = None
        if not isinstance(other, val_curve):
            other = val_curve(other)
        print(len(other.value))
        print(len(self.value))
        assert len(self.value) == len(other.value) # n!=m, n-knot and m-knot flows interacting is UB
        value = f(self.value, other.value)
        if self.value2 is not None:
            other = val_curve.as2d(other)
            value2 = f(self.value2, other.value2)
        return cls(value, value2, self.knots, self.ften, self.bten)

    @classmethod
    def _uoperatorimpl(cls, self, f):
        value2 = None
        value = f(self.value)
        if self.value2 is not None:
            value2 = f(self.value2)
        return cls(value, value2, self.knots, self.ften, self.bten)

    def __add__(self, other):
        return self._boperatorimpl(self, other, (lambda x, y : x + y))

    def __mul__(self, other):
        return self._boperatorimpl(self, other, (lambda x, y : x * y))

    def __truediv__(self, other):
        return self._boperatorimpl(self, other, (lambda x, y : x / y))

    def __pow__(self, other):
        return self._boperatorimpl(self, other, (lambda x, y : x ** y))

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def cos(self):
        return self._uoperatorimpl(self, (lambda x : np.cos(x)))

    def sin(self):
        return self._uoperatorimpl(self, (lambda x : np.sin(x)))

    def unpack(self):
        return self.value, self.value2, self.knots, self.bten, self.ften

class iterator:
    def __init__(self, params):
        self.__dict__['iterator'] = params
    def __setattr__(self, param, flow):
        def encode_flow(values, values2=None):
            return " ".join(np.char.mod('%f', values)) if values2 is None \
              else " ".join(np.char.mod('%f', np.dstack((values, values2)).flatten()))
        global flow_size
        param = self.__getattr__(param)
        values, values2, knots, bten, ften = flow.unpack()
        assert len(values) == len(knots) == len(bten) == len(ften)
        assert values2 is None or len(values) == len(values2)
        param[0][0].text = encode_flow(knots)  # knot positions
        param[1][0].text = encode_flow(values, values2)  # values
        param[2][0].text = encode_flow(bten)
        param[3][0].text = encode_flow(ften)
        return
    def __getattr__(self, item):
        if item in self.__dict__['iterator']:
            return self.__dict__['iterator'][item]
        raise KeyError


class flowholder():
    def __init__(self, flowdict):
        self.__dict__['flowdict'] = flowdict

    def __getattr__(self, key):
        return self.flowdict[key]

    def __setattr__(self, key, value):
        self.__dict__['flowdict'][key] = value

    def __iter__(self):
        for flow in self.__dict__['flowdict']:
            yield flow
def load_song(path, stem=False):
    song, sr = librosa.load(path, sr=None)
    fl = int(sr / 30) #remove later, update call in fractalanim
    duration_f = int(librosa.get_duration(y=song, sr=sr) * 30)
    duration_s = int(librosa.get_duration(y=song, sr=sr))
    global flow_size
    if stem is False:
        flow_size = duration_f  # only place this should EVER be written to
    else:
        assert duration_f == flow_size #if stems aren't the same size there is a good chance of alignment issues
    return song,sr,fl,duration_f,duration_s

def compute_flows(song, sr):
    global flow_size


    fl = int(sr / 30)

    #more chroma features?
    #rms frequency??
    #peak freq
    #articulation index??
    #signal noise ratio
    #intonation
    #prosody??
    #jitter and shimmer
    #speech activity detection
    #non-stationairty index
    #formants
    def compute_spectral_flows():
        D = librosa.stft(song, hop_length=fl)
        d = np.abs(D)
        S = librosa.amplitude_to_db(d, ref=np.max)

        flux = np.sqrt(np.mean(np.diff(S, axis=1) ** 2, axis=0))
        contrast = librosa.feature.spectral_contrast(S=S ** 2, sr=sr)[0] #PER OCTAVE. split
        bandwidth = librosa.feature.spectral_bandwidth(S=S ** 2, sr=sr)[0] # also does nothing lol
        centroid = librosa.feature.spectral_centroid(S=S ** 2, sr=sr)[0]
        rolloff = librosa.feature.spectral_rolloff(S=S ** 2, sr=sr)[0]
        harm, perc = librosa.decompose.hpss(d)
        harmrms = librosa.feature.rms(S=harm, hop_length=fl)
        percrms = librosa.feature.rms(S=perc, hop_length=fl)
        onset = librosa.onset.onset_strength(S=d, sr=sr)

        #formants do not work atm
        nformants = 5
        fft_signal = fft(song)
        freq_bins = np.fft.fftfreq(len(song), d=1.0 / sr)
        formant_freqs = np.zeros((flow_size, nformants))
        for i in range(flow_size):
            magnitude_spectrum = np.abs(fft_signal[i * fl:(i + 1) * fl])
            formant_freqs[i] = freq_bins[np.argsort(magnitude_spectrum)[-nformants:]]

        return flux, contrast, bandwidth, centroid, rolloff, harmrms, percrms, onset, formant_freqs

    def compute_chromatic_flows():
        cg = chroma_cqt(y=song, sr=sr, hop_length=fl)
        dcg = np.tile(cg, (2, 1))
        #print(dcg.shape)
        augmask = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
        majmask = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
        minmask = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
        dimmask = np.array([1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0])
        flow_colorwheel = np.zeros((flow_size))
        augcorr = np.zeros(flow_size)
        majcorr = np.zeros(flow_size)
        mincorr = np.zeros(flow_size)
        dimcorr = np.zeros(flow_size)
        flow_colorwheel = np.argmax(cg, axis=0) / 12
        for i in range(flow_size):
            j=0
            #flow_colorwheel[i] = cg[:, i].argmax()  # most active pitch
            align = lambda mask : j-2 if (j := np.max(np.correlate(dcg[:, i], mask, mode='full'))) > 2 else 0
            augcorr[i] = align(augmask)
            majcorr[i] = align(majmask)
            mincorr[i] = align(minmask)
            dimcorr[i] = align(dimmask)

        return flow_colorwheel, cg, augcorr, majcorr, mincorr, dimcorr

    def compute_util_flows():
        pitch = librosa.piptrack(y=song, sr=sr, hop_length=fl)
        zcr = librosa.feature.zero_crossing_rate(y=song, frame_length=fl, hop_length=fl)[0]
        rms = librosa.feature.rms(y=song, hop_length=fl)
        mbandsplit = librosa.feature.melspectrogram(y=song, sr=sr, n_mels=4, hop_length=fl)
        for i in range(0, 4):
            mbandsplit[i] = np.minimum(mbandsplit[i],
                                       np.full(mbandsplit[i].size, 2 * np.mean(mbandsplit[i])))  # clip @ 2x mean
            mbandsplit[i] = mbandsplit[i] / np.max(mbandsplit[i])  # normalize
        return pitch, zcr, rms, mbandsplit

    unorm = lambda n : (n.flatten()[:flow_size])/n.max()
    bnorm = lambda n: ((n.flatten()[:flow_size])/n.max()) * 2 - 1

    r = flowholder({})

    (r.flux, r.contrast, r.bandwidth, r.centroid, r.rolloff,
     r.harmrms, r.percrms, r.onset, formant_freqs) = compute_spectral_flows()
    r.f0 = formant_freqs[:,0]
    #r.f1 = formant_freqs[:, 0]... figure out how this is supposed to be indexed first
    pitch, r.zcr, r.rms, mbandsplit = compute_util_flows()
    r.lf = mbandsplit[0]
    r.lm = mbandsplit[1]
    r.hm = mbandsplit[2]
    r.hf = mbandsplit[3]
    #pitch # do something here
    r.colorwheel, cg, r.augcorr, r.majcorr, r.mincorr, r.dimcorr = compute_chromatic_flows()
    r.noteC = cg[0]
    r.noteDb = cg[1]
    r.noteD = cg[2]
    r.noteEb = cg[3]
    r.noteE = cg[4]
    r.noteF = cg[5]
    r.noteGb = cg[6]
    r.noteG = cg[7]
    r.noteAb = cg[8]
    r.noteA = cg[9]
    r.noteBb = cg[10]
    r.noteB = cg[11]

    for key in r:
        value = r.__dict__['flowdict'][key]
        assert isinstance(value, np.ndarray)
        if key != "colorwheel" or not np.all(value): #it's special because it has to be [0,1)
            value = unorm(value)
        assert len(value) == flow_size
        r.__dict__['flowdict'][key] = val_curve(value)

    return r

def lin():
    global flow_size
    return val_curve(np.linspace(0, 1, flow_size))