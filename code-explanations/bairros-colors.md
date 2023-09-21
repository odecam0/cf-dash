# Explicação das cores dos bairros

Ao gerar o mapa inicialmente, este é exibido com uma legenda que atribui uma cor distinta a cada valor de um atributo dos dados, neste caso, os bairros. No entanto, enfrentei uma dificuldade: o componente 'Dropdown' do Dash não estava diretamente integrado com a criação do mapa. Isso significava que, embora a lógica para filtrar os dados funcionasse corretamente, o dropdown funcionava, mas as cores exibidas no dropdown não correspondiam às cores exibidas no mapa.

Para superar esse obstáculo, desenvolvi uma solução que envolveu a criação de uma paleta de cores com um número exato de cores correspondendo ao número de bairros.

[Módulo map](../map.py)

```python
def sample_color_space_given_bairros(arr, cs):
    colors = px.colors.sample_colorscale(cs,
                                         [n/(len(arr) - 1) for n in range(len(arr))])
    bairros_colors = {} 
    [bairros_colors.update({b: c}) for b,c in zip(arr, colors)]
    return bairros_colors
```

Essas cores foram então passadas como parâmetro para a função que gera o mapa. Uma vez que o mapa estava gerado, incluí junto com ele o esquema de cores para que pudesse ser reaproveitado na definição do dropdown.

```python
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
```

No módulo da aplicação em si, precisei lidar com essa nova informação retornada do procedimento de geração do mapa.

[app.py](../app.py)

```python

@callback(
    Output("bairros-multi-dropdown", "options"),
    Input("bairros_colors_store", "data"),
    prevent_initial_call=True
    )
def update_bairros_checklist(data):
    data = json.loads(data)
    options = [{"label": html.Div([n], style={'color': data[n]}), "value": n} for n in data.keys()]
    value = [e['value'] for e in options]
    return options
```

No callback que atualiza as opções do Dropdown com os valores possíveis, utilizei uma list comprehension para associar esses valores às cores corretas, fazendo uso dos dados retornados pelo módulo do mapa.

Essa solução pode parecer simples, mas demandou algum esforço para ser implementada e garantir a sincronização das cores entre o mapa e o dropdown.

