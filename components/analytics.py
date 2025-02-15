
import streamlit.components.v1 as components
import os

def inject_ga():
    ga_js = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-SHFQGXHS8E"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-SHFQGXHS8E');
    </script>
    """
    components.html(ga_js, height=0, width=0)
