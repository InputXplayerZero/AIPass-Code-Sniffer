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
    """Simple skill catalog organized by category."""
    timestamp: str
    codebase_path: str
    total_files_analyzed: int
    total_skills_detected: int
    skill_modules: List[SkillModule]
    high_priority_skills: List[SkillSignature]
    category_breakdown: Dict[str, int]
    extraction_recommendations: List[Dict[str, Any]]
    integration_roadmap: List[Dict[str, Any]]
    skills_by_category: Dict[str, List[SkillSignature]]

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
        """Generate simple, category-based skill catalog."""
        
        # Calculate category breakdown
        category_breakdown = {}
        for skill in skills:
            category_name = skill.category.value
            category_breakdown[category_name] = category_breakdown.get(category_name, 0) + 1
        
        # Group skills by category for browsing
        skills_by_category = {}
        for skill in skills:
            category_name = skill.category.value
            if category_name not in skills_by_category:
                skills_by_category[category_name] = []
            skills_by_category[category_name].append(skill)
        
        # Sort skills within each category by name for easy browsing
        for category in skills_by_category:
            skills_by_category[category].sort(key=lambda x: x.name)
        
        # No artificial priorities or recommendations - just organize the data
        extraction_recommendations = []
        integration_roadmap = []
        
        return SkillAnalysisReport(
            timestamp=datetime.now().isoformat(),
            codebase_path=codebase_path,
            total_files_analyzed=files_analyzed,
            total_skills_detected=len(skills),
            skill_modules=modules,
            high_priority_skills=[],  # No artificial priorities
            category_breakdown=category_breakdown,
            extraction_recommendations=extraction_recommendations,
            integration_roadmap=integration_roadmap,
            skills_by_category=skills_by_category  # Add for easy browsing
        )
    
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
        """Save simple category-based skill catalog."""
        content = f"""# Skill Catalog

**Generated:** {report.timestamp}  
**Codebase:** `{report.codebase_path}`  
**Files Analyzed:** {report.total_files_analyzed}  
**Skills Detected:** {report.total_skills_detected}

## Skills by Category

Browse skills organized by their primary capability. Click file links to view source code.

"""
        
        # Generate category sections
        for category_name in sorted(report.skills_by_category.keys()):
            skills = report.skills_by_category[category_name]
            if not skills:
                continue
                
            # Category header
            category_display = category_name.replace('_', ' ').title()
            content += f"### {category_display} ({len(skills)} skills)\n\n"
            
            # List all skills in this category
            for skill in skills:
                # Create relative file path for better readability
                rel_path = skill.file_path.replace(report.codebase_path, '').lstrip('\\').lstrip('/')
                
                content += f"- **{skill.name}**\n"
                content += f"  - File: [`{rel_path}`](file:///{skill.file_path})\n"
                content += f"  - Lines: {skill.line_start}-{skill.line_end}\n"
                content += f"  - Confidence: {skill.confidence:.0%}\n"
                if skill.dependencies:
                    content += f"  - Dependencies: {', '.join(skill.dependencies[:3])}\n"
                content += "\n"
            
        
        content += "\n---\n*Generated by AIPass-Code-Sniffer - Simple Skill Catalog*\n"
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
