"""
Model Monitoring Module
--------------------------------------
해당 모듈은 모델의 모니터링을 수행하는 모듈입니다.
주로 모델의 예측 결과를 모니터링하고, 이상치를 탐지하는 기능을 제공합니다.
"""

def rai_dashboard(reference_data, current_data, model, sensitive_features, target_column):
    """
    Generate RAI dashboard for drift check

    Args:
        reference_data (pd.DataFrame): 기준 데이터셋.
        current_data (pd.DataFrame): 현재 평가할 데이터셋.
        model: 평가할 모델 객체.
        sensitive_features (list or pd.Series): 민감한 특성의 리스트 또는 시리즈.
        target_column (str): 목표 변수의 열 이름.

    Returns:
        dashboard: 생성된 RAI 대시보드 객체.
    """
    pass
    # from raiwidgets import ResponsibleAIDashboard
    # from responsibleai import RAIInsights

    # # RAIInsights 객체 생성
    # rai_insights = RAIInsights(
    #     model=model,
    #     train=reference_data,
    #     test=current_data,
    #     target_column=target_column,
    #     categorical_features=sensitive_features
    # )

    # # 필요한 메트릭 계산
    # rai_insights.compute()

    # # RAI 대시보드 생성 및 표시
    # dashboard = ResponsibleAIDashboard(rai_insights)
    # dashboard.show()
    # return dashboard

def evidently_dashboard(reference_data, current_data, column_mapping=None):
    """
    Generate evidently.ai dashboard for drift check

    Args:
        reference_data (pd.DataFrame): 기준 데이터셋.
        current_data (pd.DataFrame): 현재 평가할 데이터셋.
        column_mapping (dict, optional): 컬럼 매핑을 위한 딕셔너리.

    Returns:
        None
    """
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    # Data Drift 대시보드 생성
    dashboard = Report(tabs=[DataDriftPreset()])
    dashboard.calculate(reference_data, current_data, column_mapping=column_mapping)
    dashboard.save('evidently_dashboard.html')

def alert_report(metric_thresholds, current_metrics):
    """
    Generate alert report upon trigger

    Args:
        metric_thresholds (dict): 메트릭 임계값의 딕셔너리.
        current_metrics (dict): 현재 메트릭 값의 딕셔너리.

    Returns:
        alert_report (dict): 트리거된 알림의 상세 정보를 담은 딕셔너리.
    """
    alerts = {}
    for metric, threshold in metric_thresholds.items():
        current_value = current_metrics.get(metric)
        if current_value is not None and current_value > threshold:
            alerts[metric] = {
                'current_value': current_value,
                'threshold': threshold,
                'alert': True
            }
    return alerts

def model_decision_making(performance_metrics, drift_metrics, thresholds):
    """
    현재 모델이 충분한지 또는 재훈련이 필요한지 결정

    Args:
        performance_metrics (dict): 모델 성능 메트릭의 딕셔너리.
        drift_metrics (dict): 데이터 또는 모델 드리프트 메트릭의 딕셔너리.
        thresholds (dict): 성능 및 드리프트 임계값의 딕셔너리.

    Returns:
        decision (str): 'retrain' 또는 'keep' 중 하나.
    """
    retrain_needed = False

    for metric, value in performance_metrics.items():
        if value < thresholds.get(metric, float('inf')):
            retrain_needed = True
            break

    for metric, value in drift_metrics.items():
        if value > thresholds.get(metric, 0):
            retrain_needed = True
            break

    decision = 'retrain' if retrain_needed else 'keep'
    return decision

def output_recommendation(decision):
    """
    현재 모델을 계속 사용할지 또는 새로운 모델을 훈련할지에 대한 추천 제공

    Args:
        decision (str): 모델 결정 ('retrain' 또는 'keep').

    Returns:
        recommendation (str): 추천 사항에 대한 설명 문자열.
    """
    if decision == 'retrain':
        recommendation = "모델의 성능 저하 또는 데이터 드리프트가 감지되었습니다. 모델 재훈련이 권장됩니다."
    else:
        recommendation = "현재 모델이 안정적으로 작동하고 있습니다. 계속해서 사용할 수 있습니다."
    return recommendation

def update_monitoring(new_results, monitoring_data_path):
    """
    가장 최근 모형 결과로 모니터링 정보 업데이트

    Args:
        new_results (pd.DataFrame): 최신 모델 결과 데이터.
        monitoring_data_path (str): 모니터링 데이터를 저장할 파일 경로.

    Returns:
        None
    """
    import pandas as pd
    import os

    # 기존 모니터링 데이터 로드 또는 새로운 데이터로 초기화
    if os.path.exists(monitoring_data_path):
        monitoring_data = pd.read_csv(monitoring_data_path)
        updated_data = pd.concat([monitoring_data, new_results], ignore_index=True)
    else:
        updated_data = new_results

    # 업데이트된 모니터링 데이터 저장
    updated_data.to_csv(monitoring_data_path, index=False)
