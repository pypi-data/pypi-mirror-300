
# volkanoban

`volkanobanClassifier` is a stacking classifier that combines several machine learning models, including Random Forest, XGBoost, LightGBM, CatBoost, and more. The package also includes advanced features such as explainability through LIME, feature importance visualization, and a model dashboard using `explainerdashboard`.

## Features

- **Stacking Classifier:** Combines multiple machine learning models to improve performance.
- **Voting Classifier:** Uses soft voting for final predictions.
- **Explainability:** Provides insights using LIME (Local Interpretable Model-agnostic Explanations).
- **Feature Importance:** Visualizes the importance of features from multiple models.
- **Interactive Dashboard:** Creates an interactive dashboard using `explainerdashboard` for better model understanding.

## Installation

You can install the package using pip:

```bash
pip install volkanoban
```

## Usage Example 1: Breast Cancer Dataset

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from volkanoban import volkanobanClassifier

# Load the breast cancer dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Initialize the volkanobanClassifier
classifier = volkanobanClassifier()

# Train the classifier
X_train, X_test, y_train, y_test = classifier.train(X, y)

# Predict on new data (tüm test verisi üzerinde)
y_pred = classifier.predict(X_test)

# Evaluate performance (model performansını değerlendir)
num_classes = len(np.unique(y_test))  # Test setindeki sınıf sayısını belirleyin
classifier.evaluate_performance(y_test, y_pred, num_classes)

# Perform LIME analysis (tek bir örnek üzerinde analiz)
feature_names = X.columns  # Özellik isimlerini al
class_names = [str(i) for i in np.unique(y)]  # Sınıf isimlerini belirle
classifier.lime_analysis(X_train, X_test, 0, feature_names, class_names)

# Plot feature importance (özellik önemini görselleştir)
classifier.plot_feature_importance(X.columns)

# Run the ExplainerDashboard (modelin açıklayıcı gösterge tablosunu çalıştır)
classifier.run_explainer_dashboard(X_train, X_test, y_test, feature_names)

```

## Usage Example 2: Forest Cover Type Dataset

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_covtype
from volkanoban import volkanobanClassifier

# Load the forest cover type dataset
data = fetch_covtype()
X = pd.DataFrame(data.data)  # Özellik matrisi
y = pd.Series(data.target)   # Hedef değişken

# Initialize the volkanobanClassifier
classifier = volkanobanClassifier()

# Train the classifier (veri setini eğit)
X_train, X_test, y_train, y_test = classifier.train(X, y)

# Predict on new data (tüm test verisi üzerinde tahmin yap)
y_pred = classifier.predict(X_test)

# Evaluate performance (model performansını değerlendir)
num_classes = len(np.unique(y_test))  # Test setindeki sınıf sayısını belirleyin
classifier.evaluate_performance(y_test, y_pred, num_classes)

# Perform LIME analysis (tek bir örnek üzerinde analiz)
feature_names = X.columns  # Özellik isimlerini al
class_names = [str(i) for i in np.unique(y)]  # Sınıf isimlerini belirle
classifier.lime_analysis(X_train, X_test, 0, feature_names, class_names)

# Plot feature importance (özellik önemini görselleştir)
classifier.plot_feature_importance(X.columns)

# Run the ExplainerDashboard (modelin açıklayıcı gösterge tablosunu çalıştır)
classifier.run_explainer_dashboard(X_train, X_test, y_test, feature_names)

```

## Usage Example 3: Wine Dataset (Multi-class Classification)

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from volkanoban import volkanobanClassifier

# Load the wine dataset
data = load_wine()
X = pd.DataFrame(data.data, columns=data.feature_names)  # Özellik matrisi
y = pd.Series(data.target)  # Hedef değişken

# Initialize the volkanobanClassifier
classifier = volkanobanClassifier()

# Train the classifier (veri setini eğit)
X_train, X_test, y_train, y_test = classifier.train(X, y)

# Predict on new data (tüm test verisi üzerinde tahmin yap)
y_pred = classifier.predict(X_test)

# Evaluate performance (model performansını değerlendir)
num_classes = len(np.unique(y_test))  # Test setindeki sınıf sayısını belirleyin
classifier.evaluate_performance(y_test, y_pred, num_classes)

# Perform LIME analysis (tek bir örnek üzerinde analiz)
feature_names = X.columns  # Özellik isimlerini al
class_names = [str(i) for i in np.unique(y)]  # Sınıf isimlerini belirle
classifier.lime_analysis(X_train, X_test, 0, feature_names, class_names)

# Plot feature importance (özellik önemini görselleştir)
classifier.plot_feature_importance(X.columns)

# Run the ExplainerDashboard (modelin açıklayıcı gösterge tablosunu çalıştır)
classifier.run_explainer_dashboard(X_train, X_test, y_test, feature_names)

```

## Predict Function Description

The `predict` function allows making predictions for new input data. It supports making predictions on unseen data and ensures the input data matches the expected features used by the model.

**Example Usage:**

```python
from volkanoban import volkanobanClassifier
import pandas as pd

# Example input features in dictionary form
input_data = {"feature_1": 1.5, "feature_2": 3.0, "feature_3": 2.1}

# Convert to DataFrame
df_input = pd.DataFrame([input_data])

# Predict the behavior
y_pred = classifier.predict(df_input)
print("Predicted behavior:", y_pred)
```

## Function Descriptions

### evaluate_performance

This function evaluates the model's performance using metrics like accuracy, precision, recall, F1 score, and confusion matrix. It prints a well-formatted table for easy interpretation.

**Arguments:**

- `y_true`: Ground truth labels.
- `y_pred`: Predicted labels by the model.
- `num_classes`: Number of unique classes in the dataset.

**Example Usage:**

```python
classifier.evaluate_performance(y_test, y_pred, num_classes)
```

### lime_analysis

This function generates a LIME explanation for a specific test instance, showing how individual features influence the model's prediction.

**Arguments:**

- `X_train`: The scaled training dataset.
- `X_test`: The scaled testing dataset.
- `index`: Index of the test instance to analyze.
- `feature_names`: List of feature names from the dataset.
- `class_names`: List of class names corresponding to the target variable.

**Example Usage:**

```python
classifier.lime_analysis(X_train, X_test, 0, feature_names, class_names)
```

### plot_feature_importance

This function visualizes feature importance across base models in the stacking classifier.

**Arguments:**

- `feature_names`: List of feature names from the dataset.

**Example Usage:**

```python
classifier.plot_feature_importance(feature_names)
```

### run_explainer_dashboard

This function launches an interactive dashboard using `explainerdashboard`, allowing exploration of the model's predictions, feature importance, and more.

**Arguments:**

- `X_train`: The scaled training dataset.
- `X_test`: The scaled testing dataset.
- `y_test`: Ground truth labels for the testing dataset.
- `feature_names`: List of feature names from the dataset.
- `dashboard_title`: Optional title for the dashboard.

**Example Usage:**

```python
classifier.run_explainer_dashboard(X_train, X_test, y_test, feature_names, dashboard_title="Model Explainer")
```
