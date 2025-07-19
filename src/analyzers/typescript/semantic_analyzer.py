"""
Enhanced TypeScript analyzer with AI-powered semantic understanding.

This module extends the basic TypeScript AST parsing with AI-powered analysis
to understand business context, architectural patterns, and code quality.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Import our AI services
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.ai_services import AIServiceManager, SemanticAnalysis, PatternAnalysis, QualityAssessment


@dataclass
class EnhancedTypeScriptAnalysis:
    """Enhanced TypeScript analysis results with AI-powered insights."""
    # Basic AST analysis (from existing analyzer)
    file_path: str
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    imports: List[str]
    
    # AI-powered semantic analysis
    semantic_analysis: Optional[SemanticAnalysis] = None
    pattern_analysis: Optional[PatternAnalysis] = None
    quality_assessment: Optional[QualityAssessment] = None
    ai_summary: Optional[str] = None
    
    # Enhanced metadata
    framework_detection: Dict[str, Any] = None
    architectural_insights: Dict[str, Any] = None
    business_context: Dict[str, Any] = None


class EnhancedTypeScriptAnalyzer:
    """Enhanced TypeScript analyzer with AI-powered semantic understanding."""
    
    def __init__(self, ai_config: Dict[str, Any]):
        self.ai_manager = AIServiceManager(ai_config.get("ai_services", {}))
        self.analysis_settings = ai_config.get("analysis_settings", {})
        self.enabled_features = set()
        
    def set_analysis_level(self, level: str, ai_config: Dict[str, Any]):
        """Set the analysis level (basic, enhanced, premium)."""
        levels = ai_config.get("analysis_levels", {})
        if level in levels:
            level_config = levels[level]
            self.enabled_features = set(level_config.get("enabled_features", []))
            self.ai_features = set(level_config.get("ai_features", []))
    
    async def analyze_file(self, file_path: str, analysis_level: str = "enhanced") -> EnhancedTypeScriptAnalysis:
        """Perform enhanced analysis of a TypeScript file."""
        # Load AI configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', 'ai_config.json')
        with open(config_path, 'r') as f:
            ai_config = json.load(f)
        
        self.set_analysis_level(analysis_level, ai_config)
        
        # Step 1: Basic AST analysis (existing functionality)
        basic_analysis = await self._run_basic_analysis(file_path)
        
        # Step 2: Read the source code for AI analysis
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            return EnhancedTypeScriptAnalysis(
                file_path=file_path,
                functions=[],
                classes=[],
                imports=[],
                ai_summary=f"Error reading file: {str(e)}"
            )
        
        # Step 3: AI-powered analysis (if enabled)
        semantic_analysis = None
        pattern_analysis = None
        quality_assessment = None
        ai_summary = None
        
        try:
            if "semantic" in self.ai_features:
                semantic_analysis = await self.ai_manager.analyze_with_ai(
                    source_code, file_path, "typescript", "semantic"
                )
            
            if "patterns" in self.ai_features:
                pattern_analysis = await self.ai_manager.analyze_with_ai(
                    source_code, file_path, "typescript", "patterns"
                )
            
            if "quality" in self.ai_features:
                quality_assessment = await self.ai_manager.analyze_with_ai(
                    source_code, file_path, "typescript", "quality"
                )
            
            if "summary" in self.ai_features:
                ai_summary = await self.ai_manager.analyze_with_ai(
                    source_code, file_path, "typescript", "summary"
                )
        
        except Exception as e:
            ai_summary = f"AI analysis failed: {str(e)}"
        
        # Step 4: Enhanced metadata extraction
        framework_detection = self._detect_frameworks(basic_analysis, source_code)
        architectural_insights = self._extract_architectural_insights(basic_analysis, semantic_analysis)
        business_context = self._extract_business_context(semantic_analysis, pattern_analysis)
        
        return EnhancedTypeScriptAnalysis(
            file_path=file_path,
            functions=basic_analysis.get("functions", []),
            classes=basic_analysis.get("classes", []),
            imports=basic_analysis.get("imports", []),
            semantic_analysis=semantic_analysis,
            pattern_analysis=pattern_analysis,
            quality_assessment=quality_assessment,
            ai_summary=ai_summary,
            framework_detection=framework_detection,
            architectural_insights=architectural_insights,
            business_context=business_context
        )
    
    async def _run_basic_analysis(self, file_path: str) -> Dict[str, Any]:
        """Run the basic TypeScript AST analysis."""
        import subprocess
        
        # Use the existing TypeScript analyzer
        script_path = os.path.join(os.path.dirname(__file__), 'ts_analyzer_cli.js')
        
        try:
            process = subprocess.run(
                ['node', script_path, file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(process.stdout)
        except Exception as e:
            return {
                "file_path": file_path,
                "functions": [],
                "classes": [],
                "imports": [],
                "error": str(e)
            }
    
    def _detect_frameworks(self, basic_analysis: Dict[str, Any], source_code: str) -> Dict[str, Any]:
        """Detect frameworks and libraries used."""
        frameworks = {
            "react": False,
            "vue": False,
            "angular": False,
            "express": False,
            "nestjs": False,
            "next": False,
            "nuxt": False,
            "cli_framework": False,
            "testing_framework": False
        }
        
        imports = basic_analysis.get("imports", [])
        
        # React detection
        react_indicators = ["react", "react-dom", "jsx", "tsx", "useState", "useEffect"]
        if any(indicator in str(imports).lower() or indicator in source_code.lower() 
               for indicator in react_indicators):
            frameworks["react"] = True
        
        # CLI framework detection
        cli_indicators = ["commander", "yargs", "inquirer", "chalk", "ora", "cli"]
        if any(indicator in str(imports).lower() for indicator in cli_indicators):
            frameworks["cli_framework"] = True
        
        # Express detection
        if "express" in str(imports).lower():
            frameworks["express"] = True
        
        # Testing framework detection
        testing_indicators = ["jest", "mocha", "chai", "vitest", "cypress", "playwright"]
        if any(indicator in str(imports).lower() for indicator in testing_indicators):
            frameworks["testing_framework"] = True
        
        return frameworks
    
    def _extract_architectural_insights(self, basic_analysis: Dict[str, Any], 
                                      semantic_analysis: Optional[SemanticAnalysis]) -> Dict[str, Any]:
        """Extract architectural insights from analysis results."""
        insights = {
            "separation_of_concerns": "unknown",
            "modularity": "unknown",
            "complexity": "unknown",
            "architectural_pattern": "unknown"
        }
        
        if semantic_analysis:
            insights["architectural_pattern"] = semantic_analysis.architectural_pattern
            
            # Assess modularity based on function/class count and structure
            function_count = len(basic_analysis.get("functions", []))
            class_count = len(basic_analysis.get("classes", []))
            
            if function_count + class_count > 20:
                insights["complexity"] = "high"
            elif function_count + class_count > 10:
                insights["complexity"] = "medium"
            else:
                insights["complexity"] = "low"
            
            # Basic modularity assessment
            if class_count > 0 and function_count > 0:
                insights["modularity"] = "good"
            elif class_count > 0 or function_count > 5:
                insights["modularity"] = "moderate"
            else:
                insights["modularity"] = "basic"
        
        return insights
    
    def _extract_business_context(self, semantic_analysis: Optional[SemanticAnalysis],
                                pattern_analysis: Optional[PatternAnalysis]) -> Dict[str, Any]:
        """Extract business context from AI analysis."""
        context = {
            "domain": "unknown",
            "purpose": "unknown",
            "user_interaction": "unknown",
            "safety_level": "unknown"
        }
        
        if semantic_analysis:
            context["domain"] = semantic_analysis.domain_type
            context["purpose"] = semantic_analysis.business_context
        
        if pattern_analysis:
            # Assess safety level based on safety patterns
            safety_patterns = pattern_analysis.safety_patterns
            if len(safety_patterns) >= 3:
                context["safety_level"] = "high"
            elif len(safety_patterns) >= 1:
                context["safety_level"] = "moderate"
            else:
                context["safety_level"] = "basic"
            
            # Determine user interaction type
            react_patterns = pattern_analysis.react_patterns
            if any("ui" in pattern.lower() or "component" in pattern.lower() 
                   for pattern in react_patterns):
                context["user_interaction"] = "gui"
            elif "cli" in str(pattern_analysis.architectural_patterns).lower():
                context["user_interaction"] = "cli"
            else:
                context["user_interaction"] = "api"
        
        return context
    
    def to_enhanced_ability_card(self, analysis: EnhancedTypeScriptAnalysis) -> str:
        """Generate an enhanced ability card with AI insights."""
        # Extract key information
        file_name = os.path.basename(analysis.file_path)
        ability_name = file_name.replace('.ts', '').replace('.js', '').replace('_', ' ').title()
        
        # Get AI-generated summary or create basic one
        if analysis.ai_summary:
            description = analysis.ai_summary
        else:
            description = f"TypeScript module with {len(analysis.functions)} functions and {len(analysis.classes)} classes."
        
        # Quality information
        quality_info = ""
        if analysis.quality_assessment:
            qa = analysis.quality_assessment
            quality_info = f"""
