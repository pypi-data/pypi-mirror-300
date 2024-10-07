import warnings
from typing import Tuple, Optional

import pandas as pd


def prepare_data(
        data: pd.DataFrame,
        position: Tuple[str, ...],
        source: str = 'source',
        target: str = 'target',
        interaction: str = 'interaction',
        weight: Optional[str] = None,
):
    """
    Prepare data, validation, and renaming columns
    :param weight:
    :param data:
    :param position:
    :param source:
    :param target:
    :param interaction:
    :return:
    """
    # check required columns
    required_columns = list(position) + [source, target]
    if weight:
        required_columns.append(weight)
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"""Missing required columns.\nExpected: {required_columns}\nFound: {data.columns.tolist()}""")

    # examine data
    _check_numeric_position(data, position)

    # sort by position
    df = data.sort_values(by=list(position)).reset_index(drop=True)

    # use multi-index for quick interval selection
    df.set_index(list(position), inplace=True)

    # rename columns
    df = df.rename(columns={source: 'source', target: 'target'})
    if interaction:
        df = df.rename(columns={interaction: 'interaction'})

    # Process 'source', 'target', 'observer' columns to ensure lists
    df['source'] = _process_column(df['source'])
    df['target'] = _process_column(df['target'])

    if weight:
        df = df.rename(columns={weight: 'weight'})
        df['weight'] = df['weight'].astype(float)
        df = _flatten_weights(df)

    return df

def segment(data, start=None, end=None, position=None):
    """
    Get interactions based on interval
    :param data: dataframe
    :param interval: interval
    :return: a dataframe with interactions
    """
    if (len(start) > 1 or len(end) > 1) and not isinstance(data.index, pd.MultiIndex):
        if position is None:
            raise ValueError("Position columns required for multi-level time step.")
        data.set_index(list(position), inplace=True)
    idx = pd.IndexSlice
    interval = data.loc[idx[start:end], :].copy()

    return interval


def calculate_weights(data, weight_func=lambda x: len(x)):
    """
    Calculate weights based on interaction
    :param data: dataframe
    :param weight_func: a function to calculate edge weights
    :return: a dictionary of edge weights
    """
    data['weight'] = data['interaction'].apply(weight_func)
    data = _flatten_weights(data)
    return data


def _flatten_weights(df):
    """
    Flatten weights in the dataframe
    :param df: dataframe
    :return: a dataframe with flattened weights
    """
    return df.explode('source').explode('target')


def agg_weights(data, position, agg_func=lambda x: sum(x)):
    # group by position and source, target, observer
    # raise error if 'weight' column is not found
    if 'weight' not in data.columns:
        raise ValueError("No 'weight' column found. You should run calculate_weights() first.")
    grouped = data.groupby(list(position) + ['source', 'target'])['weight'].agg(agg_func).reset_index()
    return grouped


def _process_column(series):
    def clean_cell(cell):
        if isinstance(cell, list):
            items = cell
        elif isinstance(cell, str):
            items = [item.strip() for item in cell.strip('[]').split(',')]
        else:
            items = [str(cell).strip()]
        return pd.unique([str(item).strip() for item in items])

    return series.apply(clean_cell)


def _check_numeric_position(data, position):
    # check required columns
    for col in position:
        if not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"Position column '{col}' must be numeric.")
