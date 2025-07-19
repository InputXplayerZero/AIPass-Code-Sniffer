
import ast
import sys
import os


def analyze_python_code(file_path):
    """
    Analyzes a Python file to extract information about its classes and functions.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing the analysis results.
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

    results = {
        'file_path': file_path,
        'functions': [],
        'classes': []
    }
    
    # To avoid adding methods to the top-level functions list, we first find all classes
    class_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    method_nodes = []
    for class_node in class_nodes:
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                method_nodes.append(node)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node not in method_nodes:
            function_info = {
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'docstring': ast.get_docstring(node)
            }
            results['functions'].append(function_info)
        elif isinstance(node, ast.ClassDef):
            class_info = {
                'name': node.name,
                'methods': [],
                'docstring': ast.get_docstring(node)
            }
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_info = {
                        'name': method.name,
                        'args': [arg.arg for arg in method.args.args],
                        'docstring': ast.get_docstring(method)
                    }
                    class_info['methods'].append(method_info)
            results['classes'].append(class_info)
            
    return results





import subprocess
import json

def analyze_typescript_code(file_path):
    """
    Analyzes a TypeScript/JavaScript file using the ts_analyzer_cli.js Node.js script.

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

def analyze_code(file_path, language):
    """
    Analyzes a code file based on its detected language.
    """
    if language == 'python':
        return analyze_python_code(file_path)
    elif language == 'typescript/javascript':
        return analyze_typescript_code(file_path)
    else:
        return {'error': f"Unsupported language for analysis: {language}", 'file_path': file_path}


def format_as_markdown(analysis):
    """
    Formats the analysis results into a Markdown string.

    Args:
        analysis (dict): The analysis results from analyze_python_code or analyze_typescript_code.

    Returns:
        str: A Markdown formatted string.
    """
    if 'error' in analysis:
        return f"**Error:** {analysis['error']}"

    markdown = f"# Analysis for `{analysis['file_path']}`\n\n"

    if analysis['classes']:
        markdown += "## Classes\n\n"
        for cls in analysis['classes']:
            markdown += f"### `class {cls['name']}`\n\n"
            if cls['docstring']:
                markdown += f"**Docstring:**\n```\n{cls['docstring']}\n```\n\n"
            if cls['methods']:
                markdown += "**Methods:**\n\n"
                for method in cls['methods']:
                    args_str = ", ".join(method['args'])
                    markdown += f"- **`{method['name']}({args_str})`**\n"
                    if method['docstring']:
                        docstring_preview = method['docstring'].strip().split('\n')[0]
                        markdown += f"  - *Docstring:* {docstring_preview}\n"
            markdown += "\n---\n\n"

    if analysis['functions']:
        markdown += "## Top-Level Functions\n\n"
        for func in analysis['functions']:
            args_str = ", ".join(func['args'])
            markdown += f"### `def {func['name']}({args_str})`\n\n"
            if func['docstring']:
                markdown += f"**Docstring:**\n```\n{func['docstring']}\n```\n\n"
            markdown += "\n---\n\n"

    return markdown

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        # Assuming language detection happens before calling analyze_code
        # For testing purposes, we'll assume Python for now.
        # In ability_extractor, this will be properly detected.
        analysis = analyze_python_code(file_path) # This will be analyze_code(file_path, detected_language)
        markdown_output = format_as_markdown(analysis)
        print(markdown_output)
    else:
        print("Usage: python code_summarizer.py <path_to_python_file>")
