import imgui


def init(window):
    imgui.create_context()
    imgui.get_io().display_size = 100, 100
    imgui.get_io().fonts.get_tex_data_as_rgba32()
