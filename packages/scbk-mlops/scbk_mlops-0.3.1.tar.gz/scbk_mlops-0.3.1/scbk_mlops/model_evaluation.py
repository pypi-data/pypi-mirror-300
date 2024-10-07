"""
Model Evaluation Module
--------------------------------------
해당 모듈은 모델링 결과를 평가하는 기능을 제공하는 모듈입니다.
주로 Classification 및 Clustering을 위한 함수를 제공하며, 해당 함수를 활용하여 모델링 결과를 평가하시면 됩니다.
"""

def create_leaderboard(model_results):
    """
    Create model leaderboard based on @30 S3

    Args:
        model_results (list of dict): 각 모델의 결과를 포함한 딕셔너리의 리스트.
            예: [{'model_name': 'Model1', 'accuracy': 0.95, 'f1_score': 0.94}, ...]

    Returns:
        leaderboard (pd.DataFrame): 모델 성능을 비교한 리더보드 데이터프레임.
    """
    import pandas as pd
    leaderboard = pd.DataFrame(model_results)
    leaderboard = leaderboard.sort_values(by='accuracy', ascending=False)
    return leaderboard

def output_evaluation_artifacts(reference_data, current_data):
    """
    공정성 편향 등과 같은 다양한 RAI 및 거버넌스 평가 자료 출력

    Args:
        reference_data (pd.DataFrame): 기준 데이터셋.
        current_data (pd.DataFrame): 평가할 현재 데이터셋.

    Returns:
        None
    """
    # Evidently를 사용하여 평가 자료 생성
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset

    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset(),
        DataQualityPreset()
    ])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html('evaluation_artifacts.html')

def model_evaluation_rai(model, X_test, y_test, sensitive_features):
    """
    Responsible AI (RAI) 도구를 고려하여 공정성 검토

    Args:
        model: 평가할 모델.
        X_test (pd.DataFrame): 테스트 입력 데이터.
        y_test (pd.Series): 테스트 목표 변수.
        sensitive_features (pd.Series): 민감한 특성의 시리즈.

    Returns:
        rai_metrics (dict): 공정성 평가 메트릭 딕셔너리.
    """
    from fairlearn.metrics import MetricFrame, selection_rate
    from sklearn.metrics import accuracy_score

    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score,
        'selection_rate': selection_rate
    }
    metric_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    rai_metrics = {
        'overall': metric_frame.overall,
        'by_group': metric_frame.by_group.to_dict()
    }
    return rai_metrics

def generate_leaderboard_report(models, X_test, y_test):
    """
    모델 비교 (e.g. S1 vs S2 S1 vs S3) 리더보드 보고서 생성

    Args:
        models (dict): 모델 이름과 모델 객체의 딕셔너리.
            예: {'Model1': model1, 'Model2': model2}
        X_test (pd.DataFrame): 테스트 입력 데이터.
        y_test (pd.Series): 테스트 목표 변수.

    Returns:
        report (pd.DataFrame): 모델별 성능 지표를 포함한 리더보드 보고서.
    """
    import pandas as pd
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

    results = []
    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else None
        results.append({
            'model_name': name,
            'accuracy': accuracy,
            'f1_score': f1,
            'roc_auc': roc_auc
        })

    report = pd.DataFrame(results)
    report = report.sort_values(by='accuracy', ascending=False)
    return report

def feature_impact(model, X_train, y_train, grootcv_importances):
    """
    GrootCV 결과와의 차이를 평가

    Args:
        model: 평가할 모델.
        X_train (pd.DataFrame): 훈련 입력 데이터.
        y_train (pd.Series): 훈련 목표 변수.
        grootcv_importances (pd.Series): GrootCV로부터 얻은 특징 중요도 시리즈.

    Returns:
        comparison (pd.DataFrame): 모델과 GrootCV 간의 특징 중요도 비교 결과.
    """
    import pandas as pd

    model_importances = pd.Series(model.feature_importances_, index=X_train.columns)
    comparison = pd.DataFrame({
        'Model Importances': model_importances,
        'GrootCV Importances': grootcv_importances
    })
    comparison['Difference'] = comparison['Model Importances'] - comparison['GrootCV Importances']
    return comparison

def model_explainability(model, X_train):
    """
    모델 해석 가능성 통찰 제공 (Global Explainability/Feature Impact/Local Explainability)

    Args:
        model: 해석할 모델.
        X_train (pd.DataFrame): 훈련 입력 데이터.

    Returns:
        explainability_reports (dict): 해석 가능성 보고서를 포함한 딕셔너리.
    """
    import shap
    import matplotlib.pyplot as plt
    shap.initjs()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)

    # Global Explainability
    plt.figure()
    shap.summary_plot(shap_values, X_train, show=False)
    plt.savefig('global_explainability.png')
    plt.close()

    # Feature Impact
    plt.figure()
    shap.summary_plot(shap_values, X_train, plot_type='bar', show=False)
    plt.savefig('feature_impact.png')
    plt.close()

    # Local Explainability
    plt.figure()
    shap.force_plot(explainer.expected_value, shap_values[0, :], X_train.iloc[0, :], matplotlib=True)
    plt.savefig('local_explainability.png')
    plt.close()

    explainability_reports = {
        'global_explainability': 'global_explainability.png',
        'feature_impact': 'feature_impact.png',
        'local_explainability': 'local_explainability.png'
    }
    return explainability_reports

