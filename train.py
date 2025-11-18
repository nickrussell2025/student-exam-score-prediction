import pickle

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def prepare_data(df):
    """
    Takes dataframe, shares key info & completes basic transformations
    """

    df = df.copy()

    print(f"dataset shape: {df.shape}")
    print(f"total duplicates: {df.duplicated().sum()}")
    print(f"total null values: {df.isnull().sum()}")

    # change column names to lowercase and remove spaces
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    print(f"column names: {df.columns}")

    # remove spaces in object columns
    strings = list(df.dtypes[df.dtypes == "object"].index)

    # drop empty columns
    df = df.dropna()

    for col in strings:
        df[col] = df[col].str.lower().str.replace(" ", "_")

    # sort features into categorical & numerical based on data type
    categorical = []
    numerical = []

    for col in df.columns:
        if df[col].dtype == "object":
            categorical.append(col)
        elif df[col].dtype == "int64":
            numerical.append(col)

    return categorical, numerical, df


def create_framework(df):
    """
    Takes dataframe, shares key info & completes basic transformations
    """

    df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
    df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)

    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    y_train = df_train.exam_score.values
    y_val = df_val.exam_score.values
    y_test = df_test.exam_score.values

    del df_train["exam_score"]
    del df_val["exam_score"]
    del df_test["exam_score"]

    print(
        f"training/validation/testing length: {len(df_train)}/{len(df_val)}/{len(df_test)}"
    )

    return df_full_train, df_train, df_val, df_test, y_train, y_val, y_test


def encode_features(df_train, df_val, df_test):
    """
    One-hot encode categorical features, keep numerical as-is
    """

    # convert to dictionaries
    train_dicts = df_train.to_dict(orient="records")
    val_dicts = df_val.to_dict(orient="records")
    test_dicts = df_test.to_dict(orient="records")

    # fit encoder on training data
    dv = DictVectorizer(sparse=False)
    dv.fit(train_dicts)

    # transform all datasets
    X_train = dv.transform(train_dicts)
    X_val = dv.transform(val_dicts)
    X_test = dv.transform(test_dicts)

    print(f"Original df_train shape: {df_train.shape}")
    print(f"Encoded X_train shape: {X_train.shape}")
    print(f"\nFeature names (first 20): {dv.get_feature_names_out()[:20]}")

    return dv, X_train, X_val, X_test


# Main training script
if __name__ == "__main__":
    # Load data
    df = pd.read_csv("./data/StudentPerformanceFactors.csv")

    # Prepare
    categorical, numerical, df = prepare_data(df)

    # Split
    df_full_train, df_train, df_val, df_test, y_train, y_val, y_test = create_framework(
        df
    )

    # Encode
    dv, X_train, X_val, X_test = encode_features(df_train, df_val, df_test)

    # Train linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("dv.pkl", "wb") as f:
        pickle.dump(dv, f)

    print("Model trained and saved!")
