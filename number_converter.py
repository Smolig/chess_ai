import numpy as np

from engine_v3 import Engine

# draw a bitbboard and convert it to an uint64

test_state = Engine()

pos_array = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1],
    ],
    dtype=np.uint64,
)

"""
[0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1],
[0, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 1],
[0, 1, 0, 0, 0, 0, 1, 0],
[0, 0, 1, 0, 0, 1, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 1],
"""

for i in range(0, 8):
    pos_array[i] = pos_array[i][::-1]


output = np.packbits(pos_array)

result = np.uint64(0)
for i in range(0, 8):
    result += np.uint64(output[i]) << np.uint64(8 * (7 - i))

test_state.print_board(result)
print(result)






