# PhishNet AI - Phishing Email Detection System

A machine learning-powered phishing email detection system with educational features, built with Streamlit and scikit-learn.

## Features

- **AI-Powered Detection**: Uses TF-IDF vectorization and Logistic Regression
- **Educational Insights**: Identifies common phishing patterns and red flags
- **Modern UI**: Dark theme with smooth scrolling and responsive design
- **Real-time Analysis**: Instant email classification with safety tips

## Dataset Sources

This project uses multiple phishing email datasets (excluded from git due to size):

1. **[Kuladeep19 Phishing Dataset](https://www.kaggle.com/datasets/kuladeep19/phishing-and-legitimate-emails-dataset)**
   - 10,000 balanced emails (phishing + legitimate)
   - Columns: text, label, phishing_type, severity, confidence

2. **[Human-LLM Generated Emails](https://www.kaggle.com/datasets/francescogreco97/human-llm-generated-phishing-legitimate-emails)**
   - Modern phishing and legitimate emails
   - Separate files for phishing and legitimate samples

3. **[Nigerian Fraud Corpus](https://www.kaggle.com/datasets/rtatman/fraudulent-email-corpus)**
   - Traditional "419" scam emails
   - Text format with email samples

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/mlikespizza/improved-pancake-phishnet-ai.git
cd improved-pancake-phishnet-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download and prepare data
```bash
python download_data.py    # Downloads datasets from Kaggle
python merge_data.py       # Combines all datasets
python train_model.py      # Trains the ML model
```

### 4. Run the web app
```bash
streamlit run app.py
```

## Project Structure

```
phishnet-AI-final-year-project/
├── app.py                 # Main Streamlit web application
├── train_model.py         # ML model training script
├── download_data.py       # Data download from Kaggle
├── merge_data.py          # Data processing pipeline
├── explore_data.py        # Data exploration script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── phishnet_model.pkl    # Trained ML model (generated)
├── tfidf_vectorizer.pkl  # TF-IDF vectorizer (generated)
├── total_emails_master.csv # Combined dataset (generated)
└── data/                 # Raw datasets (downloaded)
```

## Model Details

- **Algorithm**: Logistic Regression
- **Feature Extraction**: TF-IDF Vectorization (5,000 features)
- **Dataset Size**: ~15,571 emails combined
- **Accuracy**: ~95% (varies by training)
- **Features**: Stop-word removal, max features limiting

## How It Works

1. **Text Processing**: Emails are cleaned and converted to TF-IDF vectors
2. **Pattern Detection**: AI identifies linguistic patterns common in phishing
3. **Rule-Based Analysis**: Additional checks for urgency, credential harvesting, and financial fraud keywords
4. **Educational Output**: Provides specific red flags and safety tips

## Usage

1. **Paste Email Text**: Copy suspicious email content into the text area
2. **Click Analyze**: Get instant classification and educational feedback
3. **Review Results**: See identified red flags and safety recommendations

## Performance

- **Training Time**: ~30 seconds
- **Prediction Time**: <1 second
- **Memory Usage**: ~50MB model size
- **Accuracy**: 94-96% on test data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Notes

- Data files are excluded from git due to size (see .gitignore)
- Model files (.pkl) are generated after training
- Requires Kaggle API access for dataset download
- Educational tool - always verify with professional security services

## Disclaimer

PhishNet AI is an educational tool and should not replace professional security services. Always verify suspicious emails through official channels and use your own judgment for critical security decisions.

## License

This project is open source and available under the MIT License.
