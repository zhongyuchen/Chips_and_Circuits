import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='chipsandcircuits', api_key='9A2KpJpwzbsL04AhXSTY')


def lineplot(costs_names, filename=""):
    costs_list = []
    name_list = []
    for cost_name in costs_names:
        costs_list.append(cost_name[0])
        name_list.append(cost_name[1])

    # draw line plot
    data = []
    for i, costs in enumerate(costs_list):
        trace = go.Scatter(
            x=list(range(len(costs))),
            y=costs,
            mode='lines',
            name=name_list[i]
        )
        data.append(trace)

    if filename == "":
        filename = "lineplot"

    layout = dict(
        title=filename,
        xaxis=dict(title='step'),
        yaxis=dict(title='cost')
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)
