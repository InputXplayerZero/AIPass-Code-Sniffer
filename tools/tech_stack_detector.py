import os
import json
import toml
import re

def detect_tech_stack(project_path):
    tech_stack = {
        "languages": [],
        "frameworks": [],
        "libraries": [],
        "build_tools": [],
        "package_managers": []
    }

    # --- JavaScript/TypeScript Detection ---
    package_json_path = os.path.join(project_path, "package.json")
    if os.path.exists(package_json_path):
        tech_stack["languages"].append("JavaScript/TypeScript")
        tech_stack["package_managers"].append("npm/yarn/pnpm")
        try:
            with open(package_json_path, "r") as f:
                package_data = json.load(f)
                if "devDependencies" in package_data:
                    if "typescript" in package_data["devDependencies"]:
                        tech_stack["languages"].append("TypeScript")
                    if "react" in package_data["devDependencies"] or "react" in package_data.get("dependencies", {}):
                        tech_stack["frameworks"].append("React")
                    if "next" in package_data["devDependencies"] or "next" in package_data.get("dependencies", {}):
                        tech_stack["frameworks"].append("Next.js")
                    if "express" in package_data["devDependencies"] or "express" in package_data.get("dependencies", {}):
                        tech_stack["frameworks"].append("Express.js")
                    if "webpack" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("Webpack")
                    if "esbuild" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("esbuild")
                    if "vite" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("Vite")
                    if "jest" in package_data["devDependencies"] or "vitest" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("Testing Framework (Jest/Vitest)")
                    if "eslint" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("ESLint")
                    if "prettier" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("Prettier")
                    if "turbo" in package_data["devDependencies"]:
                        tech_stack["build_tools"].append("Turborepo")

        except json.JSONDecodeError:
            pass # Malformed JSON

    # --- Python Detection ---
    requirements_txt_path = os.path.join(project_path, "requirements.txt")
    pyproject_toml_path = os.path.join(project_path, "pyproject.toml")
    
    if os.path.exists(requirements_txt_path) or os.path.exists(pyproject_toml_path):
        tech_stack["languages"].append("Python")
        if os.path.exists(requirements_txt_path):
            tech_stack["package_managers"].append("pip")
            try:
                with open(requirements_txt_path, "r") as f:
                    content = f.read()
                    if re.search(r"django", content, re.IGNORECASE):
                        tech_stack["frameworks"].append("Django")
                    if re.search(r"flask", content, re.IGNORECASE):
                        tech_stack["frameworks"].append("Flask")
                    if re.search(r"fastapi", content, re.IGNORECASE):
                        tech_stack["frameworks"].append("FastAPI")
                    if re.search(r"numpy|pandas|matplotlib", content, re.IGNORECASE):
                        tech_stack["libraries"].append("Data Science/Analysis Libraries")
                    if re.search(r"tensorflow|pytorch", content, re.IGNORECASE):
                        tech_stack["libraries"].append("Machine Learning Libraries")
            except Exception: # Catch all for file read errors
                pass
        
        if os.path.exists(pyproject_toml_path):
            tech_stack["package_managers"].append("Poetry")
            try:
                with open(pyproject_toml_path, "r") as f:
                    pyproject_data = toml.load(f)
                    if "tool" in pyproject_data and "poetry" in pyproject_data["tool"] and "dependencies" in pyproject_data["tool"]["poetry"]:
                        dependencies = pyproject_data["tool"]["poetry"]["dependencies"]
                        if "django" in dependencies:
                            tech_stack["frameworks"].append("Django")
                        if "flask" in dependencies:
                            tech_stack["frameworks"].append("Flask")
                        if "fastapi" in dependencies:
                            tech_stack["frameworks"].append("FastAPI")
                        if any(lib in dependencies for lib in ["numpy", "pandas", "matplotlib"]):
                            tech_stack["libraries"].append("Data Science/Analysis Libraries")
                        if any(lib in dependencies for lib in ["tensorflow", "pytorch"]):
                            tech_stack["libraries"].append("Machine Learning Libraries")
            except Exception: # Catch all for file read/toml parse errors
                pass

    # --- Java Detection ---
    pom_xml_path = os.path.join(project_path, "pom.xml")
    build_gradle_path = os.path.join(project_path, "build.gradle")
    
    if os.path.exists(pom_xml_path) or os.path.exists(build_gradle_path):
        tech_stack["languages"].append("Java")
        if os.path.exists(pom_xml_path):
            tech_stack["build_tools"].append("Maven")
        if os.path.exists(build_gradle_path):
            tech_stack["build_tools"].append("Gradle")

    # --- Rust Detection ---
    cargo_toml_path = os.path.join(project_path, "Cargo.toml")
    if os.path.exists(cargo_toml_path):
        tech_stack["languages"].append("Rust")
        tech_stack["package_managers"].append("Cargo")

    # Remove duplicates and empty lists
    for key in tech_stack:
        tech_stack[key] = sorted(list(set(tech_stack[key])))
    
    return tech_stack

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Detect the technology stack of a project.')
    parser.add_argument('project_path', type=str, help='The path to the project directory.')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.project_path):
        print(f"Error: Project directory not found at {args.project_path}")
    else:
        stack = detect_tech_stack(args.project_path)
        print("Detected Technology Stack:")
        for category, items in stack.items():
            if items:
                print(f"  {category.replace("_", " ").title()}: {", ".join(items)}")
