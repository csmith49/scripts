import requests
from bs4 import BeautifulSoup
import click


def get_reference_titles(arxiv_id):
    """
    Fetch the HTML version of an arXiv paper and extract reference titles.
    :param arxiv_id: The arXiv ID of the paper.
    :return: A list of reference titles.
    """
    html_url = f"https://ar5iv.org/html/{arxiv_id}"
    response = requests.get(html_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    bib_items = soup.find_all("li", class_="ltx_bibitem")

    references = []
    for item in bib_items:
        title_block = item.find_all("span", class_="ltx_bibblock")[1].get_text(
            strip=True
        )
        references.append(title_block)

    return references


def search_arxiv_id_by_title(title):
    """
    Search for a title on arXiv using the API and return the arXiv ID without version.
    :param title: The title of the reference to search for.
    :return: The arXiv ID without version, or None if not found.
    """
    base_url = "http://export.arxiv.org/api/query"
    params = {"search_query": f'ti:"{title}"', "start": 0, "max_results": 1}
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    if "<entry>" in response.text:
        start_idx = response.text.find("<id>http://arxiv.org/abs/") + len(
            "<id>http://arxiv.org/abs/"
        )
        end_idx = response.text.find("</id>", start_idx)
        arxiv_id = response.text[start_idx:end_idx]
        arxiv_id = arxiv_id.split("v")[0]
        return arxiv_id
    else:
        return None


@click.command()
@click.argument("arxiv_id")
def main(arxiv_id):
    references = get_reference_titles(arxiv_id)
    arxiv_ids = []
    for title in references:
        arxiv_id = search_arxiv_id_by_title(title)
        if arxiv_id:
            arxiv_ids.append(arxiv_id)

    for arxiv_id in arxiv_ids:
        print(arxiv_id)


if __name__ == "__main__":
    main()
