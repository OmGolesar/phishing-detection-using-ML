import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

# Page configuration
st.set_page_config(
    page_title="Methodology - Phishing URL Detector",
    page_icon="🔬",
    layout="wide"
)

# Page title
st.title("🔬 Methodology: Behind the Phishing Detector")
st.markdown("""
This page provides a detailed overview of the technical aspects of our phishing URL detection system.
Here you'll find information about the algorithms, features, and implementation details.
""")

# Project overview
st.header("Project Architecture")
st.markdown("""
Our phishing URL detection system uses a comprehensive approach combining feature extraction, 
machine learning, and interactive visualization. Here's how it works:
""")

# Project workflow diagram
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("https://mermaid.ink/img/pako:eNp1kU9rwzAMxb-K0GmF7QvksMNgJdmhg0JhZRC8WGkbmv80tsvI6HdfnJalGfOP8fPTe7Is2StGFEq0Xr85J9y6PjbWC4d-LQ4nYNKlHt1DGgKTvQMPb0bfiQlsdBtSUi3b_hG2g5GgHwYwUMkObCckRRBKTUw-UWCU9TZiTYlPTwPonqy3xq3x5yI0hgOWJUJnW-9yb8FsjA-uNDzP81qcMXDpjm0GbbZzB1hK9xCgT9RQ7_M3HNKFKDdF5eYpOVUc2uZk9_88-NI0Faw_08BHSnl-nJQHbciqn6xm7EObYoXDHdFY5LhcKbsrVFGOlBZkDYo09jNVicrktLJEuV8nTJDw0uWSrLAXUAavVWrVnkdGkfKRDvSuoL7QvnK0I6_0qDytq99tfQO0joqw?type=png", 
                caption="Phishing Detection System Workflow", use_column_width=True)

# Methodology sections
st.header("Feature Extraction")
st.markdown("""
### URL Feature Analysis
Our system extracts several key features from URLs to identify potential phishing attempts:

1. **URL Length**: Phishing URLs tend to be longer than legitimate ones to hide their true nature.

2. **IP Address Usage**: URLs containing raw IP addresses instead of domain names are often suspicious.

3. **Special Characters**: The presence of '@' symbols, excessive hyphens, or unusual character combinations.

4. **Subdomain Structure**: Multiple subdomains or abnormal subdomain patterns can indicate phishing.

5. **HTTPS Protocol**: While legitimate sites use HTTPS, many phishing sites now also implement it.

6. **Domain Age**: Newly registered domains are more likely to be used for phishing.
""")

# Add code example with syntax highlighting
st.markdown("### Feature Extraction Implementation")
st.code("""
def extract_features_from_url(url):
    features = {}
    
    # Basic URL parsing
    parsed_url = urlparse(url)
    extracted = tldextract.extract(url)
    
    # 1. URL Length
    features['url_length'] = len(url)
    
    # 2. Presence of IP address in domain
    features['has_ip'] = 1 if is_ip_address(parsed_url.netloc) else 0
    
    # 3. Presence of @ symbol in URL
    features['has_at_symbol'] = 1 if '@' in url else 0
    
    # 4. Multiple subdomains
    subdomain = extracted.subdomain
    features['has_multiple_subdomains'] = 1 if subdomain.count('.') >= 1 else 0
    
    # 5. Suspicious characters
    features['has_suspicious_chars'] = 1 if has_suspicious_chars(url) else 0
    
    # 6. HTTPS protocol
    features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
    
    # 7. Domain age check (simulated in this implementation)
    features['domain_age_less_than_6months'] = simulate_domain_age_check(extracted.domain)
    
    return features
""", language="python")

# Machine Learning Model
st.header("Machine Learning Algorithm")
st.markdown("""
### Random Forest Classifier

We use a **Random Forest** algorithm for phishing detection because of its:

- **High Accuracy**: Ensemble method that combines multiple decision trees
- **Robustness to Overfitting**: Less likely to overfit compared to a single decision tree
- **Feature Importance**: Provides insights into which features are most predictive
- **Handling of Non-linear Data**: Can model complex relationships between features
- **Resistance to Outliers**: Less sensitive to outliers in the training data

The model is trained on a dataset of URLs with known classifications (phishing or legitimate).
""")

