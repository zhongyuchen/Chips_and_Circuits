import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


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
        x = y = []
        for gate in self.gate:
            x.append(gate[0])
            y.append(gate[1])
        z = [0] * len(self.gate)
        gates = go.Scatter3d(x=x, y=y, z=z,
            marker=dict(size=8, color='#ffffff')
        )

        wires = []

        trace = go.Scatter3d(
            x=range(0, len(self.grid[0][0])),
            y=range(0, len(self.grid[0])),
            z=range(0, len(self.grid)),
            marker=dict(size=4, color=z, colorscale='Viridis'),
            line=dict(color='#1f77b4', width=1)
        )

        data = [gates, wires]

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
                    backgroundcolor='rgb(230, 230,230)'
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
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

        fig = go.Figure(data=data, layout=layout)

        py.iplot(fig, filename='test-3d', height=700, validate=False)


if __name__ == "__main__":
    chip = chip()