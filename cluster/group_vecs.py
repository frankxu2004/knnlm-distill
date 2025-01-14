import numpy as np
import tqdm

from fairseq.data import Dictionary

dstore_size = 153225485
vec_dim = 1024

dictionary = Dictionary.load('data-bin/wikitext103-bpe/dict.txt')
print(len(dictionary))

keys_from_memmap = np.memmap('checkpoints/wikitext103-bpe/dstore_keys.npy',
                             dtype=np.float16, mode='r', shape=(dstore_size, vec_dim))
vals_from_memmap = np.memmap('checkpoints/wikitext103-bpe/dstore_vals.npy',
                             dtype=np.int64, mode='r', shape=(dstore_size, 1))

keys = np.zeros((dstore_size, vec_dim), dtype=np.float16)
vals = np.zeros((dstore_size, 1), dtype=np.int64)

keys[:] = keys_from_memmap[:]
vals[:] = vals_from_memmap[:]
del keys_from_memmap, vals_from_memmap

vals = vals.squeeze()

# exclude 0
for word_id in tqdm.tqdm(range(1, len(dictionary))):
    np.save('dstore/ids/' + str(word_id) + '.npy', keys[vals == word_id])
