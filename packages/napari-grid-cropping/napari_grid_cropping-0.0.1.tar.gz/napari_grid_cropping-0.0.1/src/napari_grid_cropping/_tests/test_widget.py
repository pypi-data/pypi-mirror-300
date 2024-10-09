from magicgui import magicgui

from napari_grid_cropping._annotating import label_widget
from napari_grid_cropping._cropping import grid_widget


def test_label_widget_magicgui(make_napari_viewer):
    viewer = make_napari_viewer()
    widget = magicgui(label_widget)

    viewer.window.add_dock_widget(widget)


def test_grid_widget_magicgui(make_napari_viewer):
    viewer = make_napari_viewer()
    widget = magicgui(grid_widget)

    viewer.window.add_dock_widget(widget)
