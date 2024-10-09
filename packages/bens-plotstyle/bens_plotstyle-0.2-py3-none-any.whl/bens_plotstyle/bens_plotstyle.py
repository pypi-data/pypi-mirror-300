import importlib.resources
import importlib.util
import matplotlib as mpl    
import matplotlib.pyplot as plt
import importlib
import os

def main():
    font_dirs = ["~/Library/Fonts/"]  # The path to the custom font file. Modify if your font library isn't here
    font_files = mpl.font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        mpl.font_manager.fontManager.addfont(font_file) 
    try:    
        mpl.font_manager.findfont('JuliaMono')
        print("Found font: JuliaMono")
    except:
        print("Font 'JuliaMono' not found")
    with importlib.resources.path(package='mplstyle_templates',resource='pretty_plotting_default.mplstyle') as path:
        package_path = path.absolute()
    # mpl_path = os.path.dirname(package_path)
    # print(package_path)
    plt.style.use(style=package_path)
   

def paper():
    with importlib.resources.path(package='mplstyle_templates',resource='pretty_plotting_paper.mplstyle') as path:
        package_path = path.absolute()
    # mpl_path = os.path.dirname(package_path)
    # print(package_path)
    plt.style.use(style=package_path)

if __name__ == '__main__':
    main()
