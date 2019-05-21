import matplotlib.font_manager as fm

# フォント一覧
for font in fm.findSystemFonts():
    print(fm.FontProperties(fname=font).get_name())
