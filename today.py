import os
import requests
from lxml import etree

USERNAME = os.environ["USER_NAME"]
TOKEN = os.environ["ACCESS_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

GRAPHQL_URL = "https://api.github.com/graphql"

def graphql(query, variables):
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]

def get_stats():
    query = """
    query($login: String!) {
      user(login: $login) {
        followers { totalCount }
        repositories(
          first: 100,
          ownerAffiliations: OWNER,
          privacy: PUBLIC
        ) {
          totalCount
          nodes {
            stargazerCount
          }
        }
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    user = graphql(query, {"login": USERNAME})["user"]
    repos = user["repositories"]["totalCount"]
    followers = user["followers"]["totalCount"]
    stars = sum(repo["stargazerCount"] for repo in user["repositories"]["nodes"])
    contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return {
        "repo_data": repos,
        "follower_data": followers,
        "star_data": stars,
        "contrib_data": contributions,
    }

def update_svg(path, stats):
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(path, parser)
    root = tree.getroot()
    for element_id, value in stats.items():
        element = root.find(f".//*[@id='{element_id}']")
        if element is not None:
            element.text = f"{value:,}"
    tree.write(path, encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
    stats = get_stats()
    for path in ("dark_mode.svg", "light_mode.svg"):
        update_svg(path, stats)
    print(stats)
