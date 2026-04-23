import kagglehub
import os
import shutil

# 1. Define the local data folder
local_data_dir = os.path.join(os.getcwd(), "data")

# 2. Safety Check: If 'data' exists as a file, remove it; if not, create the folder
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
        # Since you've already downloaded them, this will be instant
        cached_path = kagglehub.dataset_download(ds)
        
        # Walk through the cached folder
        for root, dirs, files in os.walk(cached_path):
            for file in files:
                # Skip system files like .DS_Store or hidden metadata
                if file.startswith('.') or file.endswith('.archive'):
                    continue
                
                source_file = os.path.join(root, file)
                # Create a unique name to avoid overwriting
                unique_name = f"{ds.split('/')[-1]}_{file}"
                destination = os.path.join(local_data_dir, unique_name)
                
                # Copy the file to your project
                shutil.copy2(source_file, destination)
                print(f"  + Successfully copied: {file}")
                
    except Exception as e:
        print(f"  ! Error processing {ds}: {e}")

print("\n--- DONE ---")
print(f"Check your 'data' folder on the left side of Windsurf.")