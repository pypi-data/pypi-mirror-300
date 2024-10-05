from __future__ import annotations

import inspect
import logging
import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import catboost
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from numpy import log1p
from pandas.api.types import is_numeric_dtype
from sklearn.metrics import check_scoring, get_scorer, make_scorer, roc_auc_score

from upgini.utils.features_validator import FeaturesValidator
from upgini.utils.sklearn_ext import cross_validate

try:
    from sklearn.metrics import get_scorer_names

    available_scorers = get_scorer_names()
except ImportError:
    from sklearn.metrics._scorer import SCORERS

    available_scorers = SCORERS
from sklearn.metrics._regression import (
    _check_reg_targets,
    check_consistent_length,
    mean_squared_error,
)
from sklearn.model_selection import BaseCrossValidator

from upgini.errors import ValidationError
from upgini.metadata import ModelTaskType
from upgini.resource_bundle import bundle
from upgini.utils.target_utils import correct_string_target

DEFAULT_RANDOM_STATE = 42

CATBOOST_REGRESSION_PARAMS = {
    "iterations": 250,
    "learning_rate": 0.05,
    "min_child_samples": 10,
    "max_depth": 5,
    "early_stopping_rounds": 20,
    "use_best_model": True,
    "one_hot_max_size": 100,
    "verbose": False,
    "random_state": DEFAULT_RANDOM_STATE,
    "allow_writing_files": False,
}

CATBOOST_BINARY_PARAMS = {
    "iterations": 250,
    "learning_rate": 0.05,
    "min_child_samples": 10,
    "max_depth": 5,
    "early_stopping_rounds": 20,
    "use_best_model": True,
    "one_hot_max_size": 100,
    "verbose": False,
    "random_state": DEFAULT_RANDOM_STATE,
    "allow_writing_files": False,
    "auto_class_weights": "Balanced",
}

CATBOOST_MULTICLASS_PARAMS = {
    "n_estimators": 250,
    "learning_rate": 0.25,
    "max_depth": 3,
    "border_count": 15,
    "max_ctr_complexity": 1,
    "loss_function": "MultiClass",
    "subsample": 0.5,
    "bootstrap_type": "Bernoulli",
    "early_stopping_rounds": 20,
    "use_best_model": True,
    "rsm": 0.1,
    "verbose": False,
    "random_state": DEFAULT_RANDOM_STATE,
    "allow_writing_files": False,
    "auto_class_weights": "Balanced",
}

LIGHTGBM_PARAMS = {
    "random_state": DEFAULT_RANDOM_STATE,
    "num_leaves": 16,
    "max_depth": 4,
    "n_estimators": 150,
    "learning_rate": 0.05,
    "min_child_weight": 1,
}

N_FOLDS = 5
BLOCKED_TS_TEST_SIZE = 0.2

NA_VALUES = [
    "",
    " ",
    "   ",
    "#n/a",
    "#n/a n/a",
    "#na",
    "-1.#ind",
    "-1.#qnan",
    "-nan",
    "1.#ind",
    "1.#qnan",
    "n/a",
    "na",
    "null",
    "nan",
    "n/a",
    "nan",
    "none",
    "-",
    "undefined",
    "[[unknown]]",
    "[not provided]",
    "[unknown]",
]

NA_REPLACEMENT = "NA"