## Quality Assessment

- **Overall Score:** {qa.overall_score:.1f}/10
- **Code Quality:** {qa.code_quality:.1f}/10
- **Design Quality:** {qa.design_quality:.1f}/10
- **Maintainability:** {qa.maintainability:.1f}/10
- **Reusability:** {qa.reusability:.1f}/10

### Strengths
{chr(10).join(f"- {strength}" for strength in qa.strengths)}

### Recommendations
{chr(10).join(f"- {rec}" for rec in qa.recommendations)}
"""
        
        # Pattern information
        pattern_info = ""
        if analysis.pattern_analysis:
            pa = analysis.pattern_analysis
            pattern_info = f"""
## Patterns Detected

### Architectural Patterns
{chr(10).join(f"- {pattern}" for pattern in pa.architectural_patterns)}

### Design Patterns
{chr(10).join(f"- {pattern}" for pattern in pa.design_patterns)}

### React Patterns
{chr(10).join(f"- {pattern}" for pattern in pa.react_patterns)}

### Safety Patterns
{chr(10).join(f"- {pattern}" for pattern in pa.safety_patterns)}
"""
        
        # Business context
        context_info = ""
        if analysis.business_context:
            bc = analysis.business_context
            context_info = f"""
## Business Context

- **Domain:** {bc.get('domain', 'Unknown')}
- **Purpose:** {bc.get('purpose', 'Unknown')}
- **User Interaction:** {bc.get('user_interaction', 'Unknown')}
- **Safety Level:** {bc.get('safety_level', 'Unknown')}
"""
        
        # Framework detection
        framework_info = ""
        if analysis.framework_detection:
            detected_frameworks = [name for name, detected in analysis.framework_detection.items() if detected]
            if detected_frameworks:
                framework_info = f"""
