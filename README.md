# AI Human Potential & Burnout Risk Predictor with Personalized Intervention

A Streamlit + Python Human-Centered AI project prototype. It includes an assessment form, a demo ML score, response-pattern visualization, optional intervention suggestions, session history, and CSV export.

## Important limitation

The model is trained on **synthetic/artificial data with artificial labels** created by hand-written rules. It is only for demonstrating the software workflow. It is **not validated for actual burnout prediction**, and the displayed score is not a real probability of burnout or a diagnosis.

Do not use this prototype to make employment, academic, medical, or other consequential decisions about a person.

## Requirements

- Python 3.10 or newer recommended
- pip
- Internet connection for initial package installation

## Run on Windows

1. Extract this ZIP file.
2. Open the extracted folder.
3. Open Command Prompt or PowerShell in that folder.
4. (Recommended) Create a virtual environment:

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Launch the application:

   ```bash
   streamlit run app.py
   ```

7. Open the local URL printed in the terminal, commonly `http://localhost:8501`.

## Project structure

```text
AI_Human_Potential_Burnout_Predictor/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── predictor.py
│   └── interventions.py
├── scripts/
│   ├── generate_demo_data.py
│   └── evaluate_demo_model.py
├── data/
└── models/
```

## Optional scripts

Generate a CSV of synthetic examples:

```bash
python scripts/generate_demo_data.py
```

Run an illustrative evaluation against the artificial labels:

```bash
python scripts/evaluate_demo_model.py
```

These metrics only indicate how well the model reproduces the artificial labeling rule. They do not demonstrate real-world validity.

## Main features

- Dashboard
- Self-assessment form
- Demo risk score and category
- Charts of self-reported response indicators
- Rule-based personalized action suggestions
- User choice over suggested actions
- In-session history and CSV download
- Project limitations and responsible-use explanation

## Responsible next steps

For a credible research project, first define the intended use and target outcome. Locate a suitable, documented dataset with legitimate access and clear labels; inspect its consent and license conditions; use train/validation/test separation; compare baselines; evaluate precision, recall, F1, calibration and relevant subgroup performance; document limitations; and obtain appropriate approval before collecting personal or sensitive data.
