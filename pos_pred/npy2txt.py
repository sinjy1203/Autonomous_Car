import numpy as np
from pathlib import Path
path = Path('./camera_param')
dist = np.load(str(path / 'dist.npy'))
mtx = np.load(str(path / 'mtx.npy'))
np.savetxt(str(path / 'dist.txt'), dist)
np.savetxt(str(path / 'mtx.txt'), mtx)
