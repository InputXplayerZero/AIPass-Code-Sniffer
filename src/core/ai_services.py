"""
AI Services abstraction layer for semantic code analysis.

This module provides a unified interface for different AI models specialized
for various aspects of code analysis.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class SemanticAnalysis:
    """Results of semantic code analysis."""
    business_context: str
    architectural_pattern: str
    design_patterns: List[str]
    quality_score: float
    recommendations: List[str]
    domain_type: str  # "ai_tools", "web_framework", "cli_utility", etc.


@dataclass
class PatternAnalysis:
    """Results of pattern recognition analysis."""
    react_patterns: List[str]
    architectural_patterns: List[str]
    design_patterns: List[str]
    anti_patterns: List[str]
    safety_patterns: List[str]


@dataclass
class QualityAssessment:
    """Comprehensive quality assessment results."""
    overall_score: float
    code_quality: float
    design_quality: float
    documentation_quality: float
    maintainability: float
    reusability: float
    recommendations: List[str]
    strengths: List[str]
    weaknesses: List[str]


class AIService(ABC):
    """Abstract base class for AI services."""
    
    @abstractmethod
    async def analyze_semantic(self, code: str, file_path: str, language: str) -> SemanticAnalysis:
        """Perform semantic analysis of code."""
        pass
    
    @abstractmethod
    async def detect_patterns(self, code: str, language: str) -> PatternAnalysis:
        """Detect patterns in code."""
        pass
    
    @abstractmethod
    async def assess_quality(self, code: str, context: str) -> QualityAssessment:
        """Assess code quality."""
        pass
    
    @abstractmethod
    async def generate_summary(self, code: str, context: str) -> str:
        """Generate human-readable code summary."""
        pass


class OpenAIService(AIService):
    """OpenAI-based AI service for code analysis."""
    
    def __init__(self, api_key: str, summarization_model: str = "gpt-4o-mini", analysis_model: str = "gpt-4"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available. Install with: pip install openai")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.summarization_model = summarization_model
        self.analysis_model = analysis_model
    
    async def analyze_semantic(self, code: str, file_path: str, language: str) -> SemanticAnalysis:
        """Perform semantic analysis using GPT-4."""
        prompt = f"""
        Analyze this {language} code and provide semantic understanding:

        File: {file_path}
        Code:
        ```{language}
        {code}
        ```

        Please analyze and return a JSON response with:
        1. business_context: What business domain does this code serve? (1-2 sentences)
        2. architectural_pattern: What architectural pattern is used? (e.g., "CLI + Core separation", "MVC", "Component-based")
        3. design_patterns: List of design patterns used (e.g., ["Factory", "Observer", "Strategy"])
        4. quality_score: Overall code quality score (0-10)
        5. recommendations: List of improvement suggestions
        6. domain_type: Primary domain category ("ai_tools", "web_framework", "cli_utility", "data_processing", "testing", "configuration", etc.)

        Focus on understanding the PURPOSE and BUSINESS CONTEXT, not just the syntax.
        """
        
        try:
            # Remove json_object format for gpt-4o-mini compatibility
            response = self.client.chat.completions.create(
                model=self.analysis_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return SemanticAnalysis(
                business_context=result.get("business_context", "Unknown"),
                architectural_pattern=result.get("architectural_pattern", "Unknown"),
                design_patterns=result.get("design_patterns", []),
                quality_score=float(result.get("quality_score", 5.0)),
                recommendations=result.get("recommendations", []),
                domain_type=result.get("domain_type", "unknown")
            )
        except Exception as e:
            # Return default analysis if AI fails
            return SemanticAnalysis(
                business_context=f"Analysis failed: {str(e)}",
                architectural_pattern="Unknown",
                design_patterns=[],
                quality_score=5.0,
                recommendations=["AI analysis unavailable"],
                domain_type="unknown"
            )
    
    async def detect_patterns(self, code: str, language: str) -> PatternAnalysis:
        """Detect patterns using GPT-4."""
        prompt = f"""
        Analyze this {language} code for patterns:

        ```{language}
        {code}
        ```

        Return JSON with:
        1. react_patterns: React-specific patterns (hooks, components, state management, etc.)
        2. architectural_patterns: High-level architectural patterns (MVC, MVVM, microservices, etc.)
        3. design_patterns: GOF and other design patterns (Factory, Observer, Strategy, etc.)
        4. anti_patterns: Code smells and anti-patterns found
        5. safety_patterns: Security, validation, and safety mechanisms

        Focus on identifying meaningful patterns, not just syntax.
        """
        
        try:
            # Remove json_object format for gpt-4o-mini compatibility
            response = self.client.chat.completions.create(
                model=self.analysis_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return PatternAnalysis(
                react_patterns=result.get("react_patterns", []),
                architectural_patterns=result.get("architectural_patterns", []),
                design_patterns=result.get("design_patterns", []),
                anti_patterns=result.get("anti_patterns", []),
                safety_patterns=result.get("safety_patterns", [])
            )
        except Exception as e:
            return PatternAnalysis(
                react_patterns=[],
                architectural_patterns=[],
                design_patterns=[],
                anti_patterns=[f"Pattern analysis failed: {str(e)}"],
                safety_patterns=[]
            )
    
    async def assess_quality(self, code: str, context: str) -> QualityAssessment:
        """Assess code quality using GPT-4."""
        prompt = f"""
        Assess the quality of this code:

        Context: {context}
        Code:
        ```
        {code}
        ```

        Return JSON with scores (0-10) and analysis:
        1. overall_score: Overall quality score
        2. code_quality: Readability, clarity, performance
        3. design_quality: Modularity, separation of concerns, architecture
        4. documentation_quality: Comments, docstrings, self-documenting code
        5. maintainability: How easy is it to modify and extend?
        6. reusability: How reusable are the components?
        7. recommendations: List of specific improvement suggestions
        8. strengths: List of what the code does well
        9. weaknesses: List of areas for improvement

        Be specific and actionable in recommendations.
        """
        
        try:
            # Remove json_object format for gpt-4o-mini compatibility
            response = self.client.chat.completions.create(
                model=self.analysis_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return QualityAssessment(
                overall_score=float(result.get("overall_score", 5.0)),
                code_quality=float(result.get("code_quality", 5.0)),
                design_quality=float(result.get("design_quality", 5.0)),
                documentation_quality=float(result.get("documentation_quality", 5.0)),
                maintainability=float(result.get("maintainability", 5.0)),
                reusability=float(result.get("reusability", 5.0)),
                recommendations=result.get("recommendations", []),
                strengths=result.get("strengths", []),
                weaknesses=result.get("weaknesses", [])
            )
        except Exception as e:
            return QualityAssessment(
                overall_score=5.0,
                code_quality=5.0,
                design_quality=5.0,
                documentation_quality=5.0,
                maintainability=5.0,
                reusability=5.0,
                recommendations=[f"Quality assessment failed: {str(e)}"],
                strengths=[],
                weaknesses=[]
            )
    
    async def generate_summary(self, code: str, context: str) -> str:
        """Generate human-readable summary using GPT-4o-mini."""
        prompt = f"""
        Generate a clear, human-readable summary of this code:

        Context: {context}
        Code:
        ```
        {code}
        ```

        Write a 2-3 paragraph summary that explains:
        1. What this code does (purpose and functionality)
        2. How it works (key mechanisms and approach)
        3. Why it's designed this way (architectural decisions)

        Write for developers who need to understand this code quickly.
        Use clear, professional language without jargon.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.summarization_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"


