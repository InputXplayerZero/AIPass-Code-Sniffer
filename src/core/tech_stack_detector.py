import os
import json
import toml
import re

def detect_tech_stack(project_path):
    tech_stack = {
        "languages": set(),
        "frameworks": set(),
        "libraries": set(),
        "build_tools": set(),
        "package_managers": set()
    }

    # Helper to add unique items (now using sets)
    def add_unique(category, item):
        tech_stack[category].add(item)

    for root, dirs, files in os.walk(project_path):
        # Skip common non-code directories
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'build', 'dist', 'venv', '.venv', '__pycache__')]

        # --- JavaScript/TypeScript Detection ---
        if "package.json" in files:
            package_json_path = os.path.join(root, "package.json")
            tsconfig_json_path = os.path.join(root, "tsconfig.json")

            add_unique("languages", "JavaScript")
            add_unique("languages", "Node.js") # Node.js is implied by package.json
            add_unique("package_managers", "npm/yarn/pnpm")
            try:
                with open(package_json_path, "r", encoding='utf-8') as f:
                    package_data = json.load(f)
                    
                    all_deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

                    if "typescript" in all_deps or "typescript-eslint" in all_deps or os.path.exists(tsconfig_json_path):
                        add_unique("languages", "TypeScript")
                    
                    # Frameworks
                    if "react" in all_deps or "eslint-plugin-react" in all_deps or "react-devtools-core" in all_deps:
                        add_unique("frameworks", "React")
                    if "next" in all_deps:
                        add_unique("frameworks", "Next.js")
                    if "express" in all_deps:
                        add_unique("frameworks", "Express.js")
                    if "angular" in all_deps:
                        add_unique("frameworks", "Angular")
                    if "vue" in all_deps:
                        add_unique("frameworks", "Vue.js")
                    if "yargs" in all_deps:
                        add_unique("frameworks", "Yargs (CLI)")

                    # Build Tools / Linters / Testers
                    if "webpack" in all_deps:
                        add_unique("build_tools", "Webpack")
                    if "esbuild" in all_deps:
                        add_unique("build_tools", "esbuild")
                    if "vite" in all_deps:
                        add_unique("build_tools", "Vite")
                    if "jest" in all_deps:
                        add_unique("build_tools", "Jest (Testing)")
                    if "vitest" in all_deps:
                        add_unique("build_tools", "Vitest (Testing)")
                    if "eslint" in all_deps:
                        add_unique("build_tools", "ESLint (Linting)")
                    if "prettier" in all_deps:
                        add_unique("build_tools", "Prettier (Formatting)")
                    if "turbo" in all_deps:
                        add_unique("build_tools", "Turborepo (Monorepo)")
                    if "gulp" in all_deps:
                        add_unique("build_tools", "Gulp (Task Runner)")
                    if "rollup" in all_deps:
                        add_unique("build_tools", "Rollup (Bundler)")

                    # Libraries (examples)
                    if "lodash" in all_deps:
                        add_unique("libraries", "Lodash (Utility)")
                    if "axios" in all_deps or "node-fetch" in all_deps:
                        add_unique("libraries", "HTTP Client")
                    if "@modelcontextprotocol/sdk" in all_deps:
                        add_unique("libraries", "Model Context Protocol SDK")
                    if "electron" in all_deps:
                        add_unique("frameworks", "Electron (Desktop App)")

            except json.JSONDecodeError:
                pass # Malformed JSON

        # --- Python Detection ---
        if "requirements.txt" in files or "pyproject.toml" in files:
            add_unique("languages", "Python")
            
            requirements_txt_path = os.path.join(root, "requirements.txt")
            if os.path.exists(requirements_txt_path):
                add_unique("package_managers", "pip")
                try:
                    with open(requirements_txt_path, "r", encoding='utf-8') as f:
                        content = f.read()
                        if re.search(r"django", content, re.IGNORECASE):
                            add_unique("frameworks", "Django")
                        if re.search(r"flask", content, re.IGNORECASE):
                            add_unique("frameworks", "Flask")
                        if re.search(r"fastapi", content, re.IGNORECASE):
                            add_unique("frameworks", "FastAPI")
                        if re.search(r"numpy|pandas|scipy|matplotlib|seaborn", content, re.IGNORECASE):
                            add_unique("libraries", "Data Science/Analysis Libraries")
                        if re.search(r"tensorflow|pytorch|scikit-learn|huggingface", content, re.IGNORECASE):
                            add_unique("libraries", "Machine Learning Libraries")
                        if re.search(r"requests", content, re.IGNORECASE):
                            add_unique("libraries", "Requests (HTTP Client)")
                        if re.search(r"typer|click", content, re.IGNORECASE):
                            add_unique("frameworks", "CLI Framework (Python)")
                        if re.search(r"mcp", content, re.IGNORECASE):
                            add_unique("libraries", "Model Context Protocol (Python)")

                except Exception: # Catch all for file read errors
                    pass
            
            pyproject_toml_path = os.path.join(root, "pyproject.toml")
            if os.path.exists(pyproject_toml_path):
                add_unique("package_managers", "Poetry")
                try:
                    with open(pyproject_toml_path, "r", encoding='utf-8') as f:
                        pyproject_data = toml.load(f)
                        if "tool" in pyproject_data and "poetry" in pyproject_data["tool"] and "dependencies" in pyproject_data["tool"]["poetry"]:
                            dependencies = pyproject_data["tool"]["poetry"]["dependencies"]
                            
                            if "django" in dependencies:
                                add_unique("frameworks", "Django")
                            if "flask" in dependencies:
                                add_unique("frameworks", "Flask")
                            if "fastapi" in dependencies:
                                add_unique("frameworks", "FastAPI")
                            if any(lib in dependencies for lib in ["numpy", "pandas", "scipy", "matplotlib", "seaborn"]):
                                add_unique("libraries", "Data Science/Analysis Libraries")
                            if any(lib in dependencies for lib in ["tensorflow", "pytorch", "scikit-learn", "huggingface"]):
                                add_unique("libraries", "Machine Learning Libraries")
                            if "requests" in dependencies:
                                add_unique("libraries", "Requests (HTTP Client)")
                            if any(lib in dependencies for lib in ["typer", "click"]):
                                add_unique("frameworks", "CLI Framework (Python)")
                            if "mcp" in dependencies:
                                add_unique("libraries", "Model Context Protocol (Python)")

                except Exception: # Catch all for file read/toml parse errors
                    pass

        # --- Java Detection ---
        if "pom.xml" in files or "build.gradle" in files:
            add_unique("languages", "Java")
            if "pom.xml" in files:
                add_unique("build_tools", "Maven")
            if "build.gradle" in files:
                add_unique("build_tools", "Gradle")

        # --- Rust Detection ---
        if "Cargo.toml" in files:
            add_unique("languages", "Rust")
            add_unique("package_managers", "Cargo")

        # --- Go Detection ---
        if "go.mod" in files:
            add_unique("languages", "Go")
            add_unique("package_managers", "Go Modules")

        # --- C# Detection ---
        csproj_files = [f for f in files if f.endswith(".csproj")]
        if csproj_files:
            add_unique("languages", "C#")
            add_unique("frameworks", ".NET")

    # Convert sets to sorted lists for consistent output
    for key in tech_stack:
        tech_stack[key] = sorted(list(tech_stack[key]))
    
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