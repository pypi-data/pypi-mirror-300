import os
import string
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from tifffile import imread, imwrite

if TYPE_CHECKING:
    import napari


files = None
analysis_path = None
std_shapes = []
shape_names = []
global_add_text = None


def load_next_file(i, viewer):
    file = files[i]
    img = imread(file)
    name = Path(file).name
    img_layer = viewer.add_image(img, name=name)
    shape_layer = viewer.add_shapes(
        std_shapes,
        name=f"grid-{name}",
        shape_type="rectangle",
        edge_color="white",
        face_color="#ffffff00",
        edge_width=5,
        features={"shape_names": shape_names} if global_add_text else None,
        text=(
            {
                "string": "{shape_names}",
                "anchor": "upper_right",
                "size": 9,
                "color": "white",
                "translation": [48, -10],
            }
            if global_add_text
            else None
        ),
        metadata={
            "savepath_csv": os.path.join(
                analysis_path, name.replace(".tif", "._grid.csv")
            ),
            "savepath_img": os.path.join(
                analysis_path, name.replace(".tif", "")
            ),
            "i": i,
            "img_layer": img_layer,
        },
    )
    shape_layer.mode = "select"
    shape_layer.selected_data = set(range(len(std_shapes)))
    # shape_layer._fixed_aspect = True
    # fixed aspect disallows fine grained rotations


def save_and_next(viewer):
    for layer in viewer.layers:
        if layer.name.startswith("grid"):
            layer.save(layer.metadata["savepath_csv"])
            i = layer.metadata["i"]

            savepath_img = layer.metadata["savepath_img"]
            Path(savepath_img).mkdir(parents=True, exist_ok=True)
            for j, rect in enumerate(layer.data):
                start = np.floor(rect.min(axis=0)).astype(int)
                stop = np.ceil(rect.max(axis=0)).astype(int)
                sly = slice(start[0], stop[0])
                slx = slice(start[1], stop[1])

                tmp_img = layer.metadata["img_layer"].data[sly, slx]
                imwrite(
                    os.path.join(savepath_img, f"{shape_names[j]}_img.tif"),
                    tmp_img,
                )
    viewer.layers.clear()
    if i + 1 < len(files):
        load_next_file(i + 1, viewer)


def grid_widget(
    viewer: "napari.Viewer",
    path: str,
    cube_len: int = 206,
    start_height: int = 300,
    start_width: int = 700,
    num_rows: int = 12,
    num_cols: int = 8,
    add_text: bool = False,
):
    global files
    global analysis_path
    global global_add_text
    for i in range(num_cols):
        for j in range(num_rows):
            std_shapes.append(
                np.array(
                    [
                        [
                            start_height + j * cube_len,
                            start_width + i * cube_len,
                        ],
                        [
                            start_height + (j + 1) * cube_len - 1,
                            start_width + (i + 1) * cube_len - 1,
                        ],
                    ]
                )
            )
            shape_names.append(f"{string.ascii_uppercase[i]}{j+1}")

    files = glob(os.path.join(path, "*.tif"))
    analysis_path = os.path.join(path, "analysis")
    Path(analysis_path).mkdir(parents=True, exist_ok=True)
    global_add_text = add_text

    viewer.bind_key("q", save_and_next, overwrite=True)
    load_next_file(0, viewer)
