# Demir GitHub profile README

This folder is a ready-to-use GitHub profile repository inspired by the dynamic
neofetch-style profile you linked, but with an original layout and content.

## 1. Create your profile repository

Create a public GitHub repository whose name is EXACTLY your GitHub username.

Example:
- username: `demirkhan`
- repository: `demirkhan/demirkhan`

GitHub will automatically show that repository's `README.md` on your profile.

## 2. Replace placeholders

Search the repository for:

- `YOUR_GITHUB_USERNAME`
- `YOUR_LINKEDIN_HANDLE`
- `YOUR_EMAIL`

Replace them with your real details in:
- README.md
- dark_mode.svg
- light_mode.svg

You can also edit any stack/role text directly in the SVG files.

## 3. Add a GitHub token

The scheduled workflow reads profile stats through GitHub's GraphQL API.

Create a fine-grained personal access token with read access to public repository
metadata, then add it to the profile repo as this Actions secret:

`PROFILE_TOKEN`

Repository:
Settings → Secrets and variables → Actions → New repository secret

## 4. Run it

Go to:
Actions → Update profile stats → Run workflow

The action updates:
- public repo count
- follower count
- total stars on the first 100 public repositories
- current GitHub contribution-calendar total

It runs automatically once per day as well.

## Notes

The design intentionally does NOT copy Andrew Grant's ASCII portrait or wording.
It uses the same broad idea — a responsive light/dark SVG profile card with live
GitHub values — with a different layout and personalised content.
