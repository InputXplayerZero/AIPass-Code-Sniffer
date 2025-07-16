import os
import argparse

def map_directory(root_dir, max_depth):
    """
    Generates a string representation of the directory structure.
    """
    tree = ""
    for root, dirs, files in os.walk(root_dir):
        depth = root.replace(root_dir, '').count(os.sep)
        if depth > max_depth:
            del dirs[:]  # Don't go deeper
            continue

        indent = ' ' * 4 * depth
        tree += f"{indent}{os.path.basename(root)}/\n"
        
        sub_indent = ' ' * 4 * (depth + 1)
        for f in files:
            tree += f"{sub_indent}{f}\n"
    return tree

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Map a directory structure to a specified depth.')
    parser.add_argument('directory', type=str, help='The root directory to map.')
    parser.add_argument('--depth', type=int, default=2, help='The maximum depth to map.')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at {args.directory}")
    else:
        project_map = map_directory(args.directory, args.depth)
        with open("project_map.txt", "w") as f:
            f.write(project_map)
        print(f"Project map saved to project_map.txt")