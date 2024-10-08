"""
Reporting Module
--------------------------------------
해당 모듈은 모델링 결과를 리포팅하는 기능을 제공하는 모듈입니다.
주로 모형 개발과 관련된 문서 생성에 초점을 맞추고 있으며, EDA Report는 EDA Module에서 생성하시면 됩니다.
"""

import pandas as pd
import numpy as np
import xlwings as xw
import logging
import os
from evidently.report import Report
from evidently.metrics import *
from evidently import ColumnMapping
from evidently.options import ColorOptions

color_scheme = ColorOptions(
    primary_color = "#0473ea",
    fill_color = "#fff4f2",
    zero_line_color = "#525355",
    current_data_color = "#38d200",
    reference_data_color = "#0061c7"
)

logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def response_crosstab(df: pd.DataFrame, r_col_name: str, a_col_name: str, 
                      band=[0,1000000,5000000,10000000,30000000,50000000,100000000,float("inf")], 
                      band_labels=['0Mto1M', '1Mto5M', '5Mto10M', '10Mto30M', '30Mto50M', '50Mto100M', '100M+'], 
                      pct_bins=[0,10,20,30,40,50,60,70,80,90,100,float("inf")], 
                      pct_labels=['0-10%', '10%-20%', '20%-30%', '30%-40%', '40%-50%', '50%-60%', '60%-70%', '70%-80%', '80%-90%', '90%-100%', '100%+'], 
                      tot_period=['0'], positive_direction=True):
    """
    (ENG) Creates a crosstab to use when exploring the response definition
    (KOR) Response 변수 정의를 위한 crosstab 생성
    
    Output:
    - client_crosstab: returns a table based on client number counts for each cross 'bins'
    - balance_crosstab: returns a table based on balance amount for each cross 'bins'
    
    Args:
    - df (DataFrame): input data
    - r_col_name: ratio column name (for percentage calculation)
    - a_col_name: amount column name (for balance calculation)
    - band (List): List of predefined ranges for 'bins'
    - band_labels (List): List of predefined names for each 'bins'
    - pct_bins (List): List of predefined percent ranges for 'bins'
    - pct_labels (List): List of predefined percent names for each 'bins'
    - tot_period: '0' takes the entire period while others will take individual snapshots based on the input (typically base_yymm)
    - positive_direction: positives and negatives should be taken into consideration
    
    * By default, the bins are left inclusive and right exclusive
    """
    
    client_crosstab = pd.DataFrame()
    balance_crosstab = pd.DataFrame()
    
    bal_category_nm = f"{a_col_name}_BAL_CATEGORY"
    pct_category_nm = f"{r_col_name}_PCT_CATEGORY"
    
    if tot_period == ['0']:  # For the entire period, take df as a whole
        if positive_direction:
            df[bal_category_nm] = pd.cut(df[a_col_name], bins=band, labels=band_labels)
            df[pct_category_nm] = pd.cut(df[r_col_name], bins=pct_bins, labels=pct_labels)
            client_crosstab = pd.crosstab(index=df[pct_category_nm], columns=df[bal_category_nm], values=df[a_col_name], aggfunc='count')
            balance_crosstab = pd.crosstab(index=df[pct_category_nm], columns=df[bal_category_nm], values=df[a_col_name], aggfunc='sum')
            # 통계자료 출력 (Null 값 개수/Decrease 개수, Percentile - 이건 참고용)
            series_99 = df[a_col_name].copy()
            percentile_99 = df[a_col_name].quantile(0.99)
            above_99th = series_99[series_99 > percentile_99]
            average_above_99th = above_99th.mean()
            count_above_99th = above_99th.count()
            print("[Processing Successful for Total Period] Avg Bal Above 99th Percentile:", average_above_99th, "# of Clients Above 99th Percentile:", count_above_99th, "Null:", df[bal_category_nm].isna().sum(), df[pct_category_nm].isna().sum())
        else:
            a_col_name_neg = f"{a_col_name}_NEG"
            r_col_name_neg = f"{r_col_name}_NEG"
            df[a_col_name_neg] = df[a_col_name] * -1
            df[bal_category_nm] = pd.cut(df[a_col_name_neg], bins=band, labels=band_labels)
            df[pct_category_nm] = pd.cut(df[r_col_name_neg], bins=pct_bins, labels=pct_labels)
            client_crosstab = pd.crosstab(index=df[pct_category_nm], columns=df[bal_category_nm], values=df[a_col_name_neg], aggfunc='count')
            balance_crosstab = pd.crosstab(index=df[pct_category_nm], columns=df[bal_category_nm], values=df[a_col_name_neg], aggfunc='sum')
            # 통계자료 출력 (Null 값 개수/Decrease 개수, Percentile - 이건 참고용)
            series_99 = df[a_col_name_neg].copy()
            percentile_99 = df[a_col_name_neg].quantile(0.99)
            above_99th = series_99[series_99 > percentile_99]
            average_above_99th = above_99th.mean()
            count_above_99th = above_99th.count()
            print("[Processing Successful for Total Period] Avg Bal Above 99th Percentile:", average_above_99th, "# of Clients Above 99th Percentile:", count_above_99th, "Null:", df[bal_category_nm].isna().sum(), df[pct_category_nm].isna().sum())

    else:  # When the period is specified, redefine the df and calculate accordingly
        df2 = df[df['BASE_YYMM'].isin(tot_period)].copy()  # Can take in multiple periods as a list
        if positive_direction:
            df2[bal_category_nm] = pd.cut(df2[a_col_name], bins=band, labels=band_labels)
            df2[pct_category_nm] = pd.cut(df2[r_col_name], bins=pct_bins, labels=pct_labels)
            client_crosstab = pd.crosstab(index=df2[pct_category_nm], columns=df2[bal_category_nm], values=df2[a_col_name], aggfunc='count')
            balance_crosstab = pd.crosstab(index=df2[pct_category_nm], columns=df2[bal_category_nm], values=df2[a_col_name], aggfunc='sum')
            # 통계자료 출력 (Null 값 개수/Decrease 개수, Percentile - 이건 참고용)
            series_99 = df2[a_col_name].copy()
            percentile_99 = df2[a_col_name].quantile(0.99)
            above_99th = series_99[series_99 > percentile_99]
            average_above_99th = above_99th.mean()
            count_above_99th = above_99th.count()
            print(f"[Processing Successful for {tot_period}] Avg Bal Above 99th Percentile:", average_above_99th, "# of Clients Above 99th Percentile:", count_above_99th, "Null:", df2[bal_category_nm].isna().sum(), df2[pct_category_nm].isna().sum())
        else:
            a_col_name_neg = f"{a_col_name}_NEG"
            r_col_name_neg = f"{r_col_name}_NEG"
            df2[a_col_name_neg] = df2[a_col_name] * -1
            df2[r_col_name_neg] = df2[r_col_name] * -1
            df2[bal_category_nm] = pd.cut(df2[a_col_name_neg], bins=band, labels=band_labels)
            df2[pct_category_nm] = pd.cut(df2[r_col_name_neg], bins=pct_bins, labels=pct_labels)
            client_crosstab = pd.crosstab(index=df2[pct_category_nm], columns=df2[bal_category_nm], values=df2[a_col_name_neg], aggfunc='count')
            balance_crosstab = pd.crosstab(index=df2[pct_category_nm], columns=df2[bal_category_nm], values=df2[a_col_name_neg], aggfunc='sum')
            # 통계자료 출력 (Null 값 개수/Decrease 개수, Percentile - 이건 참고용)
            series_99 = df2[a_col_name_neg].copy()
            percentile_99 = df2[a_col_name_neg].quantile(0.99)
            above_99th = series_99[series_99 > percentile_99]
            average_above_99th = above_99th.mean()
            count_above_99th = above_99th.count()
            print(f"[Processing Successful for {tot_period}] Avg Bal Above 99th Percentile:", average_above_99th, "# of Clients Above 99th Percentile:", count_above_99th, "Null:", df2[bal_category_nm].isna().sum(), df2[pct_category_nm].isna().sum())

    return client_crosstab, balance_crosstab

