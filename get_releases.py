#!/usr/bin/env python3

import requests
import json
import datetime

def get_releases(repo_owner, repo_name, start_date, end_date):
    """
    Fetch releases from a GitHub repository between two dates.
    
    Args:
        repo_owner (str): Owner of the repository
        repo_name (str): Name of the repository
        start_date (str): Start date in ISO format (YYYY-MM-DD)
        end_date (str): End date in ISO format (YYYY-MM-DD)
        
    Returns:
        list: List of releases with their details
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    
    # GitHub API parameters
    params = {
        'per_page': 100
    }
    
    all_releases = []
    page = 1
    
    # Convert date strings to timezone-aware datetime objects
    start_datetime = datetime.datetime.fromisoformat(f"{start_date}T00:00:00+00:00")
    end_datetime = datetime.datetime.fromisoformat(f"{end_date}T23:59:59+00:00")
    
    while True:
        params['page'] = page
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            break
        
        releases = response.json()
        
        if not releases:
            break
        
        for release in releases:
            # Convert release date to datetime object
            published_at = datetime.datetime.fromisoformat(release['published_at'].replace('Z', '+00:00'))
            
            # Check if the release is within our date range
            if start_datetime <= published_at <= end_datetime:
                all_releases.append({
                    'id': release['id'],
                    'name': release['name'],
                    'tag_name': release['tag_name'],
                    'published_at': release['published_at'],
                    'body': release['body']
                })
        
        page += 1
        
        # Check if we've reached the last page
        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            break
    
    return all_releases

def main():
    # Q1 2024: January 1, 2024 to March 31, 2024
    # Q1 2025: January 1, 2025 to March 31, 2025
    start_date = "2024-01-01"
    end_date = "2025-03-31"
    
    repo_owner = "tektoncd"
    repo_name = "pipeline"
    
    print(f"Fetching releases from {repo_owner}/{repo_name} between {start_date} and {end_date}...")
    
    releases = get_releases(repo_owner, repo_name, start_date, end_date)
    
    print(f"Found {len(releases)} releases")
    
    # Save to JSON file
    output_file = "tektoncd_pipeline_releases.json"
    with open(output_file, 'w') as f:
        json.dump(releases, f, indent=2)
    
    print(f"Releases saved to {output_file}")

if __name__ == "__main__":
    main() 