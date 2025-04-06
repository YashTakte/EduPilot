import pandas as pd
import os
from huggingface_hub import InferenceClient

# === Load the course catalog CSV ===
DEFAULT_COURSE_CSV_PATH = "dataset.csv"  # Expect the file in the same directory

if not os.path.exists(DEFAULT_COURSE_CSV_PATH):
    raise FileNotFoundError(f"Could not find course catalog file at: {DEFAULT_COURSE_CSV_PATH}")

try:
    df = pd.read_csv(DEFAULT_COURSE_CSV_PATH, encoding='utf-8')  # Try UTF-8 first
except Exception as e:
    # Fallback to windows-1252 if utf-8 fails
    try:
        df = pd.read_csv(DEFAULT_COURSE_CSV_PATH, encoding='windows-1252')
    except Exception as e2:
        raise FileNotFoundError(f"Could not load course catalog from {DEFAULT_COURSE_CSV_PATH}. Error: {e2}")

# === Build a formatted course catalog string ===
def build_course_catalog(df):
    df.columns = df.columns.str.strip()
    catalog = ""

    for idx, row in df.iterrows():
        catalog += f"""
        Course ID: {row['Course Code']}
        Course Name: {row['Course Title']}
        Credits: {row['Credits']}
        Description: {row['Description']}
        Prerequisites: {row['Prerequisites']}
        Skills: {row['Skills']}
        Semester Offered: {row['Semester Offered']}
        Delivery Mode: {row['Delivery Mode']}
        Project Based: {row['Project Based']}
        Instructor Name: {row['Instructor Name']}
        Instructor Rating: {row['Instructor Rating']}
        Course Value Score: {row['Course Value Score']}
        Total Feedback Count: {row['Total Feedback Count']}
        Positive Percentage: {row['Positive Percentage']}
        """

    return catalog

course_catalog_text = build_course_catalog(df)

# === Hugging Face Inference Function ===
def query_deepseek_model(prompt: str, api_key: str) -> str:
    """
    Sends a prompt to the DeepSeek-V3 model via Hugging Face InferenceClient.
    """
    try:
        client = InferenceClient(provider = 'novita',api_key=api_key)  # Removed 'provider'
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"⚠ Error from Hugging Face API: {e}"

# === Main function for Streamlit UI ===
def get_recommendations_from_input(user_input: str, api_key: str) -> str:
    prompt = f"""
You are a smart university course advisor.

Here is the available course catalog:
{course_catalog_text}

A student says: "{user_input}"

Based on their goals, recommend 3 to 5 courses. 
For each recommendation, include:
- Course Name
- Credits
- Prerequisites
- Semester Offered
- A short reason

Make sure to respect any prerequisites listed.
Assume the student prefers a manageable credit load.
"""
    print("🟡 Prompt being sent to model:\n", prompt[:1000], "...\n")  # Truncated for console
    return query_deepseek_model(prompt, api_key)

