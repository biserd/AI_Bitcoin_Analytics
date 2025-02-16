"""Sitemap generator for Bitcoin Analytics Dashboard"""
from datetime import datetime
import os
from typing import List, Dict
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

def generate_sitemap(base_url: str, routes: List[Dict[str, str]]) -> str:
    """
    Generate sitemap XML for the application
    
    Args:
        base_url: Base URL of the application
        routes: List of route dictionaries with path and last_modified
    
    Returns:
        Formatted XML string
    """
    # Create the root element
    urlset = ET.Element(
        "urlset", 
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )
    
    # Add each route to the sitemap
    for route in routes:
        url = ET.SubElement(urlset, "url")
        
        # Add location
        loc = ET.SubElement(url, "loc")
        loc.text = urljoin(base_url, route['path'])
        
        # Add last modified date
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = route.get('last_modified', datetime.now().strftime('%Y-%m-%d'))
        
        # Add change frequency
        changefreq = ET.SubElement(url, "changefreq")
        changefreq.text = route.get('changefreq', 'daily')
        
        # Add priority
        priority = ET.SubElement(url, "priority")
        priority.text = route.get('priority', '0.8')
    
    # Convert to string
    return ET.tostring(urlset, encoding='unicode', method='xml')

def write_sitemap(xml_content: str, filepath: str = 'sitemap.xml') -> None:
    """Write sitemap XML to file"""
    with open(filepath, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(xml_content)