class AnthropicService(AIService):
    """Anthropic Claude-based AI service for code analysis."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic library not available. Install with: pip install anthropic")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    async def analyze_semantic(self, code: str, file_path: str, language: str) -> SemanticAnalysis:
        """Perform semantic analysis using Claude."""
        # Implementation similar to OpenAI but using Claude's API
        # This would be implemented based on Anthropic's API structure
        pass
    
    async def detect_patterns(self, code: str, language: str) -> PatternAnalysis:
        """Detect patterns using Claude."""
        # Implementation for Claude pattern detection
        pass
    
    async def assess_quality(self, code: str, context: str) -> QualityAssessment:
        """Assess code quality using Claude."""
        # Implementation for Claude quality assessment
        pass
    
    async def generate_summary(self, code: str, context: str) -> str:
        """Generate summary using Claude."""
        # Implementation for Claude summary generation
        pass


class AIServiceManager:
    """Manager for AI services with fallback and load balancing."""
    
    def __init__(self, config: Dict[str, Any]):
        self.services: Dict[str, AIService] = {}
        self.config = config
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize available AI services based on configuration."""
        if "openai" in self.config and OPENAI_AVAILABLE:
            openai_config = self.config["openai"]
            # Get API key from environment, not from config literal
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                # Fallback to config if it's not a template string
                config_key = openai_config.get("api_key", "")
                if config_key and not config_key.startswith("${"):
                    api_key = config_key
            
            if api_key:
                self.services["openai"] = OpenAIService(
                    api_key=api_key,
                    summarization_model=openai_config.get("models", {}).get("summarization", "gpt-4o-mini"),
                    analysis_model=openai_config.get("models", {}).get("analysis", "gpt-4")
                )
        
        if "anthropic" in self.config and ANTHROPIC_AVAILABLE:
            anthropic_config = self.config["anthropic"]
            api_key = anthropic_config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.services["anthropic"] = AnthropicService(
                    api_key=api_key,
                    model=anthropic_config.get("model", "claude-3-5-sonnet-20241022")
                )
    
    def get_service(self, preferred: str = "openai") -> Optional[AIService]:
        """Get an AI service, with fallback to available services."""
        if preferred in self.services:
            return self.services[preferred]
        
        # Fallback to any available service
        if self.services:
            return next(iter(self.services.values()))
        
        return None
    
    def has_services(self) -> bool:
        """Check if any AI services are available."""
        return len(self.services) > 0
    
    async def generate_summary(self, code_content: str, language: str, file_path: str) -> str:
        """Generate AI summary for code."""
        return await self.analyze_with_ai(code_content, file_path, language, "summary")
    
    async def analyze_semantics(self, code_content: str, language: str) -> SemanticAnalysis:
        """Analyze semantic meaning of code."""
        return await self.analyze_with_ai(code_content, "", language, "semantic")
    
    async def detect_patterns(self, code_content: str, language: str) -> PatternAnalysis:
        """Detect patterns in code."""
        return await self.analyze_with_ai(code_content, "", language, "patterns")
    
    async def assess_quality(self, code_content: str, language: str) -> QualityAssessment:
        """Assess code quality."""
        return await self.analyze_with_ai(code_content, "", language, "quality")
    
    async def analyze_with_ai(self, code: str, file_path: str, language: str, 
                             analysis_type: str = "semantic") -> Union[SemanticAnalysis, PatternAnalysis, QualityAssessment, str]:
        """Perform AI analysis with automatic service selection."""
        service = self.get_service()
        if not service:
            raise RuntimeError("No AI services available. Please configure API keys.")
        
        if analysis_type == "semantic":
            return await service.analyze_semantic(code, file_path, language)
        elif analysis_type == "patterns":
            return await service.detect_patterns(code, language)
        elif analysis_type == "quality":
            return await service.assess_quality(code, f"File: {file_path}")
        elif analysis_type == "summary":
            return await service.generate_summary(code, f"File: {file_path}")
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")


# Convenience functions for easy integration
async def get_semantic_analysis(code: str, file_path: str, language: str, 
                               config: Dict[str, Any]) -> SemanticAnalysis:
    """Get semantic analysis for code."""
    manager = AIServiceManager(config)
    return await manager.analyze_with_ai(code, file_path, language, "semantic")


async def get_pattern_analysis(code: str, language: str, 
                              config: Dict[str, Any]) -> PatternAnalysis:
    """Get pattern analysis for code."""
    manager = AIServiceManager(config)
    return await manager.analyze_with_ai(code, "", language, "patterns")


async def get_quality_assessment(code: str, file_path: str, 
                                config: Dict[str, Any]) -> QualityAssessment:
    """Get quality assessment for code."""
    manager = AIServiceManager(config)
    return await manager.analyze_with_ai(code, file_path, "", "quality")


async def get_ai_summary(code: str, file_path: str, 
                        config: Dict[str, Any]) -> str:
    """Get AI-generated summary for code."""
    manager = AIServiceManager(config)
    return await manager.analyze_with_ai(code, file_path, "", "summary")
