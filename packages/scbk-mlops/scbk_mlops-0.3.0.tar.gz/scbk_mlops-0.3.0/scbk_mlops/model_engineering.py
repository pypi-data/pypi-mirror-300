"""
Model Engineering Module
--------------------------------------
해당 모듈은 모델링을 수행하는 모듈입니다.
AutoML 및 MLFlow를 활용하여 모형을 만드는 함수를 구현하였으며, 해당 함수를 활용하여 진행하시면 됩니다.
"""

from pycaret.classification import setup, compare_models
import joblib
import mlflow
import json
from sklearn.model_selection import cross_val_score
import pandas as pd
import mlflow
import mlflow.sklearn
import pandas as pd

def init_mlflow(experiment_name, tracking_uri=None):
    """
    MLFlow 실행

    Args:
        experiment_name (str): 사용할 MLFlow 실험의 이름.
        tracking_uri (str, optional): MLFlow 추적 서버의 URI. 기본값은 로컬 파일 시스템.

    Returns:
        None
    """
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

def pycaret_automl(data, target, session_id=None):
    """
    AutoML을 위해 Pycaret 실행

    Args:
        data (pd.DataFrame): 모델 학습을 위한 입력 데이터.
        target (str): 예측할 목표 변수의 열 이름.
        session_id (int, optional): 재현성을 위한 세션 ID.

    Returns:
        best_model: Pycaret에서 선택한 최고의 모델.
    """
    clf = setup(data=data, target=target, session_id=session_id, silent=True)
    best_model = compare_models()
    return best_model

def save_best_model(model, file_name):
    """
    평가 메트릭에 따라 가장 성능이 좋은 모델을 .pkl 파일로 저장

    Args:
        model: 저장할 학습된 모델 객체.
        file_name (str): 모델을 저장할 파일의 이름.

    Returns:
        None
    """
    joblib.dump(model, file_name)

def save_experiment_parameters(params, file_path):
    """
    Kedro에 사용할 실험 매개변수 저장

    Args:
        params (dict): 저장할 실험 매개변수의 딕셔너리.
        file_path (str): 매개변수를 저장할 파일 경로.

    Returns:
        None
    """
    with open(file_path, 'w') as f:
        json.dump(params, f)

def output_scored_predictions(data, model_path):
    """
    저장된 최고의 모델을 사용하여 각 행에 대한 예측 점수 출력

    Args:
        data (pd.DataFrame): 예측할 입력 데이터.
        model_path (str): 저장된 모델 파일의 경로.

    Returns:
        predictions (pd.Series): 각 행에 대한 예측 점수.
    """
    model = joblib.load(model_path)
    predictions = model.predict_proba(data)[:, 1]
    return predictions

def save_scored_predictions(predictions, file_path):
    """
    향후 사용을 위해 예측 점수를 .json 파일로 저장

    Args:
        predictions (pd.Series or pd.DataFrame): 저장할 예측 점수.
        file_path (str): 예측 점수를 저장할 .json 파일의 경로.

    Returns:
        None
    """
    predictions_list = predictions.tolist()
    with open(file_path, 'w') as f:
        json.dump(predictions_list, f)

def load_oot_dataset(train_path, valid_path, test_path):
    """
    훈련 검증 테스트 데이터셋 로드

    Args:
        train_path (str): 훈련 데이터셋 파일의 경로.
        valid_path (str): 검증 데이터셋 파일의 경로.
        test_path (str): 테스트 데이터셋 파일의 경로.

    Returns:
        train_data (pd.DataFrame): 훈련 데이터셋.
        valid_data (pd.DataFrame): 검증 데이터셋.
        test_data (pd.DataFrame): 테스트 데이터셋.
    """
    train_data = pd.read_csv(train_path)
    valid_data = pd.read_csv(valid_path)
    test_data = pd.read_csv(test_path)
    return train_data, valid_data, test_data

def automl_pipeline(data, target, experiment_name):
    """
    Pycaret을 사용하여 자동화된 모델 선택 및 튜닝 수행

    Args:
        data (pd.DataFrame): 입력 데이터셋.
        target (str): 데이터셋에서 목표 변수의 이름.
        experiment_name (str): Pycaret 실험의 이름.

    Returns:
        best_model: Pycaret이 선택하고 튜닝한 최고의 모델.
    """
    clf = setup(
        data=data,
        target=target,
        experiment_name=experiment_name,
        silent=True,
        log_experiment=True
    )
    best_model = compare_models()
    return best_model

def mlflow_pipeline(model, params, metrics, artifact_path):
    """
    실험 추적 및 모델 라이프사이클 관리를 위해 MLFlow 사용

    Args:
        model: MLFlow에 로깅할 모델.
        params (dict): 모델과 연관된 매개변수.
        metrics (dict): 모델의 평가 메트릭.
        artifact_path (str): 모델 아티팩트를 저장할 경로.

    Returns:
        run_id (str): MLFlow 실행 ID.
    """
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, artifact_path)
        run_id = run.info.run_id
    return run_id

def cross_validation(model, data, target, cv, scoring):
    """
    강력한 모델 평가를 위해 교차 검증 기법 적용 (e.g. k-fold stratified k-fold)

    Args:
        model: 평가할 모델.
        data (pd.DataFrame): 교차 검증에 사용할 데이터셋.
        target (str): 목표 변수의 이름.
        cv (int): 교차 검증 폴드 수.
        scoring (str): 평가에 사용할 스코어링 메트릭.

    Returns:
        cv_results (pd.DataFrame): 각 폴드의 스코어를 포함한 교차 검증 결과.
    """

    X = data.drop(columns=[target])
    y = data[target]

    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    cv_results = pd.DataFrame(scores, columns=['score'])
    return cv_results
