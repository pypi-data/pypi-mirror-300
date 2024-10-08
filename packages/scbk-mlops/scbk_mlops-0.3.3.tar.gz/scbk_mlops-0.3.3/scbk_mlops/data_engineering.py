"""
Data Engineering Module
--------------------------------------
해당 모듈은 데이터 전처리 및 Feature Engineering을 수행하는 모듈입니다.
"""

import pickle
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from arfs.feature_selection import GrootCV, CollinearityThreshold
from arfs.benchmark import highlight_tick
import os
cwd = os.getcwd()
import numpy as np

def add_change_features(df) -> pd.DataFrame:
    """
    Adding Change Features
    """
    # CASA Balance
    df['CASA_A_CNG_LM_3M'] = df['CASA_A_CASABAL_LM'] / df['CASA_A_CASABAL_AVG3M']  # Latest month / Avg of last 3 months
    df['CASA_A_CNG_LM_3M'].fillna(1, inplace=True)
    
    df['CASA_A_CNG_3M_6M'] = df['CASA_A_CASABAL_AVG3M'] / df['CASA_A_CASABAL_AVG6M']  # Avg of last 3 months / Avg of last 6 months
    df['CASA_A_CNG_3M_6M'].fillna(1, inplace=True)
    
    df['CASA_A_CNG_6M_12M'] = df['CASA_A_CASABAL_AVG6M'] / df['CASA_A_CASABAL_AVG12M']  # Avg of last 6 months / Avg of last 12 months
    df['CASA_A_CNG_6M_12M'].fillna(1, inplace=True)

    # TD Balance
    df['TD_A_CNG_LM_3M'] = df['TD_A_BAL_LM'] / df['TD_A_BAL_AVG3M']  # Latest month / Avg of last 3 months
    df['TD_A_CNG_LM_3M'].fillna(1, inplace=True)
    
    df['TD_A_CNG_3M_6M'] = df['TD_A_BAL_AVG3M'] / df['TD_A_BAL_AVG6M']  # Avg of last 3 months / Avg of last 6 months
    df['TD_A_CNG_3M_6M'].fillna(1, inplace=True)
    
    df['TD_A_CNG_6M_12M'] = df['TD_A_BAL_AVG6M'] / df['TD_A_BAL_AVG12M']  # Avg of last 6 months / Avg of last 12 months
    df['TD_A_CNG_6M_12M'].fillna(1, inplace=True)

    # MMF Balance
    df['MMF_A_CNG_LM_3M'] = df['MMF_A_BAL_LM'] / df['MMF_A_BAL_AVG3M']  # Latest month / Avg of last 3 months
    df['MMF_A_CNG_LM_3M'].fillna(1, inplace=True)
    
    df['MMF_A_CNG_3M_6M'] = df['MMF_A_BAL_AVG3M'] / df['MMF_A_BAL_AVG6M']  # Avg of last 3 months / Avg of last 6 months
    df['MMF_A_CNG_3M_6M'].fillna(1, inplace=True)
    
    df['MMF_A_CNG_6M_12M'] = df['MMF_A_BAL_AVG6M'] / df['MMF_A_BAL_AVG12M']  # Avg of last 6 months / Avg of last 12 months
    df['MMF_A_CNG_6M_12M'].fillna(1, inplace=True)

    # INV Balance
    df['INV_A_CNG_LM_3M'] = df['INV_A_BALLCY_LM'] / df['INV_A_BALLCY_AVG3M']  # Latest month / Avg of last 3 months
    df['INV_A_CNG_LM_3M'].fillna(1, inplace=True)
    
    df['INV_A_CNG_3M_6M'] = df['INV_A_BALLCY_AVG3M'] / df['INV_A_BALLCY_AVG6M']  # Avg of last 3 months / Avg of last 6 months
    df['INV_A_CNG_3M_6M'].fillna(1, inplace=True)
    
    df['INV_A_CNG_6M_12M'] = df['INV_A_BALLCY_AVG6M'] / df['INV_A_BALLCY_AVG12M']  # Avg of last 6 months / Avg of last 12 months
    df['INV_A_CNG_6M_12M'].fillna(1, inplace=True)

    # INS Balance
    df['INS_A_CNG_LM_3M'] = df['INS_A_PREMAMT_LM'] / df['INS_A_PREMAMT_AVG3M']  # Latest month / Avg of last 3 months
    df['INS_A_CNG_LM_3M'].fillna(1, inplace=True)
    
    df['INS_A_CNG_3M_6M'] = df['INS_A_PREMAMT_AVG3M'] / df['INS_A_PREMAMT_AVG6M']  # Avg of last 3 months / Avg of last 6 months
    df['INS_A_CNG_3M_6M'].fillna(1, inplace=True)
    
    df['INS_A_CNG_6M_12M'] = df['INS_A_PREMAMT_AVG6M'] / df['INS_A_PREMAMT_AVG12M']  # Avg of last 6 months / Avg of last 12 months
    df['INS_A_CNG_6M_12M'].fillna(1, inplace=True)

    return df

