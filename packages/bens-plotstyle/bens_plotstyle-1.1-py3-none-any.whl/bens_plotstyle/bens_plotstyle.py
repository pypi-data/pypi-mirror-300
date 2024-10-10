import matplotlib as mpl    
import matplotlib.pyplot as plt
import importlib
import os

def main():
    font_dirs = [
        "~/Library/Fonts/",  # macOS
        "/usr/share/fonts/",  # Linux
        "/usr/local/share/fonts/",  # Linux
        "C:\\Windows\\Fonts\\"  # Windows
    ]
    for dir in font_dirs:
        if os.path.exists(dir):
            font_dirs = [dir]
    font_files = mpl.font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        print(font_file)
        try:
            mpl.font_manager.fontManager.addfont(font_file) 
        except:
            print("Failed to add font: ", font_file)
    try:    
        mpl.font_manager.findfont('JuliaMono')
        print("Found font: JuliaMono")
    except:
        print("Font 'JuliaMono' not found \n Please install JuliaMono font from https://juliamono.netlify.app/")
    package_path = os.path.dirname(os.path.realpath(__file__))
    # mpl_path = os.path.dirname(package_path)
    
    plt.style.use(style=os.path.join(package_path,'mplstyle_templates/pretty_plotting_default.mplstyle'))
   

def paper():
    package_path = os.path.dirname(os.path.realpath(__file__))
    # mpl_path = os.path.dirname(package_path)
    # print(package_path)
    plt.style.use(style=os.path.join(package_path,'mplstyle_templates/pretty_plotting_paper.mplstyle'))

if __name__ == '__main__':
    main()
