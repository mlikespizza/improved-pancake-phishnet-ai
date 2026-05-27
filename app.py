import streamlit as st
import joblib

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(page_title="PhishNet AI", page_icon="🤺", layout="centered")

# 2. Load the saved model and vectorizer (Without Cache to prevent Cloud memory crashes)
try:
    model = joblib.load('phishnet_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
except Exception as e:
    st.error("Model files not found. Please ensure phishnet_model.pkl and tfidf_vectorizer.pkl are uploaded.")

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
email_input = st.text_area("Email Content", label_visibility="collapsed", placeholder="Paste the suspicious email text here...", height=250)

# 6. Analysis and Expert Heuristic Logic
if st.button("Analyze Email Threat"):
    if email_input.strip():
        # Preprocessing & Vectorization
        transformed_input = tfidf.transform([email_input])
        
        # Machine Learning Predictions
        probability = model.predict_proba(transformed_input)[0][1] 
        
        # Initialize Heuristic Evaluation Tracking
        red_flags = []
        
        # Normalize input with strict spaces to isolate words
        clean_input = " " + email_input.lower() + " "
        for punct in ['.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}', '\n', '\r', '"', "'", '-']:
            clean_input = clean_input.replace(punct, ' ')
        padded_input = " " + " ".join(clean_input.split()) + " "

        # Heuristic 1: Artificial Urgency Matrix
        urgency_keywords = ['urgent', 'immediately', '2 hours', '12 hours', 'action required', 'act now', 'suspended', 'suspension', 'deadline']
        if any(f" {word} " in padded_input for word in urgency_keywords):
            red_flags.append("**Artificial Urgency:** Scammers implement aggressive time pressure matrices to bypass your critical evaluation loops.")
        
        # Heuristic 2: Credential Harvesting Phrasing
        harvesting_keywords = ['verify', 'login', 'password', 'identity', 'compromised', 'restricted', 'bvn', 'nin', 'linkage', 'restriction']
        if any(f" {word} " in padded_input for word in harvesting_keywords):
            red_flags.append("**Credential Harvesting Target:** The email text targets security verification patterns or account linkage dependencies.")
        
        # Heuristic 3: 419 / Financial Fraud Tokens
        scam_keywords = ['transfer', 'transfers', 'million', 'inheritance', 'partnership', 'funds', 'prize', 'claim', 'central bank']
        if any(f" {word} " in padded_input for word in scam_keywords):
            red_flags.append("🇳🇬 **Advance Fee / Localized Fraud:** Semantic tokens match risk profiles common to traditional 419 social engineering architectures.")

        # Heuristic 4: Link Safety Check (Removed generic "link" keyword to stop false positives)
        if "http" in email_input.lower():
            trusted_domains = ['amazon.com', 'microsoft.com', 'netflix.com', 'google.com', 'pau.edu.ng', 'youversion']
            if not any(domain in email_input.lower() for domain in trusted_domains):
                red_flags.append("**Unverified Hyperlink Redirect:** The system detected web redirect parameters unverified by trusted infrastructure whitelists.")

        st.divider()

        # 7. Intelligent Multi-Tiered Classification Boundary
        flag_count = len(red_flags)
        
        # Base condition: The ML model is highly confident it's a threat (>70%)
        if probability >= 0.70:
            is_threat = True
        # Safety Valve: There are MULTIPLE severe behavioral red flags (Catches the BVN-NIN email)
        elif flag_count >= 2:
            is_threat = True
        # Borderline Case: Model is suspicious (>40%) AND there is at least one red flag
        elif probability >= 0.40 and flag_count >= 1:
            is_threat = True
        else:
            is_threat = False

        # Dynamic Risk Calculator for Display
        if is_threat:
            if flag_count > 0:
                # Add a 20% penalty per heuristic flag to accurately represent structural risk
                boost = flag_count * 0.20
                display_probability = min(probability + boost, 0.99)
            else:
                display_probability = probability
            
            st.error(f"[!] THREAT IDENTIFIED | RISK INDEX: {display_probability*100:.1f}%")
            
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
            # For safe emails, display the actual safety certainty (100% - risk probability)
            st.success(f"[OK] ANALYSIS COMPLETE | CERTAINTY: {(1-probability)*100:.1f}%")
            st.markdown("### [+] Why this was marked safe")
            st.write("The evaluated data block maps cleanly inside standard safe communication distributions and lacks concentrated high-risk social engineering markers.")

    else:
        st.warning("Please paste an email body to analyze.")

st.markdown('<p class="footer">PhishNet AI is an educational tool. Use your own judgment for critical security decisions.</p>', unsafe_allow_html=True)