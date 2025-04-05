import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Phishing - Phishing URL Detector",
    page_icon="🎣",
    layout="wide"
)

# Page title
st.title("🎣 About Phishing: Understanding the Threat")

# Introduction section
st.markdown("""
## What is Phishing?

Phishing is a type of cybercrime where attackers disguise themselves as trustworthy entities to deceive victims into revealing 
sensitive information such as usernames, passwords, credit card details, or other personal information. These attacks are typically 
carried out through fraudulent emails, websites, or messages that appear legitimate but are designed to steal information.

Phishing is one of the oldest and most successful forms of cyberattack, dating back to the 1990s, and it continues to evolve and 
become more sophisticated.
""")

# How phishing works
st.markdown("""
## How Phishing Attacks Work

Phishing attacks typically follow a predictable pattern:

1. **Impersonation**: Attackers pose as legitimate organizations (banks, social networks, online stores, etc.)

2. **Contact**: They contact potential victims through emails, text messages, social media, or even phone calls

3. **Urgency/Fear**: They create a sense of urgency or fear to pressure victims into acting quickly without thinking

4. **Payload Delivery**: They provide a malicious link or attachment that leads to:
   - Fake websites that look like legitimate ones
   - Malware downloads
   - Forms requesting sensitive information

5. **Data Collection**: They collect the victim's sensitive information or credentials

6. **Exploitation**: They use the stolen information for financial gain, identity theft, or further attacks
""")

# Types of phishing
st.markdown("""
## Common Types of Phishing Attacks

### Spear Phishing
Targeted attacks directed at specific individuals or companies, often using personalized information to appear more credible.

### Clone Phishing
Attackers create an identical copy of a legitimate message but replace links or attachments with malicious ones.

### Whaling
High-profile targets like C-level executives are targeted with sophisticated, customized approaches.

### Smishing (SMS Phishing)
Phishing conducted via SMS text messages rather than email.

### Vishing (Voice Phishing)
Phone-based phishing where attackers use voice communication to deceive victims.

### Pharming
Redirecting users from legitimate websites to fraudulent ones through DNS hijacking or poisoning.
""")

# URL-based phishing techniques
st.markdown("""
## URL-Based Phishing Techniques

Attackers use various URL manipulation techniques to deceive users:

### Domain Spoofing
Creating domains that look similar to legitimate ones, such as:
- faceb00k.com (using zeros instead of 'o's)
- amaz0n-secure.com (adding hyphens and words)
- paypa1.com (replacing 'l' with the number '1')

### Typosquatting
Registering domains with common typos of popular websites:
- amazno.com
- gooogle.com
- facebok.com

### URL Shortening
Using URL shorteners to hide the actual malicious destination:
- bit.ly/2xCt0pQ
- tinyurl.com/y8r3e2q7

### Subdomain Abuse
Placing the legitimate domain in the subdomain section:
- paypal.secure-billing-information.com
- microsoft.login-verify.com

### IP Address URLs
Using raw IP addresses instead of domain names:
- http://192.168.1.1/login.php

### HTTPS Abuse
Adding HTTPS to create a false sense of security, when the domain itself is fraudulent
""")

# Statistics
st.markdown("""
## Phishing by the Numbers

### Global Impact

- Phishing accounts for **more than 80%** of reported security incidents
- An estimated **1.4 million** new phishing sites are created each month
- The global cost of phishing is estimated at **$12 billion annually**
- Business Email Compromise (BEC) scams alone caused **$1.7 billion in losses** in 2019

### Effectiveness and Targets

- Approximately **30% of phishing emails** are opened by targeted users
- **12% of users** who open phishing emails click on the malicious attachment or link
- Financial institutions, email/online services, and e-commerce platforms are the **most targeted sectors**
- **57% of organizations** experienced a successful phishing attack in 2020

*Sources: Anti-Phishing Working Group (APWG), FBI Internet Crime Complaint Center (IC3), Verizon Data Breach Investigations Report*
""")

# Protection strategies
st.markdown("""
## How to Protect Yourself from Phishing

### Verify the Source
- Check email sender addresses carefully
- Contact organizations directly through official channels if you're unsure
- Don't trust unsolicited communications asking for personal information

### Scrutinize URLs
- Hover over links before clicking to see the actual URL
- Check for misspellings or unusual domains
- Manually type known URLs rather than clicking links in emails

### Maintain Security Measures
- Use two-factor authentication (2FA) wherever possible
- Keep your software, browsers, and operating systems updated
- Use anti-phishing features in browsers and email services
- Install reputable security software

### Develop Skeptical Habits
- Be suspicious of urgent requests or too-good-to-be-true offers
- Don't open unexpected attachments, even from known senders
- Be wary of generic greetings or poor grammar/spelling
- Take time to think before responding to requests for information
""")

# Additional resources
st.markdown("""
## Additional Resources

### Organizations Focused on Fighting Phishing
- [Anti-Phishing Working Group (APWG)](https://apwg.org/)
- [FBI Internet Crime Complaint Center (IC3)](https://www.ic3.gov/)
- [National Cyber Security Alliance](https://staysafeonline.org/)

### Tools and Services
- [Google Safe Browsing](https://safebrowsing.google.com/)
- [PhishTank](https://www.phishtank.com/)
- [Have I Been Pwned?](https://haveibeenpwned.com/)

### Educational Resources
- [FTC's Phishing Information](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams)
- [CISA's Phishing Resources](https://www.cisa.gov/topics/cybersecurity-best-practices/phishing)
""")

# Important note for users
st.info("""
**Remember**: Legitimate organizations like banks, government agencies, and reputable companies will never ask you to provide 
sensitive information through email, text messages, or over the phone. When in doubt, contact the organization directly using 
official contact information—not the contact details provided in a suspicious message.
""")

# Add creator footer
st.markdown("---")
st.markdown("*Created by OmGolesar*", help="Phishing URL Detection Project")
