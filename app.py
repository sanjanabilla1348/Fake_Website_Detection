import streamlit as st
import pandas as pd
import pickle
import re
from urllib.parse import urlparse

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="WebGuard - Fake Website Detection",
    page_icon="🔐",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Main Header */
.main-header {
    text-align: center;
    padding: 20px;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

/* Online Status */
.status {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
    font-weight: 600;
}

/* Cards */
.card {
    padding: 25px;
    border-radius: 15px;
    background-color: white;
    border: 1px solid #e6e9ef;
    margin-bottom: 20px;
}

/* Result Card */
.safe-card {
    padding: 30px;
    border-radius: 18px;
    background-color: #eaf8ef;
    border: 2px solid #4caf50;
    text-align: center;
    margin-top: 20px;
}

.fake-card {
    padding: 30px;
    border-radius: 18px;
    background-color: #fff0f0;
    border: 2px solid #f44336;
    text-align: center;
    margin-top: 20px;
}

.result-title {
    font-size: 32px;
    font-weight: 700;
}

.confidence {
    font-size: 22px;
    font-weight: 600;
    margin-top: 10px;
}

/* Feature Cards */
.feature-card {
    padding: 20px;
    border-radius: 14px;
    background-color: white;
    border: 1px solid #e5e7eb;
    min-height: 125px;
    margin-bottom: 15px;
}

.feature-icon {
    font-size: 28px;
}

.feature-name {
    font-size: 15px;
    color: #666;
    margin-top: 5px;
}

.feature-value {
    font-size: 20px;
    font-weight: 600;
}

/* Section Title */
.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Info Cards */
.info-card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    border: 1px solid #e6e9ef;
    text-align: center;
    min-height: 140px;
}

.info-number {
    font-size: 30px;
    font-weight: 700;
}

.info-label {
    color: #666;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    padding: 30px;
    margin-top: 30px;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
}

