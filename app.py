import streamlit as st
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
import pickle
import os
import plotly.graph_objects as go
from model.feature_extraction import extract_features_from_url
from model.phishing_classifier import PhishingURLClassifier
from utils import load_data, get_explanation_for_features

# Page configuration
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("## 🧭 Explore the app")

# App title and introduction
st.title("🔍 Phishing URL Detector")
st.markdown("""
This application helps you identify potentially malicious phishing URLs using machine learning.
Enter a URL below to check if it's legitimate or potentially harmful.
""")

# Initialize and cache the model
@st.cache_resource
def load_model():
    try:
        model = PhishingURLClassifier()
        model.train_model()  # This will only train if no saved model exists
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# URL input section
st.markdown("### 🌐 Enter a URL to analyze")
url_input = st.text_input("URL", placeholder="https://example.com")

# Prediction section
if st.button("Analyze URL"):
    if not url_input:
        st.warning("⚠️ Please enter a URL to analyze.")
    else:
        try:
            # Basic URL validation
            if not url_input.startswith(('http://', 'https://')):
                url_input = 'http://' + url_input
                
            # Check if the URL format is valid
            try:
                result = urlparse(url_input)
                if not all([result.scheme, result.netloc]):
                    st.error("⚠️ Invalid URL format. Please enter a valid URL.")
                else:
                    with st.spinner("Analyzing the URL..."):
                        # Extract features
                        features = extract_features_from_url(url_input)
                        
                        # Make prediction
                        prediction, confidence = model.predict(features)
                        
                        # Display result
                        st.markdown("### Results")
                        if prediction == 1:
                            st.error(f"🚨 **PHISHING DETECTED!** (Confidence: {confidence:.2f}%)")
                            st.markdown("This URL shows characteristics commonly found in phishing websites.")
                        else:
                            st.success(f"✅ **LEGITIMATE URL** (Confidence: {confidence:.2f}%)")
                            st.markdown("This URL appears to be legitimate based on our analysis.")
                        
                        # Display feature explanation
                        st.markdown("### 🔬 Feature Analysis")
                        st.markdown("Below are the key features extracted from the URL and how they contributed to the prediction:")
                        
                        # Convert features to DataFrame for display
                        feature_df = pd.DataFrame({"Feature": list(features.keys()), "Value": list(features.values())})
                        
                        # Add explanations
                        feature_df["Explanation"] = feature_df["Feature"].apply(lambda x: get_explanation_for_features(x))
                        
                        # Display features
                        st.dataframe(feature_df)
                        
                        # Add interactive visualization of features
                        st.markdown("### 📊 Feature Visualization")
                        
                        # Convert features to DataFrame for visualization
                        features_for_viz = pd.DataFrame({
                            "Feature": list(features.keys()),
                            "Value": list(features.values()),
                            "Impact": [0.25, 0.18, 0.12, 0.15, 0.14, 0.06, 0.10]  # Example feature importance
                        })
                        
                        # Filter only binary features for the radar chart
                        binary_features = features_for_viz[features_for_viz["Feature"].isin(
                            ["has_ip", "has_at_symbol", "has_multiple_subdomains", 
                             "has_suspicious_chars", "has_https", "domain_age_less_than_6months"]
                        )]
                        
                        # Create radar chart columns
                        radar_col1, radar_col2 = st.columns([2, 1])
                        
                        with radar_col1:
                            # Prepare radar chart data
                            categories = binary_features["Feature"].tolist()
                            values = binary_features["Value"].tolist()
                            
                            # Add the first point also at the end to close the polygon
                            categories.append(categories[0])
                            values.append(values[0])
                            
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                name='URL Features',
                                line_color='red' if prediction == 1 else 'green',
                                fillcolor='rgba(255, 0, 0, 0.2)' if prediction == 1 else 'rgba(0, 255, 0, 0.2)'
                            ))
                            
                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(
                                        visible=True,
                                        range=[0, 1]
                                    )
                                ),
                                title="URL Feature Radar Chart",
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with radar_col2:
                            # Add impact color explanation
                            st.markdown("#### What This Means")
                            st.markdown("""
                            The radar chart shows the presence (1) or absence (0) of key features in the URL:
                            
                            - **IP Address**: URLs with IP addresses instead of domain names
                            - **@ Symbol**: Can be used to hide the actual destination
                            - **Multiple Subdomains**: Many subdomains can be suspicious
                            - **Suspicious Characters**: Special characters used to deceive
                            - **HTTPS**: Secure protocol (often present in legitimate sites)
                            - **New Domain**: Domains registered recently
                            
                            A larger "footprint" in the radar chart typically indicates more phishing characteristics.
                            """)
                        
                        # Security recommendations
                        st.markdown("### 🛡️ Security Recommendation")
                        if prediction == 1:
                            st.warning("""
                            **We recommend not visiting this URL.** If you've already entered information on this site, 
                            consider changing your passwords and monitoring your accounts for suspicious activity.
                            """)
                        else:
                            st.info("""
                            While this URL appears legitimate, always practice good security habits:
                            - Verify the sender if you received this link via email
                            - Check for HTTPS before entering sensitive information
                            - Keep your browser and security software updated
                            """)
            except ValueError:
                st.error("⚠️ Invalid URL format. Please enter a valid URL.")
                
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.markdown("Please try again with a different URL or contact support if the issue persists.")

# Additional information
st.markdown("---")
st.markdown("""
### 📊 Want to learn more?

Check out the **Visual Insights** and **About Phishing** pages for:
- Statistical analysis of phishing URLs
- Interactive visualizations of URL characteristics
- Educational content about phishing attacks
- Tips to protect yourself online

Navigate using the sidebar menu.
""")

# App footer
st.markdown("---")
st.markdown("### 📚 References")
st.markdown("""
- Anti-Phishing Working Group (APWG): [https://apwg.org/](https://apwg.org/)
- Google Safe Browsing: [https://safebrowsing.google.com/](https://safebrowsing.google.com/)
- FBI Internet Crime Complaint Center (IC3): [https://www.ic3.gov/](https://www.ic3.gov/)
""")

# Add creator footer
st.markdown("---")
st.markdown("*Created by OmGolesar*", help="Phishing URL Detection Project")
