import os
import time
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# -----------------------------
# Columns
# -----------------------------

CATEGORICAL_COLUMNS = [
    "education",
    "employmenttype",
    "maritalstatus",
    "hasmortgage",
    "hasdependents",
    "loanpurpose",
    "hascosigner",
]

NUMERICAL_COLUMNS = [
    "age",
    "income",
    "loanamount",
    "creditscore",
    "monthsemployed",
    "numcreditlines",
    "interestrate",
    "loanterm",
    "dtiratio",
]

DROP_COLUMNS = [
    "loanid",
    "id",
    "loan_id",
    "unnamed: 0",
]

MODEL_PATH = "loan_default_model.joblib"

RANDOM_STATE = 42


# -----------------------------
# Find Dataset
# -----------------------------

def find_dataset():

    candidates = [
        os.getenv("DATA_PATH"),
        "data/Loan_default.csv",
        "data/loan_default.csv",
        "Loan_default.csv",
    ]

    for path in candidates:

        if path and os.path.isfile(path):
            return path

    raise FileNotFoundError(
        "Loan_default.csv was not found. "
        "Put it inside data/Loan_default.csv"
    )


# -----------------------------
# Clean Columns
# -----------------------------

def clean_columns(df):

    df = df.copy()

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


# -----------------------------
# Evaluate Model
# -----------------------------

def evaluate_model(model, X_train, y_train, X_test, y_test):

    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "f1": f1_score(
            y_test, predictions, zero_division=0
        ),
    }

    return model, train_score, test_score, metrics


# -----------------------------
# Check Overfitting
# -----------------------------

def fit_verdict(train_score, test_score):

    gap = train_score - test_score

    if gap > 0.05:
        return "Overfitting"

    if train_score < 0.65 and test_score < 0.65:
        return "Underfitting"

    return "Good fit"




def main():

    start_time = time.time()

    # 1. Load dataset
    csv_path = find_dataset()

    df = pd.read_csv(csv_path)

    # 2. Clean columns
    df = clean_columns(df)

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    # Check target
    if "default" not in df.columns:
        raise ValueError(
            "Target column 'default' was not found."
        )

    # -----------------------------
    # 3. Encode categorical columns
    # -----------------------------

    encoders = {}

    categorical_columns = [
        col
        for col in CATEGORICAL_COLUMNS
        if col in df.columns
    ]

    for col in categorical_columns:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(
            df[col].astype(str)
        )

        encoders[col] = encoder

    # -----------------------------
    # 4. Select features
    # -----------------------------

    drop_columns = [
        col
        for col in DROP_COLUMNS
        if col in df.columns
    ]

    feature_columns = [
        col
        for col in df.columns
        if col not in drop_columns + ["default"]
    ]

    X = df[feature_columns].copy()

    y = df["default"].astype(int)

    # -----------------------------
    # 5. Train/Test Split
    # -----------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # -----------------------------
    # 6. Scale numerical columns
    # -----------------------------

    numerical_columns = [
        col
        for col in NUMERICAL_COLUMNS
        if col in X.columns
    ]

    scaler = StandardScaler()

    X_train[numerical_columns] = scaler.fit_transform(
        X_train[numerical_columns]
    )

    X_test[numerical_columns] = scaler.transform(
        X_test[numerical_columns]
    )

    # -----------------------------
    # 7. Define Models
    # -----------------------------

    models = {

        "Logistic Regression":
            LogisticRegression(max_iter=1000),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=150,
                max_depth=8,
                random_state=RANDOM_STATE,
                n_jobs=-1
            ),

        "AdaBoost":
            AdaBoostClassifier(
                n_estimators=100,
                random_state=RANDOM_STATE
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                n_estimators=100,
                max_depth=3,
                random_state=RANDOM_STATE
            ),
    }

    # -----------------------------
    # 8. Train and Compare Models
    # -----------------------------

    comparison_table = []

    best_model = None
    best_model_name = None
    best_test_accuracy = 0

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    for name, model in models.items():

        trained_model, train_score, test_score, metrics = \
            evaluate_model(
                model,
                X_train,
                y_train,
                X_test,
                y_test
            )

        verdict = fit_verdict(
            train_score,
            test_score
        )

        row = {
            "model": name,
            "train_score": float(train_score),
            "test_score": float(test_score),
            "accuracy": float(metrics["accuracy"]),
            "precision": float(metrics["precision"]),
            "recall": float(metrics["recall"]),
            "f1": float(metrics["f1"]),
            "fit_verdict": verdict,
        }

        comparison_table.append(row)

        print("\nModel:", name)
        print("Train Accuracy:", round(train_score, 4))
        print("Test Accuracy:", round(test_score, 4))
        print("Precision:", round(metrics["precision"], 4))
        print("Recall:", round(metrics["recall"], 4))
        print("F1 Score:", round(metrics["f1"], 4))
        print("Fit:", verdict)

        # Select best model based on test accuracy
        if test_score > best_test_accuracy:

            best_test_accuracy = test_score
            best_model = trained_model
            best_model_name = name

    # -----------------------------
    # 9. Final Best Model
    # -----------------------------

    best_result = next(
        row for row in comparison_table
        if row["model"] == best_model_name
    )

    print("\n" + "=" * 60)
    print("BEST MODEL")
    print("=" * 60)

    print("Best Model:", best_model_name)
    print(
        "Test Accuracy:",
        round(best_result["test_score"], 4)
    )

    # -----------------------------
    # 10. Save Model
    # -----------------------------

    bundle = {

        "model": best_model,

        "scaler": scaler,

        "encoders": encoders,

        "feature_columns": feature_columns,

        "categorical_columns": categorical_columns,

        "numerical_columns": numerical_columns,

        "metrics": {
            "accuracy": best_result["accuracy"],
            "precision": best_result["precision"],
            "recall": best_result["recall"],
            "f1": best_result["f1"],
        },

        "best_model_name": best_model_name,

        "train_score": best_result["train_score"],

        "test_score": best_result["test_score"],

        "fit_verdict": best_result["fit_verdict"],

        "comparison_table": comparison_table,
    }

    joblib.dump(bundle, MODEL_PATH)

    print("\nModel saved successfully to:")
    print(MODEL_PATH)

    print(
        "\nTraining completed in:",
        round(time.time() - start_time, 2),
        "seconds"
    )




if __name__ == "__main__":
    main()