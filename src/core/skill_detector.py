"""
Enhanced Skill Detection Engine for AIPass-Code-Sniffer

Comprehensive skill detection with expanded patterns and semantic analysis.
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
    
    # Enhanced Categories
    COMMUNICATION = "communication"  # Email, messaging, notifications
    AUTHENTICATION = "authentication"  # Login, validation, security
    DATA_TRANSFORMATION = "data_transformation"  # Parsing, formatting, conversion
    
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

class EnhancedSkillDetector:
    """Enhanced skill detection engine with broader pattern recognition."""
    
    def __init__(self):
        self.patterns = self._init_enhanced_patterns()
        self.semantic_patterns = self._init_semantic_patterns()
    
    def _init_enhanced_patterns(self) -> Dict[SkillCategory, Dict[str, Any]]:
        """Initialize enhanced detection patterns with broader coverage."""
        patterns = {
            # Core Performance Modules
            SkillCategory.CLI_OPERATIONS: {
                "keywords": [
                    # Direct CLI terms
                    "command", "cli", "args", "argv", "commander", "yargs", "option", "flag", "subcommand",
                    # Process and execution
                    "execute", "run", "invoke", "call", "spawn", "exec", "process", "shell",
                    # Terminal I/O
                    "terminal", "console", "stdin", "stdout", "stderr", "pipe", "input", "output",
                    # Parsing and handling
                    "parse", "handle", "dispatch", "route"
                ],
                "function_patterns": [
                    r".*command.*", r".*execute.*", r".*run.*", r".*invoke.*", r".*spawn.*",
                    r".*parse.*args.*", r".*handle.*args.*", r".*dispatch.*", r".*route.*"
                ],
                "imports": ["argparse", "click", "commander", "yargs", "inquirer", "process", "subprocess"],
                "confidence": 0.8,
                "base_confidence": 0.6
            },
            
            SkillCategory.FILE_OPERATIONS: {
                "keywords": [
                    # Basic file ops
                    "read", "write", "file", "path", "directory", "folder",
                    # File system operations
                    "create", "delete", "copy", "move", "rename", "exists", "stat", "mkdir", "rmdir",
                    # File I/O
                    "open", "close", "save", "load", "import", "export",
                    # File watching
                    "watch", "monitor", "track", "observe",
                    # File system navigation
                    "list", "find", "search", "walk", "traverse"
                ],
                "function_patterns": [
                    r".*read.*", r".*write.*", r".*save.*", r".*load.*", r".*create.*file.*",
                    r".*delete.*", r".*copy.*", r".*move.*", r".*list.*", r".*find.*",
                    r"get.*file.*", r"set.*file.*", r".*directory.*", r".*folder.*"
                ],
                "imports": ["fs", "path", "os", "glob", "chokidar", "watchdog", "pathlib", "shutil"],
                "confidence": 0.8,
                "base_confidence": 0.6
            },
            
            SkillCategory.CODE_PROCESSING: {
                "keywords": [
                    # AST and parsing
                    "ast", "parse", "syntax", "tree", "node", "visitor",
                    # Code transformation
                    "transform", "generate", "compile", "transpile", "convert",
                    # Code analysis
                    "analyze", "scan", "lint", "format", "validate",
                    # Language tools
                    "babel", "typescript", "eslint", "prettier", "acorn", "esprima"
                ],
                "function_patterns": [
                    r".*parse.*", r".*transform.*", r".*generate.*", r".*compile.*",
                    r".*analyze.*", r".*scan.*", r".*lint.*", r".*format.*"
                ],
                "imports": ["ast", "babel", "typescript", "esprima", "acorn", "@babel/core", "@typescript-eslint"],
                "confidence": 0.9,
                "base_confidence": 0.7
            },
            
            SkillCategory.INDEXING_SYSTEMS: {
                "keywords": [
                    # Search and retrieval
                    "search", "find", "query", "lookup", "retrieve", "fetch", "get",
                    # Organization
                    "index", "categorize", "classify", "tag", "label", "group",
                    # Data operations
                    "filter", "sort", "rank", "score", "match", "compare",
                    # Metadata
                    "metadata", "extract", "collect", "gather", "aggregate",
                    # Search engines
                    "elasticsearch", "solr", "lucene", "whoosh"
                ],
                "function_patterns": [
                    r".*search.*", r".*find.*", r".*query.*", r".*lookup.*", r".*retrieve.*",
                    r".*index.*", r".*categorize.*", r".*classify.*", r".*filter.*", r".*sort.*",
                    r"get.*", r"find.*", r"search.*", r"list.*"
                ],
                "imports": ["elasticsearch", "solr", "whoosh", "lunr"],
                "confidence": 0.8,
                "base_confidence": 0.6
            },
            
            SkillCategory.MEMORY_SYSTEMS: {
                "keywords": [
                    # Storage and persistence (more specific)
                    "cache", "store", "persist", "save", "restore", "backup", "archive",
                    # State management (refined)
                    "state", "session", "context", "memory", "data", "storage",
                    # Cache systems
                    "redis", "memcache", "sqlite", "leveldb", "lmdb",
                    # Operations (more specific to avoid noise)
                    "initialize", "reset_state", "clear_cache", "flush", "sync", "update_state",
                    "checkpoint", "snapshot"
                ],
                "function_patterns": [
                    r".*save.*", r".*load.*", r".*persist.*", r".*restore.*",
                    r".*cache.*", r".*store.*", r".*state.*", r".*memory.*", 
                    r".*reset.*", r".*backup.*", r".*checkpoint.*",
                    r".*initialize.*", r".*sync.*"  # More specific patterns
                ],
                "imports": ["redis", "memcache", "sqlite3", "leveldb", "lmdb"],
                "confidence": 0.85,  # Higher base confidence
                "base_confidence": 0.7  # Higher base confidence
            },
            
            # Advanced Capabilities
            SkillCategory.NATURAL_LANGUAGE: {
                "keywords": [
                    # NLP core
                    "nlp", "text", "language", "linguistic", "semantic", "syntax",
                    # Processing
                    "tokenize", "parse", "analyze", "process", "extract",
                    # Understanding
                    "understand", "interpret", "meaning", "context", "intent",
                    # Generation
                    "generate", "complete", "respond", "chat", "conversation",
                    # ML/AI
                    "embedding", "vector", "similarity", "sentiment", "classification",
                    # Libraries
                    "spacy", "nltk", "transformers", "bert", "gpt", "openai"
                ],
                "function_patterns": [
                    r".*chat.*", r".*message.*", r".*respond.*", r".*reply.*", r".*conversation.*",
                    r".*text.*", r".*language.*", r".*nlp.*", r".*semantic.*", r".*embedding.*",
                    r".*tokenize.*", r".*parse.*text.*", r".*analyze.*text.*"
                ],
                "imports": ["spacy", "nltk", "transformers", "sentence-transformers", "openai"],
                "confidence": 0.8,
                "base_confidence": 0.6
            },
            
            SkillCategory.COMMUNICATION: {
                "keywords": [
                    # Email
                    "email", "mail", "send", "receive", "inbox", "message", "smtp", "imap",
                    # Messaging
                    "notify", "notification", "alert", "broadcast", "publish", "subscribe",
                    # Communication
                    "communicate", "transmit", "deliver", "dispatch", "forward"
                ],
                "function_patterns": [
                    r".*mail.*", r".*email.*", r".*send.*", r".*receive.*", r".*notify.*",
                    r".*message.*", r".*communicate.*", r".*transmit.*", r".*deliver.*"
                ],
                "imports": ["smtplib", "email", "imaplib", "poplib"],
                "confidence": 0.9,
                "base_confidence": 0.7
            },
            
            SkillCategory.API_FRAMEWORKS: {
                "keywords": [
                    # HTTP and networking
                    "api", "http", "https", "request", "response", "client", "server",
                    # Methods and protocols
                    "get", "post", "put", "delete", "patch", "fetch", "call", "invoke",
                    # REST and GraphQL
                    "rest", "restful", "graphql", "endpoint", "route", "url", "uri",
                    # Authentication and security
                    "auth", "authenticate", "authorize", "token", "key", "oauth",
                    # Rate limiting
                    "rate", "limit", "throttle", "quota",
                    # Libraries
                    "requests", "axios", "fetch", "express", "fastapi", "flask", "django"
                ],
                "function_patterns": [
                    r".*request.*", r".*fetch.*", r".*call.*", r".*invoke.*", r".*api.*",
                    r".*http.*", r".*auth.*", r".*authenticate.*", r".*token.*",
                    r"get.*", r"post.*", r"put.*", r"delete.*", r"send.*", r"receive.*"
                ],
                "imports": ["requests", "axios", "fetch", "express", "fastapi", "flask", "django", "urllib"],
                "confidence": 0.8,
                "base_confidence": 0.6
            },
            
            # Utility and support
            SkillCategory.ERROR_HANDLING: {
                "keywords": [
                    "error", "exception", "try", "catch", "throw", "raise", "handle",
                    "validate", "verify", "check", "assert", "debug", "log", "warn",
                    "fail", "recover", "retry", "fallback"
                ],
                "function_patterns": [
                    r".*error.*", r".*exception.*", r".*handle.*", r".*validate.*",
                    r".*verify.*", r".*check.*", r".*debug.*", r".*log.*"
                ],
                "imports": ["winston", "pino", "debug", "logging"],
                "confidence": 0.7,
                "base_confidence": 0.5
            },
            
            SkillCategory.UTILITY_FUNCTIONS: {
                "keywords": [
                    "util", "utility", "helper", "common", "shared", "library", "tool",
                    "format", "convert", "transform", "calculate", "compute", "process",
                    "clean", "normalize", "validate", "sanitize"
                ],
                "function_patterns": [
                    r".*util.*", r".*helper.*", r".*format.*", r".*convert.*",
                    r".*transform.*", r".*calculate.*", r".*process.*", r".*clean.*"
                ],
                "imports": ["lodash", "ramda", "utils"],
                "confidence": 0.6,
                "base_confidence": 0.4
            }
        }
        return patterns
    
    def _init_semantic_patterns(self) -> Dict[str, SkillCategory]:
        """Initialize semantic function name patterns (refined for accuracy)."""
        return {
            # Common CRUD operations
            "create": SkillCategory.FILE_OPERATIONS,
            "read": SkillCategory.FILE_OPERATIONS,
            "update": SkillCategory.FILE_OPERATIONS,
            "delete": SkillCategory.FILE_OPERATIONS,
            "get": SkillCategory.INDEXING_SYSTEMS,
            "set": SkillCategory.MEMORY_SYSTEMS,
            "put": SkillCategory.MEMORY_SYSTEMS,
            "post": SkillCategory.API_FRAMEWORKS,
            
            # Communication patterns
            "send": SkillCategory.COMMUNICATION,
            "receive": SkillCategory.COMMUNICATION,
            "mail": SkillCategory.COMMUNICATION,
            "email": SkillCategory.COMMUNICATION,
            "notify": SkillCategory.COMMUNICATION,
            "message": SkillCategory.COMMUNICATION,
            
            # State management (refined - no bare "init")
            "initialize": SkillCategory.MEMORY_SYSTEMS,
            "init_state": SkillCategory.MEMORY_SYSTEMS,
            "init_cache": SkillCategory.MEMORY_SYSTEMS,
            "reset": SkillCategory.MEMORY_SYSTEMS,
            "save": SkillCategory.MEMORY_SYSTEMS,
            "load": SkillCategory.MEMORY_SYSTEMS,
            "restore": SkillCategory.MEMORY_SYSTEMS,
            "backup": SkillCategory.MEMORY_SYSTEMS,
            "cache": SkillCategory.MEMORY_SYSTEMS,
            "store": SkillCategory.MEMORY_SYSTEMS,
            "persist": SkillCategory.MEMORY_SYSTEMS,
            
            # Processing
            "parse": SkillCategory.CODE_PROCESSING,
            "format": SkillCategory.DATA_TRANSFORMATION,
            "transform": SkillCategory.DATA_TRANSFORMATION,
            "convert": SkillCategory.DATA_TRANSFORMATION,
            "validate": SkillCategory.ERROR_HANDLING,
            
            # Natural language
            "chat": SkillCategory.NATURAL_LANGUAGE,
            "respond": SkillCategory.NATURAL_LANGUAGE,
            "reply": SkillCategory.NATURAL_LANGUAGE,
            "conversation": SkillCategory.NATURAL_LANGUAGE,
            
            # Search and indexing
            "search": SkillCategory.INDEXING_SYSTEMS,
            "find": SkillCategory.INDEXING_SYSTEMS,
            "query": SkillCategory.INDEXING_SYSTEMS,
            "lookup": SkillCategory.INDEXING_SYSTEMS,
            "index": SkillCategory.INDEXING_SYSTEMS,
            "filter": SkillCategory.INDEXING_SYSTEMS,
            "sort": SkillCategory.INDEXING_SYSTEMS,
            
            # CLI operations
            "execute": SkillCategory.CLI_OPERATIONS,
            "run": SkillCategory.CLI_OPERATIONS,
            "invoke": SkillCategory.CLI_OPERATIONS,
            "command": SkillCategory.CLI_OPERATIONS,
            "spawn": SkillCategory.CLI_OPERATIONS
        }
    
    def detect_skills_in_file(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect skills in a file with enhanced pattern matching."""
        ext = Path(file_path).suffix.lower()
        
        if ext == '.py':
            return self._detect_python_skills(content, file_path)
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            return self._detect_js_skills(content, file_path)
        return []
    
    def _detect_python_skills(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect Python skills using enhanced AST analysis."""
        skills = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    skill = self._analyze_function_enhanced(node, content, file_path)
                    if skill:
                        skills.append(skill)
        
        except SyntaxError:
            # Fallback to regex with enhanced patterns
            skills.extend(self._regex_detection_enhanced(content, file_path))
        
        return skills
    
    def _analyze_function_enhanced(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], 
                                 content: str, file_path: str) -> Optional[SkillSignature]:
        """Enhanced function analysis with semantic patterns and filtering."""
        func_name = node.name
        
        # Skip private functions but allow magic methods
        if func_name.startswith('_') and not func_name.startswith('__'):
            return None
        
        # Skip obvious non-skills with refined filtering
        if self._should_exclude_function(func_name, node):
            return None
        
        # Get function source
        try:
            func_source = ast.get_source_segment(content, node) or ""
        except:
            func_source = ""
        
        # Enhanced classification
        category, confidence = self._classify_function_enhanced(func_name, func_source, node)
        
        # Higher threshold for skill detection (reduced false positives)
        if confidence > 0.6:  # Increased from 0.4
            return SkillSignature(
                name=func_name,
                category=category,
                confidence=confidence,
                description=self._generate_description_enhanced(func_name, category),
                file_path=file_path,
                line_start=node.lineno,
                line_end=getattr(node, 'end_lineno', node.lineno),
                parameters=self._extract_parameters_enhanced(node),
                dependencies=self._extract_dependencies(func_source),
                complexity=self._assess_complexity_enhanced(func_source, node),
                async_function=isinstance(node, ast.AsyncFunctionDef),
                extraction_priority=self._calculate_extraction_priority_enhanced(func_name, category, confidence, func_source)
            )
        
        return None
    
    def _should_exclude_function(self, func_name: str, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
        """Exclude obvious non-skills to improve accuracy."""
        
        # Exclude simple constructors (unless they're complex)
        if func_name == "__init__":
            # Allow complex constructors with significant logic
            line_count = (getattr(node, 'end_lineno', node.lineno) - node.lineno)
            if line_count < 5:  # Simple constructors
                return True
            # Check if it's just basic assignment
            # This is a simplified heuristic - could be improved with AST analysis
            return False
        
        # Exclude common test setup methods (unless in test files we want to analyze)
        if func_name in ["setUp", "tearDown", "setUpClass", "tearDownClass"]:
            return True
        
        # Exclude property getters/setters without business logic
        if func_name.startswith("get_") and len(node.args.args) <= 1:
            # Simple getters are usually not interesting skills
            line_count = (getattr(node, 'end_lineno', node.lineno) - node.lineno)
            if line_count < 3:
                return True
        
        # Exclude simple setters
        if func_name.startswith("set_") and len(node.args.args) <= 2:
            line_count = (getattr(node, 'end_lineno', node.lineno) - node.lineno)
            if line_count < 3:
                return True
        
        return False
    
    def _classify_function_enhanced(self, func_name: str, func_source: str, 
                                  node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Tuple[SkillCategory, float]:
        """Enhanced function classification with multiple scoring methods."""
        scores = {}
        
        # Method 1: Semantic pattern matching (highest priority)
        semantic_score = self._score_semantic_patterns(func_name)
        if semantic_score[1] > 0:
            scores['semantic'] = semantic_score
        
        # Method 2: Enhanced keyword matching
        keyword_score = self._score_keyword_patterns(func_name, func_source)
        if keyword_score[1] > 0:
            scores['keyword'] = keyword_score
        
        # Method 3: Function signature analysis
        signature_score = self._score_function_signature(node)
        if signature_score[1] > 0:
            scores['signature'] = signature_score
        
        # Method 4: Import context analysis
        import_score = self._score_import_context(func_source)
        if import_score[1] > 0:
            scores['import'] = import_score
        
        # Combine scores with weighted average
        if not scores:
            return SkillCategory.UTILITY_FUNCTIONS, 0.3
        
        # Weight the different scoring methods
        weights = {
            'semantic': 0.4,    # Highest weight for semantic patterns
            'keyword': 0.3,     # Good weight for keyword matching
            'signature': 0.2,   # Medium weight for function signature
            'import': 0.1       # Lower weight for imports
        }
        
        final_scores = {}
        for category in SkillCategory:
            total_score = 0.0
            total_weight = 0.0
            
            for method, (cat, score) in scores.items():
                if cat == category:
                    weight = weights.get(method, 0.1)
                    total_score += score * weight
                    total_weight += weight
            
            if total_weight > 0:
                final_scores[category] = total_score / total_weight
        
        if final_scores:
            best_category = max(final_scores.items(), key=lambda x: x[1])
            return best_category[0], min(best_category[1], 1.0)
        
        # Fallback
        return SkillCategory.UTILITY_FUNCTIONS, 0.3
    
    def _score_semantic_patterns(self, func_name: str) -> Tuple[SkillCategory, float]:
        """Score function based on semantic patterns with better precision."""
        func_lower = func_name.lower()
        
        # Direct semantic matches with higher confidence
        for pattern, category in self.semantic_patterns.items():
            if pattern == func_lower:  # Exact match
                return category, 0.95
            elif func_lower == f"{pattern}_":  # With underscore suffix
                return category, 0.9
        
        # Partial matches with context analysis
        for pattern, category in self.semantic_patterns.items():
            # Strong prefix/suffix matches
            if func_lower.startswith(f"{pattern}_") or func_lower.endswith(f"_{pattern}"):
                return category, 0.8
            # Contains pattern (but not as simple substring to avoid false positives)
            elif f"_{pattern}_" in func_lower or f"{pattern}_" in func_lower[:len(pattern)+1]:
                return category, 0.7
        
        return SkillCategory.UTILITY_FUNCTIONS, 0.0
    
    def _score_keyword_patterns(self, func_name: str, func_source: str) -> Tuple[SkillCategory, float]:
        """Score function based on enhanced keyword patterns."""
        best_category = SkillCategory.UTILITY_FUNCTIONS
        best_score = 0.0
        
        for category, patterns in self.patterns.items():
            score = 0.0
            
            # Enhanced name matching
            name_matches = 0
            for keyword in patterns["keywords"]:
                if keyword.lower() in func_name.lower():
                    name_matches += 1
            
            # Function pattern matching
            pattern_matches = 0
            for pattern in patterns.get("function_patterns", []):
                if re.search(pattern, func_name, re.IGNORECASE):
                    pattern_matches += 1
            
            # Source content matching (reduced weight)
            source_matches = 0
            for keyword in patterns["keywords"][:10]:  # Limit to avoid noise
                if keyword.lower() in func_source.lower():
                    source_matches += 1
            
            # Calculate weighted score
            name_weight = 0.5
            pattern_weight = 0.3
            source_weight = 0.2
            
            total_keywords = len(patterns["keywords"])
            total_patterns = len(patterns.get("function_patterns", []))
            
            if total_keywords > 0:
                score += (name_matches / total_keywords) * name_weight
            if total_patterns > 0:
                score += (pattern_matches / total_patterns) * pattern_weight
            if total_keywords > 0:
                score += (source_matches / min(total_keywords, 10)) * source_weight
            
            # Apply base confidence
            final_score = score * patterns.get("base_confidence", 0.5)
            
            if final_score > best_score:
                best_category = category
                best_score = final_score
        
        return best_category, min(best_score, 1.0)
    
    def _score_function_signature(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Tuple[SkillCategory, float]:
        """Score function based on signature characteristics."""
        # Async functions likely for I/O or API operations
        if isinstance(node, ast.AsyncFunctionDef):
            return SkillCategory.API_FRAMEWORKS, 0.6
        
        # Functions with many parameters might be configuration or utility
        param_count = len(node.args.args)
        if param_count > 5:
            return SkillCategory.CONFIGURATION, 0.5
        elif param_count == 0:
            return SkillCategory.UTILITY_FUNCTIONS, 0.4
        
        return SkillCategory.UTILITY_FUNCTIONS, 0.0
    
    def _score_import_context(self, func_source: str) -> Tuple[SkillCategory, float]:
        """Score function based on import context."""
        for category, patterns in self.patterns.items():
            for imp in patterns["imports"]:
                if imp in func_source:
                    return category, 0.7
        
        return SkillCategory.UTILITY_FUNCTIONS, 0.0
    
    def _extract_parameters_enhanced(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[Dict[str, Any]]:
        """Enhanced parameter extraction."""
        params = []
        for arg in node.args.args:
            param_info = {
                "name": arg.arg,
                "type": self._get_type_hint(arg.annotation) if arg.annotation else None
            }
            params.append(param_info)
        return params
    
    def _get_type_hint(self, annotation: ast.expr) -> str:
        """Extract type hint as string."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            try:
                if hasattr(annotation.value, 'id'):
                    return f"{annotation.value.id}.{annotation.attr}"
                else:
                    return annotation.attr
            except AttributeError:
                return annotation.attr
        return "Any"
    
    def _assess_complexity_enhanced(self, func_source: str, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        """Enhanced complexity assessment."""
        # Count control flow statements
        control_flow = (
            func_source.count('if ') + func_source.count('elif ') + 
            func_source.count('for ') + func_source.count('while ') +
            func_source.count('try:') + func_source.count('except ')
        )
        
        # Count function calls (approximation)
        function_calls = func_source.count('(') - func_source.count('def ')
        
        # Count lines of code (excluding empty lines and comments)
        lines = [line.strip() for line in func_source.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        loc = len(lines)
        
        # Complexity scoring
        complexity_score = control_flow * 2 + function_calls * 0.5 + loc * 0.1
        
        if complexity_score >= 20:
            return "high"
        elif complexity_score >= 10:
            return "medium"
        else:
            return "low"
    
    def _calculate_extraction_priority_enhanced(self, func_name: str, category: SkillCategory, 
                                              confidence: float, func_source: str) -> float:
        """Enhanced extraction priority calculation."""
        base_priority = confidence
        
        # Boost priority for high-value categories
        category_boosts = {
            SkillCategory.MCP_INTEGRATION: 0.3,
            SkillCategory.API_FRAMEWORKS: 0.2,
            SkillCategory.NATURAL_LANGUAGE: 0.2,
            SkillCategory.COMMUNICATION: 0.25,
            SkillCategory.MEMORY_SYSTEMS: 0.15,
            SkillCategory.CLI_OPERATIONS: 0.1
        }
        
        priority = base_priority + category_boosts.get(category, 0.0)
        
        # Boost for async functions (usually more valuable)
        if 'async ' in func_source:
            priority += 0.1
        
        # Boost for well-documented functions
        if '"""' in func_source or "'''" in func_source:
            priority += 0.05
        
        # Boost for functions with type hints
        if '->' in func_source:
            priority += 0.05
        
        return min(priority, 1.0)
    
    def _extract_dependencies(self, func_source: str) -> List[str]:
        """Extract function dependencies."""
        deps = []
        
        # Enhanced import detection
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'require\([\'"]([^\'"]+)[\'"]\)',  # JavaScript require
            r'import.*from\s+[\'"]([^\'"]+)[\'"]'  # ES6 imports
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, func_source)
            deps.extend(matches)
        
        return list(set(deps))
    
    def _generate_description_enhanced(self, func_name: str, category: SkillCategory) -> str:
        """Generate enhanced skill descriptions."""
        templates = {
            # Core Performance Modules
            SkillCategory.CLI_OPERATIONS: f"Command-line operation: {func_name}",
            SkillCategory.FILE_OPERATIONS: f"File system operation: {func_name}",
            SkillCategory.CODE_PROCESSING: f"Code analysis/transformation: {func_name}",
            SkillCategory.INDEXING_SYSTEMS: f"Search/indexing capability: {func_name}",
            SkillCategory.MEMORY_SYSTEMS: f"State/memory management: {func_name}",
            
            # Advanced Capabilities
            SkillCategory.NATURAL_LANGUAGE: f"Natural language processing: {func_name}",
            SkillCategory.PROMPT_ENGINEERING: f"Prompt/template system: {func_name}",
            SkillCategory.MCP_INTEGRATION: f"Model Context Protocol: {func_name}",
            SkillCategory.API_FRAMEWORKS: f"API/HTTP operation: {func_name}",
            
            # Enhanced Categories
            SkillCategory.COMMUNICATION: f"Communication system: {func_name}",
            SkillCategory.AUTHENTICATION: f"Authentication/security: {func_name}",
            SkillCategory.DATA_TRANSFORMATION: f"Data processing: {func_name}",
            
            # Utility Categories
            SkillCategory.ERROR_HANDLING: f"Error handling: {func_name}",
            SkillCategory.CONFIGURATION: f"Configuration management: {func_name}",
            SkillCategory.UTILITY_FUNCTIONS: f"Utility function: {func_name}"
        }
        
        return templates.get(category, f"Function: {func_name}")
    
    def _detect_js_skills(self, content: str, file_path: str) -> List[SkillSignature]:
        """Detect JavaScript/TypeScript skills using enhanced regex patterns."""
        skills = []
        
        # Enhanced function detection patterns
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>\s*{|\([^)]*\)\s*=>)',
            r'let\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>\s*{|\([^)]*\)\s*=>)',
            r'var\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>\s*{|\([^)]*\)\s*=>)',
            r'(\w+)\s*:\s*(?:async\s+)?function\s*\(',
            r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*{',  # Method definitions
            r'export\s+(?:async\s+)?function\s+(\w+)\s*\(',
            r'export\s+const\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>\s*{|\([^)]*\)\s*=>)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                func_name = match.group(1)
                if not func_name or func_name.startswith('_'):
                    continue
                
                # Get line number
                line_num = content[:match.start()].count('\n') + 1
                
                # Get function context (try to get the whole function)
                func_context = self._extract_js_function_context(content, match.start())
                
                # Classify the function
                category, confidence = self._classify_js_function(func_name, func_context)
                
                if confidence > 0.4:  # Lower threshold
                    skills.append(SkillSignature(
                        name=func_name,
                        category=category,
                        confidence=confidence,
                        description=self._generate_description_enhanced(func_name, category),
                        file_path=file_path,
                        line_start=line_num,
                        line_end=line_num,  # Approximate
                        parameters=[],  # Could be enhanced later
                        dependencies=self._extract_js_dependencies(func_context),
                        complexity=self._assess_js_complexity(func_context),
                        async_function='async' in match.group(0),
                        extraction_priority=self._calculate_extraction_priority_enhanced(func_name, category, confidence, func_context)
                    ))
        
        return skills
    
    def _extract_js_function_context(self, content: str, start_pos: int) -> str:
        """Extract JavaScript function context for analysis."""
        # Find the function block (simplified approach)
        lines = content[start_pos:start_pos+2000].split('\n')  # Look at next ~2000 chars
        context_lines = []
        
        brace_count = 0
        in_function = False
        
        for line in lines:
            context_lines.append(line)
            
            for char in line:
                if char == '{':
                    brace_count += 1
                    in_function = True
                elif char == '}':
                    brace_count -= 1
                    
            if in_function and brace_count == 0:
                break
                
            if len(context_lines) > 50:  # Limit context size
                break
        
        return '\n'.join(context_lines)
    
    def _classify_js_function(self, func_name: str, func_context: str) -> Tuple[SkillCategory, float]:
        """Classify JavaScript function using enhanced patterns."""
        # Use the same enhanced classification as Python
        return self._classify_function_enhanced_js(func_name, func_context)
    
    def _classify_function_enhanced_js(self, func_name: str, func_source: str) -> Tuple[SkillCategory, float]:
        """Enhanced JavaScript function classification."""
        scores = {}
        
        # Method 1: Semantic pattern matching
        semantic_score = self._score_semantic_patterns(func_name)
        if semantic_score[1] > 0:
            scores['semantic'] = semantic_score
        
        # Method 2: Enhanced keyword matching
        keyword_score = self._score_keyword_patterns(func_name, func_source)
        if keyword_score[1] > 0:
            scores['keyword'] = keyword_score
        
        # Method 3: JavaScript-specific patterns
        js_score = self._score_js_specific_patterns(func_name, func_source)
        if js_score[1] > 0:
            scores['js_specific'] = js_score
        
        # Combine scores
        if not scores:
            return SkillCategory.UTILITY_FUNCTIONS, 0.3
        
        weights = {
            'semantic': 0.4,
            'keyword': 0.4,
            'js_specific': 0.2
        }
        
        final_scores = {}
        for category in SkillCategory:
            total_score = 0.0
            total_weight = 0.0
            
            for method, (cat, score) in scores.items():
                if cat == category:
                    weight = weights.get(method, 0.1)
                    total_score += score * weight
                    total_weight += weight
            
            if total_weight > 0:
                final_scores[category] = total_score / total_weight
        
        if final_scores:
            best_category = max(final_scores.items(), key=lambda x: x[1])
            return best_category[0], min(best_category[1], 1.0)
        
        return SkillCategory.UTILITY_FUNCTIONS, 0.3
    
    def _score_js_specific_patterns(self, func_name: str, func_source: str) -> Tuple[SkillCategory, float]:
        """Score JavaScript-specific patterns."""
        # DOM manipulation
        if any(term in func_source.lower() for term in ['document.', 'window.', 'element.', 'dom', 'jquery', '$(']):
            return SkillCategory.UTILITY_FUNCTIONS, 0.6
        
        # Node.js file system
        if any(term in func_source.lower() for term in ['fs.', 'path.', 'require(', '__dirname', '__filename']):
            return SkillCategory.FILE_OPERATIONS, 0.8
        
        # Express/API patterns
        if any(term in func_source.lower() for term in ['req.', 'res.', 'app.', 'router.', 'middleware']):
            return SkillCategory.API_FRAMEWORKS, 0.8
        
        # Async/Promise patterns
        if any(term in func_source.lower() for term in ['await ', 'promise', '.then(', '.catch(', 'async']):
            return SkillCategory.API_FRAMEWORKS, 0.6
        
        return SkillCategory.UTILITY_FUNCTIONS, 0.0
    
    def _extract_js_dependencies(self, func_context: str) -> List[str]:
        """Extract JavaScript dependencies."""
        deps = []
        
        # JavaScript import patterns
        patterns = [
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import.*from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, func_context)
            deps.extend(matches)
        
        return list(set(deps))
    
    def _assess_js_complexity(self, func_context: str) -> str:
        """Assess JavaScript function complexity."""
        # Count control flow and complexity indicators
        complexity_indicators = (
            func_context.count('if ') + func_context.count('for ') + 
            func_context.count('while ') + func_context.count('switch ') +
            func_context.count('try ') + func_context.count('catch ') +
            func_context.count('?.') + func_context.count('&&') + func_context.count('||')
        )
        
        # Count lines
        lines = len([l for l in func_context.split('\n') if l.strip() and not l.strip().startswith('//')])
        
        if complexity_indicators >= 5 or lines >= 30:
            return "high"
        elif complexity_indicators >= 2 or lines >= 15:
            return "medium"
        else:
            return "low"
    
    def _regex_detection_enhanced(self, content: str, file_path: str) -> List[SkillSignature]:
        """Enhanced regex-based skill detection as fallback."""
        skills = []
        
        # Enhanced Python function detection
        pattern = r'def\s+(\w+)\s*\([^)]*\):'
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            func_name = match.group(1)
            if func_name.startswith('_') and not func_name.startswith('__'):
                continue
            
            line_num = content[:match.start()].count('\n') + 1
            
            # Get some context around the function
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 1000)
            context = content[start:end]
            
            # Classify using enhanced patterns
            category, confidence = self._score_keyword_patterns(func_name, context)
            
            if confidence > 0.4:
                skills.append(SkillSignature(
                    name=func_name,
                    category=category,
                    confidence=confidence,
                    description=self._generate_description_enhanced(func_name, category),
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parameters=[],
                    dependencies=self._extract_dependencies(context),
                    complexity="medium",
                    async_function=False,
                    extraction_priority=confidence
                ))
        
        return skills
    
    def create_skill_module(self, skills: List[SkillSignature], file_path: str) -> Optional[SkillModule]:
        """Create a skill module from multiple related skills."""
        if len(skills) < 2:
            return None
        
        # Determine primary category based on most common category
        categories = [skill.category for skill in skills]
        primary_category = max(set(categories), key=categories.count)
        
        # Generate module name from file path
        module_name = Path(file_path).stem.replace('_', '-').replace('.', '-')
        
        return SkillModule(
            name=module_name,
            primary_category=primary_category,
            skills=skills,
            file_path=file_path,
            extraction_priority=sum(skill.extraction_priority for skill in skills) / len(skills)
        )


# Maintain backward compatibility by aliasing the new class
AdvancedSkillDetector = EnhancedSkillDetector
