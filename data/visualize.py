import tempfile
import numpy as np
from PIL import Image
from anytree.exporter import UniqueDotExporter


def get_grid(grid_size):
    H, W = grid_size
    img = np.ones((H, W, 3))
    for i in range(0, H // 10):
        for j in range(0, W // 10):
            if i % 2 == 0 and j % 2 == 1:
                img[i * 10:(i + 1) * 10, j * 10:(j + 1) * 10] = 0.8
            if i % 2 == 1 and j % 2 == 0:
                img[i * 10:(i + 1) * 10, j * 10:(j + 1) * 10] = 0.8
    return Image.fromarray((img * 255).astype(np.uint8))


def to_transparent(img, grid_size=(300, 400)):
    W, H = img.size
    ratio = W / float(H)
    grid = get_grid(grid_size)
    W_grid, H_grid = grid.size

    if ratio * H_grid < W_grid:
        H = int(round(H_grid * 0.98))
        W = int(round(H * ratio))
    else:
        W = int(round(W_grid * 0.98))
        H = int(round(W / ratio))

    if H == 0:
        H = H + 1

    if W == 0:
        W = W + 1

    img = img.resize((W, H), 1)
    W, H = img.size
    x = int(round((W_grid - W) / 2))
    y = int(round((H_grid - H) / 2))
    grid.paste(img, (x, y), mask=img)

    return grid


def save_tree_image(layout, out_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        def nodeattrfunc(e):
            img_path = tmpdir + f'/{e.name}.png'
            to_transparent(e.image).save(img_path)

            attr = {
                'label': '',
                'image': img_path,
                'shape': 'rect',
            }

            if e.name == 'root':
                attr.update({
                    'label': 'Root',
                    'labelloc': 't',
                    'fontsize': '28',
                })

            return ' '.join(
                f'{k}="{v}"' for k, v in attr.items()
            )

        UniqueDotExporter(layout.root,
                          nodeattrfunc=nodeattrfunc,
                          ).to_picture(out_path)


def save_composite_image(layout, out_path):
    out = layout.root.image.copy()
    M = layout.root.base_size
    for e in layout.elements:
        width = int(round(e.W * M))
        height = int(round(e.H * M))
        if width > 0 and height > 0:
            im = e.image.resize((width, height), Image.LANCZOS)
            x, y = int(round(e.x * M)), int(round(e.y * M))
            out.alpha_composite(im, (x, y))
    out.save(out_path)
