
import os
import sys
import json
from code_summarizer import analyze_code, format_as_markdown as format_summary_as_markdown
from dependency_visualizer import analyze_dependencies, format_as_dot

ABILITY_CARD_TEMPLATE = """
# Ability Card: {ability_name}

**Project:** `{project_name}`

**Description:**
{description}

---

## Entry Points

*   `{entry_point_file}`

---

## Components

### Code Summary

{code_summary}

### Dependency Graph

```dot
{dependency_graph}
```

---

## Best Practices & Observations

*   (To be filled in manually)

---

## Potential for AIPass-Echosystem

*   (To be filled in manually)

"""

def detect_language(file_path):
    """
    Detects the programming language based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.py':
        return 'python'
    elif ext in ['.ts', '.tsx', '.js', '.jsx']:
        return 'typescript/javascript' # Grouping for now, can be more granular later
    else:
        return 'unsupported'

def generate_ability_card(target_path, project_name):
    """
    Generates a draft "Ability Card" for a given file or directory, with language detection.
    """
    language = detect_language(target_path)
    
    code_summary_md = ""
    dep_graph_dot = ""
    entry_point_file = os.path.basename(target_path)
    ability_name = entry_point_file.replace(os.path.splitext(entry_point_file)[1], '').replace('_', ' ').title()
    description = f"(A brief, one-sentence description of the ability's primary function, to be filled in manually)."

    # 1. Analyze the code structure
    code_analysis = analyze_code(target_path, language)
    if 'file_path' not in code_analysis:
        code_analysis['file_path'] = target_path
    code_summary_md = format_summary_as_markdown(code_analysis)

    # 2. Analyze dependencies
    all_files = []
    if os.path.isfile(target_path):
        all_files.append(target_path)
    else:
        for root, _, files in os.walk(target_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.py', '.ts', '.tsx', '.js', '.jsx']:
                    all_files.append(os.path.join(root, file))
    
    dep_analysis_results = [analyze_dependencies(f) for f in all_files]
    valid_deps = [res for res in dep_analysis_results if 'error' not in res]
    dep_graph_dot = format_as_dot(valid_deps, target_path)

    if 'error' in code_analysis:
        code_summary_md = f"**Error:** {code_analysis['error']}"
    if not valid_deps:
        dep_graph_dot = f"**Note:** No dependencies found or supported for {language} files."
    
    # 3. Populate the template
    card = ABILITY_CARD_TEMPLATE.format(
        ability_name=ability_name,
        project_name=project_name,
        description=description,
        entry_point_file=entry_point_file,
        code_summary=code_summary_md,
        dependency_graph=dep_graph_dot
    )

    return card

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python ability_extractor.py <path_to_file_or_dir> <project_name>")
        sys.exit(1)

    target_path = sys.argv[1]
    project_name = sys.argv[2]

    ability_card_md = generate_ability_card(target_path, project_name)

    output_filename = f"AbilityCard_{os.path.basename(target_path).replace(os.path.splitext(target_path)[1], '')}.md"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(ability_card_md)

    print(f"Successfully generated Ability Card: {output_filename}")
