import sys
import json
import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter

###########################################################
# Styles and config
plt.style.use('ggplot')
mpl.rcParams['font.family'] = 'monospace'
mpl.rcParams['font.monospace'] = 'DejaVu Sans Mono'
mpl.rcParams['grid.color'] = 'b0b0b0'
mpl.rcParams['axes.edgecolor'] = 'b0b0b0'

###########################################################
# sample single
data = {
    'title': 'Generic Title',
    'label': {'x': 'X-AXIS', 'y': 'Y-AXIS'},
    'percentage': True,
    'collection': [
        {'name': 'Vehicle', 'values': [2.32, 4.33]},
        {'name': 'CBC123', 'values': [3.01, 4.14, 3.36]},
    ]
}

###########################################################
# 
class MyBarGraph:
    """ plot, show, or save """
    def __init__(self, data):
        self.width = 0.75
        self.data = data
        self.transparent = data['transparent']
        self.percentage = data['percentage']
        self.title = data['title']
        self.x_label = data['label']['x']
        self.y_label = data['label']['y']
        self.x_values = np.arange(len(data['collection']))
        self.y_values = self.calculate(data['collection'])
        self.x_tick_label = [_['name'] for _ in data['collection']]
        self.fig, self.ax = plt.subplots()
        
    def calculate(self, collection):
        """ Get means of lists """
        retval = []
        for c in collection:
            mean = np.mean(c['values'])
            retval.append(mean)
        return retval
        
    def plot(self):
        """ Background plotting, must call. """
        for i, _ in enumerate(self.x_values):
            self.ax.bar(self.x_values[i], self.y_values[i], 
                        width=self.width, label=self.x_tick_label[i])

        buffer = 0.75
        self.ax.set_xlim(left=self.x_values[0]-buffer, 
                         right=self.x_values[-1]+buffer)
        self.ax.set_ylim(bottom=0, top=max(self.y_values)*1.2)

        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_xticks(self.x_values)
        self.ax.set_xticklabels(self.x_tick_label)
        if self.percentage:
            self.ax.yaxis.set_major_formatter(PercentFormatter())
        self.ax.grid(True)
        self.ax.legend()
        self.fig.tight_layout()

    def show(self):
        plt.show()
    
    def save(self, directory):
        """ Save as image. """
        filedir = Path(directory)
        
        if not filedir.exists():
            print(f'Creating directory {filedir} ...')
            filedir.mkdir()
        
        filepath = Path(filedir, self.title)
        print(f'Saving {filepath} ...')
        self.fig.savefig(filepath, dpi=300,
            transparent=self.transparent,
            )
        
###########################################################
# 
def test_plot(data):
    bg1 = MyBarGraph(data)
    bg1.plot()
    bg1.show()

    # bg1.save('sample')

def load_data(filepath):
    abspath = Path(filepath).absolute()
    if not abspath.exists():
        print(f'Error: Cannot find file: {abspath}')
        sys.exit(1)
    
    print(f'Loading from {abspath}...')
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

###########################################################
# 
def main():
    parser = argparse.ArgumentParser(
        description='Plot custom graphs.',
        epilog='Little Fei Fei'
        )
    parser.add_argument('--infile', '-i', type=str, dest='infile',
                        help='JSON file containing list of data')
    parser.add_argument('--outdir', '-o', type=str, dest='outdir',
                        default='.',
                        help='Output directory')
    args = parser.parse_args()
    
    if not args.infile:
        parser.print_help()
        sys.exit()

    data = load_data(args.infile)
    for d in data:
        bg = MyBarGraph(d)
        bg.plot()
        bg.save(args.outdir)
    print('DONE')

if __name__ == "__main__":
    main()

