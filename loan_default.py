import os
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #1f2937;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.result-card {
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "Loan_default.csv")
    df = pd.read_csv(file_path)
    return df


df = load_data()

# ============================================================
# PREPARE DATA
# ============================================================

@st.cache_resource
def train_model(df):

    data = df.copy()

    # One-hot encoding
    data = pd.get_dummies(
        data,
        columns=[
            "Education",
            "EmploymentType",
            "MaritalStatus",
            "HasMortgage",
            "HasDependents",
            "LoanPurpose",
            "HasCoSigner"
        ],
        dtype=int
    )

    # Remove LoanID
    X = data.drop(columns=["LoanID", "Default"])

    # Target
    y = data["Default"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Logistic Regression
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    return model, X.columns.tolist(), accuracy


model, feature_columns, accuracy = train_model(df)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🏦 Loan Default Prediction System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict whether a loan applicant is likely to default'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# DASHBOARD INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Loan Records",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Model",
        "Logistic Regression"
    )

with col3:
    st.metric(
        "Model Accuracy",
        f"{accuracy * 100:.2f}%"
    )

st.divider()

# ============================================================
# LOAN APPLICATION FORM
# ============================================================

st.subheader("📋 Applicant Information")

st.write("Enter the applicant's details below.")

# ------------------------------------------------------------
# NUMERICAL INPUTS
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=69,
        value=30
    )

    income = st.number_input(
        "Income",
        min_value=15000,
        max_value=149999,
        value=50000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=5000,
        max_value=249999,
        value=100000
    )

with col2:

    credit_score = st.number_input(
        "Credit Score",
        min_value=300,
        max_value=849,
        value=650
    )

    months_employed = st.number_input(
        "Months Employed",
        min_value=0,
        max_value=119,
        value=24
    )

    num_credit_lines = st.number_input(
        "Number of Credit Lines",
        min_value=1,
        max_value=4,
        value=2
    )

with col3:

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=2.0,
        max_value=25.0,
        value=10.0,
        step=0.01
    )

    loan_term = st.selectbox(
        "Loan Term (Months)",
        [12, 24, 36, 48, 60]
    )

    dti_ratio = st.number_input(
        "DTI Ratio",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.01
    )

# ============================================================
# CATEGORICAL INPUTS
# ============================================================

st.subheader("👤 Personal & Loan Details")

col1, col2 = st.columns(2)

with col1:

    education = st.selectbox(
        "Education",
        [
            "High School",
            "Bachelor's",
            "Master's",
            "PhD"
        ]
    )

    employment_type = st.selectbox(
        "Employment Type",
        [
            "Full-time",
            "Part-time",
            "Self-employed",
            "Unemployed"
        ]
    )

    marital_status = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Divorced"
        ]
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        [
            "Auto",
            "Business",
            "Education",
            "Home",
            "Other"
        ]
    )

with col2:

    has_mortgage = st.selectbox(
        "Has Mortgage?",
        ["Yes", "No"]
    )

    has_dependents = st.selectbox(
        "Has Dependents?",
        ["Yes", "No"]
    )

    has_cosigner = st.selectbox(
        "Has Co-Signer?",
        ["Yes", "No"]
    )

# ============================================================
# PREDICTION BUTTON
# ============================================================

st.divider()

predict_button = st.button(
    "🔍 Predict Loan Default",
    use_container_width=True
)

# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    # Create input DataFrame
    input_data = pd.DataFrame({
        "Age": [age],
        "Income": [income],
        "LoanAmount": [loan_amount],
        "CreditScore": [credit_score],
        "MonthsEmployed": [months_employed],
        "NumCreditLines": [num_credit_lines],
        "InterestRate": [interest_rate],
        "LoanTerm": [loan_term],
        "DTIRatio": [dti_ratio],
        "Education": [education],
        "EmploymentType": [employment_type],
        "MaritalStatus": [marital_status],
        "HasMortgage": [has_mortgage],
        "HasDependents": [has_dependents],
        "LoanPurpose": [loan_purpose],
        "HasCoSigner": [has_cosigner]
    })

    # Apply same one-hot encoding
    input_data = pd.get_dummies(
        input_data,
        columns=[
            "Education",
            "EmploymentType",
            "MaritalStatus",
            "HasMortgage",
            "HasDependents",
            "LoanPurpose",
            "HasCoSigner"
        ],
        dtype=int
    )

    # Make sure input has exactly the same columns as training data
    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Prediction
    prediction = model.predict(input_data)[0]

    # Probability
    probability = model.predict_proba(input_data)[0]

    default_probability = probability[1] * 100
    no_default_probability = probability[0] * 100

    # ========================================================
    # RESULT
    # ========================================================

    st.subheader("📊 Prediction Result")

    if prediction == 1:

        st.error(
            "⚠️ HIGH RISK — Loan Default Predicted"
        )

        st.write(
            f"Probability of Default: **{default_probability:.2f}%**"
        )

    else:

        st.success(
            "✅ LOW RISK — No Loan Default Predicted"
        )

        st.write(
            f"Probability of No Default: **{no_default_probability:.2f}%**"
        )

    # Probability chart
    result_df = pd.DataFrame({
        "Result": [
            "No Default",
            "Default"
        ],
        "Probability": [
            no_default_probability,
            default_probability
        ]
    })

    st.bar_chart(
        result_df.set_index("Result")
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Loan Default Prediction System | Machine Learning Project"
)