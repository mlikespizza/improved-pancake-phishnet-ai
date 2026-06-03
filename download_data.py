import kagglehub
import os
import shutil

# 1. Defines the local data folder
local_data_dir = os.path.join(os.getcwd(), "data")

# 2. Safety Check: If the 'data' exists as a file, it removes it. if not, it creates the folder
if os.path.exists(local_data_dir):
    if os.path.isfile(local_data_dir):
        os.remove(local_data_dir)
        os.makedirs(local_data_dir)
else:
    os.makedirs(local_data_dir)

datasets = [
    "rtatman/fraudulent-email-corpus",
    "kuladeep19/phishing-and-legitimate-emails-dataset",
    "francescogreco97/human-llm-generated-phishing-legitimate-emails"
]

print("--- PhishNet AI: Step 1 (Data Retrieval) ---")

for ds in datasets:
    try:
        print(f"\nLocating: {ds}...")
        cached_path = kagglehub.dataset_download(ds)
        
        # Walks through the cached folder
        for root, dirs, files in os.walk(cached_path):
            for file in files:
                # Skips system files like .DS_Store or hidden metadata
                if file.startswith('.') or file.endswith('.archive'):
                    continue
                
                source_file = os.path.join(root, file)
                # Creates a unique name to avoid overwriting
                unique_name = f"{ds.split('/')[-1]}_{file}"
                destination = os.path.join(local_data_dir, unique_name)
                
                # Copies the file to your project
                shutil.copy2(source_file, destination)
                print(f"  + Successfully copied: {file}")
                
    except Exception as e:
        print(f"  ! Error processing {ds}: {e}")

print("\n--- DONE ---")
print(f"Check your 'data' folder.")