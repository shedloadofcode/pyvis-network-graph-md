"""Searches the Markdown files for internal links in blog articles.

Reads in the all files in the /content/blog directory and then searches for
any link which contains /blog/.

Outputs the results of this to a graph visual 'links.html'

Install packages using `pip install pandas pyvis`
"""
import os
import re
import pandas as pd
from pyvis.network import Network

def get_edge_data() -> pd.DataFrame:
    source = []
    target = []
    weight = []
    pages_with_no_internal_links = set()

    count = 0
    path = "../content/blog"
    links_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        name, extension = os.path.splitext(filename)
        count += 1

        try:
            with open(file_path, encoding="utf8") as f:
                md = f.read()
                links = list(links_regex.findall(md))
                links_added = 0

                for link in links:
                    if link[1].startswith("/blog/"):
                        source.append("/blog/" + name + "/")
                        target.append(link[1])
                        weight.append(0.4)
                        links_added += 1
                    
                if links_added == 0:
                    pages_with_no_internal_links.add(name)
        except Exception as error:
            print("An exception occurred:", error)
    
    print(f"{count} files searched.")

    print(f"{len(source)} sources and {len(target)} targets.", end="\n\n")

    print(f"{len(pages_with_no_internal_links)} pages with no internal links:")

    for link in pages_with_no_internal_links:
        print(link)

    return zip(source, target, weight)

def display_graph(edge_data) -> None:
    net = Network(height="900px", 
                  width="100%", 
                  directed=True,
                  bgcolor="#222222", 
                  font_color="#b1b4b6",
                  select_menu=True, 
                  filter_menu=True,
                  cdn_resources="remote")
    
    net.show_buttons(filter_=["nodes", "physics"])

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        net.add_node(src, src, title=src)   
        net.add_node(dst, dst, title=dst)
        net.add_edge(src, dst, value=w)

    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node["title"] += " links to:\n" + "\n".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    net.show("links.html", notebook=False)

if __name__ == "__main__":
    edge_data = get_edge_data()
    display_graph(edge_data)