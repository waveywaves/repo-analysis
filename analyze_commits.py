#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os
import argparse
from collections import Counter, defaultdict

def load_data(filename):
    """Load commit data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def filter_bots(commits):
    """Filter out bot commits, specifically dependabot."""
    return [commit for commit in commits if 'dependabot' not in commit['author'].lower()]

def filter_by_date(commits, start_date, end_date):
    """Filter commits by date range."""
    filtered = []
    for commit in commits:
        commit_date = commit['date_obj']
        if start_date <= commit_date <= end_date:
            filtered.append(commit)
    return filtered

def convert_dates(commits):
    """Convert ISO date strings to datetime objects."""
    for commit in commits:
        commit['date_obj'] = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
    return commits

def get_date_range(commits):
    """Get the earliest and latest commit dates."""
    dates = [commit['date_obj'] for commit in commits]
    earliest = min(dates)
    latest = max(dates)
    return earliest, latest

def analyze_commits_by_time(commits):
    """Analyze commits by time period."""
    # Group by month
    monthly_commits = defaultdict(int)
    for commit in commits:
        year_month = commit['date_obj'].strftime('%Y-%m')
        monthly_commits[year_month] += 1
    
    # Sort by month
    monthly_sorted = dict(sorted(monthly_commits.items()))
    
    # Group by day of week
    day_of_week = defaultdict(int)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for commit in commits:
        weekday = commit['date_obj'].strftime('%A')
        day_of_week[weekday] += 1
    
    # Ensure all days are represented in order
    days_sorted = {day: day_of_week.get(day, 0) for day in day_order}
    
    # Group by hour
    hour_commits = defaultdict(int)
    for commit in commits:
        hour = commit['date_obj'].hour
        hour_commits[hour] += 1
    
    # Sort by hour
    hours_sorted = dict(sorted(hour_commits.items()))
    
    return {
        'monthly': monthly_sorted,
        'daily': days_sorted,
        'hourly': hours_sorted
    }

def analyze_top_contributors(commits):
    """Analyze top contributors."""
    authors = [commit['author'] for commit in commits]
    return Counter(authors).most_common(10)

def analyze_commit_messages(commits):
    """Analyze commit message patterns."""
    # Extract first word of each commit message (often the type of change)
    first_words = []
    for commit in commits:
        message = commit['message'].strip().split('\n')[0].strip()
        if message:
            first_word = message.split(' ')[0].lower().strip(':')
            if first_word:
                first_words.append(first_word)
    
    return Counter(first_words).most_common(10)

def plot_monthly_activity(monthly_counts, start_date, end_date):
    """Plot monthly commit activity."""
    months = list(monthly_counts.keys())
    counts = list(monthly_counts.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(months, counts, color='skyblue')
    title = f'Commits per Month (Excluding Dependabot) - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Number of Commits')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_commits.png')
    plt.close()

def plot_daily_activity(daily_counts, start_date, end_date):
    """Plot commits by day of the week."""
    days = list(daily_counts.keys())
    counts = list(daily_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(days, counts, color='lightgreen')
    title = f'Commits by Day of Week (Excluding Dependabot) - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    plt.title(title)
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Commits')
    plt.tight_layout()
    plt.savefig('daily_commits.png')
    plt.close()

def plot_hourly_activity(hourly_counts, start_date, end_date):
    """Plot commits by hour of the day."""
    hours = list(hourly_counts.keys())
    counts = list(hourly_counts.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts, color='salmon')
    title = f'Commits by Hour of Day (Excluding Dependabot) - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    plt.title(title)
    plt.xlabel('Hour (UTC)')
    plt.ylabel('Number of Commits')
    plt.xticks(range(24))
    plt.tight_layout()
    plt.savefig('hourly_commits.png')
    plt.close()

def plot_top_contributors(top_contributors, start_date, end_date):
    """Plot top contributors."""
    if not top_contributors:
        print("No top contributors to plot.")
        return
        
    authors, counts = zip(*top_contributors)
    
    plt.figure(figsize=(12, 8))
    plt.barh(authors, counts, color='purple')
    title = f'Top 10 Contributors (Excluding Dependabot) - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    plt.title(title)
    plt.xlabel('Number of Commits')
    plt.ylabel('Author')
    plt.tight_layout()
    plt.savefig('top_contributors.png')
    plt.close()

def plot_commit_types(commit_types, start_date, end_date):
    """Plot common commit message types."""
    if not commit_types:
        print("No commit types to plot.")
        return
        
    words, counts = zip(*commit_types)
    
    plt.figure(figsize=(12, 8))
    plt.barh(words, counts, color='teal')
    title = f'Common Commit Message Types (Excluding Dependabot) - {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
    plt.title(title)
    plt.xlabel('Frequency')
    plt.ylabel('First Word in Commit Message')
    plt.tight_layout()
    plt.savefig('commit_types.png')
    plt.close()

def parse_date(date_string):
    """
    Parse date string in YYYY-MM-DD format and return as timezone-aware datetime.
    """
    try:
        # Parse the date and make it timezone-aware by adding UTC timezone
        dt = datetime.fromisoformat(date_string)
        # If the datetime is naive (has no timezone info), make it timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Please use YYYY-MM-DD format.")

def main():
    # Setup command line argument parser
    parser = argparse.ArgumentParser(description='Analyze commits in a date range')
    parser.add_argument('--start', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--input', type=str, default='tektoncd_pipeline_commits.json', 
                        help='Input JSON file with commit data (default: tektoncd_pipeline_commits.json)')
    args = parser.parse_args()
    
    # Load commit data
    input_file = args.input
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
    
    print(f"Loading commit data from {input_file}...")
    commits = load_data(input_file)
    total_commits = len(commits)
    print(f"Loaded {total_commits} commits.")
    
    # Convert dates to datetime objects for all commits
    commits = convert_dates(commits)
    
    # Get overall date range in the data
    data_start_date, data_end_date = get_date_range(commits)
    print(f"\nData time period: {data_start_date.strftime('%Y-%m-%d')} to {data_end_date.strftime('%Y-%m-%d')}")
    
    # Set user-specified date range or use full range
    start_date = parse_date(args.start) if args.start else data_start_date
    end_date = parse_date(args.end) if args.end else data_end_date
    
    print(f"Analysis period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"That's approximately {(end_date - start_date).days} days or {(end_date - start_date).days / 30:.1f} months")
    
    # Filter by date range
    date_filtered_commits = filter_by_date(commits, start_date, end_date)
    print(f"Found {len(date_filtered_commits)} commits in the specified date range.")
    
    # Filter out dependabot commits
    filtered_commits = filter_bots(date_filtered_commits)
    filtered_count = len(filtered_commits)
    bot_count = len(date_filtered_commits) - filtered_count
    print(f"\nFiltered out {bot_count} bot commits. Analyzing {filtered_count} human commits.")
    
    if filtered_count == 0:
        print("No commits to analyze after filtering. Please try a different date range.")
        return
    
    # Create output directory for charts
    os.makedirs('charts', exist_ok=True)
    
    # Change to charts directory for output
    os.chdir('charts')
    
    # Analyze commits by time
    print("Analyzing commit patterns by time...")
    time_analysis = analyze_commits_by_time(filtered_commits)
    
    # Plot time-based charts
    plot_monthly_activity(time_analysis['monthly'], start_date, end_date)
    plot_daily_activity(time_analysis['daily'], start_date, end_date)
    plot_hourly_activity(time_analysis['hourly'], start_date, end_date)
    
    # Analyze and plot top contributors
    print("Analyzing top contributors...")
    top_contributors = analyze_top_contributors(filtered_commits)
    plot_top_contributors(top_contributors, start_date, end_date)
    
    # Analyze and plot commit message patterns
    print("Analyzing commit message patterns...")
    commit_types = analyze_commit_messages(filtered_commits)
    plot_commit_types(commit_types, start_date, end_date)
    
    print(f"Analysis complete! Charts saved in the 'charts' directory.")
    
    # Print some interesting statistics
    date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    print(f"\nInteresting Statistics (Excluding Dependabot) - {date_range_str}:")
    print(f"Total human commits: {filtered_count}")
    print(f"Number of unique contributors: {len(set(commit['author'] for commit in filtered_commits))}")
    
    if top_contributors:
        print("\nTop 5 contributors:")
        for author, count in top_contributors[:5]:
            print(f"  - {author}: {count} commits")
    
    if time_analysis['monthly']:
        print("\nMost active month(s):")
        if time_analysis['monthly']:
            month_items = list(time_analysis['monthly'].items())
            if month_items:
                most_active_month = max(month_items, key=lambda x: x[1])
                print(f"  - {most_active_month[0]}: {most_active_month[1]} commits")
    
    if commit_types:
        print("\nMost common commit types:")
        for word, count in commit_types[:5]:
            print(f"  - {word}: {count} occurrences")

if __name__ == "__main__":
    main() 