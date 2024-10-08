"""
This module contains tunable neural network architectures designed for graph-based learning tasks, 
particularly for graph classification.

The models utilize various types of graph convolutional layers, allowing users to experiment with 
different architectures and hyperparameters to achieve optimal performance. The architectures are 
highly customizable. Hyperparameter tuning is facilitated using Optuna to tailor the models for specific 
tasks or datasets.

Each neural network architecture supports the some features for example:
- **Activation Functions**: Customizable activation layers such as ReLU, LeakyReLU, and GELU.
- **Dropout Regularization**: Dropout layers to prevent overfitting during training.
- **Hyperparameter Optimization**: Integrated Optuna support for automatic hyperparameter tuning, including the ability to tune the number of layers, hidden channels, attention heads (if applicable), learning rate, and batch size.

These flexible and tunable architectures are suitable for a wide range of applications involving graph-structured data, offering versatility for research and industry-focused projects.
"""
