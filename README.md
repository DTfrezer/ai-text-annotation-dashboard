# 🏷️ LabelLab — AI Text Annotation & Dataset Quality Dashboard

An interactive data annotation dashboard built with **Python, Pandas, and Streamlit** to label text datasets, review annotation quality, track progress, and export structured data for machine learning workflows.

## 📌 Project Overview

LabelLab provides a simple interface for human reviewers to annotate text by sentiment and topic. It also identifies common dataset quality issues, helping prepare cleaner datasets for downstream machine learning tasks.

The application includes a sample dataset to demonstrate the annotation workflow and supports uploading custom CSV datasets.

## ✨ Features

- **Sentiment Annotation:** Label text as Positive, Negative, Neutral, or Unreviewed.
- **Topic Classification:** Categorize records into Technology, Sports, Finance, Health, Education, Entertainment, or Other.
- **Interactive Annotation Table:** Edit labels and add reviewer notes.
- **Dataset Filtering:** Filter by sentiment and topic, search text, and isolate unreviewed records.
- **Annotation Progress Tracking:** View total records, reviewed records, completion percentage, and duplicate text counts.
- **Dataset Quality Checks:** Detect blank text, duplicate records, unreviewed sentiment labels, and unassigned topics.
- **Visual Analytics:** View sentiment and topic distributions through charts.
- **CSV Export:** Download annotated data and a dataset quality report.
- **Custom Dataset Support:** Upload CSV files containing a `text` column.

## 🖥️ Screenshots

<img width="1200" height="638" alt="image" src="https://github.com/user-attachments/assets/dbe3efeb-3eba-4bcc-ad56-229727ca53ee" />



<img width="1200" height="639" alt="image" src="https://github.com/user-attachments/assets/760587ee-0da7-497d-9c2f-33db228dc190" />



<img width="1200" height="640" alt="image" src="https://github.com/user-attachments/assets/19ac834b-6fb4-4fcc-8c9c-af6521d81b09" />



## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Pandas | Dataset manipulation and quality checks |
| Streamlit | Interactive web interface |
| CSV | Dataset import and export |
| Git & GitHub | Version control and project hosting |

## 📂 Project Structure

```text
ai-text-annotation-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    ├── 01-annotation-workflow.png
    ├── 02-dataset-quality-report.png
    └── 03-csv-export.png
```

The screenshot files are examples of the expected filenames; add your actual screenshots to this folder.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or newer
- pip
- Visual Studio Code or another Python editor

### 1. Clone the repository

```bash
git clone https://github.com/DTfrezer/ai-text-annotation-dashboard.git
cd ai-text-annotation-dashboard
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

If PowerShell blocks activation, you can use the environment's Python executable directly in the following steps.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 📊 How to Use

1. Launch the application.
2. Use the included sample dataset or upload your own CSV.
3. Review the text records in the annotation queue.
4. Assign sentiment and topic labels using the dropdowns.
5. Add reviewer notes where appropriate.
6. Click **Save annotation edits** to save changes in the current session.
7. Open **Quality checks** to inspect missing labels, blank text, and duplicate records.
8. Review the sentiment and topic distribution charts.
9. Open **Export** to download the annotated dataset or quality report as CSV.

## 📄 Input Dataset Format

Your CSV must contain a `text` column. The other columns below are optional.

| Column | Description |
|---|---|
| `id` | Unique record identifier |
| `text` | Sentence or text to annotate; required |
| `sentiment` | Sentiment label |
| `topic` | Topic category |
| `review_notes` | Optional reviewer comments |

Example:

```csv
id,text,sentiment,topic,review_notes
1,"The product is excellent",Unreviewed,Unassigned,
2,"The application crashes frequently",Unreviewed,Unassigned,
3,"The stock market rose today",Unreviewed,Unassigned,
```

When optional annotation columns are missing, the application supplies default values.

## 🔍 Dataset Quality Checks

LabelLab checks for:

- Empty or whitespace-only text
- Duplicate text records
- Missing or unreviewed sentiment labels
- Missing or unassigned topic labels

These checks help reviewers identify records that may need additional attention before exporting a dataset.

## 🚀 Future Improvements

- Persistent database storage for annotations
- Multi-user annotation and reviewer management
- Annotation history and audit logs
- Inter-annotator agreement metrics
- Advanced text classification and evaluation
- Integration with external annotation platforms

## ⚠️ Limitations

- Annotation edits are stored in the active Streamlit session; export your data to preserve your work.
- Duplicate detection is based on matching text after trimming surrounding whitespace.
- Quality checks identify potential issues but do not determine whether a human-assigned label is factually correct.
- This project is a portfolio demonstration, not a production-ready multi-user annotation platform.

## 👨‍💻 Author

**Sarthak Bhosale**

GitHub: [@DTfrezer](https://github.com/DTfrezer)

## 📜 License

This project is available for educational and portfolio use. Add a `LICENSE` file if you intend to distribute it under a specific open-source license.

---

*Built to demonstrate practical skills in text annotation, dataset validation, data processing, and Python application development.*
