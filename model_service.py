import os
import glob
import joblib
import pandas as pd


class LoanDefaultModel:

    """Loads the trained model and performs predictions."""

    MODEL_PATH = "loan_default_model.joblib"

    def __init__(self):

        self.is_ready = False

        self.data = None

        self.model = None

        self.scaler = None

        self.encoders = {}

        self.feature_columns = []

        self.categorical_columns = []

        self.numerical_columns = []

        self.metrics = {}

        self.options = {}

        self.defaults = {}

        self.best_model_name = None

        self.train_score = None

        self.test_score = None

        self.fit_verdict = None

        self.comparison_table = []

        self._load_model()

        self._load_dataset_for_dashboard()

    # --------------------------------
    # Find Model
    # --------------------------------

    def _find_model(self):

        env = os.getenv("MODEL_PATH")

        candidates = [
            env,
            self.MODEL_PATH,
            "./models/loan_default_model.joblib",
        ]

        for path in candidates:

            if path and os.path.isfile(path):
                return path

        return None

    # --------------------------------
    # Find Dataset
    # --------------------------------

    def _find_csv(self):

        env = os.getenv("DATA_PATH")

        candidates = [
            env,
            "data/Loan_default.csv",
            "data/loan_default.csv",
            "Loan_default.csv",
        ]

        for path in candidates:

            if path and os.path.isfile(path):
                return path

        for path in glob.glob(
            "**/*.csv",
            recursive=True
        ):

            name = os.path.basename(path).lower()

            if "loan" in name and "default" in name:
                return path

        return None

    # --------------------------------
    # Clean Columns
    # --------------------------------

    @staticmethod
    def _clean_columns(df):

        df = df.copy()

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(
                " ",
                "_",
                regex=False
            )
        )

        return df

    # --------------------------------
    # Load Model
    # --------------------------------

    def _load_model(self):

        path = self._find_model()

        if not path:

            raise FileNotFoundError(
                "loan_default_model.joblib was not found. "
                "Run python train_model.py first."
            )

        bundle = joblib.load(path)

        self.model = bundle["model"]

        self.scaler = bundle["scaler"]

        self.encoders = bundle["encoders"]

        self.feature_columns = \
            bundle["feature_columns"]

        self.categorical_columns = \
            bundle["categorical_columns"]

        self.numerical_columns = \
            bundle["numerical_columns"]

        self.metrics = bundle["metrics"]

        self.best_model_name = \
            bundle.get("best_model_name")

        self.train_score = \
            bundle.get("train_score")

        self.test_score = \
            bundle.get("test_score")

        self.fit_verdict = \
            bundle.get("fit_verdict")

        self.comparison_table = \
            bundle.get("comparison_table", [])

        self.is_ready = True

    # --------------------------------
    # Load Dataset
    # --------------------------------

    def _load_dataset_for_dashboard(self):

        path = self._find_csv()

        if not path:
            return

        df = pd.read_csv(path)

        df = self._clean_columns(df)

        self.data = df

        # Options for dropdowns
        for col in self.categorical_columns:

            if col in df.columns:

                self.options[col] = sorted(
                    df[col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

        # Default values for numerical inputs
        for col in self.numerical_columns:

            if col in df.columns:

                self.defaults[col] = float(
                    df[col].median()
                )

    # --------------------------------
    # Prepare User Input
    # --------------------------------

    def _prepare_input(self, row):

        incoming = pd.DataFrame(
            [row]
        ).copy()

        incoming = self._clean_columns(
            incoming
        )

        # Encode categorical values
        for col, encoder in self.encoders.items():

            if col not in incoming.columns:

                raise ValueError(
                    f"Missing input column: {col}"
                )

            value = str(
                incoming.at[0, col]
            )

            if value not in encoder.classes_:

                raise ValueError(
                    f"Unknown value '{value}' "
                    f"for {col}."
                )

            incoming[col] = encoder.transform(
                [value]
            )

        # Put columns in correct order
        incoming = incoming.reindex(
            columns=self.feature_columns,
            fill_value=0
        )

        # Scale numerical columns
        incoming[
            self.numerical_columns
        ] = self.scaler.transform(
            incoming[
                self.numerical_columns
            ]
        )

        return incoming

    # --------------------------------
    # Prediction
    # --------------------------------

    def predict_probability(
        self,
        row: dict
    ) -> float:

        if not self.is_ready:

            raise RuntimeError(
                "Model is not ready."
            )

        X = self._prepare_input(row)

        probability = self.model.predict_proba(
            X
        )[0, 1]

        return float(probability)