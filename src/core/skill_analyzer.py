"""
Skill Analysis and Reporting Engine

Generates comprehensive skill discovery reports with extraction recommendations
for AIPass-Ecosystem integration.
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from .skill_detector import AdvancedSkillDetector, SkillSignature, SkillModule, SkillCategory

@dataclass
class SkillAnalysisReport:
    """Comprehensive skill analysis report."""
    timestamp: str
    codebase_path: str
    total_files_analyzed: int
    total_skills_detected: int
    skill_modules: List[SkillModule]
    high_priority_skills: List[SkillSignature]
    category_breakdown: Dict[str, int]
    extraction_recommendations: List[Dict[str, Any]]
    integration_roadmap: List[Dict[str, Any]]

class SkillAnalyzer:
    """Advanced skill analysis and reporting engine."""
    
    def __init__(self):
        self.detector = AdvancedSkillDetector()
    
    def analyze_codebase(self, codebase_path: str, output_dir: Optional[str] = None) -> SkillAnalysisReport:
        """Perform comprehensive codebase skill analysis."""
        print(f"🔍 Starting skill analysis of {codebase_path}...")
        
        all_skills = []
        all_modules = []
        files_analyzed = 0
        
        # Supported file extensions
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
        
        # Walk through codebase
        for root, dirs, files in os.walk(codebase_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {
                '.git', '__pycache__', 'node_modules', '.venv', 'venv',
                'build', 'dist', '.next', 'coverage'
            }]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Detect skills in file
                        file_skills = self.detector.detect_skills_in_file(content, file_path)
                        all_skills.extend(file_skills)
                        files_analyzed += 1
                        
                        # Create module if multiple skills
                        if len(file_skills) > 1:
                            module = self.detector.create_skill_module(file_skills, file_path)
                            if module:
                                all_modules.append(module)
                        
                        if files_analyzed % 10 == 0:
                            print(f"📊 Analyzed {files_analyzed} files, found {len(all_skills)} skills...")
                    
                    except Exception as e:
                        print(f"⚠️ Error analyzing {file_path}: {e}")
                        continue
        
        print(f"✅ Analysis complete: {files_analyzed} files, {len(all_skills)} skills detected")
        
        # Generate comprehensive report
        report = self._generate_report(
            codebase_path, files_analyzed, all_skills, all_modules
        )
        
        # Save report if output directory specified
        if output_dir:
            self._save_report(report, output_dir)
        
        return report
    
    def _generate_report(self, codebase_path: str, files_analyzed: int, 
                        skills: List[SkillSignature], modules: List[SkillModule]) -> SkillAnalysisReport:
        """Generate comprehensive skill analysis report."""
        
        # Calculate category breakdown
        category_breakdown = {}
        for skill in skills:
            category_name = skill.category.value
            category_breakdown[category_name] = category_breakdown.get(category_name, 0) + 1
        
        # Identify high-priority skills
        high_priority_skills = [
            skill for skill in skills 
            if skill.extraction_priority > 0.7 and skill.confidence > 0.8
        ]
        high_priority_skills.sort(key=lambda x: x.extraction_priority, reverse=True)
        
        # Generate extraction recommendations
        extraction_recommendations = self._generate_extraction_recommendations(skills, modules)
        
        # Generate integration roadmap
        integration_roadmap = self._generate_integration_roadmap(high_priority_skills)
        
        return SkillAnalysisReport(
            timestamp=datetime.now().isoformat(),
            codebase_path=codebase_path,
            total_files_analyzed=files_analyzed,
            total_skills_detected=len(skills),
            skill_modules=modules,
            high_priority_skills=high_priority_skills[:20],  # Top 20
            category_breakdown=category_breakdown,
            extraction_recommendations=extraction_recommendations,
            integration_roadmap=integration_roadmap
        )
    
    def _generate_extraction_recommendations(self, skills: List[SkillSignature], 
                                           modules: List[SkillModule]) -> List[Dict[str, Any]]:
        """Generate skill extraction recommendations."""
        recommendations = []
        
        # Group skills by category for analysis
        category_groups = {}
        for skill in skills:
            category = skill.category.value
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(skill)
        
        # Generate recommendations per category
        for category, category_skills in category_groups.items():
            if len(category_skills) >= 3:  # Only recommend if sufficient skills
                top_skills = sorted(category_skills, 
                                  key=lambda x: x.extraction_priority, reverse=True)[:5]
                
                recommendations.append({
                    "category": category,
                    "priority": "high" if category in ["ai_tools", "api_integration"] else "medium",
                    "skill_count": len(category_skills),
                    "top_skills": [skill.name for skill in top_skills],
                    "extraction_effort": self._estimate_extraction_effort(top_skills),
                    "integration_value": self._estimate_integration_value(category, top_skills),
                    "recommended_action": self._get_recommended_action(category, top_skills)
                })
        
        # Sort by priority and integration value
        recommendations.sort(key=lambda x: (
            x["priority"] == "high",
            x["integration_value"]
        ), reverse=True)
        
        return recommendations
    
    def _generate_integration_roadmap(self, high_priority_skills: List[SkillSignature]) -> List[Dict[str, Any]]:
        """Generate step-by-step integration roadmap."""
        roadmap = []
        
        # Phase 1: Quick wins (low complexity, high value)
        phase1_skills = [
            skill for skill in high_priority_skills
            if skill.complexity == "low" and skill.category in [
                SkillCategory.FILE_OPERATIONS, SkillCategory.UTILITY_FUNCTIONS
            ]
        ][:5]
        
        if phase1_skills:
            roadmap.append({
                "phase": 1,
                "title": "Quick Wins - Basic Utilities",
                "duration": "1-2 weeks",
                "skills": [skill.name for skill in phase1_skills],
                "description": "Extract simple, reusable utility functions",
                "effort": "low",
                "value": "medium"
            })
        
        # Phase 2: Core integrations (medium complexity, high value)
        phase2_skills = [
            skill for skill in high_priority_skills
            if skill.category in [SkillCategory.API_FRAMEWORKS, SkillCategory.CLI_OPERATIONS]
        ][:5]
        
        if phase2_skills:
            roadmap.append({
                "phase": 2,
                "title": "Core Integrations - APIs & CLI",
                "duration": "2-4 weeks",
                "skills": [skill.name for skill in phase2_skills],
                "description": "Extract API and command-line interface skills",
                "effort": "medium",
                "value": "high"
            })
        
        # Phase 3: Advanced features (high complexity, high value)
        phase3_skills = [
            skill for skill in high_priority_skills
            if skill.category in [SkillCategory.NATURAL_LANGUAGE, SkillCategory.MCP_INTEGRATION, SkillCategory.PROMPT_ENGINEERING]
        ][:5]
        
        if phase3_skills:
            roadmap.append({
                "phase": 3,
                "title": "Advanced Features - AI & Data",
                "duration": "3-6 weeks",
                "skills": [skill.name for skill in phase3_skills],
                "description": "Extract AI tools and data processing capabilities",
                "effort": "high",
                "value": "very_high"
            })
        
        return roadmap
    
    def _estimate_extraction_effort(self, skills: List[SkillSignature]) -> str:
        """Estimate effort required to extract skills."""
        avg_complexity = sum(1 for skill in skills if skill.complexity == "high") / len(skills)
        avg_dependencies = sum(len(skill.dependencies) for skill in skills) / len(skills)
        
        if avg_complexity > 0.5 or avg_dependencies > 3:
            return "high"
        elif avg_complexity > 0.2 or avg_dependencies > 1:
            return "medium"
        else:
            return "low"
    
    def _estimate_integration_value(self, category: str, skills: List[SkillSignature]) -> float:
        """Estimate integration value for AIPass ecosystem."""
        base_values = {
            "ai_tools": 0.9,
            "api_integration": 0.8,
            "file_operations": 0.7,
            "cli_commands": 0.7,
            "data_processing": 0.6,
            "utility_functions": 0.5
        }
        
        base_value = base_values.get(category, 0.4)
        
        # Adjust based on skill quality
        avg_confidence = sum(skill.confidence for skill in skills) / len(skills)
        avg_reusability = sum(skill.reusability for skill in skills) / len(skills)
        
        return min(base_value * (avg_confidence + avg_reusability) / 2, 1.0)
    
    def _get_recommended_action(self, category: str, skills: List[SkillSignature]) -> str:
        """Get recommended action for skill category."""
        actions = {
            "ai_tools": "Extract immediately - high value for AI agents",
            "api_integration": "Extract for reusable API clients",
            "file_operations": "Extract as core utility modules",
            "cli_commands": "Extract for command automation",
            "data_processing": "Extract for data pipeline components",
            "utility_functions": "Extract as helper libraries"
        }
        
        return actions.get(category, "Evaluate for potential extraction")
    
    def _save_report(self, report: SkillAnalysisReport, output_dir: str):
        """Save skill analysis report to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON report
        json_path = os.path.join(output_dir, "skill_analysis_report.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        
        # Save Markdown summary
        md_path = os.path.join(output_dir, "SKILL_DISCOVERY_REPORT.md")
        self._save_markdown_report(report, md_path)
        
        print(f"📋 Reports saved:")
        print(f"   📄 JSON: {json_path}")
        print(f"   📝 Markdown: {md_path}")
    
    def _save_markdown_report(self, report: SkillAnalysisReport, file_path: str):
        """Save human-readable Markdown report."""
        content = f"""# Skill Discovery Report

**Generated:** {report.timestamp}  
**Codebase:** `{report.codebase_path}`  
**Files Analyzed:** {report.total_files_analyzed}  
**Skills Detected:** {report.total_skills_detected}

## Executive Summary

This codebase contains **{report.total_skills_detected} extractable skills** across {len(report.category_breakdown)} categories. 
**{len(report.high_priority_skills)} high-priority skills** have been identified for immediate extraction.

## Category Breakdown

| Category | Skills | Priority |
|----------|---------|----------|
"""
        
        # Add category breakdown
        priority_categories = {"ai_tools", "api_integration", "file_operations"}
        for category, count in sorted(report.category_breakdown.items(), key=lambda x: x[1], reverse=True):
            priority = "🔥 High" if category in priority_categories else "📋 Medium"
            content += f"| {category.replace('_', ' ').title()} | {count} | {priority} |\n"
        
        content += f"""
## High-Priority Skills ({len(report.high_priority_skills)})

These skills are recommended for immediate extraction:

"""
        
        # Add high-priority skills
        for i, skill in enumerate(report.high_priority_skills[:10], 1):
            content += f"{i}. **{skill.name}** ({skill.category.value})\n"
            content += f"   - File: `{skill.file_path}`\n"
            content += f"   - Confidence: {skill.confidence:.1%} | Priority: {skill.extraction_priority:.1%}\n"
            content += f"   - {skill.description}\n\n"
        
        content += "## Extraction Recommendations\n\n"
        
        # Add recommendations
        for i, rec in enumerate(report.extraction_recommendations, 1):
            content += f"### {i}. {rec['category'].replace('_', ' ').title()}\n\n"
            content += f"- **Priority:** {rec['priority'].title()}\n"
            content += f"- **Skills Available:** {rec['skill_count']}\n"
            content += f"- **Extraction Effort:** {rec['extraction_effort'].title()}\n"
            content += f"- **Integration Value:** {rec['integration_value']:.1%}\n"
            content += f"- **Action:** {rec['recommended_action']}\n\n"
            content += "**Top Skills:**\n"
            for skill in rec['top_skills']:
                content += f"- {skill}\n"
            content += "\n"
        
        content += "## Integration Roadmap\n\n"
        
        # Add roadmap
        for phase in report.integration_roadmap:
            content += f"### Phase {phase['phase']}: {phase['title']}\n\n"
            content += f"- **Duration:** {phase['duration']}\n"
            content += f"- **Effort:** {phase['effort'].title()}\n"
            content += f"- **Value:** {phase['value'].replace('_', ' ').title()}\n"
            content += f"- **Description:** {phase['description']}\n\n"
            content += "**Skills to Extract:**\n"
            for skill in phase['skills']:
                content += f"- {skill}\n"
            content += "\n"
        
        content += """
---
*Generated by AIPass-Code-Sniffer Skill Discovery Engine*
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
