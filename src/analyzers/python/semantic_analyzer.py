"""
Enhanced Python analyzer with AI-powered semantic understanding.

This module provides AI-powered analysis of Python code to understand
business context, architectural patterns, and code quality.
"""

import os
import ast
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

# Import our AI services
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.ai_services import AIServiceManager, SemanticAnalysis, PatternAnalysis, QualityAssessment


@dataclass
class EnhancedPythonAnalysis:
    """Enhanced Python analysis results with AI-powered insights."""
    # Basic AST analysis
    file_path: str
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    imports: List[str]
    
    # AI-powered semantic analysis
    semantic_analysis: Optional[SemanticAnalysis] = None
    pattern_analysis: Optional[PatternAnalysis] = None
    quality_assessment: Optional[QualityAssessment] = None
    ai_summary: Optional[str] = None
    
    # Metadata
    analysis_level: str = "basic"
    frameworks_detected: List[str] = field(default_factory=list)
    complexity: str = "unknown"


class EnhancedPythonAnalyzer:
    """AI-enhanced Python code analyzer."""
    
    def __init__(self):
        # Load AI configuration with proper API key handling
        config_path = os.path.join(
            os.path.dirname(__file__), '..', '..', '..', 'config', 'ai_config.json'
        )
        
        # Create working config with environment variables
        config = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "models": {
                    "summarization": "gpt-4o-mini",
                    "analysis": "gpt-4"
                },
                "enabled": True
            }
        }
        
        # Try to load additional config from file
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                # Merge file config but keep our environment-based API key
                if "openai" in file_config:
                    config["openai"].update(file_config["openai"])
                    # Ensure we use environment API key
                    config["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
        except Exception as e:
            print(f"⚠️  Could not load config file: {e}")
        
        print(f"🔧 Initializing AI services with config: {bool(config.get('openai', {}).get('api_key'))}")
        self.ai_manager = AIServiceManager(config)
    
    def parse_python_ast(self, file_path: str) -> Dict[str, Any]:
        """Parse Python file using AST to extract basic information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extract function information
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node),
                        'line_number': node.lineno
                    }
                    functions.append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    # Extract class information
                    class_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'methods': [],
                        'line_number': node.lineno
                    }
                    
                    # Get class methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append({
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args],
                                'docstring': ast.get_docstring(item)
                            })
                    
                    classes.append(class_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Extract import information
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}" if module else alias.name)
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'content': content
            }
            
        except Exception as e:
            return {
                'error': f"Failed to parse Python file: {str(e)}",
                'functions': [],
                'classes': [],
                'imports': [],
                'content': ''
            }
    
    def detect_frameworks(self, imports: List[str], content: str) -> List[str]:
        """Detect Python frameworks and libraries."""
        frameworks = []
        
        # Web frameworks
        web_frameworks = {
            'flask': 'Flask',
            'django': 'Django',
            'fastapi': 'FastAPI',
            'tornado': 'Tornado',
            'bottle': 'Bottle'
        }
        
        # Data science
        data_frameworks = {
            'pandas': 'Pandas',
            'numpy': 'NumPy',
            'scipy': 'SciPy',
            'sklearn': 'Scikit-learn',
            'tensorflow': 'TensorFlow',
            'torch': 'PyTorch'
        }
        
        # Testing
        test_frameworks = {
            'pytest': 'Pytest',
            'unittest': 'Unittest',
            'nose': 'Nose'
        }
        
        # CLI
        cli_frameworks = {
            'click': 'Click',
            'argparse': 'Argparse',
            'fire': 'Fire'
        }
        
        # AI/ML
        ai_frameworks = {
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'transformers': 'Transformers',
            'langchain': 'LangChain'
        }
        
        all_frameworks = {**web_frameworks, **data_frameworks, **test_frameworks, **cli_frameworks, **ai_frameworks}
        
        for import_name in imports:
            for key, framework in all_frameworks.items():
                if key in import_name.lower():
                    if framework not in frameworks:
                        frameworks.append(framework)
        
        return frameworks
    
    def calculate_complexity(self, functions: List[Dict], classes: List[Dict]) -> str:
        """Calculate code complexity based on structure."""
        total_items = len(functions) + len(classes)
        
        if total_items == 0:
            return "minimal"
        elif total_items <= 5:
            return "low"
        elif total_items <= 15:
            return "medium"
        else:
            return "high"
    
    async def analyze_file(self, file_path: str, analysis_level: str = "enhanced") -> EnhancedPythonAnalysis:
        """Analyze a Python file with optional AI enhancement."""
        
        # Parse basic structure
        ast_data = self.parse_python_ast(file_path)
        
        if 'error' in ast_data:
            return EnhancedPythonAnalysis(
                file_path=file_path,
                functions=[],
                classes=[],
                imports=[],
                analysis_level="error",
                frameworks_detected=[]
            )
        
        # Detect frameworks and complexity
        frameworks = self.detect_frameworks(ast_data['imports'], ast_data['content'])
        complexity = self.calculate_complexity(ast_data['functions'], ast_data['classes'])
        
        # Create basic analysis
        analysis = EnhancedPythonAnalysis(
            file_path=file_path,
            functions=ast_data['functions'],
            classes=ast_data['classes'],
            imports=ast_data['imports'],
            analysis_level=analysis_level,
            frameworks_detected=frameworks or [],
            complexity=complexity
        )
        
        # Add AI enhancement if requested
        if analysis_level in ["enhanced", "premium"]:
            print(f"🤖 Attempting AI analysis for {analysis_level} level...")
            print(f"🔑 AI services available: {self.ai_manager.has_services()}")
            
            if self.ai_manager.has_services():
                try:
                    print("🔄 Generating AI summary...")
                    # Generate AI summary
                    analysis.ai_summary = await self.ai_manager.generate_summary(
                        code_content=ast_data['content'],
                        language="python",
                        file_path=file_path
                    )
                    print("✅ AI summary generated successfully")
                    
                    if analysis_level == "premium":
                        print("🔄 Running full AI analysis...")
                        # Full AI analysis
                        analysis.semantic_analysis = await self.ai_manager.analyze_semantics(
                            code_content=ast_data['content'],
                            language="python"
                        )
                        
                        analysis.pattern_analysis = await self.ai_manager.detect_patterns(
                            code_content=ast_data['content'],
                            language="python"
                        )
                        
                        analysis.quality_assessment = await self.ai_manager.assess_quality(
                            code_content=ast_data['content'],
                            language="python"
                        )
                        print("✅ Full AI analysis completed")
                        
                except Exception as e:
                    print(f"⚠️  AI analysis failed: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Continue with basic analysis
            else:
                print("❌ No AI services available - check API keys")
        
        return analysis
    
    def generate_ability_card(self, analysis: EnhancedPythonAnalysis, output_dir: str) -> str:
        """Generate an enhanced ability card for Python analysis."""
        
        file_name = os.path.basename(analysis.file_path)
        safe_name = file_name.replace('.', '_').replace('/', '_').replace('\\', '_')
        
        # Choose card type based on analysis level
        if analysis.analysis_level in ["enhanced", "premium"] and analysis.ai_summary:
            card_name = f"Enhanced_AbilityCard_{safe_name}.md"
        else:
            card_name = f"AbilityCard_{safe_name}.md"
        
        card_path = os.path.join(output_dir, card_name)
        
        # Generate card content
        content = self._generate_card_content(analysis)
        
        # Write card
        os.makedirs(output_dir, exist_ok=True)
        with open(card_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return card_path
    
    def _generate_card_content(self, analysis: EnhancedPythonAnalysis) -> str:
        """Generate the markdown content for the ability card."""
        
        file_name = os.path.basename(analysis.file_path).replace('_', ' ').replace('.py', '').title()
        
        # Start with header
        content = f"# {'Enhanced ' if analysis.ai_summary else ''}Ability Card: {file_name}\n\n"
        content += f"**File:** `{analysis.file_path}`  \n"
        content += f"**Full Path:** `{os.path.abspath(analysis.file_path)}`  \n"
        content += f"**Language:** Python  \n"
        content += f"**Analysis Level:** {'Enhanced with AI' if analysis.ai_summary else 'Basic'}\n\n"
        
        # Description section
        content += "## Description\n\n"
        if analysis.ai_summary:
            content += f"{analysis.ai_summary}\n\n"
        else:
            content += f"Python module with {len(analysis.imports)} imports detected.\n\n"
        
        # Technical details
        content += "## Technical Details\n\n"
        content += f"- **Functions:** {len(analysis.functions)}\n"
        content += f"- **Classes:** {len(analysis.classes)}\n"
        content += f"- **Imports:** {len(analysis.imports)}\n"
        content += f"- **Complexity:** {analysis.complexity}\n\n"
        
        # Frameworks
        if analysis.frameworks_detected:
            content += "\n## Frameworks & Libraries\n\n"
            for framework in analysis.frameworks_detected:
                content += f"- {framework}\n"
            content += "\n"
        
        # Business context (if available)
        if analysis.semantic_analysis:
            content += "\n## Business Context\n\n"
            content += f"- **Domain:** {analysis.semantic_analysis.domain_type}\n"
            content += f"- **Business Context:** {analysis.semantic_analysis.business_context}\n"
            content += f"- **Architectural Pattern:** {analysis.semantic_analysis.architectural_pattern}\n"
            content += f"- **Quality Score:** {analysis.semantic_analysis.quality_score}/10\n\n"
        
        # Patterns (if available)
        if analysis.pattern_analysis:
            content += "\n## Patterns Detected\n\n"
            content += "### Architectural Patterns\n\n"
            for pattern in analysis.pattern_analysis.architectural_patterns:
                content += f"- {pattern}\n"
            content += "\n### Design Patterns\n\n"
            for pattern in analysis.pattern_analysis.design_patterns:
                content += f"- {pattern}\n"
            content += "\n"
        
        # Quality assessment (if available)
        if analysis.quality_assessment:
            content += "\n## Quality Assessment\n\n"
            content += f"- **Overall Score:** {analysis.quality_assessment.overall_score}/10\n"
            content += f"- **Code Quality:** {analysis.quality_assessment.code_quality}/10\n"
            content += f"- **Design Quality:** {analysis.quality_assessment.design_quality}/10\n"
            content += f"- **Maintainability:** {analysis.quality_assessment.maintainability}/10\n"
            content += f"- **Reusability:** {analysis.quality_assessment.reusability}/10\n\n"
            
            content += "### Strengths\n\n"
            for strength in analysis.quality_assessment.strengths:
                content += f"- {strength}\n"
            content += "\n### Recommendations\n\n"
            for rec in analysis.quality_assessment.recommendations:
                content += f"- {rec}\n"
            content += "\n"
        
        # Functions
        if analysis.functions:
            content += "\n## Functions\n\n"
            for func in analysis.functions:
                args_str = ", ".join(func['args']) if func['args'] else ""
                content += f"- **{func['name']}**({args_str}): "
                if func['docstring']:
                    content += func['docstring'].split('\n')[0]  # First line of docstring
                else:
                    content += "No description available"
                content += "\n"
            content += "\n"
        
        # Classes
        if analysis.classes:
            content += "\n## Classes\n\n"
            for cls in analysis.classes:
                content += f"### {cls['name']}\n\n"
                if cls['docstring']:
                    content += f"{cls['docstring']}\n\n"
                
                if cls['methods']:
                    content += "**Methods:**\n"
                    for method in cls['methods']:
                        args_str = ", ".join(method['args']) if method['args'] else ""
                        content += f"- `{method['name']}({args_str})`"
                        if method['docstring']:
                            content += f": {method['docstring'].split('.')[0]}"
                        content += "\n"
                content += "\n"
        
        # Footer
        content += "---\n"
        content += f"*Generated by AIPass-Code-Sniffer {'Enhanced' if analysis.ai_summary else 'Basic'} Analyzer*\n"
        if not analysis.ai_summary:
            content += "*Upgrade to enhanced/premium analysis for AI-powered insights*\n"
        
        return content


# Convenience function for direct usage
async def analyze_python_file(file_path: str, analysis_level: str = "enhanced", output_dir: str = "./output") -> Dict[str, Any]:
    """Analyze a Python file and generate ability card."""
    analyzer = EnhancedPythonAnalyzer()
    analysis = await analyzer.analyze_file(file_path, analysis_level)
    card_path = analyzer.generate_ability_card(analysis, output_dir)
    
    return {
        'analysis': asdict(analysis),
        'card_path': card_path,
        'success': True
    }
