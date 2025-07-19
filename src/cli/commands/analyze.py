"""
Enhanced analysis command with AI-powered semantic understanding.
"""

import os
import sys
import json
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from analyzers.python import EnhancedPythonAnalyzer
from analyzers.typescript.semantic_analyzer import EnhancedTypeScriptAnalyzer, analyze_typescript_file_enhanced
from core.dependency_visualizer import analyze_python_dependencies, analyze_typescript_dependencies
from utils.index_updater import update_abilities_index
from core.skill_analyzer import SkillAnalyzer


class EnhancedAnalyzer:
    """Enhanced analyzer with AI capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', '..', '..', 'config', 'ai_config.json'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load AI configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file not found: {self.config_path}")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid JSON in config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration when config file is unavailable."""
        return {
            "ai_services": {},
            "analysis_levels": {
                "basic": {
                    "enabled_features": ["syntax", "dependencies"],
                    "ai_features": []
                },
                "enhanced": {
                    "enabled_features": ["syntax", "dependencies", "ai_summary"],
                    "ai_features": ["summary"]
                },
                "premium": {
                    "enabled_features": ["syntax", "dependencies", "ai_summary", "semantic_analysis", "pattern_detection", "quality_assessment"],
                    "ai_features": ["summary", "semantic", "patterns", "quality"]
                }
            }
        }
    
    def get_supported_extensions(self) -> Dict[str, str]:
        """Get supported file extensions and their languages."""
        return {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript'
        }
    
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        supported = self.get_supported_extensions()
        return supported.get(ext, 'unknown')
    
    async def analyze_file(self, file_path: str, analysis_level: str = "enhanced", 
                          output_dir: str = "./output/ability_cards") -> Dict[str, Any]:
        """Analyze a single file with specified analysis level."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        language = self.detect_language(file_path)
        if language == 'unknown':
            return {"error": f"Unsupported file type: {file_path}"}
        
        print(f"🔍 Analyzing {file_path} ({language}) at {analysis_level} level...")
        
        try:
            if language in ['typescript', 'javascript']:
                # Use enhanced TypeScript analyzer
                analysis = await analyze_typescript_file_enhanced(file_path, analysis_level)
                
                # Generate enhanced ability card
                analyzer = EnhancedTypeScriptAnalyzer(self.config)
                ability_card = analyzer.to_enhanced_ability_card(analysis)
                
                # Save ability card
                os.makedirs(output_dir, exist_ok=True)
                file_name = os.path.basename(file_path)
                card_name = f"Enhanced_AbilityCard_{file_name.replace('.', '_')}.md"
                card_path = os.path.join(output_dir, card_name)
                
                with open(card_path, 'w', encoding='utf-8') as f:
                    f.write(ability_card)
                
                return {
                    "file_path": file_path,
                    "language": language,
                    "analysis_level": analysis_level,
                    "ability_card": card_path,
                    "functions": len(analysis.functions),
                    "classes": len(analysis.classes),
                    "imports": len(analysis.imports),
                    "ai_enhanced": bool(analysis.semantic_analysis or analysis.ai_summary),
                    "quality_score": analysis.quality_assessment.overall_score if analysis.quality_assessment else None
                }
            
            elif language == 'python':
                # Use enhanced Python analyzer
                python_analyzer = EnhancedPythonAnalyzer()
                analysis = await python_analyzer.analyze_file(file_path, analysis_level)
                
                # Generate ability card
                card_path = python_analyzer.generate_ability_card(analysis, output_dir)
                
                return {
                    "file_path": file_path,
                    "language": language,
                    "analysis_level": analysis_level,
                    "ability_card": card_path,
                    "functions": len(analysis.functions),
                    "classes": len(analysis.classes),
                    "imports": len(analysis.imports),
                    "ai_enhanced": bool(analysis.semantic_analysis or analysis.ai_summary),
                    "quality_score": analysis.quality_assessment.overall_score if analysis.quality_assessment else None
                }
            
            else:
                return {"error": f"Unsupported language: {language}"}
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _has_existing_card(self, file_path: str, existing_cards: set) -> bool:
        """Check if an ability card already exists for this file."""
        file_name = os.path.basename(file_path)
        card_name = f"Enhanced_AbilityCard_{file_name.replace('.', '_')}.md"
        return card_name in existing_cards
    
    def _generate_basic_ability_card(self, file_path: str, analysis: Dict[str, Any], language: str) -> str:
        """Generate a basic ability card for non-AI analysis."""
        file_name = os.path.basename(file_path)
        ability_name = file_name.replace('.py', '').replace('_', ' ').title()
        
        imports = analysis.get("imports", [])
        
        return f"""# Ability Card: {ability_name}

**File:** `{file_path}`  
**Language:** {language.title()}  
**Analysis Level:** Basic