def response_analysis_to_excel(output_dict, file_name, topic="", leave_opened=False):
    """
    Exports data from the output_dict to an Excel file with the specified name.
    
    Args:
    - output_dict (dict): Dictionary containing months as keys and dictionaries with dataframes 'df1' and 'df2' as values.
    - file_name (str): Desired name/path for the Excel file.
    - topic (str): Topic (product) for the analysis.
    - leave_opened (bool): Leaves the workbook opened for final check.
    """
    wb = xw.Book()  # Create a new workbook
    sheet = wb.sheets[0]
    current_row = 1  # Start at the first row
    var_name_row = 1  # Starting row for variable names list (for drop down menu)
    for month, data in output_dict.items():
        # Write the name of the dataset (month in this case)
        if month == '0':
            sheet.range(f"A{current_row}").value = "Total"
        else:
            sheet.range(f"A{current_row}").value = month
        
        current_row += 1  # Move to the next row
        
        # Write the two datasets side by side, separated by 1 column
        df1_start_cell = f"A{current_row}"
        df2_start_cell = f"{chr(65 + data['client_crosstab'].shape[1] + 1)}{current_row}"  # Starting cell for the second dataframe
        
        sheet.range(df1_start_cell).options(index=True, header=True).value = data['client_crosstab']
        sheet.range(df2_start_cell).options(index=True, header=True).value = data['balance_crosstab']
        
        # Determine the combined range for df1 and df2
        combined_end_col = chr(ord(df2_start_cell[0]) + data['balance_crosstab'].shape[1])
        combined_end_row = current_row + max(data['client_crosstab'].shape[0], data['balance_crosstab'].shape[0])
        combined_end_cell = f"{combined_end_col}{combined_end_row}"
        
        # Create a single Excel variable for the combined range
        df_range = sheet.range(f"{df1_start_cell}:{combined_end_cell}")
        
        if month == '0':
            df_range.name = f"{topic}_Total"
            # Write the variable name (to create dropdown menu easily) - Setting it to Column V but can be adjusted
            sheet.range(f"V{var_name_row}").value = f"{topic}_Total"
        else:
            df_range.name = f"{topic}_{month}"
            # Write the variable name (to create dropdown menu easily) - Setting it to Column V but can be adjusted
            sheet.range(f"V{var_name_row}").value = f"{topic}_{month}"
        
        var_name_row += 1
        
        # Adjust current_row to point to the row after the last populated row
        max_rows = max(data['client_crosstab'].shape[0], data['balance_crosstab'].shape[0])
        current_row += max_rows + 3  # 2 rows for spacing, and 1 row for the next dataset name
    
    # Save the workbook with the specified name
    sheet.name = 'data'
    if leave_opened:
        print("Process Complete. Please Save the File")
    else:
        wb.save(f"{file_name}.xlsx")
        wb.close()
        print("Process Complete. File Saved Under <notebooks>")


