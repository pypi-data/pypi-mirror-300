"""
Package overview
----------------

This module contains tunable scikit-learn classifier models with Optuna for hyperparameter optimization.

Each model is designed to extend the base class `SklearnTunable`, providing hyperparameter suggestions and
model building for scikit-learn classifiers.

- **AdaBoostTunable**: Implements the AdaBoost algorithm with tunable hyperparameters.
- **BaggingTunable**: Implements the Bagging algorithm with tunable hyperparameters.
- **BernoulliNaiveBayesTunable**: Implements the Bernoulli Naive Bayes algorithm with tunable hyperparameters.
- **ComplementNaiveBayesTunable**: Implements the Complement Naive Bayes algorithm with tunable hyperparameters.
- **DecisionTreeTunable**: Implements the Decision Tree algorithm with tunable hyperparameters.
- **ExtraTreesTunable**: Implements the Extra Trees (Extremely Randomized Trees) algorithm with tunable hyperparameters.
- **GaussianNaiveBayesTunable**: Implements the Gaussian Naive Bayes algorithm with tunable hyperparameters.
- **GradientBoostingTunable**: Implements the Gradient Boosting algorithm with tunable hyperparameters.
- **KNeighborsTunable**: Implements the K-Nearest Neighbors (KNN) algorithm with tunable hyperparameters.
- **LinearDiscriminantTunable**: Implements Linear Discriminant Analysis (LDA) with tunable hyperparameters.
- **MLPTunable**: Implements the Multi-layer Perceptron (MLP) classifier with tunable hyperparameters.
- **MultinomialNaiveBayesTunable**: Implements the Multinomial Naive Bayes algorithm with tunable hyperparameters.
- **QuadraticDiscriminantTunable**: Implements Quadratic Discriminant Analysis (QDA) with tunable hyperparameters.
- **RandomForestTunable**: Implements the Random Forest algorithm with tunable hyperparameters.

Each model utilizes Optuna to suggest hyperparameters during training, enabling automated optimization of the classifier's performance.
"""

from .AdaBoostTunable import AdaBoostTunable
from .BaggingTunable import BaggingTunable
from .BernoulliNaiveBayesTunable import BernoulliNaiveBayesTunable
from .ComplementNaiveBayesTunable import ComplementNaiveBayesTunable
from .DecisionTreeTunable import DecisionTreeTunable
from .ExtraTreesTunable import ExtraTreesTunable
from .GaussianNaiveBayesTunable import GaussianNaiveBayesTunable
from .GradientBoostingTunable import GradientBoostingTunable
from .KNeighborsTunable import KNeighborsTunable
from .LinearDiscriminantTunable import LinearDiscriminantTunable
from .MLPTunable import MLPTunable
from .MultinomialNaiveBayesTunable import MultinomialNaiveBayesTunable
from .QuadraticDiscriminantTunable import QuadraticDiscriminantTunable
from .RandomForestTunable import RandomForestTunable
