"""
Data Ingestion Module
--------------------------------------
해당 모듈은 데이터를 불러오는 기능을 제공하는 모듈입니다.
데이터 추출단계에서부터 미리 정의된 데이터를 불러오는 것을 추천 드리며, 그렇지 않더라도 최대한 일반화하여 진행이 가능하도록 Function을 구성하였습니다.
"""

import pandas as pd
import os

def convert_and_save_to_parquet(input_dataframe: pd.DataFrame, output_file_name: str) -> None:
    """
    (ENG) Saves txt, csv filetypes into parquet
    (KOR) txt, csv 등의 파일 형태를 parquet(pq) 형태로 저장해주는 함수입니다.

    Args:
        input_dataframe (pd.DataFrame): The DataFrame to be converted. Recommended to bring from the Data Catalog.
        output_file_name (str): Desired name for the output Parquet file (including the ".parquet" extension).

    Returns:
        None

    Examples:
        >>> df = pd.read_csv('input.csv')
        >>> save_as_parquet(df, 'output.parquet')
    """
    # Save the DataFrame as a Parquet file
    try:
        output_file_name_full = f'{output_file_name}.pq'
        input_dataframe.to_parquet(output_file_name_full, index=False)
        print(f'{output_file_name}.pq Successfully Saved.')
    except:
        print("Error")

def capitalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    dataframe 칼럼들을 모두 대문자로 변환.
    Convert all DataFrame column names to uppercase.

    Args:
        df (pd.DataFrame): Input DataFrame to transform.

    Returns:
        pd.DataFrame: A new DataFrame with column names in uppercase.

    Examples:
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        >>> capitalize_columns(df)
           COL1  COL2
        0     1     3
        1     2     4
    """
    df = df.copy()
    df.columns = df.columns.str.upper()
    return df

def typecast(df: pd.DataFrame) -> pd.DataFrame:
    """
    string, int, float 등 각 칼럼을 인식해 typecast 해주는 함수. Null 값 같은 경우 coerce로 그대로 두는 형태를 선정.
    Cast DataFrame columns to appropriate data types while preserving null values.
    Null values are preserved using 'errors="coerce"' where applicable.

    Args:
        df (pd.DataFrame): The input DataFrame to be typecasted.

    Returns:
        pd.DataFrame: A new DataFrame with columns cast to appropriate data types.
    """
    df = df.copy()

    # Use convert_dtypes to infer and convert data types
    df = df.convert_dtypes()

    # Attempt to convert columns to datetime if they match the 'YYYY-MM-DD' pattern
    date_pattern = r'^\d{4}-\d{2}-\d{2}'
    for col in df.select_dtypes(include='string').columns:
        if df[col].str.match(date_pattern).any():
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def partition_data(
    df: pd.DataFrame, 
    partition_column: str, 
    output_dir: str, 
    file_format: str = 'csv'
) -> None:
    """
    (KOR) 지정해준 칼럼의 Unique한 값들로 데이터를 개별 파일로 나눠주는 방식
    (ENG) Split the DataFrame into individual files based on unique values in a specified column.
    
    Args:
        df (pd.DataFrame): The input DataFrame to be partitioned.
        partition_column (str): The column name to partition the DataFrame by.
        output_dir (str): The directory where the partitioned files will be saved.
        file_format (str, optional): The format of the output files ('csv' or 'parquet'). Default is 'csv'.

    Returns:
        None

    Raises:
        ValueError: If the specified file format is not supported.

    Examples:
        >>> partition_data(df, 'Scorecard', './output', 'csv')
    """
    os.makedirs(output_dir, exist_ok=True)
    unique_values = df[partition_column].dropna().unique()

    for value in unique_values:
        partition_df = df[df[partition_column] == value]
        value_str = str(value).replace(' ', '_').replace('/', '_')
        filename = f"{partition_column}_{value_str}.{file_format}"
        filepath = os.path.join(output_dir, filename)

        if file_format == 'csv':
            partition_df.to_csv(filepath, index=False)
        elif file_format == 'parquet':
            partition_df.to_parquet(filepath, index=False)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
