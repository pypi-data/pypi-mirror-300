import os
from datetime import datetime
from github import Github
import requests
from bs4 import BeautifulSoup
import re
import json

class cms:
    def __init__(self, GHPAT=None):
        if not GHPAT:
            GHPAT = os.getenv("GHPAT")
        self.GHPAT = GHPAT
        self.original_pdfs_url = "https://sslpdfs.gospelsounders.org/"
    def get_decades(self):
        # Get the current year
        current_year = datetime.now().year

        # Determine the starting year for the first decade
        start_year = 1888

        # Create a list to hold the decades
        decades = {}

        # Generate decades from 1888 to the current year
        for year in range(start_year, current_year + (1 if current_year %10==0 else 10)):
            # Check if the year is the start of a new decade
            if year % 10 == 0:
                # Create the decade string
                end_year = year  # End at the previous year            
                if end_year >= start_year:
                    # decades.append(f"{start_year}-{end_year}")
                    decade_key = f"{year - 9}-{year}"
                    decades[decade_key] = {y: {} for y in range(start_year, end_year + 1)}  # Create years in the decade
                    # create 4 quarters in each year...
                start_year = end_year +1

        return decades


    def setup_repo_for_decade(self, decade, org_name="sabbathschool"):
        g = Github(self.GHPAT)
        repo_name = decade

        # Get the organization
        org = g.get_organization(org_name)

        # Check if the repo exists in the organization, otherwise create it
        try:
            repo = org.get_repo(repo_name)
            print(f"Repository '{repo_name}' already exists in {org_name}.")
        except:
            repo = org.create_repo(repo_name)
            print(f"Repository '{repo_name}' created in {org_name}.")

        # Check if 'gh-pages' branch exists
        try:
            gh_pages_branch = repo.get_branch("gh-pages")
            print(f"'gh-pages' branch already exists in {repo_name}.")
        except:
            # Create 'gh-pages' branch and add index.html
            repo.create_file("index.html", "Initial commit", "<html><body><h1>Decade</h1></body></html>", branch="gh-pages")
            print(f"'gh-pages' branch created with index.html in {repo_name}.")
            gh_pages_branch = repo.get_branch("gh-pages")

        # Check if 'master' branch exists
        try:
            master_branch = repo.get_branch("master")
            print(f"'master' branch already exists in {repo_name}.")
        except:
            # Create 'master' branch based on 'gh-pages'
            gh_pages_sha = gh_pages_branch.commit.sha
            repo.create_git_ref(ref="refs/heads/master", sha=gh_pages_sha)
            print(f"'master' branch created in {repo_name} based on 'gh-pages'.")

            # Add README.md to 'master' branch
            repo.create_file("README.md", "Add README", f"SSL for {decade}", branch="master")
            print(f"README.md added to 'master' branch in {repo_name}.")

        # Print all branches
        branches = list(repo.get_branches())
        for branch in branches:
            print(branch.name)

    def create_repos_for_all_decades(self):
        decades = self.get_decades()
        for decade in decades.keys():
            self.setup_repo_for_decade(decade)


    def fetch_html_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
            return None

    def extract_lesson_links(self):
        decades_dict = self.get_decades()
        html_content = self.fetch_html_content(self.original_pdfs_url)

        # if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        if not table:
            print("No table found in the HTML content.")
            return decades_dict

        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 5:  # Ensure we have year and 4 quarters
                continue

            try:
                year = int(columns[0].text.strip())
            except ValueError:
                # Skip rows where the year is not a valid integer (e.g., 'All Lessons')
                continue
            
            # Find the decade for this year
            decade = None
            for decade_range, years in decades_dict.items():
                start_year = int(decade_range.split('-')[0])
                if start_year <= year < start_year + 10:
                    decade = decade_range
                    break
            
            if decade is None or year not in decades_dict[decade]:
                continue  # Skip if year is not in our dictionary

            for quarter, column in enumerate(columns[1:], start=1):
                links = column.find_all('a')
                if len(links) >= 3:  # Ensure we have HTML, PDF, and TXT links
                    pdf_link = links[1]['href'].lstrip('/')
                    txt_link = links[2]['href'].lstrip('/')
                    
                    quarter_key = f'Q{quarter}'
                    if quarter_key not in decades_dict[decade][year]:
                        decades_dict[decade][year][quarter_key] = {}
                    
                    decades_dict[decade][year][quarter_key]['pdf'] = pdf_link
                    decades_dict[decade][year][quarter_key]['txt'] = txt_link
        return decades_dict