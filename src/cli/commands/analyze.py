"""
Enhanced analysis command with AI-powered semantic understanding.
"""

import os
import sys
import json
import asyncio
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from analyzers.typescript.semantic_analyzer import analyze_typescript_file_enhanced
from core.dependency_visualizer import analyze_python_dependencies, analyze_typescript_dependencies
from utils.index_updater import update_abilities_index


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
                from analyzers.typescript.semantic_analyzer import EnhancedTypeScriptAnalyzer
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
                # Use basic Python analyzer for now
                analysis = analyze_python_dependencies(file_path)
                
                # Generate basic ability card
                card_content = self._generate_basic_ability_card(file_path, analysis, language)
                
                # Save ability card
                os.makedirs(output_dir, exist_ok=True)
                file_name = os.path.basename(file_path)
                card_name = f"AbilityCard_{file_name.replace('.', '_')}.md"
                card_path = os.path.join(output_dir, card_name)
                
                with open(card_path, 'w', encoding='utf-8') as f:
                    f.write(card_content)
                
                return {
                    "file_path": file_path,
                    "language": language,
                    "analysis_level": "basic",
                    "ability_card": card_path,
                    "imports": len(analysis.get("imports", [])),
                    "ai_enhanced": False
                }
            
            else:
                return {"error": f"Unsupported language: {language}"}
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
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
                               output_dir: str = "./output/ability_cards") -> Dict[str, Any]:
        """Analyze all supported files in a directory."""
        if not os.path.exists(dir_path):
            return {"error": f"Directory not found: {dir_path}"}
        
        supported_extensions = set(self.get_supported_extensions().keys())
        files_to_analyze = []
        
        # Find all supported files
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    files_to_analyze.append(os.path.join(root, file))
        
        if not files_to_analyze:
            return {"error": "No supported files found in directory"}
        
        print(f"📁 Found {len(files_to_analyze)} files to analyze...")
        
        results = []
        for file_path in files_to_analyze:
            result = await self.analyze_file(file_path, analysis_level, output_dir)
            results.append(result)
            
            # Print progress
            if "error" not in result:
                print(f"✅ {os.path.basename(file_path)} - {result.get('language', 'unknown')}")
            else:
                print(f"❌ {os.path.basename(file_path)} - {result['error']}")
        
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


async def analyze_command(path: str, analysis_level: str = "enhanced", 
                         output_dir: str = "./output/ability_cards") -> int:
    """Main analyze command function."""
    print(f"🚀 Starting enhanced analysis...")
    print(f"📂 Target: {path}")
    print(f"📊 Analysis Level: {analysis_level}")
    print(f"📁 Output Directory: {output_dir}")
    print()
    
    analyzer = EnhancedAnalyzer()
    
    try:
        if os.path.isfile(path):
            result = await analyzer.analyze_file(path, analysis_level, output_dir)
        elif os.path.isdir(path):
            result = await analyzer.analyze_directory(path, analysis_level, output_dir)
        else:
            print(f"❌ Path not found: {path}")
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
    
    exit_code = asyncio.run(analyze_command(args.path, args.level, args.output))
    sys.exit(exit_code)
