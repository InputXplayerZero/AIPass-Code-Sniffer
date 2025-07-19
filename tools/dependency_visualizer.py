

import os
import sys
import ast


def analyze_python_dependencies(file_path):
    """
    Analyzes a Python file to extract its import dependencies.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing the file's path and its list of imports.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        return {'error': f"File not found: {file_path}"}
    except Exception as e:
        return {'error': f"Error reading file: {e}"}

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {'error': f"Invalid Python syntax in {file_path}: {e}"}

    dependencies = {
        'file_path': file_path,
        'imports': set()
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies['imports'].add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                dependencies['imports'].add(node.module)

    dependencies['imports'] = sorted(list(dependencies['imports']))
    return dependencies






import subprocess
import json

def analyze_typescript_dependencies(file_path):
    """
    Analyzes a TypeScript/JavaScript file to extract its import dependencies using the ts_analyzer_cli.js Node.js script.

    Args:
        file_path (str): The path to the TypeScript/JavaScript file.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    try:
        # Construct the command to run the Node.js script
        script_path = os.path.join(os.path.dirname(__file__), 'ts_analyzer_cli.js')
        command = ['node', script_path, file_path]
        
        # Execute the command
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Parse the JSON output
        analysis_results = json.loads(process.stdout)
        return analysis_results
    except FileNotFoundError:
        return {'error': "Node.js or ts_analyzer_cli.js not found. Please ensure Node.js is installed and ts_analyzer_cli.js exists in the tools directory.", 'file_path': file_path}
    except subprocess.CalledProcessError as e:
        try:
            # Attempt to parse stderr as JSON if the Node.js script explicitly returned an error in JSON format
            error_output = json.loads(e.stderr)
            return {'error': f"Error analyzing TypeScript/JavaScript file: {error_output.get('error', e.stderr)}", 'file_path': file_path}
        except json.JSONDecodeError:
            return {'error': f"Error analyzing TypeScript/JavaScript file: {e.stderr}", 'file_path': file_path}
    except json.JSONDecodeError:
        return {'error': f"Invalid JSON output from ts_analyzer_cli.js: {process.stdout}", 'file_path': file_path}
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}", 'file_path': file_path}

def analyze_dependencies(file_path):
    """
    Analyzes a file to extract its import dependencies based on its extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.py':
        return analyze_python_dependencies(file_path)
    elif ext in ['.ts', '.tsx', '.js', '.jsx']:
        return analyze_typescript_dependencies(file_path)
    else:
        return {'error': f"Unsupported file type for dependency analysis: {file_path}", 'file_path': file_path}

def format_as_dot(analysis_results, project_root):
    """
    Formats the analysis results into a DOT graph format string.

    Args:
        analysis_results (list): A list of analysis results from analyze_dependencies.
        project_root (str): The root directory of the project being analyzed.

    Returns:
        str: A DOT formatted string for graph visualization.
    """
    local_modules = set()
    project_root_abs = os.path.abspath(project_root)
    if not os.path.isdir(project_root_abs):
        project_root_abs = os.path.dirname(project_root_abs)

    for result in analysis_results:
        if 'error' in result:
            continue
        abs_file_path = os.path.abspath(result['file_path'])
        rel_path = os.path.relpath(abs_file_path, project_root_abs)
        module_name = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
        local_modules.add(module_name)

    dot_string = '''digraph dependencies {
    rankdir=LR;
    node [shape=box, style="rounded,filled", fillcolor=lightgrey];
    graph [splines=ortho];
'''

    all_nodes = set()
    for result in analysis_results:
        if 'error' in result:
            continue
        file_module_name = os.path.splitext(os.path.relpath(os.path.abspath(result['file_path']), project_root_abs))[0].replace(os.path.sep, '.')
        all_nodes.add(file_module_name)
        for imp in result['imports']:
            all_nodes.add(imp)

    for node in sorted(list(all_nodes)):
        if node in local_modules:
            dot_string += f'    "{node}";\n'
        else:
            dot_string += f'    "{node}" [fillcolor=lightblue];\n'

    for result in analysis_results:
        if 'error' in result:
            continue
        file_module_name = os.path.splitext(os.path.relpath(os.path.abspath(result['file_path']), project_root_abs))[0].replace(os.path.sep, '.')
        for imp in result['imports']:
            dot_string += f'    "{file_module_name}" -> "{imp}";\n'

    dot_string += '}'
    return dot_string

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python dependency_visualizer.py <path_to_file_or_directory>")
        sys.exit(1)

    target_path = sys.argv[1]
    all_files = []

    if os.path.isfile(target_path):
        ext = os.path.splitext(target_path)[1].lower()
        if ext in ['.py', '.ts', '.tsx', '.js', '.jsx']:
            all_files.append(target_path)
        else:
            print("Error: Provided file is not a supported code file (.py, .ts, .tsx, .js, .jsx).")
            sys.exit(1)
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.py', '.ts', '.tsx', '.js', '.jsx']:
                    all_files.append(os.path.join(root, file))
    else:
        print(f"Error: Path '{target_path}' is not a valid file or directory.")
        sys.exit(1)

    analysis_results = [analyze_dependencies(f) for f in all_files]
    valid_results = [res for res in analysis_results if 'error' not in res]

    dot_output = format_as_dot(valid_results, target_path)
    print(dot_output)