/* URL input */
.stTextInput input {
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="main-header">

<div class="main-title">
🔐 WebGuard
</div>

<div class="subtitle">
Fake Website Detection System
</div>

<div class="status">
🟢 SYSTEM ONLINE
</div>

</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#666;'>"
    "AI-powered URL security analysis using Machine Learning"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

try:

    with open("fake_website_model.pkl", "rb") as file:
        model = pickle.load(file)

except FileNotFoundError:

    st.error(
        "❌ Model file not found. "
        "Please make sure fake_website_model.pkl "
        "is in the same folder as app.py."
    )

    st.stop()

# --------------------------------------------------
# FEATURE EXTRACTION
# --------------------------------------------------

def extract_features(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    # HTTPS
    https = 1 if parsed.scheme == "https" else 0

    # IP address
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    ip_address = 1 if re.match(
        ip_pattern,
        domain.split(":")[0]
    ) else 0

    # URL length
    url_length = len(url)

    # @ symbol
    at_symbol = 1 if "@" in url else 0

    # Hyphen
    hyphen = 1 if "-" in domain else 0

    # Number of dots
    dots = domain.count(".")

    # Suspicious words
    suspicious_words_list = [
        "login",
        "verify",
        "verification",
        "account",
        "update",
        "secure",
        "security",
        "bank",
        "payment",
        "confirm",
        "password",
        "free",
        "winner",
        "bonus",
        "claim",
        "urgent"
    ]

    suspicious_words = sum(
        1
        for word in suspicious_words_list
        if word in url.lower()
    )

    features = pd.DataFrame(
        [[
            https,
            ip_address,
            url_length,
            at_symbol,
            hyphen,
            dots,
            suspicious_words
        ]],
        columns=[
            "https",
            "ip_address",
            "url_length",
            "at_symbol",
            "hyphen",
            "dots",
            "suspicious_words"
        ]
    )

    return features

# --------------------------------------------------
# URL CHECKER
# --------------------------------------------------

st.markdown(
    "<div class='section-title'>🌐 Analyze a Website</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='card'>"
    "<b>Enter a website URL</b><br>"
    "<span style='color:#666;'>"
    "Our Machine Learning model will analyze the URL "
    "for suspicious characteristics."
    "</span>"
    "</div>",
    unsafe_allow_html=True
)

url = st.text_input(
    "Website URL",
    placeholder="example.com or https://example.com",
    label_visibility="collapsed"
)

check_button = st.button(
    "🔎 ANALYZE WEBSITE",
    use_container_width=True
)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if check_button:

    if url.strip() == "":

        st.warning(
            "⚠️ Please enter a website URL first."
        )

    else:

        clean_url = url.strip()

        # Extract features
        features = extract_features(clean_url)

        # Prediction
        prediction = model.predict(features)[0]

        # Probability
        probability = model.predict_proba(features)[0]

        safe_probability = probability[0] * 100
        fake_probability = probability[1] * 100

        st.divider()

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        st.markdown(
            "<div class='section-title'>📊 Security Analysis Result</div>",
            unsafe_allow_html=True
        )

        if prediction == 0:

            st.markdown(
                f"""
                <div class="safe-card">

                <div class="result-title">
                🟢 LIKELY SAFE
                </div>

                <div class="confidence">
                Confidence: {safe_probability:.2f}%
                </div>

                <p>
                No major suspicious characteristics were
                detected by the trained model.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                int(safe_probability)
            )

        else:

            st.markdown(
                f"""
                <div class="fake-card">

                <div class="result-title">
                🔴 FAKE / SUSPICIOUS
                </div>

                <div class="confidence">
                Suspicious Probability: {fake_probability:.2f}%
                </div>

                <p>
                This URL contains characteristics that may
                indicate a suspicious or fake website.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                int(fake_probability)
            )

        # --------------------------------------------------
        # WEBSITE FEATURES
        # --------------------------------------------------

        st.markdown(
            "<div class='section-title'>🔍 Website Features</div>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        # HTTPS
        with col1:

            https_value = (
                "Enabled"
                if features["https"][0]
                else "Not Enabled"
            )

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🔒</div>

                <div class="feature-name">
                HTTPS
                </div>

                <div class="feature-value">
                {https_value}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # IP Address
        with col2:

            ip_value = (
                "Detected"
                if features["ip_address"][0]
                else "Not Detected"
            )

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🌐</div>

                <div class="feature-name">
                IP Address
                </div>

                <div class="feature-value">
                {ip_value}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # URL Length
        with col3:

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">📏</div>

                <div class="feature-name">
                URL Length
                </div>

                <div class="feature-value">
                {features["url_length"][0]} characters
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        col4, col5, col6 = st.columns(3)

        # @ Symbol
        with col4:

            at_value = (
                "Detected"
                if features["at_symbol"][0]
                else "Not Detected"
            )

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">⚠️</div>

                <div class="feature-name">
                @ Symbol
                </div>

                <div class="feature-value">
                {at_value}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # Hyphen
        with col5:

            hyphen_value = (
                "Detected"
                if features["hyphen"][0]
                else "Not Detected"
            )

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">➖</div>

                <div class="feature-name">
                Hyphen
                </div>

                <div class="feature-value">
                {hyphen_value}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # Dots
        with col6:

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🔵</div>

                <div class="feature-name">
                Number of Dots
                </div>

                <div class="feature-value">
                {features["dots"][0]}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        col7, col8, col9 = st.columns(3)

        # Suspicious Words
        with col7:

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🚩</div>

                <div class="feature-name">
                Suspicious Words
                </div>

                <div class="feature-value">
                {features["suspicious_words"][0]} detected
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # Safe probability
        with col8:

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🟢</div>

                <div class="feature-name">
                Safe Probability
                </div>

                <div class="feature-value">
                {safe_probability:.2f}%
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # Fake probability
        with col9:

            st.markdown(
                f"""
                <div class="feature-card">

                <div class="feature-icon">🔴</div>

                <div class="feature-name">
                Suspicious Probability
                </div>

                <div class="feature-value">
                {fake_probability:.2f}%
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # WEBSITE CHECKED
        # --------------------------------------------------

        st.markdown(
            "<div class='section-title'>🌐 Website Checked</div>",
            unsafe_allow_html=True
        )

        st.code(
            clean_url,
            language="text"
        )

# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.divider()

st.markdown(
    "<div class='section-title'>⚙️ How It Works</div>",
    unsafe_allow_html=True
)

step1, step2, step3, step4 = st.columns(4)

with step1:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">1️⃣</div>

        <b>Enter URL</b>

        <p class="info-label">
        User enters a website address.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with step2:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">2️⃣</div>

        <b>Extract Features</b>

        <p class="info-label">
        URL characteristics are analyzed.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with step3:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">3️⃣</div>

        <b>ML Analysis</b>

        <p class="info-label">
        Random Forest analyzes the features.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with step4:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">4️⃣</div>

        <b>Prediction</b>

        <p class="info-label">
        Website is classified as safe or suspicious.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.markdown(
    "<div class='section-title'>🤖 Model Information</div>",
    unsafe_allow_html=True
)

model1, model2, model3, model4 = st.columns(4)

with model1:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">🌲</div>

        <b>Random Forest</b>

        <p class="info-label">
        Machine Learning Model
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with model2:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">100%</div>

        <b>Test Accuracy</b>

        <p class="info-label">
        On sample test dataset
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with model3:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">41</div>

        <b>Dataset URLs</b>

        <p class="info-label">
        Sample website dataset
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with model4:

    st.markdown(
        """
        <div class="info-card">

        <div class="info-number">7</div>

        <b>URL Features</b>

        <p class="info-label">
        Features analyzed
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# SECURITY TIPS
# --------------------------------------------------

st.markdown(
    "<div class='section-title'>🛡️ Website Safety Tips</div>",
    unsafe_allow_html=True
)

with st.expander("🔐 Click to view security tips"):

    st.write(
        "• Always check whether the website uses HTTPS."
    )

    st.write(
        "• Carefully check the domain name before entering information."
    )

    st.write(
        "• Avoid clicking suspicious links from unknown sources."
    )

    st.write(
        "• Never enter passwords or payment information on unknown websites."
    )

    st.write(
        "• Be careful with websites asking for urgent verification or payment."
    )

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

with st.expander("ℹ️ About This Project"):

    st.write(
        "WebGuard is a Machine Learning-based Fake Website "
        "Detection application."
    )

    st.write(
        "The system analyzes URL characteristics such as "
        "HTTPS usage, IP addresses, URL length, @ symbols, "
        "hyphens, dots, and suspicious words."
    )

    st.write(
        "A Random Forest Classifier is used to classify "
        "the website as likely safe or fake/suspicious."
    )

    st.warning(
        "This application is an educational Machine Learning "
        "project. Its prediction should not be treated as a "
        "guarantee that a website is completely safe."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">

    🔐 <b>WebGuard - Fake Website Detection</b>

    <br><br>

    Machine Learning Project | Python | Streamlit

    </div>
    """,
    unsafe_allow_html=True
)