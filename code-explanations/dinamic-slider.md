# Explicação da Barra de Valores Dinâmicos

Uma aplicação desenvolvida com Dash consiste em uma [sequência de componentes com propriedades, incluindo obrigatoriamente um identificador (ID)](https://github.com/odecam0/cf-dash/blob/9d3fff14654a3c4d74c6d9b62e3eefaf4218bdaf/app.py#L21C1-L67C2). Além disso, há uma [série de definições de funções conhecidas como "callbacks"](https://github.com/odecam0/cf-dash/blob/9d3fff14654a3c4d74c6d9b62e3eefaf4218bdaf/app.py#L69C1-L138C38), que são acionadas quando certas propriedades de determinados componentes são modificadas. Os valores de retorno dessas funções callbacks são utilizados para definir propriedades de outros componentes.

Neste contexto, destacam-se dois callbacks relevantes: [um responsável pela geração do gráfico exibido](https://github.com/odecam0/cf-dash/blob/9d3fff14654a3c4d74c6d9b62e3eefaf4218bdaf/app.py#L110) e [outro encarregado de atualizar os valores máximos e mínimos da barra de valores](https://github.com/odecam0/cf-dash/blob/9d3fff14654a3c4d74c6d9b62e3eefaf4218bdaf/app.py#L76).

O código foi estruturado de forma que, quando o mapa é gerado, também são retornadas informações adicionais sobre os dados remanescentes após a filtragem. Um desses valores de retorno é, precisamente, o novo intervalo de valores que será usado pela barra de valores.

Uma nova figura é gerada toda vez que um dos componentes de controle é modificado. Como resultado, quando você ajusta a barra de valores, um novo mapa é gerado, e quando o mapa é gerado, ele, por sua vez, altera os valores na barra. Essa situação cria uma dependência circular, onde o callback da barra depende do callback que gera o mapa, e o callback que gera o mapa depende do callback que altera a barra.

Para resolver esse problema, uma solução foi implementada, consistindo na criação de um segundo callback que gera a figura apenas quando a barra de valores é modificada, sem afetar o próprio estado da barra.

Aqui estão as três funções relevantes para compreender essa solução:

```python
@callback(
    Output("value_range_slider", "min"),
    Output("value_range_slider", "max"),
    Output("value_range_slider", "value"),
    Input("min-max-val", "data"),
    prevent_initial_call=True
)
def update_value_slider(min_max_val):
    data = json.loads(min_max_val)
    min_val, max_val = min(data) - 1, max(data) + 1
    return min_val, max_val, (min_val, max_val)

@callback(
    Output("the_map", "figure"),
    Output("min-max-val", "data"),
    Output("bairros_colors_store", "data"),
    Input("year_interval_slider", "value"),
    State("value_range_slider", "value"),
    Input("bairros-multi-dropdown", "value")
)
def generate_graph(year, value, bairros_to_include):
    data = generate_data(
        year_interval=year,
        total_value_interval=value,
        bairros_to_include=bairros_to_include
    )

    map = generate_map(data[0], data[2])

    return map[0],  json.dumps(list(data[1])), json.dumps(map[1])

@callback(
    Output("the_map","figure", allow_duplicate=True),
    Output("bairros_colors_store", "data", allow_duplicate=True),
    State("year_interval_slider", "value"),
    Input("value_range_slider", "value"),
    State("bairros-multi-dropdown", "value"),
    prevent_initial_call=True
)
def generate_graph_filter_by_value(year, min_max, bairros):
    data = generate_data(
        year_interval=year,
        total_value_interval=min_max,
        bairros_to_include=bairros
    )

    map = generate_map(data[0], data[2])

    return map[0], json.dumps(map[1])
```

Embora esta solução funcione para resolver o problema, reconheço que pode não ser a solução ideal. Se você compreendeu o problema e tiver alguma sugestão melhor, sinta-se à vontade para contribuir.