def add_penetration_features(df) -> pd.DataFrame:
    """
    Calculate penetration features by dividing account balances by AUM balances
    """
    # Calculate penetration features by dividing account balances by AUM balances
    # 6M penetration features
    df['CASA_AUM_PCT_6M'] = df['CASA_A_CASABAL_AVG6M'] / df['AUM_A_BAL_AVG6M']  # CASA Balance / AUM over last 6 months
    df['CASA_AUM_PCT_6M'].fillna(0, inplace=True)
    
    df['TD_AUM_PCT_6M'] = df['TD_A_BAL_AVG6M'] / df['AUM_A_BAL_AVG6M']  # TD Balance / AUM over last 6 months
    df['TD_AUM_PCT_6M'].fillna(0, inplace=True)
    
    df['MMF_AUM_PCT_6M'] = df['MMF_A_BAL_AVG6M'] / df['AUM_A_BAL_AVG6M']  # MMF Balance / AUM over last 6 months
    df['MMF_AUM_PCT_6M'].fillna(0, inplace=True)
    
    df['INV_AUM_PCT_6M'] = df['INV_A_BALLCY_AVG6M'] / df['AUM_A_BAL_AVG6M']  # INV Balance / AUM over last 6 months
    df['INV_AUM_PCT_6M'].fillna(0, inplace=True)
    
    df['INS_AUM_PCT_6M'] = df['INS_A_PREMAMT_AVG6M'] / df['AUM_A_BAL_AVG6M']  # INS Balance / AUM over last 6 months
    df['INS_AUM_PCT_6M'].fillna(0, inplace=True)
    
    # Additional penetration features for 3M and 12M can be added similarly if needed
    return df

def process_null_values(df):
    """
    Preprocess null values in the DataFrame based on column data types.
    
    Args:
        df (pd.DataFrame): Input DataFrame with potential null values.
    
    Returns:
        pd.DataFrame: DataFrame with null values processed based on data types.
    """
    for column in df.columns:
        if df[column].dtype == 'object':
            # Fill null values in categorical columns with 'Unknown'
            df[column].fillna('Unknown', inplace=True)
        elif pd.api.types.is_numeric_dtype(df[column]):
            # Fill null values in numeric columns with the median
            df[column].fillna(df[column].median(), inplace=True)
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            # Fill null values in datetime columns with the earliest date
            df[column].fillna(df[column].min(), inplace=True)
    
    return df

# Example usage:
# df = pd.DataFrame({'BASE_YYMM': ['202410', '202409', '202408', '202410', '202408'],
#                    'value': [10, 20, None, 40, 50],
#                    'category': [None, 'A', 'B', 'A', None]})
# df = process_null_values(df)
# S1, S2, S3 = split_data(df)

def split_data(df):
    """
    Split data into three DataFrames S1, S2, S3 based on unique BASE_YYMM values.
    
    Args:
        df (pd.DataFrame): Input DataFrame containing a column 'BASE_YYMM'.
    
    Returns:
        tuple: Three DataFrames (S1, S2, S3), where S1 corresponds to the earliest, 
               S2 corresponds to the next, and S3 corresponds to the latest BASE_YYMM.
    
    Raises:
        ValueError: If 'BASE_YYMM' column does not have exactly three distinct values or 
                    if the values are not in the required format (YYYYMM).
    """
    # Error check if BASE_YYMM column exists in the DataFrame
    if 'BASE_YYMM' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'BASE_YYMM' column.")

    # Extract unique values from BASE_YYMM column
    unique_values = df['BASE_YYMM'].unique()

    # Check if there are exactly three distinct values
    if len(unique_values) != 3:
        raise ValueError("The 'BASE_YYMM' column must have exactly three distinct values in the format YYYYMM.")

    # Check format of unique values (YYYYMM)
    for value in unique_values:
        if not isinstance(value, str) or len(value) != 6 or not value.isdigit():
            raise ValueError("The 'BASE_YYMM' column must contain values in the format YYYYMM.")

    # Sort unique values in ascending order
    sorted_values = sorted(unique_values)

    # Filter the dataset into three separate DataFrames based on BASE_YYMM values
    S1 = df[df['BASE_YYMM'] == sorted_values[0]].copy()
    S2 = df[df['BASE_YYMM'] == sorted_values[1]].copy()
    S3 = df[df['BASE_YYMM'] == sorted_values[2]].copy()

    return S1, S2, S3


