import pandas as pd
import os

data_dir = os.path.join(os.getcwd(), "data")

def clean_text(text):
    return str(text).replace('\n', ' ').replace('\r', ' ').strip()

print("--- PhishNet AI: Smart Merging ---")

all_data = []

# 1. Process the 10,000 row Balanced Dataset
file1 = os.path.join(data_dir, "phishing-and-legitimate-emails-dataset_phishing_legit_dataset_KD_10000.csv")
df1 = pd.read_csv(file1)

print(f"Columns found in Dataset 1: {df1.columns.tolist()}")

# SMART DETECTION: Find columns that look like 'Text' and 'Type'
text_col = [c for c in df1.columns if 'text' in c.lower()][0]
label_col = [c for c in df1.columns if 'type' in c.lower() or 'label' in c.lower() or 'class' in c.lower()][0]

# Standardize labels: 1 for Phishing, 0 for Safe
# We check if the values are strings like 'Phishing Email' or numbers
df1['final_label'] = df1[label_col].apply(lambda x: 1 if 'phish' in str(x).lower() else 0)

for _, row in df1.iterrows():
    all_data.append({'text': clean_text(row[text_col]), 'label': row['final_label']})
print(f"Added {len(df1)} rows from Balanced Dataset.")

# 2. Process Human-LLM Modern Emails
f_legit = os.path.join(data_dir, "human-llm-generated-phishing-legitimate-emails_legit.csv")
f_phish = os.path.join(data_dir, "human-llm-generated-phishing-legitimate-emails_phishing.csv")

# Use a helper to find the text column here too
for f, lbl in [(f_legit, 0), (f_phish, 1)]:
    try:
        # Try reading with more robust parameters
        df = pd.read_csv(f, quoting=1, on_bad_lines='skip', encoding='utf-8')
        t_col = [c for c in df.columns if 'text' in c.lower()][0]
        for text in df[t_col]:
            all_data.append({'text': clean_text(text), 'label': lbl})
        print(f"  + Successfully processed {os.path.basename(f)}")
    except Exception as e:
        print(f"  ! Error processing {f}: {e}")
        # Try alternative reading method
        try:
            df = pd.read_csv(f, sep='|', on_bad_lines='skip', encoding='utf-8')
            t_col = [c for c in df.columns if 'text' in c.lower()][0]
            for text in df[t_col]:
                all_data.append({'text': clean_text(text), 'label': lbl})
            print(f"  + Successfully processed {os.path.basename(f)} with alternative method")
        except Exception as e2:
            print(f"  ! Alternative method also failed for {f}: {e2}")

print(f"Added Human-LLM Datasets.")

# 3. Process the Nigerian Fraud Corpus (The TXT file)
f_nigerian = os.path.join(data_dir, "fraudulent-email-corpus_fradulent_emails.txt")
with open(f_nigerian, 'r', encoding='latin-1') as f:
    emails = f.read().split('From r ')
    count = 0
    for e in emails:
        if len(e) > 50:
            all_data.append({'text': clean_text(e), 'label': 1})
            count += 1
print(f"Added {count} rows from Nigerian Fraud Corpus.")

# Final Save
master_df = pd.DataFrame(all_data)
# Remove any empty text rows
master_df = master_df[master_df['text'] != '']
master_df.to_csv("total_emails_master.csv", index=False)

print("\n--- SUCCESS ---")
print(f"Total Combined Dataset: {len(master_df)} emails.")
print("Saved as: total_emails_master.csv")