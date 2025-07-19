#!/usr/bin/env python3
"""
Main CLI entry point for AIPass-Code-Sniffer.
"""

import argparse
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from commands.analyze import analyze_command
from utils.index_updater import update_abilities_index


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AIPass-Code-Sniffer: Automated codebase analysis and ability extraction tools',
        prog='code-sniffer'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Enhanced analysis command (replaces old extract)
    analyze_parser = subparsers.add_parser(
        'analyze', 
        help='Analyze codebase with AI-enhanced semantic understanding'
    )
    analyze_parser.add_argument(
        'path', 
        help='Path to the file or directory to analyze'
    )
    analyze_parser.add_argument(
        '--level', '-l',
        choices=['basic', 'enhanced', 'premium'],
        default='enhanced',
        help='Analysis level: basic (syntax only), enhanced (AI summaries), premium (full AI analysis)'
    )
    analyze_parser.add_argument(
        '--output', '-o',
        default='./output/ability_cards',
        help='Output directory for ability cards (default: ./output/ability_cards)'
    )
    
    # Legacy extract command (redirects to analyze)
    extract_parser = subparsers.add_parser(
        'extract', 
        help='Extract abilities from codebase (legacy - use analyze instead)'
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
        if args.command == 'analyze':
            # Run enhanced analysis
            import asyncio
            return asyncio.run(analyze_command(
                args.path, 
                args.level, 
                args.output
            ))
            
        elif args.command == 'extract':
            # Legacy command - redirect to analyze with enhanced level
            print("ℹ️ 'extract' command is deprecated. Use 'analyze' instead.")
            print(f"Running enhanced analysis on: {args.path}")
            import asyncio
            return asyncio.run(analyze_command(
                args.path, 
                'enhanced', 
                args.output
            ))
            
        elif args.command == 'visualize':
            print(f"Visualizing dependencies for: {args.path}")
            print(f"Output directory: {args.output}")
            print("⚠️  Standalone visualize functionality will be implemented in Phase 3")
            print("   Use 'analyze' command for comprehensive analysis including dependencies")
            
        elif args.command == 'index':
            print(f"Updating abilities index from: {args.analysis_dir}")
            update_abilities_index(args.analysis_dir)
            print("✅ Index updated successfully!")
            return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
