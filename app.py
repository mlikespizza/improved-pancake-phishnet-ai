import streamlit as st
import joblib

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(page_title="PhishNet AI", page_icon="🤺", layout="centered")

# 2. Load the saved model and vectorizer
try:
    model = joblib.load('phishnet_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
except Exception as e:
    st.error("Model files not found. Please run train_model.py first.")

# 3. Custom CSS for Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 50px !important; font-weight: 800; color: #60a5fa; text-align: center; margin-top: -20px; }
    .sub-text { font-size: 18px; color: #94a3b8; text-align: center; margin-bottom: 30px; }
    .stTextArea textarea { background-color: #1e293b !important; color: #e2e8f0 !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
    div.stButton > button { width: 100%; background-color: #3b82f6 !important; color: white !important; font-weight: bold !important; padding: 15px !important; border-radius: 8px !important; border: none !important; }
    div.stButton > button:hover { background-color: #2563eb !important; }
    .footer { font-size: 12px; color: #64748b; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 4. UI Header Elements
st.markdown('<p class="main-title">PhishNet AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Check if an email is a phishing trap.</p>', unsafe_allow_html=True)

# 5. User Input Layer
email_input = st.text_area("", placeholder="Paste the suspicious email text here...", height=250)

# 6. Analysis and Expert Heuristic Logic
if st.button("Analyze Email Threat"):
    if email_input.strip():
        # Preprocessing & Vectorization
        transformed_input = tfidf.transform([email_input])
        
        # Machine Learning Predictions
        prediction = model.predict(transformed_input)[0]
        probability = model.predict_proba(transformed_input)[0][1] 
        
        # Initialize Heuristic Evaluation Tracking
        red_flags = []
        
        # Normalize input with padded spacing to protect word boundaries
        padded_input = f" {email_input.lower().strip()} "
        # Replace common punctuation with spaces to keep word boundaries isolated
        for punct in ['.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '\n', '\r']:
            padded_input = padded_input.replace(punct, ' ')
        # Standardize multiple spaces into a single space token
        padded_input = " ".join(padded_input.split())
        padded_input = f" {padded_input} "

        # Heuristic 1: Artificial Urgency Matrix
        urgency_keywords = ['urgent', 'immediately', '2 hours', '12 hours', 'action required', 'act now', 'suspended immediately']
        if any(f" {word} " in padded_input for word in urgency_keywords):
            red_flags.append("**Artificial Urgency:** Scammers implement aggressive time pressure matrices to bypass your critical evaluation loops.")
        
        # Heuristic 2: Credential Harvesting Phrasing
        harvesting_keywords = ['verify login', 'update password', 'confirm identity', 'account compromised', 'click here to verify', 'link my identity', 'restrict outward transfers']
        if any(f" {word} " in padded_input for word in harvesting_keywords):
            red_flags.append("**Credential Harvesting:** This email text targets security account verification patterns designed to compromise sensitive user profiles.")
        
        # Heuristic 3: 419 / Nigerian Advance Fee Fraud Tokens
        scam_keywords = ['transfer', 'million', 'inheritance', 'partnership', 'funds', 'prize', 'bvn', 'nin', 'linkage failure']
        if any(f" {word} " in padded_input for word in scam_keywords):
            red_flags.append("🇳🇬 **Advance Fee / Localized Fraud:** Content vectors mirror high-risk patterns traditional to 419 social engineering architectures or local banking identification traps.")

        # Heuristic 4: Unverified Domain / Anchor Detection
        if "http" in email_input.lower():
            trusted_domains = ['amazon.com', 'microsoft.com', 'netflix.com', 'google.com', 'pau.edu.ng']
            if not any(domain in email_input.lower() for domain in trusted_domains):
                red_flags.append("**Suspicious Redirect Hook:** The system detected web hyperlinks containing parameters unverified by regional safety whitelists.")

        st.divider()

        # 7. Unified Multi-Tiered Classification Boundary
        # A threat is confirmed if the ML model signals danger (prediction == 1) AND has supporting probability density,
        # OR if a high volume of explicit psychological red flags are triggered concurrently.
        if (prediction == 1 and probability >= 0.52) or (len(red_flags) >= 2) or (probability >= 0.75):
            st.error(f"[!] THREAT IDENTIFIED | RISK INDEX: {probability*100:.1f}%")
            
            st.markdown("### [?] Educational Breakdown")
            for flag in red_flags:
                st.info(flag)
            
            if not red_flags:
                st.info("**Statistical Inference Match:** The underlying Logistic Regression coefficients isolated structural vocabulary arrays common to historic security threats.")
            
            st.warning("### [!] Recommended Security Protocol")
            st.markdown("""
            * **Don't Click:** Never open hyperlinks or fetch external attachments matching unverified text.
            * **Verify Source:** Meticulously inspect the sender's true domain configuration rather than trusting cosmetic display labels.
            * **Contact Directly:** Reach out to organizational support lines using authenticated contacts independent of the suspicious text message.
            """)
        else:
            # Safe Classification Return
            st.success(f"[OK] ANALYSIS COMPLETE | CERTAINTY: {(1-probability)*100:.1f}%")
            st.markdown("### [+] Why this was marked safe")
            st.write("The evaluated data block maps cleanly inside standard communication distributions and lacks concentrated high-risk social engineering markers.")

    else:
        st.warning("Please paste an email body to analyze.")

# Footer Disclaimer
st.markdown('<p class="footer">PhishNet AI is an educational tool. Use your own judgment for critical security decisions.</p>', unsafe_allow_html=True)