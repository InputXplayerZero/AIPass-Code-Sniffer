"""
Advanced Skill Detection Engine for AIPass-Code-Sniffer

Comprehensive skill detection and classification for atomic, reusable code modules.
"""

import ast
import re
import os
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

class SkillCategory(Enum):
    """Comprehensive skill categories."""
    FILE_OPERATIONS = "file_operations"
    CLI_COMMANDS = "cli_commands"
    API_INTEGRATION = "api_integration"
    DATA_PROCESSING = "data_processing"
    AI_TOOLS = "ai_tools"
    WEB_FRAMEWORK = "web_framework"
    DATABASE = "database"
    NETWORKING = "networking"
    ASYNC_OPERATIONS = "async_operations"
    ERROR_HANDLING = "error_handling"
    UTILITY_FUNCTIONS = "utility_functions"
    CONFIGURATION = "configuration"

@dataclass
class SkillSignature:
    """Detected skill with comprehensive metadata."""
    name: str
    category: SkillCategory
    confidence: float
    description: str
    file_path: str
    line_start: int
    line_end: int
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    complexity: str = "medium"
    reusability: float = 0.5
    async_function: bool = False
    extraction_priority: float = 0.5

@dataclass
class SkillModule:
    """Complete skill module with related functions."""
    name: str
    primary_category: SkillCategory
    skills: List[SkillSignature]
    file_path: str
    extraction_priority: float = 0.5