## Description

Python module with {len(imports)} imports detected.

## Technical Details

- **Imports:** {len(imports)}
- **Dependencies:** {', '.join(imports[:5])}{'...' if len(imports) > 5 else ''}

## Dependencies

{chr(10).join(f"- {imp}" for imp in imports)}

---
*Generated by AIPass-Code-Sniffer Basic Analyzer*
*Upgrade to enhanced/premium analysis for AI-powered insights*
"""
    
    async def analyze_directory(self, dir_path: str, analysis_level: str = "enhanced",
                               output_dir: str = "./output/ability_cards", budget: Optional[int] = None,
                               sample: Optional[str] = None, incremental: bool = False) -> Dict[str, Any]:
        """Analyze all supported files in a directory."""
        if not os.path.exists(dir_path):
            return {"error": f"Directory not found: {dir_path}"}
        
        supported_extensions = set(self.get_supported_extensions().keys())
        files_to_analyze = []
        
        # Define ignore patterns for configuration and build files
        ignore_dirs = {
            '.git', '.github', '.vscode', '.idea', 
            'node_modules', 'dist', 'build', 'coverage',
            '__pycache__', '.pytest_cache', '.mypy_cache',
            'venv', '.venv', 'env', '.env',
            '.husky', '.devcontainer', 'patches'
        }
        
        ignore_patterns = {
            # Configuration files
            'package.json', 'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock',
            'tsconfig.json', 'jsconfig.json', 'webpack.config.js',
            'rollup.config.js', 'vite.config.js', 'vitest.config.js',
            'jest.config.js', 'babel.config.js', 'eslint.config.js',
            '.prettierrc', '.eslintrc', '.gitignore', '.gitattributes',
            'requirements.txt', 'setup.py', 'pyproject.toml',
            # Build and deployment
            'Dockerfile', 'docker-compose.yml', 'Makefile',
            'flake.nix', 'flake.lock', 'cliff.toml',
            # Documentation (unless specifically analyzing docs)
            'README.md', 'CHANGELOG.md', 'LICENSE', 'NOTICE'
        }
        
        def should_ignore_file(file_path: str) -> bool:
            """Check if file should be ignored based on patterns."""
            file_name = os.path.basename(file_path)
            
            # Skip configuration files
            if file_name in ignore_patterns:
                return True
                
            # Skip test files (optional - comment out if you want to analyze tests)
            if '.test.' in file_name or '.spec.' in file_name:
                return True
                
            # Skip type definition files
            if file_name.endswith('.d.ts'):
                return True
                
            return False
        
        # Find all supported files with ignore filtering
        for root, dirs, files in os.walk(dir_path):
            # Remove ignored directories from traversal
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    if not should_ignore_file(file_path):
                        files_to_analyze.append(file_path)
        
        if not files_to_analyze:
            return {"error": "No supported files found in directory"}
        
        # Apply sampling if specified
        if sample:
            import random
            if sample.endswith('%'):
                sample_pct = float(sample[:-1]) / 100
            else:
                sample_pct = float(sample) / 100
            
            sample_size = max(1, int(len(files_to_analyze) * sample_pct))
            files_to_analyze = random.sample(files_to_analyze, sample_size)
            print(f"🎯 Sampling {sample_size} files ({sample}) from {len(files_to_analyze)} total")
        
        # Apply incremental filtering if specified
        if incremental:
            existing_cards = set()
            if os.path.exists(output_dir):
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        if file.endswith('.md'):
                            existing_cards.add(file)
            
            original_count = len(files_to_analyze)
            files_to_analyze = [f for f in files_to_analyze if not self._has_existing_card(f, existing_cards)]
            skipped = original_count - len(files_to_analyze)
            if skipped > 0:
                print(f"⏭️ Skipping {skipped} already analyzed files (incremental mode)")
        
        print(f"📁 Found {len(files_to_analyze)} files to analyze...")
        
        # Initialize tracking
        results = []
        total_tokens = 0
        total_cost = 0.0
        start_time = time.time()
        
        for i, file_path in enumerate(files_to_analyze, 1):
            # Check budget before processing
            if budget and total_tokens >= budget:
                print(f"💰 Budget limit reached ({budget} tokens). Stopping analysis.")
                break
                
            # Progress indicator
            progress = (i / len(files_to_analyze)) * 100
            elapsed = time.time() - start_time
            if i > 1:
                avg_time = elapsed / (i - 1)
                remaining_files = len(files_to_analyze) - i + 1
                eta_seconds = avg_time * remaining_files
                eta_str = f" | ETA: {eta_seconds/60:.1f}m" if eta_seconds > 60 else f" | ETA: {eta_seconds:.0f}s"
            else:
                eta_str = ""
            
            print(f"🔄 [{i}/{len(files_to_analyze)}] ({progress:.1f}%){eta_str} - {os.path.basename(file_path)}")
            
            result = await self.analyze_file(file_path, analysis_level, output_dir)
            results.append(result)
            
            # Track tokens and cost if available
            if "tokens_used" in result:
                total_tokens += result["tokens_used"]
                total_cost += result.get("cost", 0.0)
            
            # Print result
            if "error" not in result:
                quality_str = f" | Quality: {result.get('quality_score', 'N/A')}/10" if result.get('quality_score') else ""
                print(f"✅ {os.path.basename(file_path)} - {result.get('language', 'unknown')}{quality_str}")
            else:
                print(f"❌ {os.path.basename(file_path)} - {result['error']}")
        
        # Print final token usage summary
        if total_tokens > 0:
            print(f"\n💰 Token Usage Summary:")
            print(f"📊 Total tokens used: {total_tokens:,}")
            print(f"💵 Estimated cost: ${total_cost:.4f}")
            print(f"📈 Average per file: {total_tokens/len(results):,.0f} tokens")
        
        # Update abilities index
        try:
            update_abilities_index(output_dir)
            print(f"📋 Updated abilities index")
        except Exception as e:
            print(f"⚠️ Failed to update index: {e}")
        
        successful = [r for r in results if "error" not in r]
        failed = [r for r in results if "error" in r]
        
        return {
            "directory": dir_path,
            "analysis_level": analysis_level,
            "total_files": len(files_to_analyze),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
            "output_directory": output_dir
        }


async def analyze_command(args):
    """Enhanced analysis command with AI-powered semantic analysis."""
    target_path = args.target
    analysis_level = args.level
    
    # Create organized output directory structure
    base_output_dir = args.output or "./output/ability_cards"
    
    # Create scan-specific folder
    target_name = os.path.basename(os.path.abspath(target_path))
    if not target_name:  # Handle root directory case
        target_name = "root"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scan_folder = f"{target_name}_{timestamp}"
    output_dir = os.path.join(base_output_dir, scan_folder)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print("[*] Starting enhanced analysis...")
    print(f"[>] Target: {target_path}")
    print(f"[>] Analysis Level: {analysis_level}")
    print(f"[>] Scan Folder: {scan_folder}")
    print(f"[>] Output Directory: {output_dir}")
    print()
    
    analyzer = EnhancedAnalyzer()
    
    try:
        if os.path.isfile(target_path):
            result = await analyzer.analyze_file(target_path, analysis_level, output_dir)
        elif os.path.isdir(target_path):
            result = await analyzer.analyze_directory(
                target_path, analysis_level, output_dir,
                budget=getattr(args, 'budget', None),
                sample=getattr(args, 'sample', None),
                incremental=getattr(args, 'incremental', False)
            )
        else:
            print(f"❌ Path not found: {target_path}")
            return 1
        
        if "error" in result:
            print(f"❌ Analysis failed: {result['error']}")
            return 1
        
        # Print summary
        print("\n" + "="*50)
        print("📊 Analysis Summary")
        print("="*50)
        
        if "total_files" in result:
            # Directory analysis
            print(f"📁 Directory: {result['directory']}")
            print(f"📄 Files analyzed: {result['successful']}/{result['total_files']}")
            print(f"📊 Analysis level: {result['analysis_level']}")
            print(f"📂 Output directory: {result['output_directory']}")
            
            if result['failed'] > 0:
                print(f"⚠️ Failed analyses: {result['failed']}")
        else:
            # Single file analysis
            print(f"📄 File: {result['file_path']}")
            print(f"🔤 Language: {result['language']}")
            print(f"📊 Analysis level: {result['analysis_level']}")
            print(f"📝 Ability card: {result['ability_card']}")
            
            if result.get('ai_enhanced'):
                print("🤖 AI-enhanced analysis completed")
                if result.get('quality_score'):
                    print(f"⭐ Quality score: {result['quality_score']:.1f}/10")
            else:
                print("📋 Basic analysis completed")
                print("💡 Add AI API keys for enhanced semantic analysis")
        
        print("\n✅ Analysis completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced code analysis with AI")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--level", choices=["basic", "enhanced", "premium"], 
                       default="enhanced", help="Analysis level")
    parser.add_argument("--output", default="./output/ability_cards", 
                       help="Output directory for ability cards")
    
    args = parser.parse_args()
    
    # Create args object for analyze_command
    analyze_args = type('Args', (), {
        'target': args.path,
        'level': args.level,
        'output': args.output,
        'budget': None,
        'sample': None,
        'incremental': False
    })()
    
    exit_code = asyncio.run(analyze_command(analyze_args))
    sys.exit(exit_code)
