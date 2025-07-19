

import os
import sys
import re

def find_ability_cards(analysis_dir):
    """
    Finds all Ability Card Markdown files in the analysis directory.

    Args:
        analysis_dir (str): The path to the analysis directory.

    Returns:
        list: A list of paths to the Ability Card files.
    """
    ability_cards = []
    for root, _, files in os.walk(analysis_dir):
        for file in files:
            if file.startswith('AbilityCard_') and file.endswith('.md'):
                ability_cards.append(os.path.join(root, file))
    return ability_cards

def extract_card_metadata(card_path):
    """
    Extracts metadata (Ability Name, Project, Description) from an Ability Card.

    Args:
        card_path (str): The path to the Ability Card file.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """
    metadata = {
        'file_path': os.path.relpath(card_path)
    }
    try:
        with open(card_path, 'r', encoding='utf-8') as f:
            content = f.read()

        name_match = re.search(r"# Ability Card: (.*)", content)
        if name_match:
            metadata['name'] = name_match.group(1).strip()

        project_match = re.search(r"\*\*Project:\*\* `(.*)`", content)
        if project_match:
            metadata['project'] = project_match.group(1).strip()

        description_match = re.search(r"\*\*Description:\*\*\n(.*)", content)
        if description_match:
            metadata['description'] = description_match.group(1).strip()

        return metadata
    except Exception:
        return None

def update_abilities_index(analysis_dir):
    """
    Updates the ABILITIES_INDEX.md file with the latest Ability Cards.

    Args:
        analysis_dir (str): The path to the analysis directory.
    """
    cards = find_ability_cards(analysis_dir)
    all_metadata = [extract_card_metadata(card) for card in cards]
    valid_metadata = [m for m in all_metadata if m and 'name' in m]

    index_path = os.path.join(analysis_dir, 'ABILITIES_INDEX.md')

    # Group by project
    projects = {}
    for meta in valid_metadata:
        project_name = meta.get('project', 'Uncategorized')
        if project_name not in projects:
            projects[project_name] = []
        projects[project_name].append(meta)

    # Generate Markdown
    markdown = "# Abilities Index\n\nThis index provides a comprehensive list of all identified 'Abilities' from the analyzed open-source projects.\n\n---\n\n"

    for project, abilities in sorted(projects.items()):
        markdown += f"## {project}\n\n"
        markdown += "| Ability Name | Description | File Path |\n"
        markdown += "|--------------|-------------|-----------|\n"
        for ability in sorted(abilities, key=lambda x: x['name']):
            description = ability.get('description', '(No description provided)')
            # Prevent breaking the table with newlines
            description = description.replace('\n', ' ').replace('|', ' ')
            markdown += f"| {ability['name']} | {description} | [`{os.path.basename(ability['file_path'])}`]({ability['file_path']}) |\n"
        markdown += "\n"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Successfully updated '{index_path}'")

if __name__ == '__main__':
    # By default, this script will look for the 'analysis' directory
    # in the parent directory of the 'tools' directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    analysis_directory = os.path.join(base_dir, 'analysis')

    if not os.path.isdir(analysis_directory):
        print(f"Error: Analysis directory not found at '{analysis_directory}'")
        sys.exit(1)

    update_abilities_index(analysis_directory)