class AdvancedSkillDetector:
    """Advanced skill detection engine."""
    
    def __init__(self):
        self.patterns = self._init_patterns()
    
    def _init_patterns(self) -> Dict[SkillCategory, Dict[str, Any]]:
        """Initialize detection patterns."""
        return {
            SkillCategory.FILE_OPERATIONS: {
                "keywords": ["read", "write", "file", "path", "save", "load"],
                "imports": ["os", "pathlib", "shutil"],
                "confidence": 0.8
            },
            SkillCategory.CLI_COMMANDS: {
                "keywords": ["command", "cli", "arg", "parse", "subprocess"],
                "imports": ["argparse", "click", "subprocess"],
                "confidence": 0.9
            },
            SkillCategory.API_INTEGRATION: {
                "keywords": ["api", "request", "http", "client", "endpoint"],
                "imports": ["requests", "aiohttp", "fastapi"],
                "confidence": 0.85
            },
            SkillCategory.AI_TOOLS: {
                "keywords": ["openai", "anthropic", "ai", "llm", "gpt"],
                "imports": ["openai", "anthropic"],
                "confidence": 0.95
            },
            SkillCategory.DATA_PROCESSING: {
                "keywords": ["process", "transform", "parse", "filter"],
                "imports": ["pandas", "numpy", "json"],
                "confidence": 0.75
            }
        }
    
    def detect_skills_in_file(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect skills in a file."""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.py':
            return self._detect_python_skills(content, file_path)
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            return self._detect_js_skills(content, file_path)
        return []
    
    def _detect_python_skills(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect Python skills using AST."""
        skills = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    skill = self._analyze_function(node, content, file_path)
                    if skill:
                        skills.append(skill)
        
        except SyntaxError:
            # Fallback to regex
            skills.extend(self._regex_detection(content, file_path))
        
        return skills
    
    def _analyze_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], 
                         content: str, file_path: str) -> Optional[SkillSignature]:
        """Analyze Python function for skills."""
        func_name = node.name
        
        # Skip private functions
        if func_name.startswith('_') and not func_name.startswith('__'):
            return None
        
        # Get function source
        try:
            func_source = ast.get_source_segment(content, node) or ""
        except:
            func_source = ""
        
        # Classify function
        category, confidence = self._classify_function(func_name, func_source)
        
        if confidence > 0.5:
            return SkillSignature(
                name=func_name,
                category=category,
                confidence=confidence,
                description=self._generate_description(func_name, category),
                file_path=file_path,
                line_start=node.lineno,
                line_end=getattr(node, 'end_lineno', node.lineno),
                parameters=self._extract_parameters(node),
                dependencies=self._extract_dependencies(func_source),
                complexity=self._assess_complexity(func_source),
                async_function=isinstance(node, ast.AsyncFunctionDef),
                extraction_priority=confidence * 0.8
            )
        
        return None
    
    def _classify_function(self, func_name: str, func_source: str) -> Tuple[SkillCategory, float]:
        """Classify function into skill category."""
        best_category = SkillCategory.UTILITY_FUNCTIONS
        best_confidence = 0.3
        
        for category, patterns in self.patterns.items():
            score = 0.0
            
            # Check keywords in name
            name_matches = sum(1 for kw in patterns["keywords"] 
                             if kw.lower() in func_name.lower())
            score += (name_matches / len(patterns["keywords"])) * 0.4
            
            # Check keywords in source
            source_matches = sum(1 for kw in patterns["keywords"] 
                               if kw.lower() in func_source.lower())
            score += (source_matches / len(patterns["keywords"])) * 0.3
            
            # Check imports
            import_matches = sum(1 for imp in patterns["imports"] 
                               if imp in func_source)
            score += (import_matches / len(patterns["imports"])) * 0.3
            
            final_score = score * patterns["confidence"]
            
            if final_score > best_confidence:
                best_category = category
                best_confidence = final_score
        
        return best_category, min(best_confidence, 1.0)
    
    def _extract_parameters(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[Dict[str, Any]]:
        """Extract function parameters."""
        params = []
        for arg in node.args.args:
            params.append({
                "name": arg.arg,
                "type": self._get_type_hint(arg.annotation) if arg.annotation else None
            })
        return params
    
    def _get_type_hint(self, annotation: ast.expr) -> str:
        """Extract type hint as string."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return f"{annotation.value.id}.{annotation.attr}"
        return "Any"
    
    def _extract_dependencies(self, func_source: str) -> List[str]:
        """Extract function dependencies."""
        deps = []
        
        # Simple import detection
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, func_source)
            deps.extend(matches)
        
        return list(set(deps))
    
    def _assess_complexity(self, func_source: str) -> str:
        """Assess function complexity."""
        complexity_indicators = func_source.count('if') + func_source.count('for') + func_source.count('while')
        
        if complexity_indicators >= 3:
            return "high"
        elif complexity_indicators >= 1:
            return "medium"
        else:
            return "low"
    
    def _generate_description(self, func_name: str, category: SkillCategory) -> str:
        """Generate skill description."""
        templates = {
            SkillCategory.FILE_OPERATIONS: f"File operation: {func_name}",
            SkillCategory.CLI_COMMANDS: f"CLI command: {func_name}",
            SkillCategory.API_INTEGRATION: f"API integration: {func_name}",
            SkillCategory.AI_TOOLS: f"AI tool: {func_name}",
            SkillCategory.DATA_PROCESSING: f"Data processor: {func_name}",
            SkillCategory.UTILITY_FUNCTIONS: f"Utility: {func_name}"
        }
        return templates.get(category, f"Function: {func_name}")
    
    def _detect_js_skills(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect JavaScript/TypeScript skills."""
        skills = []
        
        # Function patterns
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*\(',
            r'(\w+)\s*:\s*function'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                # Simple classification
                category, confidence = self._classify_js_function(func_name, content)
                
                if confidence > 0.5:
                    skills.append(SkillSignature(
                        name=func_name,
                        category=category,
                        confidence=confidence,
                        description=self._generate_description(func_name, category),
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,
                        extraction_priority=confidence * 0.7
                    ))
        
        return skills
    
    def _classify_js_function(self, func_name: str, content: str) -> Tuple[SkillCategory, float]:
        """Classify JavaScript function."""
        # Simple keyword-based classification
        if any(kw in func_name.lower() for kw in ['api', 'fetch', 'request']):
            return SkillCategory.API_INTEGRATION, 0.8
        elif any(kw in func_name.lower() for kw in ['file', 'read', 'write']):
            return SkillCategory.FILE_OPERATIONS, 0.7
        elif any(kw in content for kw in ['React', 'component', 'jsx']):
            return SkillCategory.WEB_FRAMEWORK, 0.8
        else:
            return SkillCategory.UTILITY_FUNCTIONS, 0.4
    
    def _regex_detection(self, content: str, file_path: str) -> List[SkillSignature]:
        """Fallback regex-based detection."""
        skills = []
        
        # Simple function detection
        for match in re.finditer(r'def\s+(\w+)\s*\(', content):
            func_name = match.group(1)
            if not func_name.startswith('_'):
                line_num = content[:match.start()].count('\n') + 1
                skills.append(SkillSignature(
                    name=func_name,
                    category=SkillCategory.UTILITY_FUNCTIONS,
                    confidence=0.4,
                    description=f"Function: {func_name}",
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num
                ))
        
        return skills
    
    def create_skill_module(self, skills: List[SkillSignature], file_path: str) -> SkillModule:
        """Create skill module from multiple skills."""
        if not skills:
            return None
        
        # Determine primary category
        categories = [skill.category for skill in skills]
        primary_category = max(set(categories), key=categories.count)
        
        # Calculate module priority
        avg_priority = sum(skill.extraction_priority for skill in skills) / len(skills)
        
        module_name = Path(file_path).stem
        
        return SkillModule(
            name=module_name,
            primary_category=primary_category,
            skills=skills,
            file_path=file_path,
            extraction_priority=avg_priority
        )
