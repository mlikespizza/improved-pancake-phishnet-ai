import pandas as pd
import os

# Define the path to your data folder
data_folder = os.path.join(os.getcwd(), "data")

print("--- PhishNet AI: Data Exploration ---")

# 1. Looks at the 2026 Balanced Dataset (CSV format)
csv_file = os.path.join(data_folder, "phishing-and-legitimate-emails-dataset_phishing_email.csv")
if os.path.exists(csv_file):
    df_2026 = pd.read_csv(csv_file)
    print("\n[1] 2026 Balanced Dataset Sample:")
    # Shows the 'Email Text' and the 'Email Type' (Phishing/Safe)
    print(df_2026[['Email Text', 'Email Type']].head())
else:
    print("\n[!] 2026 CSV file not found. Check filenames in your data folder.")

# 2. Looks at the Nigerian Fraud Corpus (TXT format)
txt_file = os.path.join(data_folder, "fraudulent-email-corpus_fradulent_emails.txt")
if os.path.exists(txt_file):
    print("\n[2] Nigerian Fraud Corpus Sample (First 500 characters):")
    with open(txt_file, 'r', encoding='latin-1') as f:
        content = f.read(500)
        print(content)
else:
    print("\n[!] Nigerian TXT file not found. Check filenames in your data folder.")