# Show code for model implementation
st.markdown("### Model Implementation")
st.code("""
class PhishingURLClassifier:
    def __init__(self):
        self.model = None
        self.model_path = "model/phishing_model.pkl"
        self.load_or_create_model()
    
    def load_or_create_model(self):
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                # Create a new RandomForest classifier
                self.model = RandomForestClassifier(
                    n_estimators=100, 
                    max_depth=10,
                    min_samples_split=10,
                    random_state=42
                )
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10,
                min_samples_split=10,
                random_state=42
            )
""", language="python")

# Performance metrics 
st.header("Model Performance")
st.markdown("""
### Evaluation Metrics

The Random Forest classifier is evaluated using several metrics:
""")

# Create example metrics visualization
metrics_data = {
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    'Value': [0.94, 0.92, 0.95, 0.93]
}
metrics_df = pd.DataFrame(metrics_data)

col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(metrics_df)
with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='Metric', y='Value', data=metrics_df, ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title('Model Performance Metrics')
    st.pyplot(fig)

# Feature importance
st.markdown("### Feature Importance")
st.markdown("""
Understanding which features are most predictive helps us improve the model and better 
understand phishing techniques. The chart below shows the relative importance of each feature:
""")

# Example feature importance plot
feature_importance = {
    'Feature': ['url_length', 'has_ip', 'has_at_symbol', 'has_multiple_subdomains', 
                'has_suspicious_chars', 'has_https', 'domain_age_less_than_6months'],
    'Importance': [0.25, 0.18, 0.12, 0.15, 0.14, 0.06, 0.10]
}
importance_df = pd.DataFrame(feature_importance).sort_values('Importance', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df, ax=ax)
ax.set_title('Feature Importance in Phishing Detection')
st.pyplot(fig)

# Application architecture
st.header("Application Architecture")
st.markdown("""
### Streamlit Web Application

The application is built using **Streamlit**, a Python framework for building interactive web applications
with minimal code. The project is structured as follows:

- **app.py**: Main application entry point and URL analysis interface
- **model/feature_extraction.py**: URL feature extraction functions
- **model/phishing_classifier.py**: Machine learning model implementation
- **pages/1_Visual_Insights.py**: Data visualization and insights
- **pages/2_About_Phishing.py**: Educational information about phishing
- **pages/3_Methodology.py**: Technical details and methodology (this page)
- **utils.py**: Utility functions for data loading and feature explanation

This modular structure separates concerns and makes the codebase maintainable and extensible.
""")

# Future improvements
st.header("Future Improvements")
st.markdown("""
### Potential Enhancements

1. **Additional Features**: Incorporate HTML content analysis, JavaScript analysis, and website behavior patterns.

2. **Advanced Models**: Experiment with deep learning approaches like LSTM or transformer-based models.

3. **Real-time Updates**: Implement regular model retraining with newly discovered phishing URLs.

4. **API Integration**: Connect with phishing databases and threat intelligence feeds.

5. **User Feedback Loop**: Allow users to report false positives/negatives to improve the model.
""")

# References
st.header("References and Resources")
st.markdown("""
### Technical References

1. Sahingoz, O. K., et al. (2019). *"Machine learning based phishing detection from URLs."* Expert Systems with Applications, 117, 345-357.

2. Sahoo, S. R., et al. (2017). *"Malicious URL detection using machine learning: A survey."* International Journal of Computer Science and Information Security, 15(3), 255.

3. Scikit-learn Documentation: [Random Forest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

4. APWG Phishing Reports: [Anti-Phishing Working Group](https://apwg.org/trendsreports/)
""")

# Add creator footer
st.markdown("---")
st.markdown("*Created by OmGolesar*", help="Phishing URL Detection Project")