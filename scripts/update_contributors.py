#!/usr/bin/env python3
"""
Script to update the Collaborators section in README.md with contributors from GitHub.
This script fetches contributors from the GitHub API and updates the README automatically.
"""

import os
import sys
import re
import requests
from pathlib import Path

# GitHub repository information
GITHUB_REPO = "kshitijmarwah1/VibeCoders-AI-Citation-System"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contributors"

# Known project makers (will always be listed first)
PROJECT_MAKERS = [
    {"username": "BeastBoom", "name": "Dhruv Gupta"},
    {"username": "kshitijmarwah1", "name": "Kshitij Marwah"}
]

def fetch_contributors():
    """Fetch contributors from GitHub API."""
    try:
        # Add token if available for higher rate limits
        headers = {}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        
        response = requests.get(GITHUB_API_URL, headers=headers)
        response.raise_for_status()
        
        contributors = response.json()
        
        # Sort by contributions (descending) and then by username
        contributors.sort(key=lambda x: (-x.get('contributions', 0), x.get('login', '').lower()))
        
        return contributors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching contributors: {e}")
        return None

def get_contributor_info(username):
    """Get additional info for a contributor from GitHub API."""
    try:
        token = os.getenv("GITHUB_TOKEN")
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"
        
        response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def format_contributor(contributor, is_project_maker=False):
    """Format a contributor entry for the README."""
    username = contributor.get('login', '')
    contributions = contributor.get('contributions', 0)
    html_url = contributor.get('html_url', '')
    
    # Get additional info
    user_info = get_contributor_info(username)
    name = user_info.get('name', '') if user_info else ''
    
    # Use project maker name if available
    if is_project_maker:
        maker_info = next((m for m in PROJECT_MAKERS if m['username'] == username), None)
        if maker_info:
            name = maker_info['name']
    
    # Format the entry
    display_name = name if name else username
    badge = "👑" if is_project_maker else "🤝"
    
    return f"""#### {badge} {display_name}
**GitHub**: [@{username}]({html_url})  
**Contributions**: {contributions} commit{'s' if contributions != 1 else ''}"""

def update_readme(contributors):
    """Update the README.md file with the latest contributors."""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    if not readme_path.exists():
        print(f"README.md not found at {readme_path}")
        return False
    
    # Read the current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Collaborators section
    pattern = r'(## 👥 Collaborators.*?)(?=\n---|\n## |$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find Collaborators section in README.md")
        return False
    
    # Separate project makers from other contributors
    project_maker_usernames = {m['username'] for m in PROJECT_MAKERS}
    project_makers_list = []
    other_contributors_list = []
    
    for contrib in contributors:
        username = contrib.get('login', '')
        if username in project_maker_usernames:
            project_makers_list.append(contrib)
        else:
            other_contributors_list.append(contrib)
    
    # Build the new Collaborators section
    new_section = "## 👥 Collaborators\n\n"
    
    if project_makers_list:
        new_section += "### Project Makers\n\n"
        new_section += "This project was created and maintained by:\n\n"
        new_section += "<div align=\"center\">\n\n"
        
        for contrib in project_makers_list:
            new_section += format_contributor(contrib, is_project_maker=True) + "\n\n"
        
        new_section += "</div>\n\n"
    
    if other_contributors_list:
        new_section += "### Contributors\n\n"
        new_section += "We thank all contributors who have helped improve VibeVerifier:\n\n"
        new_section += "<div align=\"center\">\n\n"
        
        for contrib in other_contributors_list:
            new_section += format_contributor(contrib, is_project_maker=False) + "\n\n"
        
        new_section += "</div>\n\n"
    
    if not project_makers_list and not other_contributors_list:
        new_section += "### Project Makers\n\n"
        new_section += "This project was created and maintained by:\n\n"
        new_section += "<div align=\"center\">\n\n"
        for maker in PROJECT_MAKERS:
            new_section += f"#### 👑 {maker['name']}\n"
            new_section += f"**GitHub**: [@{maker['username']}](https://github.com/{maker['username']})\n\n"
        new_section += "</div>\n\n"
    
    # Replace the Collaborators section
    new_content = content[:match.start()] + new_section + content[match.end():]
    
    # Write the updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Successfully updated README.md with {len(contributors)} contributor(s)")
    return True

def main():
    """Main function."""
    print(f"Fetching contributors from {GITHUB_REPO}...")
    
    contributors = fetch_contributors()
    
    if contributors is None:
        print("❌ Failed to fetch contributors. Using fallback.")
        # Use project makers as fallback
        contributors = []
        for maker in PROJECT_MAKERS:
            contributors.append({
                'login': maker['username'],
                'contributions': 0,
                'avatar_url': '',
                'html_url': f"https://github.com/{maker['username']}"
            })
    
    if update_readme(contributors):
        print("✅ README.md updated successfully!")
    else:
        print("❌ Failed to update README.md")
        sys.exit(1)

if __name__ == "__main__":
    main()

