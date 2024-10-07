import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,BatchNormalization
from tensorflow.keras.optimizers import Adam, Nadam, AdamW
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.optimizers import SGD

import numpy as np
import pandas as pd
import seaborn as sns
import missingno
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import time
import re

# Pre-Processing
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, cross_validate
from sklearn.impute import KNNImputer
from sklearn.neighbors import LocalOutlierFactor
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.inspection import permutation_importance
from sklearn.utils.fixes import parse_version
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import CategoricalNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_auc_score

from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score


# Metrics
from sklearn.metrics import multilabel_confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score
from sklearn.metrics import RocCurveDisplay

from abc import ABC, abstractmethod

class Ensembling:

    def __init__(self, model_zoo, base_models, model_list=["LogRegression"]):
        self.model_list = model_list
        self.base_models = base_models
        self.model_zoo = model_zoo

    def runEnsemble(self,performance,shape):
        result = []

        Y_preds = []
        for model_name in self.model_list:
            model = self.base_models[model_name](performance=performance,shape=shape)

            start = time.time()
            model = self.model_zoo.model_fit(model)
            Y_pred, Y_pred_classes = self.model_zoo.model_predict(model)
            end = time.time()

            Y_preds.append(Y_pred)
            result.append({"Model": model_name,
                           "Class_probabilities": Y_pred,
                           "Classes": Y_pred_classes,
                           "Elapsed_Time": end - start,
                           })

        # Averaging results
        Y_pred = np.mean(Y_preds, axis=0)
        Y_pred_df = pd.DataFrame(Y_pred)
        Y_pred_df["grade"] = Y_pred_df.idxmax(axis=1)
        Y_pred_classes = Y_pred_df["grade"]

        return Y_pred, Y_pred_classes, result
