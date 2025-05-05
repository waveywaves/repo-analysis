# Tekton Pipeline Repository Analyzer

This project contains scripts to fetch and analyze data from the tektoncd/pipeline repository.

## Requirements

- Python 3.6+
- `requests` library
- `matplotlib` library (for visualization)

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Available Scripts

### Commit Fetcher

Run the commits script:
```
python get_commits.py
```

This will:
1. Fetch commits from the tektoncd/pipeline repository from Q1 2024 to Q1 2025
2. Save them to a JSON file named `tektoncd_pipeline_commits.json`

The JSON file contains each commit's:
- SHA
- Commit message
- Date
- Author name

### Release Fetcher

Run the releases script:
```
python get_releases.py
```

This will:
1. Fetch releases from the tektoncd/pipeline repository from Q1 2024 to Q1 2025
2. Save them to a JSON file named `tektoncd_pipeline_releases.json`

The JSON file contains each release's:
- ID
- Name
- Tag name
- Published date
- Release notes (body)

### Commit Analysis

Run the analysis script:
```
python analyze_commits.py
```

This will:
1. Load the commit data from `tektoncd_pipeline_commits.json`
2. Analyze commit patterns, authors, and messages
3. Generate charts and save them to a `charts` directory
4. Print interesting statistics about the repository

The generated charts include:
- Monthly commit activity
- Commits by day of the week
- Commits by hour of the day
- Top 10 contributors
- Common commit message types

#### Filtering by Date Range

You can analyze commits within a specific date range using the `--start` and `--end` parameters:

```
python analyze_commits.py --start 2024-01-01 --end 2024-03-31
```

This will analyze only commits made in Q1 2024 (January 1 to March 31, 2024).

Options:
- `--start`: Start date in YYYY-MM-DD format
- `--end`: End date in YYYY-MM-DD format
- `--input`: Path to input JSON file (default: tektoncd_pipeline_commits.json)

To see all available options:
```
python analyze_commits.py --help
```