def bias_fairness_assessment(model, X_test, y_test, sensitive_feature):
    """
    Wasserstein 거리 플롯 또는 기타 공정성 메트릭을 사용하여 편향 및 공정성 평가

    Args:
        model: 평가할 모델.
        X_test (pd.DataFrame): 테스트 입력 데이터.
        y_test (pd.Series): 테스트 목표 변수.
        sensitive_feature (str): 민감한 특성의 열 이름.

    Returns:
        fairness_metrics (dict): 편향 및 공정성 평가 결과 딕셔너리.
    """
    from scipy.stats import wasserstein_distance
    from sklearn.metrics import accuracy_score

    y_pred = model.predict(X_test)
    groups = X_test[sensitive_feature].unique()
    group_metrics = {}

    for group in groups:
        idx = X_test[sensitive_feature] == group
        group_y_pred = y_pred[idx]
        group_y_true = y_test[idx]
        accuracy = accuracy_score(group_y_true, group_y_pred)
        group_metrics[group] = {
            'accuracy': accuracy,
            'prediction_distribution': group_y_pred
        }

    # Wasserstein Distance between groups
    if len(groups) == 2:
        wd = wasserstein_distance(
            group_metrics[groups[0]]['prediction_distribution'],
            group_metrics[groups[1]]['prediction_distribution']
        )
    else:
        wd = None

    fairness_metrics = {
        'group_metrics': group_metrics,
        'wasserstein_distance': wd
    }
    return fairness_metrics

def check_governance_measures(governance_policies):
    """
    모든 거버넌스 관련 조치를 고려하도록 확인

    Args:
        governance_policies (list): 적용해야 할 거버넌스 정책의 리스트.

    Returns:
        compliance_report (dict): 각 정책에 대한 준수 여부.
    """
    # 거버넌스 정책 체크 (실제 구현에서는 상세한 로직 필요)
    compliance_report = {policy: True for policy in governance_policies}
    return compliance_report

def explainable_ai(model, X_train):
    """
    SHAP LIME과 같은 해석 가능성 방법을 통합하여 투명성과 해석 가능성 강화

    Args:
        model: 해석할 모델.
        X_train (pd.DataFrame): 훈련 입력 데이터.

    Returns:
        explanations (dict): SHAP 및 LIME 해석 결과를 포함한 딕셔너리.
    """
    import shap
    from lime.lime_tabular import LimeTabularExplainer
    import matplotlib.pyplot as plt

    # SHAP 설명
    explainer_shap = shap.TreeExplainer(model)
    shap_values = explainer_shap.shap_values(X_train)
    shap.summary_plot(shap_values, X_train, show=False)
    shap_plot = plt.gcf()
    plt.savefig('shap_summary.png')
    plt.close()

    # LIME 설명
    explainer_lime = LimeTabularExplainer(
        training_data=X_train.values,
        feature_names=X_train.columns.tolist(),
        mode='classification'
    )
    lime_exp = explainer_lime.explain_instance(
        data_row=X_train.iloc[0].values,
        predict_fn=model.predict_proba
    )
    lime_exp.save_to_file('lime_explanation.html')

    explanations = {
        'shap_summary_plot': 'shap_summary.png',
        'lime_explanation': 'lime_explanation.html'
    }
    return explanations

def model_fairness_check(model, X_test, y_test, sensitive_features):
    """
    모델 예측에서 편향을 식별하고 완화하기 위한 공정성 감사 수행

    Args:
        model: 평가할 모델.
        X_test (pd.DataFrame): 테스트 입력 데이터.
        y_test (pd.Series): 테스트 목표 변수.
        sensitive_features (pd.Series): 민감한 특성의 시리즈.

    Returns:
        audit_results (dict): 공정성 감사 결과.
    """
    from fairlearn.reductions import ExponentiatedGradient, DemographicParity
    from fairlearn.metrics import MetricFrame, selection_rate

    # 편향 식별
    y_pred = model.predict(X_test)
    metric_frame = MetricFrame(
        metrics=selection_rate,
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    disparity = metric_frame.difference()

    # 편향 완화
    mitigator = ExponentiatedGradient(
        estimator=model,
        constraints=DemographicParity()
    )
    mitigator.fit(X_test, y_test, sensitive_features=sensitive_features)
    y_pred_mitigated = mitigator.predict(X_test)

    # 완화 후 편향 재계산
    metric_frame_mitigated = MetricFrame(
        metrics=selection_rate,
        y_true=y_test,
        y_pred=y_pred_mitigated,
        sensitive_features=sensitive_features
    )
    mitigated_disparity = metric_frame_mitigated.difference()

    audit_results = {
        'original_disparity': disparity,
        'mitigated_disparity': mitigated_disparity
    }
    return audit_results