def fit_feature_selection(train_df, resp):
    """
    Fit the feature selection pipeline and save it to a file.

    Parameters:
    - train_df (pd.DataFrame): The training dataset.
    - resp (str): The target field/response variable for feature selection.

    This function fits a feature selection pipeline on the provided training data
    and saves the resulting pipeline object as a pickle file, named with a 
    timestamp for versioning.
    """
    # Fit the feature selection pipeline
    feature_selection_pipeline = fit_feature_selection_pipeline(train_df, target_field=resp)
    
    # Store the file in the folder
    feature_selection_pipeline_file_path = (
        dt.datetime.now(dt.timezone.utc).strftime("feature_selection_pipeline-%Y%m%d-%H%M%S.pkl")
    )
    print(feature_selection_pipeline_file_path)
    
    # Save the feature selection pipeline
    with open(f"{cwd}/data/{feature_selection_pipeline_file_path}", "wb") as writer:
        writable = pickle.dumps(feature_selection_pipeline)
        writer.write(writable)



def fit_feature_selection_pipeline(train_df, customer_id_field='CIFNO', timestamp_field='base_yyyymm', target_field=''):
    """
    Build and fit the feature selection pipeline.

    Parameters:
    - train_df (pd.DataFrame): The training dataset.
    - customer_id_field (str): The field representing customer IDs. Defaults to 'CIFNO'.
    - timestamp_field (str): The field representing timestamp or time period. Defaults to 'base_yyyymm'.
    - target_field (str): The target field/response variable.

    Returns:
    - pipeline: A fitted feature selection pipeline.

    This function breaks down the input dataset into features (X) and the target (y),
    applies sample weighting to account for class imbalance, and then fits a feature 
    selection pipeline consisting of two stages of GrootCV and collinearity filtering.
    """
    # Read the model specification for data field details (adjust this part according to your actual data)
    # customer_id_field = model_specification["data_fields"]["customer_id"]
    # timestamp_field = model_specification["data_fields"]["timestamp"]
    # target_field = model_specification["data_fields"]["target"]

    # Break down the target and the features datasets
    y = train_df[target_field]
    X = train_df.drop(columns=[customer_id_field, timestamp_field, target_field])

    # Weight the sample to give the same importance to positive & negative groups
    positive_instance_weight = (len(y) / y.sum()) - 1
    sample_weights = [1.0 if y_value == 0 else positive_instance_weight for y_value in train_df[target_field]]

    # Build the feature selection pipeline
    pipeline = Pipeline(steps=[
        ("GrootCV1", GrootCV(objective="binary", cutoff=5, n_folds=3, n_iter=3, silent=True, rf=False)),
        ("CollinearityDrop", CollinearityThreshold(threshold=0.9)),  # Typically 0.9
        ("GrootCV2", GrootCV(objective="binary", cutoff=5, n_folds=3, n_iter=3, silent=True, rf=False))
    ])

    # Fit the feature selection pipeline
    pipeline.fit(X=X.fillna(0), y=y, GrootCV1__sample_weight=sample_weights, GrootCV2__sample_weight=sample_weights)
    return pipeline

def apply_feature_selection(train_df, test_df, resp=None):
    """
    Apply feature selection to train and test datasets.

    Parameters:
    - train_df (pd.DataFrame): The training dataset.
    - test_df (pd.DataFrame): The testing dataset.
    - resp (str): The target field/response variable.

    Returns:
    - train_reduced_df (pd.DataFrame): The reduced training dataset after feature selection.
    - test_reduced_df (pd.DataFrame): The reduced testing dataset after feature selection.

    This function transforms both the train and test datasets using the fitted feature 
    selection pipeline and ensures that any protected variables (if applicable) are included 
    in the final datasets for potential fairness analysis.
    """
    # Assuming 'resp' is the target variable and 'model_specification' holds information about data fields
    customer_id_field = 'CIFNO'  # Replace with your actual customer ID field
    timestamp_field = 'base_yyyymm'  # Replace with your actual timestamp field
    target_field = resp  # Replace with your actual target field

    # Add the available protected variables for fairness analysis (if applicable)
    available_protected_variables = [
        variable for variable in ['CUST_N_AGE_LM'] if variable in train_df.columns
    ]

    # Create the final reduced datasets
    train_reduced_df = pd.concat([train_reduced_df, train_df[[customer_id_field, timestamp_field, target_field] + available_protected_variables]], axis=1)
    test_reduced_df = pd.concat([test_reduced_df, test_df[[customer_id_field, timestamp_field, target_field] + available_protected_variables]], axis=1)

    return train_reduced_df, test_reduced_df