## Frameworks & Libraries

{chr(10).join(f"- {framework.replace('_', ' ').title()}" for framework in detected_frameworks)}
"""
        
        return f"""# Enhanced Ability Card: {ability_name}

**File:** [`{os.path.basename(analysis.file_path)}`](file:///{analysis.file_path})  
**Full Path:** `{analysis.file_path}`  
**Language:** TypeScript/JavaScript  
**Analysis Level:** Enhanced with AI

## Description

{description}

## Technical Details

- **Functions:** {len(analysis.functions)}
- **Classes:** {len(analysis.classes)}
- **Imports:** {len(analysis.imports)}
- **Complexity:** {analysis.architectural_insights.get('complexity', 'Unknown') if analysis.architectural_insights else 'Unknown'}

{framework_info}

{context_info}

{pattern_info}

{quality_info}

## Functions

{chr(10).join(f"- **{func.get('name', 'Unknown')}**({', '.join(func.get('args', []))}): {func.get('docstring', 'No description')}" for func in analysis.functions)}

## Classes

{chr(10).join(f"- **{cls.get('name', 'Unknown')}**: {cls.get('docstring', 'No description')}" for cls in analysis.classes)}

---
*Generated by AIPass-Code-Sniffer Enhanced Analyzer*
"""


# Convenience function for easy usage
async def analyze_typescript_file_enhanced(file_path: str, analysis_level: str = "enhanced") -> EnhancedTypeScriptAnalysis:
    """Analyze a TypeScript file with enhanced AI-powered analysis."""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', 'ai_config.json')
    
    try:
        with open(config_path, 'r') as f:
            ai_config = json.load(f)
    except FileNotFoundError:
        # Fallback configuration if file doesn't exist
        ai_config = {
            "ai_services": {},
            "analysis_levels": {
                "enhanced": {
                    "enabled_features": ["syntax", "dependencies"],
                    "ai_features": []
                }
            }
        }
    
    analyzer = EnhancedTypeScriptAnalyzer(ai_config)
    return await analyzer.analyze_file(file_path, analysis_level)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python semantic_analyzer.py <typescript_file> [analysis_level]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analysis_level = sys.argv[2] if len(sys.argv) > 2 else "enhanced"
    
    async def main():
        analysis = await analyze_typescript_file_enhanced(file_path, analysis_level)
        
        # Print results
        print("=== Enhanced TypeScript Analysis ===")
        print(f"File: {analysis.file_path}")
        print(f"Functions: {len(analysis.functions)}")
        print(f"Classes: {len(analysis.classes)}")
        print(f"Imports: {len(analysis.imports)}")
        
        if analysis.semantic_analysis:
            print(f"\nBusiness Context: {analysis.semantic_analysis.business_context}")
            print(f"Architectural Pattern: {analysis.semantic_analysis.architectural_pattern}")
            print(f"Quality Score: {analysis.semantic_analysis.quality_score}/10")
        
        if analysis.ai_summary:
            print(f"\nAI Summary:\n{analysis.ai_summary}")
        
        # Generate enhanced ability card
        analyzer = EnhancedTypeScriptAnalyzer({})
        ability_card = analyzer.to_enhanced_ability_card(analysis)
        
        # Save ability card
        output_file = f"Enhanced_AbilityCard_{os.path.basename(file_path).replace('.ts', '').replace('.js', '')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ability_card)
        
        print(f"\nEnhanced ability card saved to: {output_file}")
    
    asyncio.run(main())
