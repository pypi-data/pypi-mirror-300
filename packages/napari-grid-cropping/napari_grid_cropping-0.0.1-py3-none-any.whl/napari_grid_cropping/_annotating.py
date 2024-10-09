import enum
import os
import random
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from tifffile import imread, imwrite

if TYPE_CHECKING:
    import napari

analysis_folder = None
extracted_imgs = None
global_iteration_type = None


def load_lbl_img(i, viewer):
    if i >= len(extracted_imgs):
        return

    file = Path(extracted_imgs[i])
    well = file.stem.split("_")[0]
    exp = file.parents[0].name

    name = f"{exp}-{well}"

    lbl_file = os.path.join(
        analysis_folder,
        exp,
        f"{well}_lbl.tif",
    )

    img = imread(file)
    if os.path.isfile(lbl_file):
        if global_iteration_type == IterationType.NOT_YET_ANNOTATED:
            load_lbl_img(i + 1, viewer)
            return
        lbl = imread(lbl_file)
    else:
        if global_iteration_type == IterationType.ONLY_ALREADY_ANNOTATED:
            load_lbl_img(i + 1, viewer)
            return
        lbl = np.zeros(img.shape[:2], dtype=np.uint16)

    viewer.add_image(img, name=name)
    lbl_layer = viewer.add_labels(
        lbl,
        name=f"lbl-{name}",
        metadata={
            "i": i,
            "savepath_lbl": lbl_file,
        },
    )
    lbl_layer.mode = "paint"


def save_lbl_and_load_next_img(viewer):
    for layer in viewer.layers:
        if layer.name.startswith("lbl-"):
            imwrite(layer.metadata["savepath_lbl"], layer.data)
            i = layer.metadata["i"]

    viewer.layers.clear()
    if i + 1 < len(extracted_imgs):
        load_lbl_img(i + 1, viewer)


class IterationType(enum.Enum):
    ALL = 1
    NOT_YET_ANNOTATED = 2
    ONLY_ALREADY_ANNOTATED = 3


def label_widget(
    viewer: "napari.Viewer",
    path: str,
    iteration_type: IterationType = IterationType.ALL,
    shuffle: bool = False,
):
    global extracted_imgs
    global analysis_folder
    global global_iteration_type

    global_iteration_type = iteration_type
    analysis_folder = os.path.join(path, "analysis")
    extracted_imgs = glob(os.path.join(analysis_folder, "**", "*_img.tif"))
    if shuffle:
        random.shuffle(extracted_imgs)

    viewer.bind_key("q", save_lbl_and_load_next_img, overwrite=True)
    load_lbl_img(0, viewer)
