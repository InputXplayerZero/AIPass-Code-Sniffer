#!/usr/bin/env python3
"""
Main CLI entry point for AIPass-Code-Sniffer.
"""

import argparse
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import functions will be added when we refactor the main functions
# from core.ability_extractor import main as extract_abilities
# from core.dependency_visualizer import main as visualize_dependencies
from utils.index_updater import update_abilities_index


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AIPass-Code-Sniffer: Automated codebase analysis and ability extraction tools',
        prog='code-sniffer'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract abilities command
    extract_parser = subparsers.add_parser(
        'extract', 
        help='Extract abilities from codebase'
    )
    extract_parser.add_argument(
        'path', 
        help='Path to the codebase to analyze'
    )
    extract_parser.add_argument(
        '--output', '-o',
        default='./output/ability_cards',
        help='Output directory for ability cards (default: ./output/ability_cards)'
    )
    
    # Visualize dependencies command
    visualize_parser = subparsers.add_parser(
        'visualize',
        help='Generate dependency visualization'
    )
    visualize_parser.add_argument(
        'path',
        help='Path to the codebase to analyze'
    )
    visualize_parser.add_argument(
        '--output', '-o',
        default='./output/dependency_graphs',
        help='Output directory for dependency graphs (default: ./output/dependency_graphs)'
    )
    
    # Update index command
    index_parser = subparsers.add_parser(
        'index',
        help='Update abilities index'
    )
    index_parser.add_argument(
        '--analysis-dir',
        default='./output/ability_cards',
        help='Directory containing ability cards (default: ./output/ability_cards)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'extract':
            print(f"Extracting abilities from: {args.path}")
            print(f"Output directory: {args.output}")
            print("⚠️  Extract functionality will be implemented in Phase 3")
            print("   Current tools are in src/core/ability_extractor.py")
            
        elif args.command == 'visualize':
            print(f"Visualizing dependencies for: {args.path}")
            print(f"Output directory: {args.output}")
            print("⚠️  Visualize functionality will be implemented in Phase 3")
            print("   Current tools are in src/core/dependency_visualizer.py")
            
        elif args.command == 'index':
            print(f"Updating abilities index from: {args.analysis_dir}")
            update_abilities_index(args.analysis_dir)
            
        print("✅ Operation completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