# with open(f"{cwd}/data/feature_selection_pipeline-20230910-123856.pkl", "rb") as f:
#     pipeline = pickle.load(f)

# Affluent_AUM_train_df, Affluent_AUM_test_df = compute_FEATURE_SELECTION(S1_Development_Affluent_AUM, S2_Validation_Affluent_AUM, resp='Resp_Affluent_AUM')

def feature_selection(S2:pd.DataFrame, resp='', existing_pipeline=''):
    """
    Apply GrootCV feature selection using the provided training data.

    Parameters:
    - S2 (pd.DataFrame): The training dataset.
    - resp (str): The target field/response variable.
    - existing_pipeline (str): The name of an existing feature selection pipeline to load and apply.

    This function either fits a new feature selection pipeline on the provided dataset
    or loads an existing one and applies it for feature selection.
    """
    
    fit_feature_selection_pipeline(S2, resp=resp)
    
    # Load an existing pipeline and apply it
    with open(f"{cwd}/data/{existing_pipeline}.pkl", "rb") as f:
        pipeline = pickle.load(f)

def output_eligible_dataset():
    """
    Output eligible dataset for model input
    """
    pass

def Data_Sampling(
    samplingdata=None,
    user_specified_ratio=None,
    response_variable=None):
    """
    Returns sampled data with snapshot, id and target variable where target variable is deduplicated 
    and non-responders are sampled using ratio at the snapshot level.
    
    Inputs:
    df: data (n_cust and responders)
    user_specified_ratio: Ratio to select the Non-Responders sample
    response_variable: The response variable to be used for sampling.
    
    Returns:
    final_sample: DataFrame with sampled data.
    """
    pass
    # # Parameters required for analysis within Function
    # Responder_count = "resp_value"
    # total_records = "records"
    # Responder_rate = "response_rate"
    # Responder_distribution = "proportion"
    # partition_variable_name = "base_yyyymm"
    # resp = response_variable

    # # Add random seed for replicability
    # np.random.seed(42)

    # # Dedupe each snapshot's responders and non-responders 
    # # (Combine all snapshots and pick one record randomly for each n_cust).
    # samplingdata[resp] = samplingdata[resp].astype(int)
    # samplingdata_resp = samplingdata[samplingdata[resp] > 0]
    # samplingdata_resp = samplingdata_resp.groupby('CIFNO').agg(np.random.choice).reset_index()

    # resp_prop1 = pd.DataFrame(samplingdata_resp[partition_variable_name].value_counts()).reset_index()
    # resp_prop1.columns = [partition_variable_name, Responder_count]
    # resp_prop1[Responder_distribution] = (resp_prop1[Responder_count] / sum(resp_prop1[Responder_count])) * 100

    # samplingdata_nonresp = samplingdata[samplingdata[resp] < 1]
    # samplingdata_nonresp = samplingdata_nonresp.groupby('CIFNO').agg(np.random.choice).reset_index()

    # Final_prop_ble = resp_prop1  # .merge(nonresp_prop)
    # print("Responder Proportion")
    # print(Final_prop_ble)

    # final_sample = pd.DataFrame()
    # # Sampling methods
    # for p in Final_prop_ble[partition_variable_name]:
    #     # The code continues here...

	# # Finalize the sampling process
    # df_non_resp = samplingdata_nonresp[samplingdata_nonresp[partition_variable_name] == p]
	# no = round(Final_prop_ble[Final_prop_ble.base_yyyymm == p].reset_index().iloc[0][Responder_count] * user_specified_ratio)
	# print(no, df_non_resp.shape)
	# df_non_resp = df_non_resp.sample(n=no, random_state=42)
	# df_resp = samplingdata_resp[samplingdata_resp[partition_variable_name] == p]
	# final_sample = pd.concat([final_sample, df_non_resp, df_resp], axis=0)
    # return final_sample