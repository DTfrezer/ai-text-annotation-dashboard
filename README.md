# LabelLab — AI Text Annotation & Dataset Quality Dashboard

A local Streamlit app for labeling text data and checking basic dataset quality.

## Features
- Sentiment labels: Positive, Negative, Neutral, Unreviewed
- Topic labels: Technology, Sports, Finance, Health, Education, Entertainment, Other
- Search and filter annotation queue
- Progress and label-distribution charts
- Quality checks for blank text, duplicate text, and unassigned labels
- CSV export for annotations and quality report

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create/activate a virtual environment (recommended).
4. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Upload a CSV with a `text` column. Optional columns: `id`, `sentiment`, `topic`, `review_notes`.

## Notes
Data edits are kept in the current app session. Download the CSV to preserve work. This is a portfolio project, not a production multi-user annotation platform.
