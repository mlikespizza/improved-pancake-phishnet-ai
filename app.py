import streamlit as st
import joblib

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(page_title="PhishNet AI", page_icon="🤺", layout="centered")

# 2. Load the saved model and vectorizer
try:
    model = joblib.load('phishnet_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
except:
    st.error("Model files not found. Please run train_model.py first.")

# 3. Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 50px !important; font-weight: 800; color: #60a5fa; text-align: center; }
    .sub-text { font-size: 18px; color: #94a3b8; text-align: center; margin-bottom: 30px; }
    .stTextArea textarea { background-color: #1e293b !important; color: #e2e8f0 !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
    div.stButton > button { width: 100%; background-color: #3b82f6 !important; color: white !important; font-weight: bold !important; padding: 15px !important; border-radius: 8px !important; }
    .footer { font-size: 12px; color: #64748b; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 4. UI Content
st.markdown('<p class="main-title">PhishNet AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Check if an email is a phishing trap.</p>', unsafe_allow_html=True)

email_input = st.text_area("", placeholder="Paste the suspicious email text here...", height=250)

# 5. The Analysis & Education Logic
if st.button("Analyze Email Threat"):
    if email_input.strip():
        # ML Prediction & Confidence Calculation
        transformed_input = tfidf.transform([email_input])
        prediction = model.predict(transformed_input)[0]
        probability = model.predict_proba(transformed_input)[0][1] 
        
        # Educational Flag Detection
        red_flags = []
        
        # Heuristic 1: Check for Urgency
        if any(word in email_input.lower() for word in ['urgent', 'immediately', '2 hours', 'action required']):
            red_flags.append("**Artificial Urgency:** Scammers use time pressure to bypass your critical thinking.")
        
        # Heuristic 2: Refined Credential Harvesting check
        if any(word in email_input.lower() for word in ['verify login', 'update password', 'confirm identity', 'account compromised', 'click here to verify']):
            red_flags.append("**Credential Harvesting:** This email likely leads to a fake login page designed to steal your data.")
        
        # Heuristic 3: Check for 419 (Nigerian) Markers
        if any(word in email_input.lower() for word in ['transfer', 'million', 'inheritance', 'partnership', 'funds']):
            red_flags.append("🇳🇬 **Advance Fee Fraud:** Matches patterns found in traditional '419' or Nigerian fraud tactics.")

        # Heuristic 4: Suspicious Links / Domain Spoofing
        if "http" in email_input.lower() and not any(domain in email_input.lower() for domain in ['amazon.com', 'microsoft.com', 'netflix.com', 'google.com', 'pau.edu.ng']):
            if any(bank in email_input.lower() for bank in ['bank', 'secure', 'verify', 'login', 'service']):
                red_flags.append("**Domain Spoofing:** The link looks suspicious. Scammers often use 'secure-verify' or unofficial domains to mimic real institutions.")

        st.divider()

        # Final Display Logic
        if prediction == 1 or probability > 0.7 or len(red_flags) > 0:
            st.error(f"[!] THREAT IDENTIFIED | RISK INDEX: {probability*100:.1f}%")
            
            st.markdown("### [?] Educational Breakdown")
            for flag in red_flags:
                st.info(flag)
            
            if not red_flags:
                st.info("**Statistical Match:** The AI detected hidden linguistic structures common in phishing attacks.")
            
            st.warning("### [!] Recommended Security Protocol")
            st.markdown("""
            * **Don't Click:** Never click links or download attachments from suspicious senders.
            * **Verify Source:** Check the sender's actual email address, not just the display name.
            * **Contact Directly:** If it claims to be your bank or service provider, call them using the official number on their website.
            """)
        else:
            st.success(f"[OK] ANALYSIS COMPLETE | CERTAINTY: {(1-probability)*100:.1f}%")
            st.markdown("### [+] Why this was marked safe")
            st.write("This email follows standard professional structures and lacks common 'threat' keywords.")

    else:
        st.warning("Please paste an email body to analyze.")

st.markdown('<p class="footer">PhishNet AI is an educational tool. Use your own judgment for critical security decisions.</p>', unsafe_allow_html=True)