def output_dict_resp_analysis():
    """
    통계자료 출력 (Null 값 개수/Decrease 개수, Percentile - 이건 참고용)
    """
    pass



# # Updated by Jong Hwa Lee DQ Script Generator
# # Update filenames..
# #======================================================
# variable_description_file = "Input_KR_Variable_Description.csv"
# proc_means_file = "Input_Proc_Means.xlsx"
# # proc_freq_file = "Input_Proc_Freq.xlsx"

# # Changing to csv files as xlsx not readable (DRM issue)
# S1_Combined = "S1_Combined.csv"
# Snapshot_202204 = "Snapshot_202204.csv"
# Snapshot_202208 = "Snapshot_202208.csv"
# Snapshot_202212 = "Snapshot_202212.csv"
# Snapshot_202304 = "Snapshot_202304.csv"



def dq_data_processing(file_path: str) -> pd.DataFrame:
    """
    Process data for data quality report.
    """
    logger.info("NUM VARS DQ")
    logger.info(f"Processing file: {file_path}")
    data = pd.read_csv(file_path)
    data["Variable"] = data["Variable"].str.upper()
    data.rename(columns={
        'N': '01_# Obs',
        'N Miss': '02_Nmiss',
        'Minimum': '03_Min',
        'Maximum': '04_Max',
        '10th Pctl': '05_P10',
        '20th Pctl': '06_P20',
        '30th Pctl': '07_P30',
        # Uncomment and include additional percentiles if needed
        # '40th Pctl': '08_P40',
        # '50th Pctl': '09_P50',
        # '60th Pctl': '10_P60',
        # '70th Pctl': '11_P70',
        # '80th Pctl': '12_P80',
        # '90th Pctl': '13_P90',
        # 'Mean': '14_Mean'
    }, inplace=True)
    
    # Drop 'Label' column if it exists
    if 'Label' in data.columns:
        data.drop(['Label'], axis=1, inplace=True)
    logger.debug(f"Columns after renaming: {list(data.columns)}")
    data = pd.melt(data, id_vars='Variable', var_name='KPI', value_name='Value')
    data.rename(columns={'Variable': 'Variable Name'}, inplace=True)
    data.sort_values(by=['Variable Name', 'KPI'], ascending=True, inplace=True)
    return data

# #======================================================
# # Processing Data
# #======================================================
# # List of snapshot files
# snapshot_files = ["S1_Combined.csv", "Snapshot_202204.csv", "Snapshot_202208.csv", "Snapshot_202212.csv", "Snapshot_202304.csv"]

# # Process the first file
# data = dq_data_processing(snapshot_files[0])
# data.rename(columns={'Value': 'Value_1'}, inplace=True)

# # Process and merge the remaining files
# for i, file in enumerate(snapshot_files[1:], start=2):
#     temp_data = dq_data_processing(file)
#     temp_data.rename(columns={'Value': f'Value_{i}'}, inplace=True)
#     data = pd.merge(data, temp_data, on=['Variable Name', 'KPI'], how='outer')

def dq_process_and_merge_snapshots(snapshot_files):
    logger.info("Starting to process snapshot files.")
    # Process the first file
    data = dq_data_processing(snapshot_files[0])
    data.rename(columns={'Value': 'Value_1'}, inplace=True)

    # Process and merge the remaining files
    for i, file in enumerate(snapshot_files[1:], start=2):
        temp_data = dq_data_processing(file)
        temp_data.rename(columns={'Value': f'Value_{i}'}, inplace=True)
        data = pd.merge(data, temp_data, on=['Variable Name', 'KPI'], how='outer')
        logger.info(f"Merged data from file: {file}")

    return data