SUPPORTED_CATBOOST_METRICS = {
    s.upper(): s
    for s in (
        "Logloss",
        "CrossEntropy",
        "CtrFactor",
        "Focal",
        "RMSE",
        "LogCosh",
        "Lq",
        "MAE",
        "Quantile",
        "MultiQuantile",
        "Expectile",
        "LogLinQuantile",
        "MAPE",
        "Poisson",
        "MSLE",
        "MedianAbsoluteError",
        "SMAPE",
        "Huber",
        "Tweedie",
        "Cox",
        "RMSEWithUncertainty",
        "MultiClass",
        "MultiClassOneVsAll",
        "PairLogit",
        "PairLogitPairwise",
        "YetiRank",
        "YetiRankPairwise",
        "QueryRMSE",
        "QuerySoftMax",
        "QueryCrossEntropy",
        "StochasticFilter",
        "LambdaMart",
        "StochasticRank",
        "PythonUserDefinedPerObject",
        "PythonUserDefinedMultiTarget",
        "UserPerObjMetric",
        "UserQuerywiseMetric",
        "R2",
        "NumErrors",
        "FairLoss",
        "AUC",
        "Accuracy",
        "BalancedAccuracy",
        "BalancedErrorRate",
        "BrierScore",
        "Precision",
        "Recall",
        "F1",
        "TotalF1",
        "F",
        "MCC",
        "ZeroOneLoss",
        "HammingLoss",
        "HingeLoss",
        "Kappa",
        "WKappa",
        "LogLikelihoodOfPrediction",
        "NormalizedGini",
        "PRAUC",
        "PairAccuracy",
        "AverageGain",
        "QueryAverage",
        "QueryAUC",
        "PFound",
        "PrecisionAt",
        "RecallAt",
        "MAP",
        "NDCG",
        "DCG",
        "FilteredDCG",
        "MRR",
        "ERR",
        "SurvivalAft",
        "MultiRMSE",
        "MultiRMSEWithMissingValues",
        "MultiLogloss",
        "MultiCrossEntropy",
        "Combination",
    )
}


