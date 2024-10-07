import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, matthews_corrcoef, roc_auc_score, roc_curve, auc
from lime.lime_tabular import LimeTabularExplainer
from sklearn.ensemble import StackingClassifier, VotingClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from pytorch_tabnet.tab_model import TabNetClassifier
import plotly.express as px
import shap
import torch
from tabulate import tabulate
from explainerdashboard import ClassifierExplainer, ExplainerDashboard

class volkanobanClassifier:
    def __init__(self, base_learners=None, voting_model=None):
        if base_learners is None:
            self.base_learners = [
                # RandomForest with reduced depth to prevent overfitting
                ('random_forest', RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5, random_state=42)),

                # XGBoost with regularization, reduced tree depth, and subsampling
                ('xgboost', XGBClassifier(n_estimators=100, max_depth=6, reg_alpha=0.5, reg_lambda=1, 
                                          subsample=0.8, colsample_bytree=0.8, learning_rate=0.05, random_state=42)),

                # LightGBM with regularization, reduced tree depth, and subsampling
                ('lightgbm', lgb.LGBMClassifier(n_estimators=100, max_depth=6, reg_alpha=0.5, reg_lambda=1, 
                                                subsample=0.8, colsample_bytree=0.8, learning_rate=0.05, random_state=42)),

                # CatBoost with reduced depth and learning rate
                ('catboost', CatBoostClassifier(iterations=100, depth=6, learning_rate=0.05, random_state=42, verbose=0)),

                # ExtraTrees with limited depth
                ('extra_trees', ExtraTreesClassifier(n_estimators=100, max_depth=10, random_state=42)),

                # MLPClassifier with regularization (alpha) and early stopping
                ('mlp', MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=1000, alpha=0.0001, early_stopping=True, validation_fraction=0.1, random_state=42)),

                # BaggingClassifier
                ('bagging', BaggingClassifier(n_estimators=100, random_state=42)),

                # HistGradientBoostingClassifier with limited depth
                ('hist_gradient_boosting', HistGradientBoostingClassifier(max_depth=10, random_state=42)),
            ]
        else:
            self.base_learners = base_learners

        if voting_model is None:
            self.voting_model = VotingClassifier(estimators=self.base_learners, voting='soft')
        else:
            self.voting_model = voting_model

        self.stacking_model = StackingClassifier(estimators=self.base_learners, final_estimator=self.voting_model)

    def preprocess_data(self, X, imputation_strategy='mean'):
        # Handle missing values using SimpleImputer or KNNImputer
        if imputation_strategy == 'knn':
            imputer = KNNImputer()
        else:
            imputer = SimpleImputer(strategy=imputation_strategy)
        
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
        X = pd.get_dummies(X, drop_first=True)  # One-hot encoding for categorical features
        return X

    def train(self, X, y, test_size=0.3, random_state=42, imputation_strategy='mean'):
        X = self.preprocess_data(X, imputation_strategy=imputation_strategy)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # Split the training data into training and validation sets for gradient-based models
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=random_state)

        # Check if any gradient-based model (MLP) requires scaling
        should_scale = any(isinstance(estimator, MLPClassifier) for _, estimator in self.base_learners)

        if should_scale:
            print("Scaling applied for gradient-based models (MLP).")
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            X_test = scaler.transform(X_test)
        else:
            print("Scaling not required for tree-based models (XGBoost, LightGBM).")

        # Train individual models (without early stopping, but with regularization and other overfitting prevention)
        for name, estimator in self.base_learners:
            estimator.fit(X_train, y_train)

        # Train the stacking model on top of the base learners
        self.stacking_model.fit(X_train, y_train)

        return X_train, X_test, y_train, y_test

    def predict(self, X_test):
        try:
            y_pred = self.stacking_model.predict(X_test)
            return y_pred
        except Exception as e:
            return {"detail": f"Prediction error: {repr(e)}"}


    def evaluate_performance(self, y_true, y_pred, num_classes):
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        precision_per_class = precision_score(y_true, y_pred, average=None)
        recall_per_class = recall_score(y_true, y_pred, average=None)
        f1_per_class = f1_score(y_true, y_pred, average=None)

        print(f"\nAccuracy: {accuracy:.4f}\n")
        
        cm_headers = [f"Predicted {i}" for i in range(num_classes)]
        cm_table = tabulate(cm, headers=cm_headers, tablefmt="fancy_grid", showindex="always", numalign="center")
        print("Confusion Matrix:")
        print(cm_table)

        metrics_table = [
            [f"Class {i}", f"{prec:.4f}", f"{rec:.4f}", f"{f1:.4f}"]
            for i, (prec, rec, f1) in enumerate(zip(precision_per_class, recall_per_class, f1_per_class))
        ]
        metrics_table = tabulate(metrics_table, headers=["Class", "Precision", "Recall", "F1 Score"], tablefmt="fancy_grid")
        print("\nPerformance Metrics:")
        print(metrics_table)

    def plot_roc_curve(self, y_true, y_pred_proba):
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        fig = px.area(
            x=fpr, y=tpr,
            title=f'ROC Curve (AUC = {roc_auc:.4f})',
            labels=dict(x='False Positive Rate', y='True Positive Rate'),
            width=700, height=500
        )
        fig.show()

    def extra_metrics(self, y_true, y_pred):
        mcc = matthews_corrcoef(y_true, y_pred)
        roc_auc = roc_auc_score(y_true, y_pred)
        print(f"Matthews Correlation Coefficient: {mcc:.4f}")
        print(f"ROC AUC Score: {roc_auc:.4f}")

    def lime_analysis(self, X_train, X_test, index, feature_names, class_names):
        explainer = LimeTabularExplainer(
            training_data=X_train,
            mode="classification",
            feature_names=feature_names,
            class_names=class_names,
            discretize_continuous=True
        )
        exp = explainer.explain_instance(X_test[index], self.stacking_model.predict_proba, num_features=10)
        exp.show_in_notebook(show_table=True)


    def plot_feature_importance(self, feature_names):
        feature_importance_dict = {}

        for name, estimator in self.stacking_model.named_estimators_.items():
            if hasattr(estimator, 'feature_importances_'):
                importance = estimator.feature_importances_
                feature_importance_dict[name] = importance

        total_importance = np.sum(list(feature_importance_dict.values()), axis=0)
        importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': total_importance})
        importance_df = importance_df.sort_values(by='Importance', ascending=False)

        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance from Model',
            text='Importance',
            color='Importance',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_title='Features', 
            xaxis_title='Importance',
            yaxis=dict(tickfont=dict(size=6)),
            showlegend=False,
            title_font=dict(size=24),
            xaxis_title_font=dict(size=18),
            yaxis_title_font=dict(size=18),
            font=dict(size=14),
            height=600,
            width=900
        )
        fig.show()
    def run_explainer_dashboard(self, X_train, X_test, y_test, feature_names, dashboard_title="Model Explainer"):
        if isinstance(X_test, np.ndarray):
            X_test = pd.DataFrame(X_test, columns=feature_names)
        
        explainer = ClassifierExplainer(self.stacking_model, X_test, y_test, model_output='logodds')
        db = ExplainerDashboard(explainer, title=dashboard_title, shap_interaction=False)

        try:
            # This checks if the code is running in an IPython environment (like Jupyter Notebook)
            if get_ipython():
                db.run(port=8051, host='localhost', mode='inline')  # Run inline if in IPython
        except NameError:
            # If not in IPython, run in a separate browser tab
            db.run(port=8051, host='localhost', mode='external')

    def cross_validate(self, X, y, cv=5):
        scores = cross_val_score(self.stacking_model, X, y, cv=cv)
        print(f"Cross-Validation Scores: {scores}")
        print(f"Mean Accuracy: {np.mean(scores):.4f}")

    # Hiperparametre tuning fonksiyonu
    def hyperparameter_tuning(self, X, y):
        param_grid = {
            'random_forest__n_estimators': [100, 200],
            'xgboost__max_depth': [3, 6, 9],
        }
        
        grid_search = GridSearchCV(estimator=self.stacking_model, param_grid=param_grid, cv=5)
        grid_search.fit(X, y)
        print(f"Best parameters found: {grid_search.best_params_}")