def dq_add_variable_type(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add variable type and serial number to the data.
    """
    logger.info("Adding Variable Type and Serial Number.")
    data['Variable Type'] = 'Num'
    
    # Add Serial Number
    unique_vars = data[['Variable Name']].drop_duplicates()
    unique_vars.sort_values(by='Variable Name', inplace=True)
    unique_vars['SI No'] = np.arange(len(unique_vars)) + 1
    logger.info(f"Number of Numerical Variables: {unique_vars.shape[0]}")
    data = pd.merge(data, unique_vars, on='Variable Name', how='left')
    return data

def dq_add_variable_description(data: pd.DataFrame, variable_description_file: str) -> pd.DataFrame:
    """
    Add variable description from the provided description file.
    """
    logger.info("Adding Variable Descriptions.")
    df_desc = pd.read_csv(variable_description_file)
    df_desc = df_desc[['Variable Name', 'Variable Description']]
    df_desc['Variable Name'] = df_desc['Variable Name'].str.upper().str.strip()
    data['Variable Name'] = data['Variable Name'].str.upper().str.strip()
    data = pd.merge(data, df_desc, on='Variable Name', how='left')
    missing_desc = data['Variable Description'].isnull().sum()
    logger.info(f"Variables with missing descriptions: {missing_desc}")
    data['Variable Description'] = data['Variable Description'].fillna("Variable Description Not Found")
    return data


def make_float(x):
    try:
        return float(x)
    except ValueError:
        return None

def dq_median_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform median analysis and determine variables to drop.
    """
    logger.info("Performing Median Analysis.")
    # Identify value columns (Value_1, Value_2, etc.)
    value_columns = [col for col in data.columns if col.startswith('Value_')]
    num_values = len(value_columns)
    logger.debug(f"Value columns identified: {value_columns}")

    # Convert value columns to numeric
    for col in value_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    data.fillna(0, inplace=True)
    
    # Calculate percentage changes between samples
    sample_pairs = []
    for i in range(num_values):
        for j in range(i+1, num_values):
            a = value_columns[i]
            b = value_columns[j]
            col_name = f"{a} vs {b}"
            data[col_name] = np.where(
                np.abs(data[a]) < 1,
                0,
                (data[b] / data[a] - 1).replace([np.inf, -np.inf], 0)
            )
            data[col_name] = data[col_name].abs()
            logger.debug(f"Calculated percentage change: {col_name}")

    data['Status'] = None
    data['Variable used in initial Sample'] = 'Yes'
    
    # Determine variables to drop based on median analysis
    median_kpi = '09_P50'
    median_data = data[data['KPI'] == median_kpi]
    percentage_change_cols = [col for col in data.columns if 'vs' in col]
    logger.debug(f"Percentage change columns: {percentage_change_cols}")

    condition_1 = (median_data[percentage_change_cols] > 1).all(axis=1)
    condition_2 = (median_data[percentage_change_cols] > 5).any(axis=1)
    variables_to_drop = median_data[condition_1 | condition_2]['Variable Name'].unique()
    drop_df = pd.DataFrame({'Variable Name': variables_to_drop, 'Variable used in Final Model': 'No'})

    # Save variables to drop
    drop_df.to_excel("Output_drop_var_list.xlsx", index=False)
    logger.info(f"Variables to drop (Total {len(variables_to_drop)}): {variables_to_drop}")

    data = pd.merge(data, drop_df, on='Variable Name', how='left')
    data['Variable used in Final Model'] = data['Variable used in Final Model'].fillna('Yes')
    return data

def dq_output_report(data: pd.DataFrame):
    """
    Generate the final DQ report and save it as an Excel and CSV file.
    """
    logger.info("Generating Output Report.")
    data['Reviewed By'] = None

    # Reorder columns
    value_columns = [col for col in data.columns if col.startswith('Value_')]
    vs_columns = [col for col in data.columns if 'vs' in col]
    columns_order = [
        'SI No', 'Variable Name', 'Variable Type', 'Variable Description', 'KPI',
    ] + value_columns + vs_columns + [
        'Status', 'Variable used in initial Sample', 'Variable used in Final Model',
        'Reviewed By'
    ]
    data = data[columns_order]

    # Rename value columns for clarity
    for i, col in enumerate(value_columns, start=1):
        data.rename(columns={col: f"Sample {i} (S{i})"}, inplace=True)

    # Write to Excel
    output_excel = "Output_DQ_Assurance_other.xlsx"
    with pd.ExcelWriter(output_excel) as writer:
        data.to_excel(writer, sheet_name="Numerical Variables", index=False)
    logger.info(f"Output Excel file saved: {output_excel}")

    # Write to CSV
    output_csv = "Output_DQ_Assurance_other.csv"
    data.to_csv(output_csv, index=False)
    logger.info(f"Output CSV file saved: {output_csv}")

# Updated file names and paths
# variable_description_file = "Input_KR_Variable_Description.csv"

# S1_Combined = "S1_Combined.csv"
# Snapshot_202204 = "Snapshot_202204.csv"
# Snapshot_202208 = "Snapshot_202208.csv"
# Snapshot_202212 = "Snapshot_202212.csv"
# Snapshot_202304 = "Snapshot_202304.csv"
# snapshot_files = [
#     S1_Combined,
#     Snapshot_202204,
#     Snapshot_202208,
#     Snapshot_202212,
#     Snapshot_202304
# ]
#data = dq_process_and_merge_snapshots(snapshot_files)
# data = dq_add_variable_type(data)
# data = dq_add_variable_description(data, variable_description_file)
# data = dq_median_analysis(data)
# dq_output_report(data)
# logger.info("Data Quality Report Generation Completed Successfully.")


def dq_data_processing_char(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process character data from a DataFrame for data quality report.
    Selects string columns and computes basic statistics.

    Parameters:
    - df: pd.DataFrame - Input DataFrame containing the data.

    Returns:
    - pd.DataFrame: Processed data for DQ report.
    """
    logger.info("Starting character data processing from DataFrame.")
    # Select string columns
    char_columns = df.select_dtypes(include=['object']).columns
    logger.info(f"Identified {len(char_columns)} character columns.")
    
    # Initialize list to collect data for each variable
    data_list = []

    # Process each character column
    for col in char_columns:
        variable_name = col.upper()
        series = df[col].astype(str).str.upper().str.strip()
        n_obs = series.count()
        n_miss = series.isnull().sum()
        mode_value = series.mode().iloc[0] if not series.mode().empty else None
        mode_freq = series.value_counts().iloc[0] if not series.value_counts().empty else None
        unique_values = series.nunique()
        
        # Collect the statistics in a dictionary
        stats = {
            'Variable Name': variable_name,
            '01_# Obs': n_obs,
            '02_Nmiss': n_miss,
            '03_Mode': mode_value,
            '04_Mode_Freq': mode_freq,
            '05_Unique_Values': unique_values
        }
        data_list.append(stats)
        logger.debug(f"Processed variable: {variable_name}")
    
    # Create a DataFrame from the collected statistics
    data = pd.DataFrame(data_list)
    
    # Melt the DataFrame to have a long format similar to the numerical processing
    data = pd.melt(data, id_vars='Variable Name', var_name='KPI', value_name='Value')
    data.sort_values(by=['Variable Name', 'KPI'], ascending=True, inplace=True)
    return data

def dq_add_variable_type_char(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add variable type label (char) to the data.
    """
    logger.info("Adding Variable Type (Char) to data.")
    data['Variable Type'] = 'Char'
    return data

def dq_add_variable_serial_number_char(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add variable serial number label (char) to the data.
    """
    logger.info("Adding Variable Serial Number for character variables.")
    unique_vars = data[['Variable Name']].drop_duplicates()
    unique_vars.sort_values(by='Variable Name', inplace=True)
    unique_vars['SI No'] = np.arange(len(unique_vars)) + 1
    logger.info(f"Number of Character Variables: {unique_vars.shape[0]}")
    data = pd.merge(data, unique_vars, on='Variable Name', how='left')
    return data

def dq_add_variable_description_char(data: pd.DataFrame, variable_description_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add variable description (char) from the provided description DataFrame.

    Parameters:
    - data: pd.DataFrame - Data with variables to describe.
    - variable_description_df: pd.DataFrame - DataFrame containing variable descriptions.

    Returns:
    - pd.DataFrame: Data with variable descriptions added.
    """
    logger.info("Adding Variable Descriptions for character variables.")
    df_desc = variable_description_df[['Variable Name', 'Variable Description']]
    df_desc['Variable Name'] = df_desc['Variable Name'].str.upper().str.strip()
    data['Variable Name'] = data['Variable Name'].str.upper().str.strip()
    data = pd.merge(data, df_desc, on='Variable Name', how='left')
    missing_desc = data['Variable Description'].isnull().sum()
    logger.info(f"Character Variables with missing descriptions: {missing_desc}")
    data['Variable Description'] = data['Variable Description'].fillna("Variable Description Not Found")
    return data

def dq_data_reconstruction_char(data: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruction of the data into report format for character variables.
    """
    logger.info("Reconstructing data for character variables into report format.")
    # Since we have only one DataFrame, the reconstruction might not be necessary,
    # but we'll pivot the data for the report format.
    data_pivot = data.pivot_table(
        index=['SI No', 'Variable Name', 'Variable Type', 'Variable Description'],
        columns='KPI',
        values='Value',
        aggfunc='first'
    ).reset_index()
    data_pivot.columns.name = None  # Remove the categorization of columns
    data_pivot.sort_values(by='SI No', inplace=True)
    return data_pivot

def dq_output_report_char(data: pd.DataFrame, output_excel: str, output_csv: str):
    """
    Generate final output for character type and save as Excel and CSV files.

    Parameters:
    - data: pd.DataFrame - Data to output.
    - output_excel: str - Filename for the Excel output.
    - output_csv: str - Filename for the CSV output.
    """
    logger.info("Generating Output Report for character variables.")
    data['Reviewed By'] = None

    # Write to Excel
    with pd.ExcelWriter(output_excel) as writer:
        data.to_excel(writer, sheet_name="Character Variables", index=False)
    logger.info(f"Output Excel file saved: {output_excel}")

    # Write to CSV
    data.to_csv(output_csv, index=False)
    logger.info(f"Output CSV file saved: {output_csv}")


# df = pd.read_csv('your_data_file.csv')
# data_char = dq_data_processing_char(df)
# data_char = dq_add_variable_type_char(data_char)
# data_char = dq_add_variable_serial_number_char(data_char)
# variable_description_df = pd.read_csv('variable_descriptions.csv')
# data_char = dq_add_variable_description_char(data_char, variable_description_df)
# data_char_report = dq_data_reconstruction_char(data_char)
# output_excel = "Output_DQ_Assurance_char.xlsx"
# output_csv = "Output_DQ_Assurance_char.csv"
# dq_output_report_char(data_char_report, output_excel, output_csv)

    logger.info("Data Quality Report Generation for Character Variables Completed Successfully.")

# Usage of toc model card from evidently
def generate_toc_model_card(
    train_data_path='train_data.csv',
    test_data_path='test_data.csv',
    target_column='target',
    prediction_column='prediction',
    report_dir='./model_card',
    model_name='Marketing Propensity Model',
    version='v1.0',
    model_description='',
    model_author='',
    model_type='',
    model_architecture='',
    date='',
    primary_use_case='',
    out_of_scope='',
    training_dataset_description='',
    training_data_source='',
    training_data_limitations='',
    evaluation_dataset_description='',
    evaluation_metrics='',
    decision_threshold='',
    considerations='',
    threshold_comment='',
    features_of_interest=None,
    limitations=None,
    ethical_considerations=None
):
    """
    Generate a Model Card using Evidently.ai with customizable text fields and plots.

    Args:
        train_data_path (str): Path to the training data CSV file.
        test_data_path (str): Path to the testing data CSV file.
        target_column (str): Name of the target column in the datasets.
        prediction_column (str): Name of the prediction column in the datasets.
        report_dir (str): Directory to store model card artifacts.
        model_name (str): Name of the model being documented.
        version (str): Version of the model.
        model_description (str): Description of the model.
        model_author (str): Author of the model.
        model_type (str): Type of the model.
        model_architecture (str): Architecture of the model.
        date (str): Date of the model.
        primary_use_case (str): Primary use case of the model.
        out_of_scope (str): Applications out of scope for the model.
        training_dataset_description (str): Description of the training dataset.
        training_data_source (str): Source of the training data.
        training_data_limitations (str): Limitations of the training data.
        evaluation_dataset_description (str): Description of the evaluation dataset.
        evaluation_metrics (str): Evaluation metrics used.
        decision_threshold (str): Decision threshold for classification.
        considerations (str): Caveats and recommendations.
        threshold_comment (str): Comments about decision thresholds.
        features_of_interest (list, optional): List of features to highlight in the report.
        limitations (str, optional): Known limitations of the model.
        ethical_considerations (str, optional): Ethical considerations for model use.

    Output:
        None: Saves the model card report as an HTML file in the specified directory.
    """
    # Set default values for optional arguments
    if features_of_interest is None:
        features_of_interest = []
    if limitations is None:
        limitations = 'The model may be biased towards certain demographics.'
    if ethical_considerations is None:
        ethical_considerations = 'Ensure internal compliance and governance.'

    os.makedirs(report_dir, exist_ok=True)

    # Load training and testing data
    try:
        train_data = pd.read_csv(train_data_path)
        test_data = pd.read_csv(test_data_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        return

    # Check if target and prediction columns exist
    if target_column not in train_data.columns or prediction_column not in train_data.columns:
        print(f"Error: Target column '{target_column}' or prediction column '{prediction_column}' not found in train data.")
        return
    if target_column not in test_data.columns or prediction_column not in test_data.columns:
        print(f"Error: Target column '{target_column}' or prediction column '{prediction_column}' not found in test data.")
        return

    # Create ColumnMapping
    column_mapping = ColumnMapping()
    column_mapping.target = target_column
    column_mapping.prediction = prediction_column

    # Prepare text fields
    model_details = f"""
  # Model Details

  ## Description
  * **Model name**: {model_name}
  * **Model version**: {version}
  * **Model author**: {model_author}
  * **Model type**: {model_type}
  * **Model architecture**: {model_architecture}
  * **Date**: {date}

  ## Intended use
  * **Primary use case**: {primary_use_case}
  * **Out of scope**: {out_of_scope}
"""

    training_dataset = f"""
  # Training dataset

  * **Training dataset**: {training_dataset_description}
  * **Source**: {training_data_source}
  * **Limitations**: {training_data_limitations}
"""

    model_evaluation = f"""
  # Model evaluation

  * **Evaluation dataset**: {evaluation_dataset_description}
  * **Metrics**: {evaluation_metrics}
  * **Decision threshold**: {decision_threshold}
"""

    considerations_text = f"""
  # Caveats and Recommendations
{considerations}
"""

    threshold_comment_text = f"""
  **Note**: {threshold_comment}
"""

    # Build the metrics list
    metrics_list = [
        Comment(model_details),
        ClassificationClassBalance(),
        Comment(training_dataset),
        DatasetSummaryMetric(),
        DatasetCorrelationsMetric(),
    ]

    for feature in features_of_interest:
        metrics_list.append(ColumnSummaryMetric(column_name=feature))

    metrics_list.extend([
        Comment(model_evaluation),
        ClassificationQualityMetric(),
        ClassificationConfusionMatrix(),
        ClassificationProbDistribution(),
        ClassificationRocCurve(),
        Comment(threshold_comment_text),
        ClassificationPRTable(),
        Comment(considerations_text)
    ])

    # Create the report
    model_card = Report(metrics=metrics_list,
                        options=[color_scheme])

    # Run the report
    model_card.run(current_data=test_data, reference_data=train_data, column_mapping=column_mapping)

    # Save the report
    report_path = os.path.join(report_dir, 'model_card_report.html')
    model_card.save_html(report_path)

    print(f"Model card report saved at: {report_path}")

def generate_dq_report(reference_data, current_data, report_path='custom_data_quality_report.html'):
    """
    Generate Evidently DQ Report
    """
    # Create the report with additional metrics
    data_quality_report = Report(metrics=[
        #DataQualityPreset(),
        #DataDriftPreset(),
        RegressionPerformanceMetrics(),
    ],
                                options=[color_scheme])

    # Run the report
    data_quality_report.run(reference_data=reference_data, current_data=current_data)

    # Save the report
    data_quality_report.save_html(report_path)

    print(f'Data Quality Report saved to {report_path}')



#========================================================================
#========================================================================
#========================================================================
#========================================================================



def snapshot_count(df, base_yymm, segment, resp):
    """
    Snapshot profile report
    """
    if segment == 'Affluent':
        df = df[(df['base_yyyymm'] == base_yymm) & ((df['SEGMENT'] == 2) | (df['SEGMENT'] == 3))]
    else:
        df = df[(df['base_yyyymm'] == base_yymm) & (df['SEGMENT'] == 4)]
    record_count = df.shape[0]
    responder_count = df[resp].sum()
    print(f"{base_yymm} {segment} {resp} Snapshot Record Count:", record_count)
    print(f"{base_yymm} {segment} {resp} Snapshot Responder Count:", responder_count)
    print(f" (responder_count / record_count) * 100: {((responder_count / record_count) * 100):.2f}%")

# for i in ['202204', '202208', '202212', '202304']:
#     for n in ['Affluent', 'PsB']:
#         if n == 'Affluent':
#             for y in ['Resp_Affluent_AUM', 'Resp_Affluent_CASA']:
#                 snapshot_count(snapshot_df, i, n, y)
#         else:
#             for y in ['Resp_PsB_AUM', 'Resp_PsB_CASA']:
#                 snapshot_count(snapshot_df, i, n, y)

def generate_eligibility_waterfall(df, segment_column, segment_values, timestamp_column, timestamps,
                                   exclusion_criteria, response_columns, output_folder):
    """
    Generate a waterfall eligibility report based on exclusion criteria.

    Args:
        df (pd.DataFrame): Input DataFrame containing customer data.
        segment_column (str): Column name indicating the customer segment.
        segment_values (list): List of values in segment_column defining the segment of interest.
        timestamp_column (str): Column name indicating the timestamp.
        timestamps (list): List of timestamps to process.
        exclusion_criteria (list): List of dictionaries, each defining an exclusion criterion.
            Each dictionary should have keys:
                - 'name': Name of the criterion.
                - 'flag_column': Name of the flag column to create.
                - 'condition': A function that takes df and returns a boolean Series.
        response_columns (list): List of response columns to analyze.
        output_folder (str): Folder path to save the CSV files.

    Returns:
        None

    Outputs:
        CSV files saved in the output_folder containing the eligibility waterfall report.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Filter the DataFrame to the segment of interest
    segment_df = df[df[segment_column].isin(segment_values)].copy()

    # Loop over timestamps
    for timestamp in timestamps:
        timestamp_df = segment_df[segment_df[timestamp_column] == timestamp].copy()
        population_size = len(timestamp_df)

        # Skip if no data for this timestamp
        if population_size == 0:
            continue

        # Initialize a DataFrame to hold waterfall data
        waterfall_data = []
        remaining_df = timestamp_df.copy()

        # Start with total population
        waterfall_step = {
            'Step': 'Total Population',
            'Remaining_Customers': len(remaining_df)
        }
        # Add total response counts
        for response_column in response_columns:
            total_response = remaining_df[response_column].sum()
            waterfall_step[f'{response_column}'] = total_response
        waterfall_data.append(waterfall_step)

        # Sequentially apply each exclusion criterion
        for criterion in exclusion_criteria:
            flag_column = criterion['flag_column']
            condition = criterion['condition']
            criterion_name = criterion['name']

            # Create exclusion flag
            remaining_df[flag_column] = condition(remaining_df).astype(int)

            # Exclude customers based on current criterion
            excluded_df = remaining_df[remaining_df[flag_column] == 1]
            remaining_df = remaining_df[remaining_df[flag_column] == 0]

            # Record the number of customers excluded at this step
            waterfall_step = {
                'Step': f'Exclude {criterion_name}',
                'Remaining_Customers': len(remaining_df)
            }
            # Add remaining response counts
            for response_column in response_columns:
                remaining_response = remaining_df[response_column].sum()
                waterfall_step[f'{response_column}'] = remaining_response
            waterfall_data.append(waterfall_step)

        # Convert waterfall data to DataFrame
        waterfall_df = pd.DataFrame(waterfall_data)

        # Save to CSV
        segment_name = '_'.join(map(str, segment_values))
        output_file = os.path.join(output_folder, f'waterfall_report_{segment_name}_{timestamp}.csv')
        waterfall_df.to_csv(output_file, index=False)

        print(f"Waterfall report saved to: {output_file}")

def data_drift_report(reference_data, current_data, column_mapping=None, report_path='data_drift_report.html'):
    """
    Generate data drift report (evidently)

    Args:
        reference_data (pd.DataFrame): The reference dataset to compare against.
        current_data (pd.DataFrame): The current dataset to evaluate for data drift.
        column_mapping (dict, optional): Column mapping for evidently.
        report_path (str, optional): Path to save the generated report.

    Returns:
        None
    """
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
    report.save_html(report_path)

def feature_selection_report(model, X_train, y_train, report_path='feature_selection_report.html'):
    """
    Generate feature selection report from GrootCV

    Args:
        model: The model used for feature selection.
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target variable.
        report_path (str, optional): Path to save the generated report.

    Returns:
        None
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    # Assuming GrootCV is a feature selection tool that provides feature importances
    # Since GrootCV is not a widely recognized tool, we'll simulate feature importances
    # For actual implementation, replace this with GrootCV's API calls

    # Example: Simulate feature importances from the model
    feature_importances = pd.Series(model.feature_importances_, index=X_train.columns)
    feature_importances = feature_importances.sort_values(ascending=False)

    # Generate the report
    plt.figure(figsize=(10, 6))
    feature_importances.plot(kind='bar')
    plt.title('Feature Importances from GrootCV')
    plt.xlabel('Features')
    plt.ylabel('Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importances.png')
    plt.close()

    # Save report as HTML
    with open(report_path, 'w') as f:
        f.write('<html><body>')
        f.write('<h1>Feature Selection Report from GrootCV</h1>')
        f.write('<img src="feature_importances.png" alt="Feature Importances">')
        f.write('</body></html>')

def generate_fine_classing_report(data, target_variable, report_path='fine_classing_report.html'):
    """
    Generate fine classing report

    Args:
        data (pd.DataFrame): Dataset for fine classing.
        target_variable (str): The target variable for classification.
        report_path (str, optional): Path to save the generated report.

    Returns:
        None
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import KBinsDiscretizer
    from sklearn.metrics import roc_auc_score

    # Exclude target variable to identify features
    features = data.drop(columns=[target_variable]).columns
    fine_classing_results = {}

    for feature in features:
        if data[feature].dtype.kind in 'bifc':  # Check if feature is numeric
            # Apply binning
            est = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
            binned_feature = est.fit_transform(data[[feature]]).flatten()
            binned_data = pd.DataFrame({feature+'_binned': binned_feature, target_variable: data[target_variable]})
            # Calculate WoE and IV
            woe_iv_table = calculate_woe_iv(binned_data, feature+'_binned', target_variable)
            fine_classing_results[feature] = woe_iv_table

    # Generate the report
    with open(report_path, 'w') as f:
        f.write('<html><body>')
        f.write('<h1>Fine Classing Report</h1>')
        for feature, woe_iv_table in fine_classing_results.items():
            f.write(f'<h2>Feature: {feature}</h2>')
            f.write(woe_iv_table.to_html(index=False))
        f.write('</body></html>')

def calculate_woe_iv(data, feature, target):
    """
    Helper function to calculate Weight of Evidence (WoE) and Information Value (IV)

    Args:
        data (pd.DataFrame): Data containing the feature and target variable.
        feature (str): The binned feature column name.
        target (str): The target variable column name.

    Returns:
        woe_iv_df (pd.DataFrame): DataFrame containing WoE and IV values for each bin.
    """
    import numpy as np
    total_good = (data[target] == 0).sum()
    total_bad = (data[target] == 1).sum()
    grouped = data.groupby(feature)
    woe_iv_df = grouped[target].agg(['count', 'sum'])
    woe_iv_df['good'] = woe_iv_df['count'] - woe_iv_df['sum']
    woe_iv_df['bad'] = woe_iv_df['sum']
    woe_iv_df['dist_good'] = woe_iv_df['good'] / total_good
    woe_iv_df['dist_bad'] = woe_iv_df['bad'] / total_bad
    woe_iv_df['WoE'] = np.log(woe_iv_df['dist_good'] / woe_iv_df['dist_bad']).replace({np.inf: 0, -np.inf: 0})
    woe_iv_df['IV'] = (woe_iv_df['dist_good'] - woe_iv_df['dist_bad']) * woe_iv_df['WoE']
    woe_iv_df = woe_iv_df.reset_index()
    return woe_iv_df
