import numpy as np
import mrcfile

filename = '4ug0_centered.mrc'
threshold = 100
pixel_size = 3

# every 1 out of 4 atoms will be P 
relateive = 4

with mrcfile.open(filename) as mrc:
    data = mrc.data.transpose()


binary = data > threshold

positions = list(zip(*np.where(binary == True)))
positions = np.array(positions, dtype=float) * pixel_size
positions -= np.mean(positions, axis=0)

def locations_to_pseudoatoms(positions):
    lines = []
    i = 1
    for position in positions:
        if i % relateive == 0:
            new_line = "ATOM {}  P   HIS{}   {}{}{}     1.00  1.00\n".format(str(i).rjust(6),
                                                                             str(i).rjust(6),
                                                                             str(format(position[0], ".3f")).rjust(8),
                                                                             str(format(position[1], ".3f")).rjust(8),
                                                                             str(format(position[2], ".3f")).rjust(8))
        else:
            new_line = "ATOM {} DENS DENS{}   {}{}{}     1  0.09      DENS\n".format(str(i).rjust(6),
                                                                                     str(i).rjust(6),
                                                                                     str(format(position[0], ".3f")).rjust(8),
                                                                                     str(format(position[1], ".3f")).rjust(8),
                                                                                     str(format(position[2], ".3f")).rjust(8))
        i += 1
        lines.append(new_line)
    return lines

lines = locations_to_pseudoatoms(positions)

with open('pseudoatomic.pdb', 'x') as file:
    file.writelines(lines)
    
