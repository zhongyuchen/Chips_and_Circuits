import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import sys
sys.path.append('../')
from algorithms.readjson import readjson

import plotly
plotly.tools.set_credentials_file(username='zhongyuchen', api_key='MVlLKp3ujiU1bFQImbKP')


MARKER = dict(size=3)
LINE = dict(size=3)


class chip:
    # data structure
    wire = 0
    grid = []
    gate = []

    def __init__(self, size, gatelist):
        # line number
        self.wire = 0
        # 3D grid -> -1: gate, 0: available, > 0: line number
        self.grid = np.zeros([size[0], size[1], size[2]])
        for gate in gatelist:
            self.grid[0][gate[0]][gate[1]] = -1
        # list of the gates' coordinates
        self.gate = gatelist

    def plot(self):
        data = []
        # gates
        i = 1
        for g in self.gate:
            gate = go.Scatter3d(
                x=[g[0]],
                y=[g[1]],
                z=[0],
                marker=dict(size=8, color='#000000'),
                name='Gate ' + str(i)
            )
            i += 1
            data.append(gate)

        """
        # wires
        wire = go.Scatter3d(
            x=range(0, len(self.grid[0][0])),
            y=range(0, len(self.grid[0])),
            z=range(0, len(self.grid)),
            marker=MARKER,
            line=LINE,
            name='wire1'
        )
        """

        # layout
        layout = dict(
            width=800,
            height=700,
            autosize=False,
            title='chip',
            scene=dict(
                xaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid[0]))
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid[0][0]))
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid))
                ),
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=-1.7428,
                        y=1.0707,
                        z=0.7100,
                    )
                ),
                aspectratio=dict(x=1, y=1, z=0.7),
                aspectmode='manual'
            ),
        )

        # figure
        fig = go.Figure(data=data, layout=layout)
        # plot figure
        py.plot(fig, filename='test-3d', height=700, validate=False)


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    chip = chip(size1, gate1)
    chip.plot()
