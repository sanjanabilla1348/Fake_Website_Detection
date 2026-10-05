import streamlit as st
import pandas as pd
import pickle
import re
from urllib.parse import urlparse

# Page settings
st.set_page_config(
    page_title="Fake Website Detection",
    page_icon="🔍",
    layout="centered"
)

# Title
st.title("🔍 Fake Website Detection")
st.write(
    "Enter a website URL below to check whether it is "
    "likely safe or suspicious."
)

st.divider()

# Load trained model
with open("fake_website_model.pkl", "rb") as file:
    model = pickle.load(file)


# Feature extraction function
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
        1 for word in suspicious_words_list
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


# URL input
url = st.text_input(
    "🌐 Enter Website URL",
    placeholder="example.com"
)


# Check button
if st.button(
    "🔎 Check Website",
    use_container_width=True
):

    if url.strip() == "":
        st.warning("⚠️ Please enter a website URL.")

    else:

        # Extract features
        features = extract_features(url.strip())

        # Prediction
        prediction = model.predict(features)[0]

        # Probability
        probability = model.predict_proba(features)[0]

        safe_probability = probability[0] * 100
        fake_probability = probability[1] * 100

        st.divider()

        # Result
        st.subheader("📊 Detection Result")

        if prediction == 0:

            st.success("✅ Likely Safe")

            st.metric(
                "Safe Probability",
                f"{safe_probability:.2f}%"
            )

            st.info(
                "This website appears safe based on the "
                "features used by the trained model."
            )

        else:

            st.error("🚨 Fake / Suspicious")

            st.metric(
                "Suspicious Probability",
                f"{fake_probability:.2f}%"
            )

            st.warning(
                "This website contains features that may "
                "indicate a suspicious or fake website."
            )

        # Features
        st.divider()

        st.subheader("🔎 Website Features")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "🔒 HTTPS:",
                "Yes" if features["https"][0] else "No"
            )

            st.write(
                "🌐 IP Address:",
                "Yes" if features["ip_address"][0] else "No"
            )

            st.write(
                "📏 URL Length:",
                features["url_length"][0]
            )

            st.write(
                "⚠️ @ Symbol:",
                "Yes" if features["at_symbol"][0] else "No"
            )

        with col2:

            st.write(
                "➖ Hyphen:",
                "Yes" if features["hyphen"][0] else "No"
            )

            st.write(
                "🔵 Number of Dots:",
                features["dots"][0]
            )

            st.write(
                "🚩 Suspicious Words:",
                features["suspicious_words"][0]
            )

        # URL entered
        st.divider()

        st.subheader("🌐 Website Checked")

        st.code(url.strip())

# About section
st.divider()

with st.expander("ℹ️ About this Project"):

    st.write(
        "This Fake  Website Detection system uses a "
        "Machine Learning model to classify website URLs "
        "as Safe or Fake/Suspicious."
    )

    st.write("The model analyzes features such as:")

    st.write("• HTTPS usage")
    st.write("• IP address")
    st.write("• URL length")
    st.write("• @ symbol")
    st.write("• Hyphens")
    st.write("• Number of dots")
    st.write("• Suspicious words")

    st.write(
        "The model was trained using a sample website dataset "
        "and should not be considered a guarantee that a website "
        "is completely safe."
    )

st.caption(
    "🔐 Fake Website Detection | Machine Learning Project"
)