import h5py
import pprint
import random

from data.tree import WebPageLayout
from data.visualize import save_tree_image, save_composite_image


with h5py.File('data/trainval.hdf5', mode='r') as f:
    g = random.choice(list(f.values()))
    layout = WebPageLayout(g)

    print('-' * 10 + '  Root  ' + '-' * 10)
    pprint.pprint(layout.root.attrs)
    print()

    print('-' * 10 + '  First element  ' + '-' * 10)
    pprint.pprint(layout.elements[0].attrs)
    print()

    out_path = 'tree.png'
    save_tree_image(layout, out_path)
    print(f'Save layout tree to "{out_path}"')

    out_path = 'composite.png'
    save_composite_image(layout, out_path)
    print(f'Save composite image to "{out_path}"')
