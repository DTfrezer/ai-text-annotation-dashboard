import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="LabelLab | Text Annotation", page_icon="🏷️", layout="wide")
st.title("🏷️ LabelLab")
st.caption("Text annotation and dataset quality workspace")
st.markdown("Label text, review dataset quality, track progress, and export a clean CSV.")

SENTIMENTS = ["Unreviewed", "Positive", "Negative", "Neutral"]
TOPICS = ["Unassigned", "Technology", "Sports", "Finance", "Health", "Education", "Entertainment", "Other"]
REQUIRED = ["text"]

def starter_data():
    return pd.DataFrame({
        "id": [f"TXT-{i:03d}" for i in range(1, 9)],
        "text": [
            "The new laptop is fast and has excellent battery life.",
            "The team lost badly and the match was disappointing.",
            "The central bank kept interest rates unchanged today.",
            "I received the package this morning.",
            "This app crashes every time I try to save a file.",
            "The new AI model improves document search.",
            "The coach praised the players after the final.",
            "Quarterly revenue increased compared with last year."
        ],
        "sentiment": ["Unreviewed"] * 8,
        "topic": ["Unassigned"] * 8,
        "review_notes": [""] * 8
    })

def normalize(df):
    df = df.copy()
    if "text" not in df.columns:
        possible = next((c for c in df.columns if c.lower() in ("sentence", "content", "review", "message")), None)
        if possible:
            df = df.rename(columns={possible: "text"})
        else:
            st.error("Your CSV needs a 'text' column (or sentence/content/message).")
            st.stop()
    if "id" not in df.columns:
        df.insert(0, "id", [f"ROW-{i:04d}" for i in range(1, len(df)+1)])
    for col, default in [("sentiment", "Unreviewed"), ("topic", "Unassigned"), ("review_notes", "")]:
        if col not in df.columns:
            df[col] = default
        df[col] = df[col].fillna(default).astype(str)
    df["text"] = df["text"].fillna("").astype(str)
    return df[["id", "text", "sentiment", "topic", "review_notes"]]

with st.sidebar:
    st.header("Dataset")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        try:
            source_df = normalize(pd.read_csv(uploaded))
            st.success(f"Loaded {len(source_df)} rows")
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
            source_df = starter_data()
    else:
        source_df = starter_data()
        st.info("Using included starter dataset. Upload your own CSV to begin.")

if "df" not in st.session_state or st.session_state.get("source_name") != (uploaded.name if uploaded else "starter"):
    st.session_state.df = source_df.copy()
    st.session_state.source_name = uploaded.name if uploaded else "starter"
df = st.session_state.df

with st.sidebar:
    st.divider()
    st.subheader("Filters")
    sentiment_filter = st.multiselect("Sentiment", SENTIMENTS, default=SENTIMENTS)
    topic_filter = st.multiselect("Topic", TOPICS, default=TOPICS)
    search = st.text_input("Search text")
    show_unreviewed = st.checkbox("Only unreviewed", value=False)

df["text"] = df["text"].fillna("").astype(str)
filtered = df[df["sentiment"].isin(sentiment_filter) & df["topic"].isin(topic_filter)]
if search:
    filtered = filtered[filtered["text"].str.contains(search, case=False, na=False)]
if show_unreviewed:
    filtered = filtered[filtered["sentiment"] == "Unreviewed"]

total = len(df)
reviewed = int((df["sentiment"] != "Unreviewed").sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total records", total)
c2.metric("Reviewed", reviewed)
c3.metric("Progress", f"{reviewed / total:.0%}" if total else "0%")
c4.metric("Duplicate texts", int(df["text"].str.strip().duplicated(keep=False).sum()))
st.progress(reviewed / total if total else 0)

tab_annotate, tab_quality, tab_export = st.tabs(["✍️ Annotate", "🔎 Quality checks", "📤 Export"])

with tab_annotate:
    st.subheader("Annotation queue")
    st.caption("Edit labels directly in the table. Use the row ID to keep records traceable.")
    edited = st.data_editor(
        filtered,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "id": st.column_config.TextColumn("Record ID", disabled=True),
            "text": st.column_config.TextColumn("Text", width="large", disabled=True),
            "sentiment": st.column_config.SelectboxColumn("Sentiment", options=SENTIMENTS, required=True),
            "topic": st.column_config.SelectboxColumn("Topic", options=TOPICS, required=True),
            "review_notes": st.column_config.TextColumn("Review notes", width="medium")
        },
        key="annotation_editor"
    )
    if st.button("Save annotation edits", type="primary"):
        updates = edited.set_index("id")
        for idx, row in df.iterrows():
            if row["id"] in updates.index:
                for col in ["sentiment", "topic", "review_notes"]:
                    df.at[idx, col] = updates.loc[row["id"], col]
        st.session_state.df = df
        st.success("Edits saved for this session.")

with tab_quality:
    st.subheader("Dataset quality report")
    blank_text = df["text"].str.strip().eq("")
    duplicate = df["text"].str.strip().duplicated(keep=False) & ~blank_text
    missing_sentiment = df["sentiment"].isin(["", "Unreviewed"])
    missing_topic = df["topic"].isin(["", "Unassigned"])
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Blank text", int(blank_text.sum()))
    q2.metric("Duplicate rows", int(duplicate.sum()))
    q3.metric("Missing sentiment", int(missing_sentiment.sum()))
    q4.metric("Missing topic", int(missing_topic.sum()))
    issues = df[blank_text | duplicate | missing_sentiment | missing_topic].copy()
    if issues.empty:
        st.success("No quality issues detected by the current checks.")
    else:
        st.warning("Review the records below before exporting a production dataset.")
        issues["quality_issue"] = [
            ", ".join(label for condition, label in [
                (blank_text.loc[i], "blank text"),
                (duplicate.loc[i], "duplicate text"),
                (missing_sentiment.loc[i], "sentiment not reviewed"),
                (missing_topic.loc[i], "topic unassigned")
            ] if condition) for i in issues.index
        ]
        st.dataframe(issues[["id", "text", "sentiment", "topic", "quality_issue"]], use_container_width=True, hide_index=True)
    st.markdown("#### Label distribution")
    st.write("Sentiment")
    st.bar_chart(df["sentiment"].value_counts())
    st.write("Topic")
    st.bar_chart(df["topic"].value_counts())

with tab_export:
    st.subheader("Export reviewed data")
    export_reviewed_only = st.checkbox("Export reviewed records only", value=False)
    export_df = df[df["sentiment"] != "Unreviewed"] if export_reviewed_only else df
    st.write(f"Ready to export **{len(export_df)}** records.")
    st.dataframe(export_df, use_container_width=True, hide_index=True)
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_bytes, file_name="annotated_dataset.csv", mime="text/csv", type="primary")
    st.download_button("Download quality report CSV", data=df.assign(
        blank_text=df["text"].str.strip().eq(""),
        duplicate_text=df["text"].str.strip().duplicated(keep=False),
        sentiment_unreviewed=df["sentiment"].isin(["", "Unreviewed"]),
        topic_unassigned=df["topic"].isin(["", "Unassigned"])
    ).to_csv(index=False).encode("utf-8"), file_name="dataset_quality_report.csv", mime="text/csv")
