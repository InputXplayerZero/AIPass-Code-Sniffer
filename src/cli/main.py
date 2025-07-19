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
    analyze_parser.add_argument(
        '--budget', '-b',
        type=int,
        help='Token budget limit (e.g., 20000). Analysis stops when budget is reached.'
    )
    analyze_parser.add_argument(
        '--sample', '-s',
        type=str,
        help='Sample percentage of files (e.g., "10%%" or "50"). Useful for large codebases.'
    )
    analyze_parser.add_argument(
        '--incremental', '-i',
        action='store_true',
        help='Skip files that have already been analyzed (based on output directory)'
    )
    analyze_parser.add_argument(
        '--skills', '-sk',
        action='store_true',
        help='Include skill detection and extraction recommendations'
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
    
    # Skill discovery command
    skills_parser = subparsers.add_parser(
        'discover-skills',
        help='Discover and analyze extractable skills in codebase'
    )
    skills_parser.add_argument(
        'path',
        help='Path to the codebase to analyze for skills'
    )
    skills_parser.add_argument(
        '--output', '-o',
        default='./output/skill_reports',
        help='Output directory for skill reports (default: ./output/skill_reports)'
    )
    
    # Update index command
    index_parser = subparsers.add_parser(
        'index',
        help='Update abilities index'
    )
    index_parser.add_argument(
        '--directory', '-d',
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
            # Create a compatible args object
            analyze_args = type('Args', (), {
                'target': args.path,
                'level': args.level,
                'output': args.output,
                'budget': getattr(args, 'budget', None),
                'sample': getattr(args, 'sample', None),
                'incremental': getattr(args, 'incremental', False)
            })()
            return asyncio.run(analyze_command(analyze_args))
            
        elif args.command == 'discover-skills':
            # Run skill discovery
            from core.skill_analyzer import SkillAnalyzer
            analyzer = SkillAnalyzer()
            report = analyzer.analyze_codebase(args.path, args.output)
            print(f"\n🎯 Skill Discovery Complete!")
            print(f"📊 Found {report.total_skills_detected} skills in {report.total_files_analyzed} files")
            print(f"🔥 {len(report.high_priority_skills)} high-priority skills identified")
            print(f"📋 Reports saved to: {args.output}")
            return 0
            
        elif args.command == 'extract':
            # Legacy command - redirect to analyze with enhanced level
            print("ℹ️ 'extract' command is deprecated. Use 'analyze' instead.")
            print(f"Running enhanced analysis on: {args.path}")
            import asyncio
            # Create a compatible args object
            analyze_args = type('Args', (), {
                'target': args.path,
                'level': 'enhanced',
                'output': args.output
            })()
            return asyncio.run(analyze_command(analyze_args))
            
        elif args.command == 'visualize':
            print(f"Visualizing dependencies for: {args.path}")
            print(f"Output directory: {args.output}")
            print("⚠️  Standalone visualize functionality will be implemented in Phase 3")
            print("   Use 'analyze' command for comprehensive analysis including dependencies")
            
        elif args.command == 'index':
            print(f"Updating abilities index from: {args.analysis_dir}")
            update_abilities_index(args.analysis_dir)
            print("[+] Index updated successfully!")
            return 0
        
    except Exception as e:
        print(f"[!] Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
