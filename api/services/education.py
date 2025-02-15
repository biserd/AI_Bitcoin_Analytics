"""Education service module for Bitcoin analytics platform"""

def get_educational_content():
    """Get educational content about Bitcoin and cryptocurrency markets"""
    return {
        "bitcoin_etfs": {
            "title": "What are Bitcoin ETFs?",
            "content": """
            Bitcoin ETFs (Exchange-Traded Funds) are investment vehicles that track the price of Bitcoin 
            and trade on traditional stock exchanges. They allow investors to gain exposure to Bitcoin 
            without directly owning the cryptocurrency.
            """,
            "key_benefits": [
                "Regulated investment vehicle",
                "Easy to buy and sell through traditional brokerage accounts",
                "No need for crypto wallets or direct crypto custody",
                "Potential tax advantages in certain accounts"
            ]
        },
        "onchain_metrics": {
            "title": "Understanding On-Chain Metrics",
            "content": """
            On-chain metrics are measurements of activity occurring on the Bitcoin blockchain. 
            They provide insights into network usage and health.
            """,
            "key_metrics": [
                {"name": "Active Addresses", "description": "Number of unique addresses participating in transactions"},
                {"name": "Transaction Volume", "description": "Total value of Bitcoin being transferred"},
                {"name": "Hash Rate", "description": "Total computational power securing the network"}
            ]
        }
    }
