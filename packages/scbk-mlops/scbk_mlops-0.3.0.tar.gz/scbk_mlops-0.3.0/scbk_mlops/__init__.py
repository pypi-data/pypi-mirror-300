"""
scbk_mlops package initialization.
"""

__author__ = "Jong Hwa Lee, Jin Young Kim"
__all__ = ["eda", "ingestion", "reporting", "data_engineering", "model_engineering", "model_evaluation", "model_monitoring"]

# Logging initialization
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"SCBK-MLOps Library 로딩 완료; Authors 데이터분석부 {__author__}")