import streamlit as st
from api.services.education import get_educational_content

st.set_page_config(page_title="Education", page_icon="📚")

st.title("Bitcoin Education Hub")

# Get educational content
content = get_educational_content()

if content:
    # Bitcoin ETFs Section
    st.header("Understanding Bitcoin ETFs")
    st.write(content['bitcoin_etfs']['content'])
    
    st.subheader("Key Benefits of Bitcoin ETFs")
    for benefit in content['bitcoin_etfs']['key_benefits']:
        st.markdown(f"✅ {benefit}")
    
    # On-chain Metrics Section
    st.header("On-chain Metrics Explained")
    st.write(content['onchain_metrics']['content'])
    
    st.subheader("Key Metrics")
    for metric in content['onchain_metrics']['key_metrics']:
        st.markdown(f"""
        **{metric['name']}**  
        {metric['description']}
        """)
        
    # Additional Resources
    st.header("Additional Resources")
    st.markdown("""
    - [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
    - [Understanding Blockchain Technology](https://bitcoin.org/en/how-it-works)
    - [Bitcoin Development](https://bitcoin.org/en/development)
    """)
else:
    st.warning("Unable to fetch educational content.")
