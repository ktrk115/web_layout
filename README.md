# WebForest: Real-world Web Page Dataset

This repository provides the WebForest dataset proposed in the paper "Modeling Visual Containment for Web Page Layout Optimization" (Pacific Graphics 2021).

| Layout tree | Composite image |
| :---------: | :-------------: |
| ![tree](https://ktrk115.github.io/web_layout/assets/tree.png) | ![composite](https://ktrk115.github.io/web_layout/assets/composite.png) |

## Installation

1. Clone this repository

    ```bash
    git clone https://github.com/ktrk115/web_layout.git
    cd web_layout
    ```

2. Create a new [conda](https://docs.conda.io/en/latest/miniconda.html) environment (Python 3.8)

    ```bash
    conda create -n web_layout python=3.8 graphviz
    conda activate web_layout
    ```

3. Install dependent libraries

    ```bash
    pip install -r requirements.txt
    ```

4. Download the WebForest dataset

    ```bash
    bash download.sh
    ```

5. Run and see `demo.py` for how to use the dataset

    ```bash
    python demo.py
    
    # ----------  Root  ----------
    # {'accessed': '2020-04-12 11:42:53.546634',
    #  'box': [0, 0, 1366, 768],
    #  'categories': ['Top/Computers/Software/Business_Drawing'],
    #  'height': 768,
    #  'nbox': [0.0, 0.0, 1.0, 0.5622254758418741],
    #  'url': 'https://www.tomsplanner.com/',
    #  'width': 1366}
    # 
    # ----------  First element  ----------
    # {'area_importance': 3,
    #  'box': [0, 0, 1366, 111],
    #  'css_selector': 'html > body > div > header',
    #  'html_tag': 'header',
    #  'label': 'image',
    #  'nbox': [0.0, 0.0, 1.0, 0.08125915080527087],
    #  'order': 0,
    #  'parent': 'root'}
    # 
    # Save layout tree to "tree.png"
    # Save composite image to "composite.png"
    ```

## Licence

GNU AGPLv3

## Citation

If this repository helps your research, please consider citing our paper.

```
@article{Kikuchi2021,
    title = {Modeling Visual Containment for Web Page Layout Optimization},
    author = {Kotaro Kikuchi and Mayu Otani and Kota Yamaguchi and Edgar Simo-Serra},
    journal = {Computer Graphics Forum},
    volume = {40},
    number = {7},
    pages = {33--44},
    year = {2021},
    doi = {10.1111/cgf.14399}
}
```
