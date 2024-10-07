import os
import argparse  # Ensure argparse is imported

def create_ml_project_structure(project_name):
    """Create a machine learning project folder structure with specified code files."""
    # Define the folder structure and corresponding code
    folder_structure = {
        "Data_Preprocessing": {
            "basic_data_inspection.py": """import pandas as pd

class BasicDataInspection:
    \"\"\"
    Class for basic data inspection.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def inspect(self):
        \"\"\"
        Print basic info about the dataframe.
        \"\"\"
        print(self.df.info())
        print(self.df.describe())
        print(self.df.isnull().sum())
""",
            "univariate_data_analysis.py": """import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class UnivariateDataAnalysis:
    \"\"\"
    Class for performing univariate data analysis.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def analyze(self):
        \"\"\"
        Analyze each numerical column's distribution.
        \"\"\"
        for column in self.df.select_dtypes(include=['float64', 'int64']).columns:
            plt.figure(figsize=(10, 4))
            sns.histplot(self.df[column], kde=True)
            plt.title(f'Distribution of {column}')
            plt.show()
""",
            "multivariate_data_analysis.py": """import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class MultivariateDataAnalysis:
    \"\"\"
    Class for performing multivariate data analysis.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def analyze(self):
        \"\"\"
        Analyze correlations between features.
        \"\"\"
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
""",
            "missing_data_handling.py": """import pandas as pd

class MissingDataHandling:
    \"\"\"
    Class for handling missing data in the DataFrame.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def fill_missing(self, method='mean'):
        \"\"\"
        Fill missing values using specified method.
        
        :param method: Method to fill missing values ('mean', 'median', 'mode')
        \"\"\"
        if method == 'mean':
            self.df.fillna(self.df.mean(), inplace=True)
        elif method == 'median':
            self.df.fillna(self.df.median(), inplace=True)
        elif method == 'mode':
            self.df.fillna(self.df.mode().iloc[0], inplace=True)
        return self.df
""",
            "feature_scaling.py": """import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class FeatureScaling:
    \"\"\"
    Class for feature scaling using normalization and standardization.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def normalize(self):
        \"\"\"
        Normalize the features using Min-Max Scaling.
        
        :return: Normalized DataFrame
        \"\"\"
        scaler = MinMaxScaler()
        return pd.DataFrame(scaler.fit_transform(self.df), columns=self.df.columns)

    def standardize(self):
        \"\"\"
        Standardize the features using Z-score scaling.
        
        :return: Standardized DataFrame
        \"\"\"
        scaler = StandardScaler()
        return pd.DataFrame(scaler.fit_transform(self.df), columns=self.df.columns)
""",
            "categorical_encoding.py": """import pandas as pd

class CategoricalEncoding:
    \"\"\"
    Class for encoding categorical variables.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def one_hot_encode(self, columns):
        \"\"\"
        Apply one-hot encoding to specified columns.
        
        :param columns: List of columns to encode
        :return: DataFrame with encoded columns
        \"\"\"
        return pd.get_dummies(self.df, columns=columns, drop_first=True)

    def label_encode(self, column):
        \"\"\"
        Apply label encoding to a specified column.
        
        :param column: Column to encode
        :return: DataFrame with encoded column
        \"\"\"
        self.df[column] = self.df[column].astype('category').cat.codes
        return self.df
""",
            "outlier_detection.py": """import pandas as pd

class OutlierDetection:
    \"\"\"
    Class for detecting outliers in the dataset.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def z_score_method(self, threshold=3):
        \"\"\"
        Detect outliers using Z-score method.
        
        :param threshold: Z-score threshold for detecting outliers
        :return: DataFrame with outliers removed
        \"\"\"
        z_scores = (self.df - self.df.mean()) / self.df.std()
        return self.df[(z_scores < threshold).all(axis=1)]

    def iqr_method(self):
        \"\"\"
        Detect outliers using IQR method.
        
        :return: DataFrame with outliers removed
        \"\"\"
        Q1 = self.df.quantile(0.25)
        Q3 = self.df.quantile(0.75)
        IQR = Q3 - Q1
        return self.df[~((self.df < (Q1 - 1.5 * IQR)) | (self.df > (Q3 + 1.5 * IQR))).any(axis=1)]
""",
            "feature_engineering.py": """import pandas as pd

class FeatureEngineering:
    \"\"\"
    Class for creating new features from existing ones.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def create_feature(self, new_feature_name, feature1, feature2):
        \"\"\"
        Create a new feature as the sum of two existing features.
        
        :param new_feature_name: Name for the new feature
        :param feature1: First feature to combine
        :param feature2: Second feature to combine
        \"\"\"
        self.df[new_feature_name] = self.df[feature1] + self.df[feature2]
        return self.df
""",
            "feature_selection.py": """import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

class FeatureSelection:
    \"\"\"
    Class for selecting features using various methods.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def recursive_feature_elimination(self, target: pd.Series):
        \"\"\"
        Perform Recursive Feature Elimination (RFE).
        
        :param target: Target variable
        :return: Selected features
        \"\"\"
        model = LinearRegression()
        rfe = RFE(model)
        rfe.fit(self.df, target)
        return self.df.columns[rfe.support_].tolist()
""",
            "dimensionality_reduction.py": """import pandas as pd
from sklearn.decomposition import PCA

class DimensionalityReduction:
    \"\"\"
    Class for reducing dimensionality using PCA.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def apply_pca(self, n_components=2):
        \"\"\"
        Apply PCA to reduce dimensions.
        
        :param n_components: Number of principal components to keep
        :return: Reduced DataFrame
        \"\"\"
        pca = PCA(n_components=n_components)
        reduced_df = pd.DataFrame(pca.fit_transform(self.df), columns=[f'PC{i+1}' for i in range(n_components)])
        return reduced_df
""",
            "data_balancing.py": """import pandas as pd
from imblearn.over_sampling import SMOTE

class DataBalancing:
    \"\"\"
    Class for handling data imbalance using SMOTE and other methods.
    \"\"\"
    def __init__(self, df: pd.DataFrame, target: pd.Series):
        \"\"\"
        Initialize with a pandas DataFrame and target variable.
        
        :param df: Input dataframe
        :param target: Target variable
        \"\"\"
        self.df = df
        self.target = target

    def smote(self):
        \"\"\"
        Apply SMOTE to balance the classes.
        
        :return: Balanced DataFrame and target
        \"\"\"
        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(self.df, self.target)
        return pd.DataFrame(X_resampled, columns=self.df.columns), y_resampled
""",
            "data_augmentation.py": """import pandas as pd
from sklearn.utils import resample

class DataAugmentation:
    \"\"\"
    Class for augmenting data using resampling methods.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def augment(self, target: str):
        \"\"\"
        Augment data by oversampling the minority class.
        
        :param target: Target variable
        :return: Augmented DataFrame
        \"\"\"
        majority = self.df[self.df[target] == 0]
        minority = self.df[self.df[target] == 1]
        minority_upsampled = resample(minority, 
                                      replace=True,     
                                      n_samples=len(majority),    
                                      random_state=42)
        return pd.concat([majority, minority_upsampled])
""",
        },
        "Model_Training": {
            "model_training.py": """import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class ModelTraining:
    \"\"\"
    Class for training and evaluating models.
    \"\"\"
    def __init__(self, df: pd.DataFrame, target: str):
        \"\"\"
        Initialize with a pandas DataFrame and target variable.
        
        :param df: Input dataframe
        :param target: Target variable
        \"\"\"
        self.df = df
        self.target = target

    def train(self, test_size=0.2, random_state=42):
        \"\"\"
        Train the model and return evaluation report.
        
        :param test_size: Proportion of data to be used for testing
        :param random_state: Random seed for reproducibility
        :return: Classification report
        \"\"\"
        X = self.df.drop(columns=[self.target])
        y = self.df[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return classification_report(y_test, y_pred)
""",
            "hyperparameter_tuning.py": """import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

class HyperparameterTuning:
    \"\"\"
    Class for hyperparameter tuning using Grid Search.
    \"\"\"
    def __init__(self, df: pd.DataFrame, target: str):
        \"\"\"
        Initialize with a pandas DataFrame and target variable.
        
        :param df: Input dataframe
        :param target: Target variable
        \"\"\"
        self.df = df
        self.target = target

    def tune(self):
        \"\"\"
        Perform hyperparameter tuning and return the best parameters.
        
        :return: Best parameters
        \"\"\"
        X = self.df.drop(columns=[self.target])
        y = self.df[self.target]

        model = RandomForestClassifier()
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10]
        }

        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', cv=3)
        grid_search.fit(X, y)
        return grid_search.best_params_
""",
            "model_evaluation.py": """import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score

class ModelEvaluation:
    \"\"\"
    Class for evaluating model performance.
    \"\"\"
    def __init__(self, y_true, y_pred):
        \"\"\"
        Initialize with true and predicted values.
        
        :param y_true: True labels
        :param y_pred: Predicted labels
        \"\"\"
        self.y_true = y_true
        self.y_pred = y_pred

    def evaluate(self):
        \"\"\"
        Evaluate the model performance and return metrics.
        
        :return: Confusion matrix and accuracy
        \"\"\"
        cm = confusion_matrix(self.y_true, self.y_pred)
        accuracy = accuracy_score(self.y_true, self.y_pred)
        return cm, accuracy
""",
            "model_saving.py": """import joblib

class ModelSaving:
    \"\"\"
    Class for saving and loading models.
    \"\"\"
    def __init__(self, model, filename):
        \"\"\"
        Initialize with a model and filename for saving.
        
        :param model: Model to be saved
        :param filename: Filename for saving the model
        \"\"\"
        self.model = model
        self.filename = filename

    def save_model(self):
        \"\"\"
        Save the model to a file.
        \"\"\"
        joblib.dump(self.model, self.filename)

    def load_model(self):
        \"\"\"
        Load the model from a file.
        
        :return: Loaded model
        \"\"\"
        return joblib.load(self.filename)
""",
        },
        "Model_Deployment": {
            "model_deployment.py": """import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

class ModelDeployment:
    \"\"\"
    Class for deploying the model using Flask.
    \"\"\"
    def __init__(self, model_filename):
        \"\"\"
        Initialize with the model filename.
        
        :param model_filename: Filename of the saved model
        \"\"\"
        self.model = joblib.load(model_filename)

    def predict(self, input_data):
        \"\"\"
        Make predictions using the model.
        
        :param input_data: Input data for prediction
        :return: Prediction result
        \"\"\"
        prediction = self.model.predict([input_data])
        return prediction

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    model_deployment = ModelDeployment('model_filename.pkl')  # Change this to your model file
    prediction = model_deployment.predict(input_data)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
""",
        },
        "Visualization": {
            "data_visualization.py": """import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataVisualization:
    \"\"\"
    Class for visualizing data.
    \"\"\"
    def __init__(self, df: pd.DataFrame):
        \"\"\"
        Initialize with a pandas DataFrame.
        
        :param df: Input dataframe
        \"\"\"
        self.df = df

    def plot_correlation_matrix(self):
        \"\"\"
        Plot the correlation matrix.
        \"\"\"
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.df.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()

    def plot_histograms(self):
        \"\"\"
        Plot histograms for each numerical column.
        \"\"\"
        self.df.hist(figsize=(12, 10), bins=30)
        plt.tight_layout()
        plt.show()
""",
            "model_performance_visualization.py": """import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

class ModelPerformanceVisualization:
    \"\"\"
    Class for visualizing model performance metrics.
    \"\"\"
    def __init__(self, y_true, y_pred):
        \"\"\"
        Initialize with true and predicted values.
        
        :param y_true: True labels
        :param y_pred: Predicted labels
        \"\"\"
        self.y_true = y_true
        self.y_pred = y_pred

    def plot_confusion_matrix(self):
        \"\"\"
        Plot the confusion matrix.
        \"\"\"
        cm = confusion_matrix(self.y_true, self.y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.show()
""",
        },
        "Documentation": {
            "README.md": """# Project Title

## Description
A brief description of the project.

## Installation
Instructions for installing the necessary packages.

## Usage
How to use the code in the project.

## License
This project is licensed under the GNU General Public License v3 (GPLv3).
""",
            "requirements.txt": """pandas
numpy
scikit-learn
seaborn
matplotlib
flask
imblearn
joblib
""",
        },
    }

    # Create project directory
    os.makedirs(project_name, exist_ok=True)

    # Create folders and files
    for folder, files in folder_structure.items():
        folder_path = os.path.join(project_name, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file_name, content in files.items():
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as file:
                file.write(content.strip())

                
    # Create setup.py file
    setup_file_path = os.path.join(project_name, 'setup.py')
    setup_file_content = """from setuptools import find_packages, setup

setup(
    name='sensor',
    version='0.0.1',
    author='YOUR_NAME_HERE',
    author_email='YOUR_EMAIL_HERE',
    packages=find_packages(),
    install_requires=['pymongo']
)
"""
    with open(setup_file_path, 'w') as setup_file:
        setup_file.write(setup_file_content)

    # Create __init__.py file
    init_file_path = os.path.join(project_name, '__init__.py')
    with open(init_file_path, 'w') as init_file:
        init_file.write("# This is the init file for the project.")

    print(f"Project '{project_name}' structure created successfully.")

def main():
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Create a machine learning project structure.')
    parser.add_argument('project_name', type=str, nargs='?', help='The name of the project to create')
    args = parser.parse_args()

    # Prompt for project name if not provided
    if not args.project_name:
        args.project_name = input("Enter the project name: ")

    create_ml_project_structure(args.project_name)

if __name__ == "__main__":
    main()