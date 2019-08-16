import numpy as np
from numpy import array


def rolling_window_1d(data:np.array,
                      window_length: int,
                      stride: int):
    assert len(data.shape)==1,'Wrong dimension, expected an Nx1 vector'
    memory_stride  = data.strides[0]
    result         = np.lib.stride_tricks.as_strided(data,
                                                     shape=[(len(data)-window_length+1)//stride,window_length],
                                                     strides=[memory_stride*stride,memory_stride])
    return result


def split_sequence(sequence, n_steps):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the sequence
		if end_ix > len(sequence)-1:
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)