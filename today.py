import json
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
        followers {
          totalCount
        }

        repositories(
          first: 100
          ownerAffiliations: OWNER
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

    return {
        "repo_data": user["repositories"]["totalCount"],
        "follower_data": user["followers"]["totalCount"],
        "star_data": sum(
            repo["stargazerCount"]
            for repo in user["repositories"]["nodes"]
        ),
        "contrib_data": user["contributionsCollection"][
            "contributionCalendar"
        ]["totalContributions"],
    }


def load_config():
    with open("profile-config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def replace_text(root, element_id, value):
    element = root.find(f".//*[@id='{element_id}']")

    if element is not None:
        element.text = str(value)


def update_svg(path, stats, config):
    parser = etree.XMLParser(remove_blank_text=False)

    tree = etree.parse(path, parser)
    root = tree.getroot()

    for element_id, value in stats.items():
        replace_text(root, element_id, f"{value:,}")

    mapping = {
        "handle_data": config.get("handle", ""),
        "subtitle_data": config.get("subtitle", ""),
        "current_data": config.get("current", ""),
        "location_data": config.get("location", ""),
        "focus_data": config.get("focus", ""),
        "languages_data": config.get("languages", ""),
        "frameworks_data": config.get("frameworks", ""),
        "tools_data": config.get("tools", ""),
        "interests_data": config.get("interests", ""),
        "linkedin_data": config.get("linkedin", ""),
        "email_data": config.get("email", ""),
    }

    for element_id, value in mapping.items():
        replace_text(root, element_id, value)

    tree.write(
        path,
        encoding="UTF-8",
        xml_declaration=True,
    )


if __name__ == "__main__":
    stats = get_stats()
    config = load_config()

    for path in ("dark_mode.svg", "light_mode.svg"):
        update_svg(path, stats, config)

    print(stats)
