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
    """Target skill categories aligned with PROJECT_PLAN.md."""
    # Core Performance Modules
    CLI_OPERATIONS = "cli_operations"  # Argument parsing, command execution, terminal I/O
    FILE_OPERATIONS = "file_operations"  # Read, write, delete, copy, move, watch
    CODE_PROCESSING = "code_processing"  # AST parsing, syntax transformation, generation
    INDEXING_SYSTEMS = "indexing_systems"  # Search, categorization, metadata extraction
    MEMORY_SYSTEMS = "memory_systems"  # Caching, persistence, state management
    
    # Advanced Capabilities
    NATURAL_LANGUAGE = "natural_language"  # Text processing, embeddings, semantic search
    PROMPT_ENGINEERING = "prompt_engineering"  # Template systems, context management
    MCP_INTEGRATION = "mcp_integration"  # Model Context Protocol implementations
    API_FRAMEWORKS = "api_frameworks"  # HTTP clients, authentication, rate limiting
    
    # Legacy/Utility Categories
    UTILITY_FUNCTIONS = "utility_functions"
    ERROR_HANDLING = "error_handling"
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
        patterns = {
            # Core Performance Modules
            SkillCategory.CLI_OPERATIONS: {
                "keywords": ["command", "cli", "args", "argv", "commander", "yargs", "option", "flag", "subcommand", "parse", "terminal", "console", "stdin", "stdout", "stderr", "process"],
                "imports": ["argparse", "click", "commander", "yargs", "inquirer", "process"],
                "confidence": 0.95
            },
            SkillCategory.FILE_OPERATIONS: {
                "keywords": ["read", "write", "file", "path", "directory", "fs", "readFile", "writeFile", "createFile", "deleteFile", "copyFile", "moveFile", "exists", "stat", "mkdir", "rmdir", "watch", "watcher"],
                "imports": ["fs", "path", "os", "glob", "chokidar", "watchdog"],
                "confidence": 0.95
            },
            SkillCategory.CODE_PROCESSING: {
                "keywords": ["ast", "parse", "syntax", "transform", "generate", "compile", "transpile", "babel", "typescript", "eslint", "prettier", "acorn", "esprima"],
                "imports": ["ast", "babel", "typescript", "esprima", "acorn", "@babel/core", "@typescript-eslint"],
                "confidence": 0.98
            },
            SkillCategory.INDEXING_SYSTEMS: {
                "keywords": ["search", "index", "categorize", "metadata", "extract", "classify", "tag", "filter", "sort", "elasticsearch", "solr", "lucene"],
                "imports": ["elasticsearch", "solr", "whoosh", "lunr"],
                "confidence": 0.9
            },
            SkillCategory.MEMORY_SYSTEMS: {
                "keywords": ["cache", "persist", "state", "storage", "redis", "memcache", "sqlite", "leveldb", "store", "session", "memory"],
                "imports": ["redis", "memcache", "sqlite3", "leveldb", "lmdb"],
                "confidence": 0.92
            },
            
            # Advanced Capabilities
            SkillCategory.NATURAL_LANGUAGE: {
                "keywords": ["nlp", "text", "embedding", "semantic", "tokenize", "sentiment", "language", "spacy", "nltk", "transformers", "bert"],
                "imports": ["spacy", "nltk", "transformers", "sentence-transformers", "openai"],
                "confidence": 0.95
            },
            SkillCategory.PROMPT_ENGINEERING: {
                "keywords": ["prompt", "template", "context", "completion", "chat", "system", "user", "assistant", "role", "message"],
                "imports": ["jinja2", "mustache", "handlebars"],
                "confidence": 0.9
            },
            SkillCategory.MCP_INTEGRATION: {
                "keywords": ["mcp", "model", "context", "protocol", "server", "client", "resource", "tool", "capability"],
                "imports": ["mcp", "@modelcontextprotocol"],
                "confidence": 0.98
            },
            SkillCategory.API_FRAMEWORKS: {
                "keywords": ["api", "request", "http", "fetch", "axios", "endpoint", "rest", "graphql", "webhook", "client", "server", "response", "auth", "rate", "limit"],
                "imports": ["requests", "axios", "fetch", "express", "fastapi", "flask", "django"],
                "confidence": 0.92
            },
            
            # Legacy/Utility Categories
            SkillCategory.CONFIGURATION: {
                "keywords": ["config", "settings", "options", "preferences", "env", "environment", "dotenv", "yaml", "toml", "ini"],
                "imports": ["dotenv", "config", "yaml", "toml"],
                "confidence": 0.8
            },
            SkillCategory.ERROR_HANDLING: {
                "keywords": ["error", "exception", "try", "catch", "throw", "handle", "validate", "assert", "debug", "log", "warn"],
                "imports": ["winston", "pino", "debug"],
                "confidence": 0.75
            },
            SkillCategory.UTILITY_FUNCTIONS: {
                "keywords": ["util", "helper", "common", "shared", "library", "tool", "format", "convert", "calculate"],
                "imports": ["lodash", "ramda", "utils"],
                "confidence": 0.6
            }
        }
        return patterns
    
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
                extraction_priority=self._calculate_extraction_priority(func_name, category, confidence, func_source)
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
            try:
                # Try to get the full qualified name
                if hasattr(annotation.value, 'id'):
                    return f"{annotation.value.id}.{annotation.attr}"  # type: ignore
                else:
                    return annotation.attr
            except AttributeError:
                return annotation.attr
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
            # Core Performance Modules
            SkillCategory.CLI_OPERATIONS: f"CLI operation: {func_name}",
            SkillCategory.FILE_OPERATIONS: f"File operation: {func_name}",
            SkillCategory.CODE_PROCESSING: f"Code processor: {func_name}",
            SkillCategory.INDEXING_SYSTEMS: f"Indexing system: {func_name}",
            SkillCategory.MEMORY_SYSTEMS: f"Memory system: {func_name}",
            
            # Advanced Capabilities
            SkillCategory.NATURAL_LANGUAGE: f"NLP capability: {func_name}",
            SkillCategory.PROMPT_ENGINEERING: f"Prompt engineer: {func_name}",
            SkillCategory.MCP_INTEGRATION: f"MCP integration: {func_name}",
            SkillCategory.API_FRAMEWORKS: f"API framework: {func_name}",
            
            # Legacy/Utility
            SkillCategory.CONFIGURATION: f"Configuration: {func_name}",
            SkillCategory.ERROR_HANDLING: f"Error handler: {func_name}",
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
                        extraction_priority=self._calculate_extraction_priority(func_name, category, confidence, content[max(0, match.start()-200):match.end()+200])
                    ))
        
        return skills
    
    def _classify_js_function(self, func_name: str, content: str) -> Tuple[SkillCategory, float]:
        """Classify JavaScript function using target skill categories."""
        func_lower = func_name.lower()
        
        # Core Performance Modules
        if any(kw in func_lower for kw in ['parse', 'ast', 'transform', 'compile', 'generate']):
            return SkillCategory.CODE_PROCESSING, 0.9
        elif any(kw in func_lower for kw in ['command', 'cli', 'args', 'terminal', 'process']):
            return SkillCategory.CLI_OPERATIONS, 0.8
        elif any(kw in func_lower for kw in ['search', 'index', 'categorize', 'metadata', 'extract']):
            return SkillCategory.INDEXING_SYSTEMS, 0.8
        elif any(kw in func_lower for kw in ['file', 'read', 'write', 'path', 'directory']):
            return SkillCategory.FILE_OPERATIONS, 0.7
        elif any(kw in func_lower for kw in ['cache', 'store', 'persist', 'memory', 'session']):
            return SkillCategory.MEMORY_SYSTEMS, 0.8
        
        # Advanced Capabilities
        elif any(kw in func_lower for kw in ['mcp', 'protocol', 'server', 'client', 'resource']):
            return SkillCategory.MCP_INTEGRATION, 0.9
        elif any(kw in func_lower for kw in ['nlp', 'text', 'embedding', 'semantic', 'language']):
            return SkillCategory.NATURAL_LANGUAGE, 0.8
        elif any(kw in func_lower for kw in ['prompt', 'template', 'context', 'completion']):
            return SkillCategory.PROMPT_ENGINEERING, 0.8
        elif any(kw in func_lower for kw in ['api', 'fetch', 'request', 'http', 'endpoint']):
            return SkillCategory.API_FRAMEWORKS, 0.8
        
        # Legacy/Utility
        elif any(kw in func_lower for kw in ['config', 'settings', 'env']):
            return SkillCategory.CONFIGURATION, 0.6
        elif any(kw in func_lower for kw in ['error', 'exception', 'handle', 'validate']):
            return SkillCategory.ERROR_HANDLING, 0.6
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
            # Return empty module for files with no detected skills
            module_name = Path(file_path).stem
            return SkillModule(
                name=module_name,
                primary_category=SkillCategory.UTILITY_FUNCTIONS,
                skills=[],
                file_path=file_path,
                extraction_priority=0.0
            )
        
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
    
    def _calculate_extraction_priority(self, func_name: str, category: SkillCategory, 
                                     confidence: float, func_source: str) -> float:
        """Calculate sophisticated extraction priority based on multiple factors."""
        base_priority = confidence
        
        # Category-based priority multipliers (aligned with PROJECT_PLAN.md targets)
        category_multipliers = {
            # Core Performance Modules (highest priority)
            SkillCategory.CODE_PROCESSING: 1.5,  # AST parsing, syntax transformation, generation
            SkillCategory.CLI_OPERATIONS: 1.4,   # Argument parsing, command execution, terminal I/O
            SkillCategory.INDEXING_SYSTEMS: 1.4, # Search, categorization, metadata extraction
            SkillCategory.FILE_OPERATIONS: 1.3,  # Read, write, delete, copy, move, watch
            SkillCategory.MEMORY_SYSTEMS: 1.3,   # Caching, persistence, state management
            
            # Advanced Capabilities (high priority)
            SkillCategory.MCP_INTEGRATION: 1.5,     # Model Context Protocol implementations
            SkillCategory.NATURAL_LANGUAGE: 1.4,    # Text processing, embeddings, semantic search
            SkillCategory.PROMPT_ENGINEERING: 1.3,  # Template systems, context management
            SkillCategory.API_FRAMEWORKS: 1.2,      # HTTP clients, authentication, rate limiting
            
            # Legacy/Utility Categories (lower priority)
            SkillCategory.CONFIGURATION: 1.0,
            SkillCategory.ERROR_HANDLING: 1.0,
            SkillCategory.UTILITY_FUNCTIONS: 0.8
        }
        
        priority = base_priority * category_multipliers.get(category, 1.0)
        
        # High-value function name patterns
        high_value_patterns = [
            'api', 'client', 'service', 'manager', 'handler', 'processor',
            'config', 'setup', 'init', 'create', 'build', 'parse', 'validate',
            'authenticate', 'authorize', 'encrypt', 'decrypt', 'compress',
            'transform', 'convert', 'export', 'import', 'sync', 'async'
        ]
        
        name_lower = func_name.lower()
        for pattern in high_value_patterns:
            if pattern in name_lower:
                priority *= 1.2
                break
        
        # Complexity bonus (more complex = potentially more valuable)
        if len(func_source) > 500:  # Large function
            priority *= 1.1
        elif len(func_source) > 200:  # Medium function
            priority *= 1.05
        
        # Async function bonus
        if 'async' in func_source or 'await' in func_source:
            priority *= 1.1
        
        # Error handling bonus
        if any(keyword in func_source for keyword in ['try', 'catch', 'except', 'error', 'throw']):
            priority *= 1.05
        
        # Documentation bonus
        if any(keyword in func_source for keyword in ['/**', '"""', 'docstring', '@param', '@return']):
            priority *= 1.05
        
        # Cap at 1.0 and ensure minimum
        return min(max(priority, 0.1), 1.0)
