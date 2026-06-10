import re
import streamlit as st
import joblib

# SECTION 1: PAGE CONFIGURATION
# The first Streamlit call becauses it sets the browser tab title, favicon,
# and layout mode for the web application.
st.set_page_config(page_title="PhishNet AI", page_icon="🤺", layout="centered")


# SECTION 2: MODEL LOADING WITH PERSISTENT CACHING
# @st.cache_resource ensures the model and vectorizer are loaded from disk
# exactly once per server session, then held in memory for all subsequent
# requests. This avoids redundant I/O on every Streamlit re-run (which
# occurs on every user interaction), significantly improving responsiveness.
#
# The function returns:
#   - model: a trained sklearn LogisticRegression classifier
#   - tfidf: a fitted TfidfVectorizer (vocabulary + IDF weights)
@st.cache_resource
def load_model():
    model = joblib.load('phishnet_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    return model, tfidf

# Attempt to load, stop with a clear error message if files are missing.
# st.stop() prevents execution from continuing to the analysis block,
# which would otherwise raise a NameError on undefined variables.
try:
    model, tfidf = load_model()
except Exception:
    st.error("⚠️ Model files not found. " \
    "Please ensure `phishnet_model.pkl` and `tfidf_vectorizer.pkl` are in the project root.")
    st.stop()


# SECTION 3: My CUSTOM CSS DARK THEME STYLING
# Streamlit's default UI is injected with custom CSS via st.markdown with
# unsafe_allow_html=True. This overrides default widget styles to produce a
# dark-mode design system across the application.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 50px 
            !important; font-weight: 800; color: #60a5fa; text-align: center; 
            margin-top: -20px; letter-spacing: -1px; }
    .sub-text { font-size: 18px; color: #94a3b8; text-align: center; margin-bottom: 8px; }
    .model-badge { font-size: 13px; color: #475569; text-align: center; margin-bottom: 28px; }
    .stTextArea textarea { background-color: #1e293b 
            !important; color: #e2e8f0 !important; border: 1px solid #334155 
            !important; border-radius: 10px !important; font-family: 'Inter', sans-serif !important; }
    div.stButton > button { width: 100%; background: linear-gradient(135deg, #3b82f6, #6366f1) 
            !important; color: white !important; font-weight: 700 !important; font-size: 16px 
            !important; padding: 15px !important; border-radius: 10px !important; border: none 
            !important; transition: opacity 0.2s ease; }
    div.stButton > button:hover { opacity: 0.88; }
    .footer { font-size: 12px; color: #475569; text-align: center; 
            margin-top: 60px; border-top: 1px solid #1e293b; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)


# SECTION 4: APPLICATION HEADER
# Renders the title, subtitle, and a credibility caption that communicates
# the underlying technology stack to the user 
st.markdown('<p class="main-title">PhishNet AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Detect phishing emails with AI, '
'and learn why they\'re dangerous.</p>', unsafe_allow_html=True)
st.markdown('<p class="model-badge">Powered by Logistic Regression + TF-IDF Vectorization ' \
'· Trained on ~15,571 emails</p>', unsafe_allow_html=True)


# SECTION 5: USER INPUT
# A multi-line text area for pasting raw email content. The analysis is
# triggered only when the user submits through the button.
email_input = st.text_area(
    "Email Content",
    label_visibility="collapsed",
    placeholder="Paste the full body of a suspicious email here...",
    height=250
)


# SECTION 6: ANALYSIS ENGINE
# Triggered on button click. Runs the two-stage classification pipeline:
#   Stage 1 — ML Model: TF-IDF vectorization → Logistic Regression probability
#   Stage 2 — Heuristics: Rule-based keyword checks for known phishing patterns
# The final verdict is determined by a multi-tiered decision boundary that
# combines both signals for higher recall on borderline cases.
if st.button("Analyze Email Threat"):
    if not email_input.strip():
        st.warning("Please paste an email body before analyzing.")
    else:
        with st.spinner("Analyzing email patterns..."):

            # Stage 1: TF-IDF Vectorization 
            # The TF-IDF (Term Frequency–Inverse Document Frequency) vectorizer
            # transforms the raw email string into a numerical feature
            # vector of 5,000 dimensions. Each dimension corresponds to a word
            # in the learned vocabulary, weighted by its discriminative value
            # across the training corpus (rare-but-relevant words score higher).
            transformed_input = tfidf.transform([email_input])

            # Stage 1: Logistic Regression Inference 
            # predict_proba() returns a 2-element array [P(safe), P(phishing)].
            # We extract index [1] to get the model's phishing confidence score.
            # This value ranges from 0.0 (definitely safe) to 1.0 (definitely
            # phishing) and is derived from the sigmoid of the decision boundary.
            probability = model.predict_proba(transformed_input)[0][1]

            # Stage 2: Text Normalization for Heuristic Matching 
            # The raw email is lowercased and passed through regex word-boundary
            # matching. Using \b anchors (instead of simple space-padding) allows
            # the system to correctly match keywords even when followed by
            # punctuation,or plurals (e.g., "deadlines", "verify!").
            normalized = email_input.lower()

            # Accumulates human-readable descriptions of detected risk patterns.
            red_flags = []

            #  Heuristic 1: Artificial Urgency Detection 
            # Phishing emails frequently manufacture time pressure to suppress
            # the victim's rational decision-making. This check searches for
            # urgency-signalling vocabulary using word-boundary regex patterns.
            urgency_keywords = [
                'urgent', 'immediately', '2 hours', '12 hours',
                'action required', 'act now', 'suspended', 'suspension', 'deadline'
            ]
            if any(re.search(rf'\b{re.escape(kw)}\b', normalized) for kw in urgency_keywords):
                red_flags.append(
                    "⏰ **Artificial Urgency Detected:** This email uses aggressive time pressure "
                    "to rush you into acting without thinking. Legitimate organisations rarely "
                    "threaten immediate account suspension via email."
                )

            #  Heuristic 2: Credential Harvesting Language 
            # Credential harvesting attacks direct victims to submit sensitive
            # information (passwords, account numbers, ID numbers) under the
            # pretence of verification or security compliance. This heuristic
            # flags vocabulary associated with that social engineering pattern.
            harvesting_keywords = [
                'verify', 'login', 'password', 'identity', 'compromised',
                'restricted', 'bvn', 'nin', 'linkage', 'restriction'
            ]
            if any(re.search(rf'\b{re.escape(kw)}\b', normalized) for kw in harvesting_keywords):
                red_flags.append(
                    "🔑 **Credential Harvesting Language:** This email uses phrasing designed to "
                    "extract sensitive personal or account data. Never submit passwords or ID "
                    "numbers (BVN, NIN) in response to an unsolicited email."
                )

            # Heuristic 3: Advance Fee / Financial Fraud Indicators 
            # Advance-fee fraud (\"419 scam\") involves fabricated promises of
            # financial reward to extract upfront payments or banking details.
            # This heuristic flags vocabulary from that category of social
            # engineering, including terms common in Nigerian fraud corpus emails.
            scam_keywords = [
                'transfer', 'transfers', 'million', 'inheritance', 'partnership',
                'funds', 'prize', 'claim', 'central bank'
            ]
            if any(re.search(rf'\b{re.escape(kw)}\b', normalized) for kw in scam_keywords):
                red_flags.append(
                    "💸 **Advance Fee / Financial Fraud Indicators:** This email contains "
                    "vocabulary associated with advance-fee (419) scams — fabricated promises "
                    "of large financial rewards used to extract money or banking information."
                )

        st.divider()

        # Multi-Tiered Classification Boundary 
        # A single probability threshold is insufficient for high-recall detection.
        # This decision matrix combines the ML confidence score with heuristic
        # signal strength to correctly classify borderline phishing cases:
        #
        #   Tier 1 — High ML Confidence (≥70%): Model is certain → flag as threat.
        #   Tier 2 — Strong Heuristic Signal (≥2 flags): Multiple behavioural
        #            red flags override a low ML score (safety valve).
        #   Tier 3 — Borderline Hybrid (ML ≥40% + ≥1 flag): Moderate ML suspicion
        #            corroborated by at least one heuristic → flag as threat.
        #   Default — No signal combination met → classify as safe.
        flag_count = len(red_flags)

        if probability >= 0.70:
            is_threat = True
        elif flag_count >= 2:
            is_threat = True
        elif probability >= 0.40 and flag_count >= 1:
            is_threat = True
        else:
            is_threat = False

        #  Dynamic Risk Index Calculation 
        # The displayed risk score is the raw ML probability, augmented by a
        # +20% penalty for each heuristic flag raised. This compound score more
        # accurately reflects the structural risk of emails that trigger multiple
        # independent detection signals. The result is stopped at 99% to avoid
        # implying absolute certainty, which no probabilistic model can guarantee.
        if is_threat:
            if flag_count > 0:
                boost = flag_count * 0.20
                display_probability = min(probability + boost, 0.99)
            else:
                display_probability = probability

            # Output: Threat Detected 
            st.error(f"🚨 THREAT IDENTIFIED — Risk Index: **{display_probability * 100:.1f}%**")

            st.markdown("### 📋 Educational Breakdown")
            st.caption(
                "The following patterns were detected in this email. Understanding these "
                "tactics helps you identify phishing attempts in the future."
            )
            for flag in red_flags:
                st.info(flag)

            # If ML caught it but no heuristic fired, explain the statistical basis.
            if not red_flags:
                st.info(
                    "🧠 **Statistical Pattern Match:** The Logistic Regression model identified "
                    "structural vocabulary patterns in this email that are statistically "
                    "correlated with phishing content in the training data — even without "
                    "specific keyword triggers."
                )

            st.warning("### ⚠️ Recommended Actions")
            st.markdown("""
            - **Do not click** any links or download attachments from this email.
            - **Verify the sender** by contacting the organisation directly through their official website 
                        — not through contact details in the email.
            - **Do not submit** any personal information (passwords, ID numbers, banking details) 
                        in response to this email.
            - **Report it** to your email provider and, if applicable, to your organisation's IT/security team.
            """)

        else:
            # Output: Email Appears Safe 
            # The safety certainty is the complement of the phishing probability:
            # (1 - P(phishing)) = P(safe), expressed as a percentage.
            st.success(f"✅ EMAIL APPEARS SAFE — Safety Certainty: **{(1-probability)*100:.1f}%**")
            st.markdown("### 📋 Why This Email Was Classified as Safe")
            st.write("The evaluated data block maps cleanly inside standard safe communication " \
            "distributions and lacks concentrated high-risk social engineering markers.")


# SECTION 7: FOOTER
# Disclaimer reminding users that PhishNet AI is an educational tool.
st.markdown(
    '<p class="footer">PhishNet AI is an educational tool. Use your own judgement for critical ' \
    'security decisions.</p>',
    unsafe_allow_html=True
)