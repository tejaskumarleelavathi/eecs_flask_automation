import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import traceback as tb
import networkx as nx
import matplotlib.pyplot as plt
from anytree import Node, PreOrderIter
import os
import pandas as pd
import json


class WebScraper:
    """
    A class to scrape and extract navigation links from a specified website.
    """

    def extract_navigation_links(self, url) -> list:
        """
        Automatically detects navigation links from a webpage and returns them.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Possible tags and keywords to identify navigation sections
            navigation_selectors = [
                'nav',
                'header',
                {'class': lambda x: x and 'nav' in x.lower()},
                {'class': lambda x: x and 'menu' in x.lower()},
                {'id': lambda x: x and 'nav' in x.lower()},
                {'id': lambda x: x and 'menu' in x.lower()},
            ]

            links = set()

            for selector in navigation_selectors:
                nav_elements = soup.find_all(attrs=selector) if isinstance(selector, dict) else soup.find_all(selector)
                for nav in nav_elements:
                    for a in nav.find_all('a', href=True):
                        full_url = urljoin(url, a['href'])
                        links.add(full_url)

            logging.info(f"Successfully extracted navigation links from {url}")
            return list(links)

        except Exception as e:
            logging.error(f"Error extracting navigation links: {e}")
            logging.error(tb.format_exc())
            return []


  
        

    def show_tree(self, professor_websites_data):
        """
        Displays a graphical tree structure for each professor's website and sub-links.
        """
        for professor, website in professor_websites_data:
            print(f"Creating tree for Professor: {professor} - Main Website: {website}")

            root = Node(f"{professor} ({website})")
            sub_links = self.extract_navigation_links(website)
            for link in sub_links:
                Node(link, parent=root)

            digraph = nx.DiGraph()
            for node in PreOrderIter(root):
                if node.parent:
                    digraph.add_edge(node.parent.name, node.name)

            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(digraph)
            nx.draw(digraph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
            plt.title(f"Website Navigation Tree for {professor}")
            save_location = os.path.join("data/data_tree_view", f"{professor}_website_tree.png")
            plt.savefig(save_location, format="png", bbox_inches="tight")
            logging.info(f"Tree structure saved at {save_location}")
            plt.close()
