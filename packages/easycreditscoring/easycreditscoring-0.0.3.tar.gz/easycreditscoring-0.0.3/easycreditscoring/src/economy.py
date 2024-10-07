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


class UnitEconomy:
    """
    Clients with Poor credit score are rejected (i.e. no loan is issued).
    Depending on the correctness of risk evaluation each approved client results in the given profit or loss in arbitrary currency units (ACU):

    - Poor client evaluated as Standard yields loss of ACU 200.
    - Poor client evaluated as Good yields loss of ACU 400.

    - Standard client evaluated as Standard yields profit of ACU 50.
    - Standard client evaluated as Good yields profit of ACU 30.

    - Good client evaluated as Standard yields profit of ACU 70.
    - Good client evaluated as Good yields profit of ACU 100.

    - Each client evaluation regardless of outcome costs ACU 5.
    """

    def __init__(self, **kwargs):
        self.eval_cost = kwargs["eval_cost"]
        self.poor_as_standard = kwargs["poor_as_standard"]
        self.poor_as_good = kwargs["poor_as_good"]
        self.standard_as_standard = kwargs["standard_as_standard"]
        self.standard_as_good = kwargs["standard_as_good"]
        self.good_as_standard = kwargs["good_as_standard"]
        self.good_as_good = kwargs["good_as_good"]

        """
        COST-BENEFIT MATRIX:

        Actual type | Evaluated as Poor | Evaluated as Standard | Evaluated as Good
        ___________________________________________________________________________

        Poor        |        -5         |       -5-200          |      -5-400
        ___________________________________________________________________________

        Standard    |        -5         |       -5+50           |      -5+30
        ___________________________________________________________________________

        Good        |        -5         |       -5+70           |      -5+100
        ___________________________________________________________________________        
        """

        self.cost_benefit_matrix = np.array(
            [[-self.eval_cost, -self.eval_cost + self.poor_as_standard, -self.eval_cost + self.poor_as_good],
             [-self.eval_cost, -self.eval_cost + self.standard_as_standard, -self.eval_cost + self.standard_as_good],
             [-self.eval_cost, -self.eval_cost + self.good_as_standard, -self.eval_cost + self.good_as_good]])

    # NumPy version of custom loss function
    def custom_loss_np(self, Y_true, Y_pred):
        """
        Custom loss function to compute the profit or loss based on the cost-benefit matrix using NumPy.

        Args:
        Y_true: true class labels as a NumPy array (0 = Poor, 1 = Standard, 2 = Good)
        Y_pred: predicted class probabilities as a NumPy array (shape: [n_samples, n_classes])

        Returns:
        A scalar representing the average loss across all examples.
        """

        # Ensure Y_true is an integer array
        Y_true = np.squeeze(Y_true.astype(int))

        # Create one-hot encoding for true labels
        Y_true_one_hot = np.eye(len(self.cost_benefit_matrix))[Y_true]

        # Calculate expected loss
        expected_loss = np.sum(Y_pred * np.dot(Y_true_one_hot, self.cost_benefit_matrix), axis=1)

        return -np.mean(expected_loss)

    # TensorFlow version of custom loss function
    def custom_loss_tf(self, Y_true, Y_pred):
        """
        Custom loss function to compute the profit or loss based on the cost-benefit matrix.

        Args:
        Y_true: true class labels (0 = Poor, 1 = Standard, 2 = Good)
        Y_pred: predicted class probabilities or labels

        Returns:
        A scalar representing the total loss across all examples.
        """

        cost_benefit = tf.constant(self.cost_benefit_matrix, dtype=tf.float32)

        # Get the predicted class by taking the argmax (index of the highest probability)
        Y_pred_labels = tf.argmax(Y_pred, axis=1, output_type=tf.int32)

        # Ensure y_true is an integer tensor
        Y_true = tf.squeeze(tf.cast(Y_true, tf.int32))
        Y_true_one_hot = tf.one_hot(Y_true, depth=3)

        # Stack y_true and y_pred_labels into pairs: shape (batch_size, 2)
        indices = tf.stack([Y_true, Y_pred_labels], axis=1)

        expected_loss = tf.reduce_sum(Y_pred * tf.matmul(Y_true_one_hot, cost_benefit), axis=1)
        expected_loss = tf.cast(expected_loss, tf.float32)

        return -tf.reduce_mean(expected_loss)