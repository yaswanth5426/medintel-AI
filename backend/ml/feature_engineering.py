import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

def load_dataset(dataset_path):
    """
    Loads a CSV dataset.

    Parameters:
        dataset_path (str): Path to the dataset.

    Returns:
        pandas.DataFrame
    """

    df = pd.read_csv(dataset_path)

    return df

def clean_data(df):
    """
    Cleans missing values and unnecessary spaces.
    """

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces from string values
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Fill missing values
    for col in df.columns:

        if df[col].dtype == "object":

            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mode()[0])

        else:

            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())

    return df    

def encode_features(df):
    """
    Encodes categorical features using LabelEncoder.
    """

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

    return df  

def scale_features(X):
    """
    Scales numerical features using StandardScaler.
    """

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler  
    
def prepare_features(df, target_column):
    """
    Complete preprocessing pipeline.
    """

    df = clean_data(df)

    df = encode_features(df)

    X = df.drop(target_column, axis=1)

    y = df[target_column]

    X, scaler = scale_features(X)

    return X, y, scaler        