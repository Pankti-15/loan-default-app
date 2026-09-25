# Loan Default Prediction

Streamlit app that predicts whether a loan applicant will default.

The model is trained in `train_model.py`, which trains and compares **4 models**
(Logistic Regression, Random Forest, AdaBoost, Gradient Boosting) and automatically
saves the best one (by test accuracy) to `loan_default_model.joblib`.
`app.py` loads that saved model via `model_service.py` and never retrains on the fly.

## Run locally

```bash
pip install -r requirements.txt
python train_model.py      # optional: re-trains and re-saves the model bundle
streamlit run app.py
```

## Deploy (Streamlit Community Cloud — free)

1. Push this folder to a public (or private) GitHub repo.
2. Go to https://share.streamlit.io, sign in with GitHub.
3. Click "New app", pick the repo/branch, set main file to `app.py`.
4. Click "Deploy". You'll get a public `*.streamlit.app` link in a couple of minutes.
