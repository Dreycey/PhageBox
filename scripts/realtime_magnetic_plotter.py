"""
DESCRIPTION:
    This script is ussed to plot figure from the output
    of the magenetometer output. This script effectively
    measures the magnetic field in real time.
TO DO:
    1. Plot the derivative graph to get rate of magnetic force,
       akin to magnetic accceleration. 
    2. Create an automatic segmenter for the diffferent times the 
       magnet is turned on.
"""
# std packages
# non-std packages
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import argparse



# Create an argparse.Namespace object from input args.
def parseArgs(argv=None) -> argparse.Namespace:
    """
    This method takes in the arguments from the command and performs
    parsing.
    INPUT: 
        Array of input arguments
    OUTPUT:
        returns a argparse.Namespace object
    """
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--csv_path", action="store_true")
    parser.add_argument("-o", "--outpath", help="output path for all figures", required=True)
    return parser.parse_args(argv)

def animate(i):
    print(f"this is being called {i}")
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    line2.set_data(x, y * 2)

def main():
    global line, line2
    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    line, = axs[0].plot([], [], lw=5)
    line2, = axs[1].plot([], [], lw=5)
    
    for ax in axs: 
        ax.set_xlim(0, 2)
        ax.set_ylim(-2, 2)
    
    anim = animation.FuncAnimation(fig, animate)

    plt.show()

if __name__ == "__main__":
    main()