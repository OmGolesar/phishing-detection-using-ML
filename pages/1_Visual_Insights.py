import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

# Page configuration
st.set_page_config(
    page_title="Visual Insights - Phishing URL Detector",
    page_icon="📊",
    layout="wide"
)

# Page title
st.title("📊 Visual Insights: Understanding Phishing URLs")
st.markdown("""
This page provides visualizations and insights into phishing URLs versus legitimate URLs.
Explore the data to better understand what makes a URL suspicious.
""")

# Load dataset (cached)
@st.cache_data
def get_dataset_stats(df):
    total = len(df)
    phishing = df[df['is_phishing'] == 1].shape[0]
    legitimate = df[df['is_phishing'] == 0].shape[0]
    
    # Calculate average URL length
    avg_phishing_length = df[df['is_phishing'] == 1]['url_length'].mean()
    avg_legitimate_length = df[df['is_phishing'] == 0]['url_length'].mean()
    
    return {
        'total': total,
        'phishing': phishing,
        'legitimate': legitimate,
        'phishing_pct': (phishing/total)*100,
        'legitimate_pct': (legitimate/total)*100,
        'avg_phishing_length': avg_phishing_length,
        'avg_legitimate_length': avg_legitimate_length
    }

try:
    # Load the dataset
    df = load_data()
    
    if df is not None and not df.empty:
        # Get statistics
        stats = get_dataset_stats(df)
        
        # Display dataset statistics in an expander
        with st.expander("Dataset Overview", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total URLs", f"{stats['total']:,}")
            
            with col2:
                st.metric("Phishing URLs", f"{stats['phishing']:,} ({stats['phishing_pct']:.1f}%)")
            
            with col3:
                st.metric("Legitimate URLs", f"{stats['legitimate']:,} ({stats['legitimate_pct']:.1f}%)")
                
            st.markdown(f"""
            - Average length of phishing URLs: {stats['avg_phishing_length']:.1f} characters
            - Average length of legitimate URLs: {stats['avg_legitimate_length']:.1f} characters
            """)
        
        # Create visualizations
        st.markdown("## 📈 Key Visualizations")
        
        # Distribution of URL lengths
        st.markdown("### URL Length Distribution")
        st.markdown("Phishing URLs often have different length characteristics compared to legitimate URLs.")
        
        fig_length = px.histogram(
            df, 
            x="url_length", 
            color="is_phishing",
            barmode="overlay",
            color_discrete_map={0: "green", 1: "red"},
            labels={"is_phishing": "URL Type", "url_length": "URL Length (characters)"},
            category_orders={"is_phishing": [0, 1]},
            title="Distribution of URL Lengths"
        )
        fig_length.update_layout(legend_title_text="URL Type", 
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ))
        
        # Update legend labels
        fig_length.data[0].name = "Legitimate"
        fig_length.data[1].name = "Phishing"
        
        st.plotly_chart(fig_length, use_container_width=True)
        
        # Class distribution
        st.markdown("### Class Distribution")
        st.markdown("Breakdown of phishing vs. legitimate URLs in our dataset.")
        
        fig_pie = px.pie(
            values=[stats['legitimate'], stats['phishing']],
            names=["Legitimate", "Phishing"],
            color_discrete_sequence=["green", "red"],
            title="Phishing vs. Legitimate URL Distribution"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # URL Structural Characteristics Comparison
        st.markdown("### URL Structural Characteristics")
        st.markdown("Comparison of various structural elements commonly found in URLs.")
        
        # Prepare data for structural characteristics
        structural_features = ['has_ip', 'has_at_symbol', 'has_multiple_subdomains', 
                              'has_suspicious_chars', 'has_https', 'domain_age_less_than_6months']
        
        structural_data = {
            'Feature': [],
            'Legitimate (%)': [],
            'Phishing (%)': []
        }
        
        for feature in structural_features:
            if feature in df.columns:
                structural_data['Feature'].append(feature.replace('_', ' ').title())
                structural_data['Legitimate (%)'].append(df[df['is_phishing'] == 0][feature].mean() * 100)
                structural_data['Phishing (%)'].append(df[df['is_phishing'] == 1][feature].mean() * 100)
        
        # Create DataFrame for visualization
        structural_df = pd.DataFrame(structural_data)
        
        # Create grouped bar chart
        if not structural_df.empty:
            # Melt the dataframe for easier plotting
            structural_df_melted = pd.melt(
                structural_df, 
                id_vars=['Feature'], 
                value_vars=['Legitimate (%)', 'Phishing (%)'],
                var_name='URL Type',
                value_name='Percentage'
            )
            
            fig_structural = px.bar(
                structural_df_melted,
                x='Feature',
                y='Percentage',
                color='URL Type',
                barmode='group',
                color_discrete_map={'Legitimate (%)': 'green', 'Phishing (%)': 'red'},
                title='Structural Characteristics Comparison'
            )
            
            fig_structural.update_layout(
                xaxis_title='Feature',
                yaxis_title='Percentage (%)',
                legend_title='URL Type',
                xaxis={'categoryorder':'total descending'}
            )
            
            st.plotly_chart(fig_structural, use_container_width=True)
        
        # Correlation heatmap
        st.markdown("### Feature Correlation")
        st.markdown("This heatmap shows correlations between different URL features and phishing status.")
        
        # Select only numeric columns for correlation
        numeric_df = df.select_dtypes(include=['number'])
        
        # Create the correlation matrix
        corr = numeric_df.corr()
        
        # Create the heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        
        sns.heatmap(
            corr, 
            mask=mask, 
            cmap=cmap, 
            vmax=1, 
            vmin=-1, 
            center=0,
            square=True, 
            linewidths=.5, 
            cbar_kws={"shrink": .5},
            annot=True,
            fmt=".2f"
        )
        
        plt.title('Correlation Between Features')
        st.pyplot(fig)
        
    else:
        st.warning("No data available for visualization. Please make sure the dataset is loaded correctly.")
        
except Exception as e:
    st.error(f"An error occurred while generating visualizations: {str(e)}")
    st.markdown("Please try refreshing the page or contact support if the issue persists.")
    
# Add creator footer
st.markdown("---")
st.markdown("*Created by OmGolesar*", help="Phishing URL Detection Project")
