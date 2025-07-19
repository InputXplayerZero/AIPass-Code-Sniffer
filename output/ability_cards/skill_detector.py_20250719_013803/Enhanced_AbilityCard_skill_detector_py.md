# Enhanced Ability Card: Skill Detector

**File:** `src/core/skill_detector.py`  
**Full Path:** `C:\Source-Codebase\src\core\skill_detector.py`  
**Language:** Python  
**Analysis Level:** Enhanced with AI

## Description

The code implements an **Advanced Skill Detection Engine** designed to analyze code files and identify reusable code modules based on their functionality. It classifies detected skills into various categories, such as CLI operations, file operations, and memory systems, among others. The engine supports both Python and JavaScript/TypeScript files, utilizing Abstract Syntax Tree (AST) parsing for Python and regex for JavaScript detection. Each identified skill is encapsulated in a `SkillSignature` object, which includes metadata like confidence level, description, and function parameters.

The detection process begins by initializing a set of patterns associated with each skill category. When analyzing a file, the engine determines the file type and applies the appropriate detection method. For Python files, it uses AST parsing to traverse the code structure and analyze functions, while for JavaScript, it relies on regex patterns to find function definitions. The classification of functions is based on keyword matching in both the function name and source code, as well as the imports used. The engine also assesses complexity and calculates an extraction priority for each skill, which influences how skills are grouped into `SkillModule` objects.

This architecture is designed for extensibility and accuracy, allowing for comprehensive skill detection across multiple programming languages. By leveraging AST parsing for Python, the engine can achieve a deeper understanding of the code structure compared to simpler text-based methods. The use of categories and confidence scoring facilitates organized skill classification, making it easier to manage and utilize detected skills in larger projects. Overall, the design choices prioritize both robustness in detection and clarity in the resulting skill data, aligning with the goals outlined in the project's plan.

## Technical Details

- **Functions:** 16
- **Classes:** 4
- **Imports:** 14
- **Complexity:** high


## Functions

- **__init__**(self): No description available
- **_init_patterns**(self): Initialize detection patterns.
- **detect_skills_in_file**(self, content, file_path): Detect skills in a file.
- **_detect_python_skills**(self, content, file_path): Detect Python skills using AST.
- **_analyze_function**(self, node, content, file_path): Analyze Python function for skills.
- **_classify_function**(self, func_name, func_source): Classify function into skill category.
- **_extract_parameters**(self, node): Extract function parameters.
- **_get_type_hint**(self, annotation): Extract type hint as string.
- **_extract_dependencies**(self, func_source): Extract function dependencies.
- **_assess_complexity**(self, func_source): Assess function complexity.
- **_generate_description**(self, func_name, category): Generate skill description.
- **_detect_js_skills**(self, content, file_path): Detect JavaScript/TypeScript skills.
- **_classify_js_function**(self, func_name, content): Classify JavaScript function using target skill categories.
- **_regex_detection**(self, content, file_path): Fallback regex-based detection.
- **create_skill_module**(self, skills, file_path): Create skill module from multiple skills.
- **_calculate_extraction_priority**(self, func_name, category, confidence, func_source): Calculate sophisticated extraction priority based on multiple factors.


## Classes

### SkillCategory

Target skill categories aligned with PROJECT_PLAN.md.


### SkillSignature

Detected skill with comprehensive metadata.


### SkillModule

Complete skill module with related functions.


### AdvancedSkillDetector

Advanced skill detection engine.

**Methods:**
- `__init__(self)`
- `_init_patterns(self)`: Initialize detection patterns
- `detect_skills_in_file(self, content, file_path)`: Detect skills in a file
- `_detect_python_skills(self, content, file_path)`: Detect Python skills using AST
- `_analyze_function(self, node, content, file_path)`: Analyze Python function for skills
- `_classify_function(self, func_name, func_source)`: Classify function into skill category
- `_extract_parameters(self, node)`: Extract function parameters
- `_get_type_hint(self, annotation)`: Extract type hint as string
- `_extract_dependencies(self, func_source)`: Extract function dependencies
- `_assess_complexity(self, func_source)`: Assess function complexity
- `_generate_description(self, func_name, category)`: Generate skill description
- `_detect_js_skills(self, content, file_path)`: Detect JavaScript/TypeScript skills
- `_classify_js_function(self, func_name, content)`: Classify JavaScript function using target skill categories
- `_regex_detection(self, content, file_path)`: Fallback regex-based detection
- `create_skill_module(self, skills, file_path)`: Create skill module from multiple skills
- `_calculate_extraction_priority(self, func_name, category, confidence, func_source)`: Calculate sophisticated extraction priority based on multiple factors

---
*Generated by AIPass-Code-Sniffer Enhanced Analyzer*
