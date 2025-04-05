import streamlit as st
import pandas as pd
import numpy as np
import os
import random

@st.cache_data
def load_data():
    """
    Load and prepare the dataset for analysis.
    
    Returns:
        pd.DataFrame: The processed dataset or a sample dataset if the real one is not available
    """
    try:
        # In a real application, you would load actual data from a file
        # Since we're not using mock data, we'll create a synthetic dataset for demonstration
        # This would be replaced with actual data in a production environment
        
        # Create a sample dataset based on known phishing URL characteristics
        data = {
            'url_length': [],
            'has_ip': [],
            'has_at_symbol': [],
            'has_multiple_subdomains': [],
            'has_suspicious_chars': [],
            'has_https': [],
            'domain_age_less_than_6months': [],
            'is_phishing': []
        }
        
        # Generate dataset with 1000 samples
        for i in range(1000):
            # Determine if this sample is a phishing URL (slightly imbalanced dataset)
            is_phishing = 1 if random.random() < 0.6 else 0
            
            if is_phishing:
                # Characteristics more common in phishing URLs
                url_length = random.randint(50, 150)
                has_ip = random.random() < 0.7
                has_at_symbol = random.random() < 0.4
                has_multiple_subdomains = random.random() < 0.6
                has_suspicious_chars = random.random() < 0.7
                has_https = random.random() < 0.3
                domain_age_less_than_6months = random.random() < 0.8
            else:
                # Characteristics more common in legitimate URLs
                url_length = random.randint(15, 80)
                has_ip = random.random() < 0.1
                has_at_symbol = random.random() < 0.05
                has_multiple_subdomains = random.random() < 0.3
                has_suspicious_chars = random.random() < 0.15
                has_https = random.random() < 0.8
                domain_age_less_than_6months = random.random() < 0.2
            
            # Add to dataset
            data['url_length'].append(url_length)
            data['has_ip'].append(int(has_ip))
            data['has_at_symbol'].append(int(has_at_symbol))
            data['has_multiple_subdomains'].append(int(has_multiple_subdomains))
            data['has_suspicious_chars'].append(int(has_suspicious_chars))
            data['has_https'].append(int(has_https))
            data['domain_age_less_than_6months'].append(int(domain_age_less_than_6months))
            data['is_phishing'].append(is_phishing)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    
def get_explanation_for_features(feature_name):
    """
    Get an explanation for a URL feature.
    
    Args:
        feature_name (str): The name of the feature to explain
        
    Returns:
        str: The explanation for the feature
    """
    explanations = {
        'url_length': 'Phishing URLs tend to be longer than legitimate ones to hide their true nature.',
        'has_ip': 'URLs containing IP addresses (like http://123.45.67.89/) are often suspicious as legitimate sites typically use domain names.',
        'has_at_symbol': 'The @ symbol in URLs can be used to hide the actual destination. Everything before @ is ignored by browsers.',
        'has_multiple_subdomains': 'Multiple subdomains (e.g., sub1.sub2.sub3.example.com) can be a sign of phishing.',
        'has_suspicious_chars': 'Suspicious characters like "-", "_", or excessive numbers are common in phishing URLs.',
        'has_https': 'Legitimate sites often use HTTPS. However, many phishing sites now also use HTTPS.',
        'domain_age_less_than_6months': 'Newly registered domains are more likely to be phishing sites.',
        'redirect_count': 'Phishing URLs may use multiple redirects to hide their true destination.',
        'uses_shortening_service': 'URL shortening services can hide the true destination of a link.',
        'has_suspicious_tld': 'Unusual top-level domains (TLDs) can indicate phishing attempts.',
        'domain_in_path': 'Having a known domain in the URL path can be an attempt to appear legitimate.',
        'low_quality_favicon': 'Low quality or missing favicons can indicate quickly created phishing sites.',
        'has_form_with_action': 'Forms with actions to external domains may be stealing information.',
        'prefix_suffix_usage': 'Using prefixes/suffixes with hyphens (e.g., paypal-secure.com) is common in phishing.'
    }
    
    return explanations.get(feature_name, 'No explanation available for this feature.')
