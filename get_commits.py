#!/usr/bin/env python3

import requests
import json
import datetime

def get_commits(repo_owner, repo_name, start_date, end_date):
    """
    Fetch commits from a GitHub repository between two dates.
    
    Args:
        repo_owner (str): Owner of the repository
        repo_name (str): Name of the repository
        start_date (str): Start date in ISO format (YYYY-MM-DD)
        end_date (str): End date in ISO format (YYYY-MM-DD)
        
    Returns:
        list: List of commits with their messages
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    
    # GitHub API parameters
    params = {
        'since': f"{start_date}T00:00:00Z",
        'until': f"{end_date}T23:59:59Z",
        'per_page': 100
    }
    
    all_commits = []
    page = 1
    
    while True:
        params['page'] = page
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            break
        
        commits = response.json()
        
        if not commits:
            break
        
        for commit in commits:
            all_commits.append({
                'sha': commit['sha'],
                'message': commit['commit']['message'],
                'date': commit['commit']['committer']['date'],
                'author': commit['commit']['author']['name']
            })
        
        page += 1
        
        # Check if we've reached the last page
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    
    return all_commits

def main():
    # Q1 2024: January 1, 2024 to March 31, 2024
    # Q1 2025: January 1, 2025 to March 31, 2025
    start_date = "2024-01-01"
    end_date = "2025-03-31"
    
    repo_owner = "tektoncd"
    repo_name = "pipeline"
    
    print(f"Fetching commits from {repo_owner}/{repo_name} between {start_date} and {end_date}...")
    
    commits = get_commits(repo_owner, repo_name, start_date, end_date)
    
    print(f"Found {len(commits)} commits")
    
    # Save to JSON file
    output_file = "tektoncd_pipeline_commits.json"
    with open(output_file, 'w') as f:
        json.dump(commits, f, indent=2)
    
    print(f"Commits saved to {output_file}")

if __name__ == "__main__":
    main() 