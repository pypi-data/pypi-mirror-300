"""
This script checks the status of URLs and their links recursively, starting from a given URL.

It uses the `click` library for command-line interface, `requests` for HTTP requests,
`BeautifulSoup` for parsing HTML content, and `alive_progress` for displaying a progress bar.

Functions:
    cli(url: str, print_all: bool = False):
        Command-line interface function that takes a URL and an optional flag to print all results.
        It checks the status of the given URL and its links recursively, printing the results in a table format.

Parameters:
    url (str): The starting URL to check.
    print_all (bool, optional): Flag to print all results, including expected status codes. Defaults to False.

Raises:
    ValueError: If the provided URL is not absolute.

Usage:
    python tools.py <url> [--print-all]

Example:
    python tools.py https://example.com --print-all
"""

from collections import Counter
from queue import Queue
from time import sleep

import click
from alive_progress import alive_bar
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError
from tabulate import tabulate
from yarl import URL

from .__version__ import __version__

EXPECTED_CODES = [200, 301, 302]


@click.command()
@click.version_option(
    version=__version__,
    prog_name="http-tools",
)
@click.argument("url", type=str, required=True)
@click.option("--print-all", is_flag=True)
def cli(  # noqa: C901 PLR0915
    url: str | URL,
    print_all: bool = False,  # noqa: FBT001 FBT002
) -> None:
    """
    Command-line interface function to check the status and content of a given URL.

    Args:
        url (str | URL): The URL to check. It must be an absolute URL.
        print_all (bool, optional): If True, print all results. If False, only print errors. Defaults to False.
    Raises:
        ValueError: If the provided URL is not absolute.
    Returns:
        None
    """
    print_errors = not print_all
    if not isinstance(url, URL):
        url = URL(url)
    if not url.is_absolute():
        raise ValueError

    queue = Queue()
    queue.put((url, None))
    results = {}
    seen = set()

    with alive_bar(manual=True) as bar:
        while not queue.empty():
            url, referrer = queue.get()
            summary = "; ".join(
                [
                    f"{r[1]} HTTP {r[0]} Responses"
                    for r in Counter(
                        [r["status_code"] for r in results.values()]
                    ).items()
                ]
            )
            bar.text(f"{summary}; {queue.qsize()} to go. Checking {url.human_repr()}")

            result = {
                "url": url.human_repr(),
                "referrer": referrer.human_repr() if referrer is not None else None,
                "title": None,
                "content-type": None,
                "status_code": None,
            }

            # Get the content of the URL
            while True:
                try:
                    response = get(
                        url,
                        allow_redirects=False,
                        timeout=5,
                    )
                except ConnectionError:
                    # sleep for a bit and try again
                    bar.text(
                        f"{summary}; {queue.qsize()} to go. Connection error for {url.human_repr()}. Sleeping for 1 second and trying again."
                    )
                    sleep(1)
                    continue
                break

            result["content-type"] = response.headers.get("content-type", None)
            result["status_code"] = response.status_code

            # If the status code is not expected, print the URL
            if result["status_code"] not in EXPECTED_CODES:
                click.echo(result["url"])
                click.echo(f" - Referrer: {result['referrer']}")
                click.echo(f" - Status Code: {result['status_code']}")

            # If the host is not the same as the URL, skip the URL
            if referrer and referrer.host != url.host:
                results[url.human_repr()] = result
                bar(len(results) / (queue.qsize() + len(results)))
                continue

            # If the status code is a redirect, add the location to the queue and skip the URL
            if result["status_code"] in [301, 302]:
                u = URL(response.headers["location"])
                queue.put((u if u.is_absolute() else url.join(u), url))
                results[url.human_repr()] = result
                bar(len(results) / (queue.qsize() + len(results)))
                continue

            # If the content-type is not text/html, skip the URL
            if "text/html" not in result["content-type"]:
                results[url.human_repr()] = result
                bar(len(results) / (queue.qsize() + len(results)))
                continue

            # Parse the URL content
            soup = BeautifulSoup(response.content, "html.parser")

            # Get the title of the URL
            result["title"] = soup.title.string if soup.title is not None else None

            [
                (
                    seen.add(u),
                    queue.put((u.with_scheme(u.scheme if u.scheme else "https"), url)),
                )
                for u in [
                    u if u.is_absolute() else url.join(u)
                    for u in [
                        *[
                            URL(o.get("href"))
                            for o in soup.select("[href]")
                            if o.get("href") is not None
                        ],
                        *[
                            URL(o.get("src"))
                            for o in soup.select("[src]")
                            if o.get("src") is not None
                        ],
                        *[
                            URL(o.get("data-href"))
                            for o in soup.select("[data-href]")
                            if o.get("data-href") is not None
                        ],
                    ]
                ]
                if u not in seen  # and u.host == url.host
            ]

            results[url.human_repr()] = result
            bar(len(results) / (queue.qsize() + len(results)))
            continue

    if print_all or print_errors:
        click.echo(
            tabulate(
                sorted(
                    [
                        v
                        for v in results.values()
                        if print_all or v["status_code"] not in EXPECTED_CODES
                    ],
                    key=lambda x: x["url"],
                ),
                headers="keys",
            )
        )

    click.echo(
        tabulate(
            Counter([r["status_code"] for r in results.values()]).items(),
            headers=["Status Code", "Count"],
        )
    )


if __name__ == "__main__":
    cli()
