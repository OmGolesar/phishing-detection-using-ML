import re
from urllib.parse import urlparse
import tldextract
import socket
import numpy as np

def extract_features_from_url(url):
    """
    Extract features from a URL for phishing detection.
    
    Args:
        url (str): The URL to extract features from
        
    Returns:
        dict: A dictionary of features
    """
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
    
    # 7. New domain (We can't actually check domain age in this demo, so we'll simulate it)
    # In a real application, you would query WHOIS data or a similar service
    features['domain_age_less_than_6months'] = simulate_domain_age_check(extracted.domain)
    
    return features

def extract_features_batch(urls):
    """
    Extract features from multiple URLs.
    
    Args:
        urls (list): List of URLs to extract features from
        
    Returns:
        pd.DataFrame: A DataFrame containing features for all URLs
    """
    features_list = []
    for url in urls:
        features_list.append(extract_features_from_url(url))
    
    return pd.DataFrame(features_list)

def is_ip_address(domain):
    """
    Check if a domain is an IP address.
    
    Args:
        domain (str): The domain to check
        
    Returns:
        bool: True if the domain is an IP address, False otherwise
    """
    # Try IPv4
    try:
        socket.inet_pton(socket.AF_INET, domain)
        return True
    except socket.error:
        pass
    
    # Try IPv6
    try:
        socket.inet_pton(socket.AF_INET6, domain)
        return True
    except socket.error:
        pass
    
    # Handle IPv4 with port number
    ipv4_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$')
    if ipv4_pattern.match(domain):
        return True
    
    return False

def has_suspicious_chars(url):
    """
    Check if a URL contains suspicious characters.
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL contains suspicious characters, False otherwise
    """
    # Check for excessive hyphens
    if url.count('-') > 2:
        return True
    
    # Check for multiple consecutive dots
    if '..' in url:
        return True
    
    # Check for excessive use of numbers in domain
    domain = urlparse(url).netloc
    domain_no_tld = domain.split('.')
    if len(domain_no_tld) > 0:
        main_domain = domain_no_tld[0]
        digit_ratio = sum(c.isdigit() for c in main_domain) / len(main_domain) if len(main_domain) > 0 else 0
        if digit_ratio > 0.5:
            return True
    
    return False

def simulate_domain_age_check(domain):
    """
    Simulate checking if a domain is less than 6 months old.
    In a real application, you would query WHOIS data.
    
    Args:
        domain (str): The domain to check
        
    Returns:
        int: 1 if the domain is likely less than 6 months old, 0 otherwise
    """
    # This is a placeholder function
    # In real implementation, you would check domain registration date
    
    # For demonstration purposes, we'll use a simple heuristic based on domain length
    # and presence of numbers (not a good real-world method, just for demonstration)
    if len(domain) > 15 or sum(c.isdigit() for c in domain) > 3:
        return 1
    
    # Return 1 for 20% of domains randomly (to simulate some domains being new)
    return 1 if np.random.random() < 0.2 else 0
