from typing import Iterable

import arxiv  # type: ignore
import click
import os
import dotenv


def get_arxiv_paper(paper_id: str):
    """Fetch an arXiv paper by its ID."""
    client = arxiv.Client()
    search = arxiv.Search(id_list=[paper_id])
    return next(client.results(search))


def format_markdown_summary(paper) -> str:
    """Format the paper details into a markdown summary."""
    title = paper.title
    authors = "\n  - ".join([f'"[[{author.name}]]"' for author in paper.authors])
    summary = paper.summary
    url = paper.entry_id
    published_date = paper.published.strftime("%Y-%m-%d")

    markdown_summary = "---\n"
    markdown_summary += f"authors:\n  - {authors}\n"
    markdown_summary += f"published: {published_date}\n"
    markdown_summary += f"url: {url}\n"
    markdown_summary += "---\n"
    markdown_summary += f"# {title}\n\n"
    markdown_summary += f"{summary.replace('\n', ' ')}\n"

    return markdown_summary


@click.command()
@click.argument("paper_id", type=str, nargs=-1)
@click.option(
    "--output_dir",
    "-o",
    default=None,
    envvar="ARXIV_SUMMARY_OUTPUT_DIR",
    help="Directory to save the summaries.",
)
def summarize_paper(paper_id: Iterable[str], output_dir: str | None):
    """Generate markdown summaries for given arXiv paper IDs."""

    for id in paper_id:
        paper = get_arxiv_paper(id)
        summary = format_markdown_summary(paper)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

            file_path = os.path.join(output_dir, f"{id}.md")
            if not os.path.exists(file_path):

                with open(file_path, "w") as f:
                    f.write(summary)

            else:
                print(f"Summary for {id} already exists.")

        else:
            print(summary + "\n\n")


if __name__ == "__main__":
    dotenv.load_dotenv()
    summarize_paper()
