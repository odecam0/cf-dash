import pandas

data = pandas.read_csv("data/data.csv")

year_values = data.exercicio.unique()
min_year = year_values.min()
max_year = year_values.max()

def filter_by_date(data, min, max):
    return data[(data['exercicio'] >= min) & (data['exercicio'] <= max)]

def include_only_bairros(data, bairros:list):
    data = data[data['bairro'].isin(bairros)]
    return data

def filter_by_total_value(data, min_val, max_val):
        return data[(data['valor_aval'] >= min_val) & (data['valor_aval'] <= max_val)]

def generate_data(data=data, year_interval=None,
                  bairros_to_include=None, total_value_interval=None):
    
    if year_interval:
        data = filter_by_date(data, year_interval[0], year_interval[1])

    all_bairros = data.bairro.unique()
    if bairros_to_include:
        data = include_only_bairros(data, bairros_to_include)

    if total_value_interval:
        data = filter_by_total_value(data, total_value_interval[0], total_value_interval[1])

    data.latitude = data.latitude.apply(lambda x: x.replace(',', '.'))
    data.longitude = data.longitude.apply(lambda x: x.replace(',', '.'))

    return data, data.valor_aval.sort_values(), all_bairros

