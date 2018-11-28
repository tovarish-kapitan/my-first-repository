import numpy as np
from scipy import ndimage

def little_research(frames):
    labels, num = ndimage.label(frame)
    print('найденные лейблы \n', num)
    cm = ndimage.measurements.center_of_mass(frame, labels)
    print('общий центр масс \n', cm)
    shit = []
    for i in range(num):
        sm = ndimage.sum(frame, labels, i + 1)
        shit.append(sm)
    print('массы лейблов\n',shit)
    fo = ndimage.find_objects(frame)
    print('найденные объекты\n',fo,'\n')

with open("matrix_saves/400_400_200_1_1_1_1_1_1_1_1_1_1_1_1_20_20_20_20_10_0_0_0_", 'br') as f:
    npzfile = np.load(f)
    frame = abs(npzfile['arr_0'][:, :, 0])
    frame = frame.astype(int)
    #frame = frame.astype(bool)

    little_research(frame)

    frame = ndimage.binary_opening(frame, structure=np.ones((2, 2))).astype(int)

    little_research(frame)