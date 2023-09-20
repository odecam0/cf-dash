import plotly.express as px

token = "pk.eyJ1Ijoib2RlY2FtIiwiYSI6ImNsbWt2ZjRpODA1bXUya280ZTd1Z2VoOHYifQ.LDBjcHJeF0007x0c3XdaZQ"
px.set_mapbox_access_token(token)

def sample_color_space_given_bairros(arr, cs):
    colors = px.colors.sample_colorscale(cs,
                                         [n/(len(arr) - 1) for n in range(len(arr))])
    bairros_colors = {} 
    [bairros_colors.update({b: c}) for b,c in zip(arr, colors)]
    return bairros_colors

def generate_map(data, bairros):
    "Made to be used with 'generate_data' from data.py in this folder"

    bairros_colors = sample_color_space_given_bairros(bairros, 'Phase')
    fig = px.scatter_mapbox(data, lat='latitude', lon='longitude', size='valor_aval',
                             mapbox_style='dark', color='bairro', zoom=12,
                             center={'lat':-22.88262, 'lon':-42.03036},
                             color_discrete_map=bairros_colors)
    fig.update_layout(showlegend=False)
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")

    return fig, bairros_colors

def generate_value_scatterplot(data):
    fig = px.scatter(range(1, len(data)+1), y=data)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

