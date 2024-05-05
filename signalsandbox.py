from parameters import *
np.set_printoptions(suppress=True,precision=3)
song, sr, _, duration_f, duration_s = load_song("audio/test/sweep.wav")
import matplotlib.pyplot as plt

flows = compute_flows(song, sr)

plt.plot(flows.constant(1))
#plt.scatter(points[:, 0], points[:, 1], c='r')
plt.show()