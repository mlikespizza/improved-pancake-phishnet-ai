import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load your master dataset
df = pd.read_csv("total_emails_master.csv")
df = df.dropna() # Remove any empty rows

# 2. Setup TF-IDF (The 'Translator')
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)

# 3. Split the data (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# 4. Transform text into numbers
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# 5. Train the Model (Logistic Regression)
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 6. Check Accuracy
predictions = model.predict(X_test_tfidf)
print(f"Model Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, predictions))

# 7. Save the "Brain" for your Streamlit App
joblib.dump(model, 'phishnet_model.pkl')
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
print("\nSUCCESS: Model and Vectorizer saved!")