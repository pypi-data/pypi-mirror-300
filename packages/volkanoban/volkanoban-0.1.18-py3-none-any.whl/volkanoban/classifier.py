import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from lime.lime_tabular import LimeTabularExplainer
from sklearn.ensemble import StackingClassifier, VotingClassifier, RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
import plotly.express as px
from tabulate import tabulate
from explainerdashboard import ClassifierExplainer, ExplainerDashboard

class volkanobanClassifier:
    def __init__(self, base_learners=None, voting_model=None):
        if base_learners is None:
            self.base_learners = [
                ('random_forest', RandomForestClassifier(n_estimators=100, random_state=42)),
                ('xgboost', XGBClassifier(n_estimators=100, random_state=42)),
                ('lightgbm', lgb.LGBMClassifier(n_estimators=100, random_state=42)),
                ('catboost', CatBoostClassifier(iterations=100, random_state=42, verbose=0)),
                ('extra_trees', ExtraTreesClassifier(n_estimators=100, random_state=42)),
                ('mlp', MLPClassifier(max_iter=600, random_state=42)),
                ('bagging', BaggingClassifier(n_estimators=100, random_state=42)),
            ]
        else:
            self.base_learners = base_learners

        if voting_model is None:
            self.voting_model = VotingClassifier(estimators=self.base_learners, voting='soft')
        else:
            self.voting_model = voting_model

        self.stacking_model = StackingClassifier(estimators=self.base_learners, final_estimator=self.voting_model)

    def train(self, X, y, test_size=0.3, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        self.stacking_model.fit(X_train, y_train)
        return X_train, X_test, y_train, y_test
        
    def predict(self, X_test):
    # Test setindeki tüm örnekler için tahmin yap
        try:
            y_pred = self.stacking_model.predict(X_test)  # Tüm test seti üzerinden tahmin yapılıyor
            return y_pred  # Tüm tahminler döndürülüyor
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
            title='Feature Importance from  Model',
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
            get_ipython
            db.run(port=8051, host='localhost', mode='inline')
        except NameError:
            db.run(port=8051, host='localhost', mode='external')