class EstimatorWrapper:
    def __init__(
        self,
        estimator,
        scorer: Callable,
        metric_name: str,
        multiplier: int,
        cv: BaseCrossValidator,
        target_type: ModelTaskType,
        add_params: Optional[Dict[str, Any]] = None,
        groups: Optional[np.ndarray] = None,
        text_features: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.estimator = estimator
        self.scorer = scorer
        self.metric_name = (
            "GINI" if metric_name.upper() == "ROC_AUC" and target_type == ModelTaskType.BINARY else metric_name
        )
        self.multiplier = multiplier
        self.cv = cv
        self.target_type = target_type
        self.add_params = add_params
        self.cv_estimators = None
        self.groups = groups
        self.text_features = text_features
        self.logger = logger or logging.getLogger()

    def fit(self, x: pd.DataFrame, y: np.ndarray, **kwargs):
        x, y, _, fit_params = self._prepare_to_fit(x, y)
        kwargs.update(fit_params)
        self.estimator.fit(x, y, **kwargs)
        return self

    def predict(self, **kwargs):
        return self.estimator.predict(**kwargs)

    def _prepare_to_fit(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, dict]:
        x, y, groups = self._prepare_data(x, y, groups=self.groups)
        return x, y, groups, {}

    def _prepare_data(
        self, x: pd.DataFrame, y: pd.Series, groups: Optional[np.ndarray] = None
    ) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
        for c in x.columns:
            if is_numeric_dtype(x[c]):
                x[c] = x[c].astype(float)
            else:
                x[c] = x[c].astype(str)

        if not isinstance(y, pd.Series):
            raise Exception(bundle.get("metrics_unsupported_target_type").format(type(y)))

        if groups is not None:
            x = x.copy()
            x["__groups"] = groups
            x, y = self._remove_empty_target_rows(x, y)
            groups = x["__groups"]
            x = x.drop(columns="__groups")
        else:
            x, y = self._remove_empty_target_rows(x, y)

        return x, y, groups

    def _remove_empty_target_rows(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        joined = pd.concat([x, y], axis=1)
        joined = joined[joined[y.name].notna()]
        joined = joined.reset_index(drop=True)
        x = joined.drop(columns=y.name)
        y = np.array(list(joined[y.name].values))

        return x, y

    def _prepare_to_calculate(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, dict]:
        x, y, _ = self._prepare_data(x, y)
        return x, y, {}

    def cross_val_predict(
        self, x: pd.DataFrame, y: np.ndarray, baseline_score_column: Optional[Any] = None
    ) -> Optional[float]:
        x, y, groups, fit_params = self._prepare_to_fit(x, y)

        if x.shape[1] == 0:
            return None

        scorer = check_scoring(self.estimator, scoring=self.scorer)

        if baseline_score_column is not None and self.metric_name == "GINI":
            self.logger.info("Calculate baseline GINI on passed baseline_score_column and target")
            metric = roc_auc_score(y, x[baseline_score_column])
        else:
            cv_results = cross_validate(
                estimator=self.estimator,
                x=x,
                y=y,
                scoring=scorer,
                cv=self.cv,
                groups=groups,
                fit_params=fit_params,
                return_estimator=True,
                error_score="raise",
            )
            metrics_by_fold = cv_results["test_score"]
            self.cv_estimators = cv_results["estimator"]

            self.check_fold_metrics(metrics_by_fold)

            metric = np.mean(metrics_by_fold) * self.multiplier
        return self.post_process_metric(metric)

    def check_fold_metrics(self, metrics_by_fold: List[float]):
        first_metric_sign = 1 if metrics_by_fold[0] >= 0 else -1
        for metric in metrics_by_fold[1:]:
            if first_metric_sign * metric < 0:
                self.logger.warning(f"Sign of metrics differs between folds: {metrics_by_fold}")

    def post_process_metric(self, metric: float) -> float:
        if self.metric_name == "GINI":
            metric = 2 * metric - 1
        return metric

    def calculate_metric(self, x: pd.DataFrame, y: np.ndarray, baseline_score_column: Optional[Any] = None) -> float:
        x, y, _ = self._prepare_to_calculate(x, y)
        if baseline_score_column is not None and self.metric_name == "GINI":
            metric = roc_auc_score(y, x[baseline_score_column])
        else:
            metrics = []
            for est in self.cv_estimators:
                metrics.append(self.scorer(est, x, y))

            metric = np.mean(metrics) * self.multiplier
        return self.post_process_metric(metric)

    @staticmethod
    def create(
        estimator,
        logger: logging.Logger,
        target_type: ModelTaskType,
        cv: BaseCrossValidator,
        x: pd.DataFrame,
        scoring: Union[Callable, str, None] = None,
        cat_features: Optional[List[str]] = None,
        text_features: Optional[List[str]] = None,
        add_params: Optional[Dict[str, Any]] = None,
        groups: Optional[List[str]] = None,
        has_date: Optional[bool] = None,
    ) -> EstimatorWrapper:
        scorer, metric_name, multiplier = _get_scorer(target_type, scoring)
        kwargs = {
            "scorer": scorer,
            "metric_name": metric_name,
            "multiplier": multiplier,
            "cv": cv,
            "target_type": target_type,
            "groups": groups,
            "text_features": text_features,
            "logger": logger,
        }
        if estimator is None:
            params = {}
            params["has_time"] = has_date
            # if metric_name.upper() in SUPPORTED_CATBOOST_METRICS:
            #     params["eval_metric"] = SUPPORTED_CATBOOST_METRICS[metric_name.upper()]
            if target_type == ModelTaskType.MULTICLASS:
                params = _get_add_params(params, CATBOOST_MULTICLASS_PARAMS)
                params = _get_add_params(params, add_params)
                estimator = CatBoostWrapper(CatBoostClassifier(**params), **kwargs)
            elif target_type == ModelTaskType.BINARY:
                params = _get_add_params(params, CATBOOST_BINARY_PARAMS)
                params = _get_add_params(params, add_params)
                estimator = CatBoostWrapper(CatBoostClassifier(**params), **kwargs)
            elif target_type == ModelTaskType.REGRESSION:
                params = _get_add_params(params, CATBOOST_REGRESSION_PARAMS)
                params = _get_add_params(params, add_params)
                estimator = CatBoostWrapper(CatBoostRegressor(**params), **kwargs)
            else:
                raise Exception(bundle.get("metrics_unsupported_target_type").format(target_type))
        else:
            if hasattr(estimator, "copy"):
                estimator_copy = estimator.copy()
            else:
                estimator_copy = deepcopy(estimator)
            kwargs["estimator"] = estimator_copy
            if isinstance(estimator, (CatBoostClassifier, CatBoostRegressor)):
                if cat_features is not None:
                    for cat_feature in cat_features:
                        if cat_feature not in x.columns:
                            logger.error(
                                f"Client cat_feature `{cat_feature}` not found in x columns: {x.columns.to_list()}"
                            )
                    estimator_copy.set_params(
                        cat_features=[x.columns.get_loc(cat_feature) for cat_feature in cat_features]
                    )
                estimator = CatBoostWrapper(**kwargs)
            else:
                try:
                    if isinstance(estimator, (LGBMClassifier, LGBMRegressor)):
                        estimator = LightGBMWrapper(**kwargs)
                    else:
                        logger.warning(
                            f"Unexpected estimator is used for metrics: {estimator}. "
                            "Default strategy for category features will be used"
                        )
                        estimator = OtherEstimatorWrapper(**kwargs)
                except ModuleNotFoundError:
                    logger.warning(
                        f"Unexpected estimator is used for metrics: {estimator}. "
                        "Default strategy for category features will be used"
                    )
                    estimator = OtherEstimatorWrapper(**kwargs)

        return estimator


class CatBoostWrapper(EstimatorWrapper):
    def __init__(
        self,
        estimator: Union[CatBoostClassifier, CatBoostRegressor],
        scorer: Callable,
        metric_name: str,
        multiplier: int,
        cv: BaseCrossValidator,
        target_type: ModelTaskType,
        groups: Optional[List[str]] = None,
        text_features: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        super(CatBoostWrapper, self).__init__(
            estimator,
            scorer,
            metric_name,
            multiplier,
            cv,
            target_type,
            groups=groups,
            text_features=text_features,
            logger=logger,
        )
        self.cat_features = None
        self.emb_features = None
        self.exclude_features = []

    def _prepare_to_fit(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, dict]:
        x, y, groups, params = super()._prepare_to_fit(x, y)

        # Find embeddings
        if hasattr(CatBoostClassifier, "get_embedding_feature_indices"):
            emb_pattern = r"(.+)_emb\d+"
            self.emb_features = [c for c in x.columns if re.match(emb_pattern, c) and is_numeric_dtype(x[c])]
            embedding_features = []
            if len(self.emb_features) > 3:  # There is no reason to reduce embeddings dimension with less than 4
                self.logger.info(
                    "Embedding features count more than 3, so group them into one vector for CatBoost: "
                    f"{self.emb_features}"
                )
                x, embedding_features = self.group_embeddings(x)
                params["embedding_features"] = embedding_features
            else:
                self.logger.info(f"Embedding features count less than 3, so use them separately: {self.emb_features}")
                self.emb_features = []
        else:
            self.logger.warning(f"Embedding features are not supported by Catboost version {catboost.__version__}")

        # Find text features from passed in generate_features
        if hasattr(CatBoostClassifier, "get_text_feature_indices"):
            if self.text_features is not None:
                self.logger.info(f"Passed text features for CatBoost: {self.text_features}")
                self.text_features = [f for f in self.text_features if f in x.columns and not is_numeric_dtype(x[f])]
                self.logger.info(f"Rest text features after checks: {self.text_features}")
                params["text_features"] = self.text_features
        else:
            self.text_features = None
            self.logger.warning(f"Text features are not supported by this Catboost version {catboost.__version__}")

        # Find rest categorical features
        self.cat_features = _get_cat_features(x, self.text_features, embedding_features)
        # x = fill_na_cat_features(x, self.cat_features)
        unique_cat_features = []
        for name in self.cat_features:
            # Remove constant categorical features
            if x[name].nunique() > 1:
                unique_cat_features.append(name)
            else:
                x = x.drop(columns=name)
        self.cat_features = unique_cat_features
        if (
            hasattr(self.estimator, "get_param")
            and hasattr(self.estimator, "_init_params")
            and self.estimator.get_param("cat_features") is not None
        ):
            estimator_cat_features = self.estimator.get_param("cat_features")
            if all([isinstance(c, int) for c in estimator_cat_features]):
                cat_features_idx = {x.columns.get_loc(c) for c in self.cat_features}
                cat_features_idx.update(estimator_cat_features)
                self.cat_features = [x.columns[idx] for idx in sorted(cat_features_idx)]
            elif all([isinstance(c, str) for c in estimator_cat_features]):
                self.cat_features = list(set(self.cat_features + estimator_cat_features))
            else:
                print(f"WARNING: Unsupported type of cat_features in CatBoost estimator: {estimator_cat_features}")

            del self.estimator._init_params["cat_features"]

        self.logger.info(f"Selected categorical features: {self.cat_features}")
        params["cat_features"] = self.cat_features

        return x, y, groups, params

    def group_embeddings(self, df: pd.DataFrame):
        emb_name = "__grouped_embeddings"
        df = df.copy()
        df[self.emb_features] = df[self.emb_features].fillna(0.0)
        df[emb_name] = df[self.emb_features].values.tolist()
        df = df.drop(columns=self.emb_features)

        return df, [emb_name]

    def _prepare_to_calculate(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, dict]:
        if self.exclude_features:
            x = x.drop(columns=self.exclude_features)
        x, y, params = super()._prepare_to_calculate(x, y)
        if self.text_features:
            params["text_features"] = self.text_features
        if self.emb_features:
            x, emb_columns = self.group_embeddings(x)
            params["embedding_features"] = emb_columns
        if self.cat_features:
            # x = fill_na_cat_features(x, self.cat_features)
            params["cat_features"] = self.cat_features

        return x, y, params

    def cross_val_predict(
        self, x: pd.DataFrame, y: np.ndarray, baseline_score_column: Optional[Any] = None
    ) -> Optional[float]:
        try:
            return super().cross_val_predict(x, y, baseline_score_column)
        except Exception as e:
            if "Dictionary size is 0" in e.args[0] and self.text_features:
                high_cardinality_features = FeaturesValidator.find_high_cardinality(x[self.text_features])
                if len(high_cardinality_features) == 0:
                    high_cardinality_features = self.text_features
                    self.logger.warning(
                        "Calculate metrics has problem with CatBoost text features. High cardinality features not found"
                        f". Try to remove all text features {high_cardinality_features} and retry"
                    )
                else:
                    self.logger.warning(
                        "Calculate metrics has problem with CatBoost text features. Try to remove high cardinality"
                        f" text features {high_cardinality_features} and retry"
                    )
                for f in high_cardinality_features:
                    self.text_features.remove(f)
                    self.exclude_features.append(f)
                    x = x.drop(columns=f, errors="ignore")
                return super().cross_val_predict(x, y, baseline_score_column)
            else:
                raise e


class LightGBMWrapper(EstimatorWrapper):
    def __init__(
        self,
        estimator,
        scorer: Callable,
        metric_name: str,
        multiplier: int,
        cv: BaseCrossValidator,
        target_type: ModelTaskType,
        groups: Optional[List[str]] = None,
        text_features: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        super(LightGBMWrapper, self).__init__(
            estimator,
            scorer,
            metric_name,
            multiplier,
            cv,
            target_type,
            groups=groups,
            text_features=text_features,
            logger=logger,
        )
        self.cat_features = None

    def _prepare_to_fit(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series, np.ndarray, dict]:
        x, y, groups, params = super()._prepare_to_fit(x, y)
        self.cat_features = _get_cat_features(x)
        x = fill_na_cat_features(x, self.cat_features)
        for feature in self.cat_features:
            x[feature] = x[feature].astype("category").cat.codes
        if not is_numeric_dtype(y):
            y = correct_string_target(y)

        return x, y, groups, params

    def _prepare_to_calculate(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, dict]:
        x, y, params = super()._prepare_to_calculate(x, y)
        if self.cat_features is not None:
            x = fill_na_cat_features(x, self.cat_features)
            for feature in self.cat_features:
                x[feature] = x[feature].astype("category").cat.codes
        if not is_numeric_dtype(y):
            y = correct_string_target(y)
        return x, y, params


class OtherEstimatorWrapper(EstimatorWrapper):
    def __init__(
        self,
        estimator,
        scorer: Callable,
        metric_name: str,
        multiplier: int,
        cv: BaseCrossValidator,
        target_type: ModelTaskType,
        groups: Optional[List[str]] = None,
        text_features: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        super(OtherEstimatorWrapper, self).__init__(
            estimator,
            scorer,
            metric_name,
            multiplier,
            cv,
            target_type,
            groups=groups,
            text_features=text_features,
            logger=logger,
        )
        self.cat_features = None

    def _prepare_to_fit(self, x: pd.DataFrame, y: np.ndarray) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, dict]:
        x, y, groups, params = super()._prepare_to_fit(x, y)
        self.cat_features = _get_cat_features(x)
        num_features = [col for col in x.columns if col not in self.cat_features]
        x[num_features] = x[num_features].fillna(-999)
        x = fill_na_cat_features(x, self.cat_features)
        # TODO use one-hot encoding if cardinality is less 50
        for feature in self.cat_features:
            x[feature] = x[feature].astype("category").cat.codes
        if not is_numeric_dtype(y):
            y = correct_string_target(y)
        return x, y, groups, params

    def _prepare_to_calculate(self, x: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, np.ndarray, dict]:
        x, y, params = super()._prepare_to_calculate(x, y)
        if self.cat_features is not None:
            num_features = [col for col in x.columns if col not in self.cat_features]
            x[num_features] = x[num_features].fillna(-999)
            x = fill_na_cat_features(x, self.cat_features)
            # TODO use one-hot encoding if cardinality is less 50
            for feature in self.cat_features:
                x[feature] = x[feature].astype("category").cat.codes
        if not is_numeric_dtype(y):
            y = correct_string_target(y)
        return x, y, params


def validate_scoring_argument(scoring: Union[Callable, str, None]):
    if isinstance(scoring, str) and scoring is not None:
        _get_scorer_by_name(scoring)
    elif isinstance(scoring, Callable):
        spec = inspect.getfullargspec(scoring)
        if len(spec.args) < 3:
            raise ValidationError(
                f"Invalid scoring function passed {scoring}. It should accept 3 input arguments: estimator, x, y"
            )
    elif scoring is not None:
        raise ValidationError(
            f"Invalid scoring argument passed {scoring}. It should be string with scoring name or function"
            " that accepts 3 input arguments: estimator, x, y"
        )


def _get_scorer_by_name(scoring: str) -> Tuple[Callable, str, int]:
    metric_name = scoring
    multiplier = 1
    if metric_name == "mean_squared_log_error" or metric_name == "MSLE" or metric_name == "msle":
        scoring = make_scorer(_ext_mean_squared_log_error, greater_is_better=False)
        multiplier = -1
    elif "root_mean_squared_log_error" in metric_name or metric_name == "RMSLE" or metric_name == "rmsle":
        scoring = make_scorer(_ext_root_mean_squared_log_error, greater_is_better=False)
        multiplier = -1
    elif metric_name == "root_mean_squared_error" or metric_name == "RMSE" or metric_name == "rmse":
        scoring = get_scorer("neg_root_mean_squared_error")
        multiplier = -1
    elif scoring in available_scorers:
        scoring = get_scorer(scoring)
    elif ("neg_" + scoring) in available_scorers:
        scoring = get_scorer("neg_" + scoring)
        multiplier = -1
    else:
        supported_metrics = set(available_scorers)
        neg_metrics = [m[4:] for m in supported_metrics if m.startswith("neg_")]
        supported_metrics.update(neg_metrics)
        supported_metrics.update(
            [
                "mean_squared_log_error",
                "MSLE",
                "msle",
                "root_mean_squared_log_error",
                "RMSLE",
                "rmsle",
                "root_mean_squared_error",
                "RMSE",
                "rmse",
            ]
        )
        raise ValidationError(bundle.get("metrics_invalid_scoring").format(scoring, sorted(supported_metrics)))
    return scoring, metric_name, multiplier


def _get_scorer(target_type: ModelTaskType, scoring: Union[Callable, str, None]) -> Tuple[Callable, str, int]:
    if scoring is None:
        if target_type == ModelTaskType.BINARY:
            scoring = "roc_auc"
        elif target_type == ModelTaskType.MULTICLASS:
            scoring = "accuracy"
        elif target_type == ModelTaskType.REGRESSION:
            scoring = "mean_squared_error"
        else:
            raise Exception(bundle.get("metrics_unsupported_target_type").format(target_type))

    multiplier = 1
    if isinstance(scoring, str):
        scoring, metric_name, multiplier = _get_scorer_by_name(scoring)
    elif hasattr(scoring, "__name__"):
        metric_name = scoring.__name__
    else:
        metric_name = str(scoring)

    return scoring, metric_name, multiplier


def _get_cat_features(
    x: pd.DataFrame, text_features: Optional[List[str]] = None, emb_features: Optional[List[str]] = None
) -> List[str]:
    text_features = text_features or []
    emb_features = emb_features or []
    exclude_features = text_features + emb_features
    return [c for c in x.columns if c not in exclude_features and not is_numeric_dtype(x[c])]


def _get_add_params(input_params, add_params):
    output_params = dict(input_params)
    if add_params is not None:
        output_params.update(add_params)

    return output_params


def _ext_root_mean_squared_log_error(y_true, y_pred, *, sample_weight=None, multioutput="uniform_average"):
    return _ext_mean_squared_log_error(
        y_true, y_pred, sample_weight=sample_weight, multioutput=multioutput, squared=False
    )


def _ext_mean_squared_log_error(y_true, y_pred, *, sample_weight=None, multioutput="uniform_average", squared=True):
    """Mean squared logarithmic error regression loss.

    Extended version with clip(0) for y_pred

    Read more in the :ref:`User Guide <mean_squared_log_error>`.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.

    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    multioutput : {'raw_values', 'uniform_average'} or array-like of shape \
            (n_outputs,), default='uniform_average'

        Defines aggregating of multiple output values.
        Array-like value defines weights used to average errors.

        'raw_values' :
            Returns a full set of errors when the input is of multioutput
            format.

        'uniform_average' :
            Errors of all outputs are averaged with uniform weight.
    squared : bool, default=True
        If True returns MSLE (mean squared log error) value.
        If False returns RMSLE (root mean squared log error) value.

    Returns
    -------
    loss : float or ndarray of floats
        A non-negative floating point value (the best value is 0.0), or an
        array of floating point values, one for each individual target.

    Examples
    --------
    >>> from sklearn.metrics import mean_squared_log_error
    >>> y_true = [3, 5, 2.5, 7]
    >>> y_pred = [2.5, 5, 4, 8]
    >>> mean_squared_log_error(y_true, y_pred)
    0.039...
    >>> mean_squared_log_error(y_true, y_pred, squared=False)
    0.199...
    >>> y_true = [[0.5, 1], [1, 2], [7, 6]]
    >>> y_pred = [[0.5, 2], [1, 2.5], [8, 8]]
    >>> mean_squared_log_error(y_true, y_pred)
    0.044...
    >>> mean_squared_log_error(y_true, y_pred, multioutput='raw_values')
    array([0.00462428, 0.08377444])
    >>> mean_squared_log_error(y_true, y_pred, multioutput=[0.3, 0.7])
    0.060...
    """
    _, y_true, y_pred, multioutput = _check_reg_targets(y_true, y_pred, multioutput)
    check_consistent_length(y_true, y_pred, sample_weight)

    if (y_true < 0).any():
        raise ValidationError(bundle.get("metrics_msle_negative_target"))

    return mean_squared_error(
        log1p(y_true),
        log1p(y_pred.clip(0)),
        sample_weight=sample_weight,
        multioutput=multioutput,
        squared=squared,
    )


def fill_na_cat_features(df: pd.DataFrame, cat_features: List[str]) -> pd.DataFrame:
    for c in cat_features:
        if c in df.columns:
            df[c] = df[c].astype("string").fillna(NA_REPLACEMENT).astype(str)
            na_filter = df[c].str.lower().isin(NA_VALUES)
            df.loc[na_filter, c] = NA_REPLACEMENT
    return df
