# AIPass-Code-Sniffer

**Automated codebase analysis and ability extraction tools with semantic understanding**

[![Quality Assessment](https://img.shields.io/badge/Quality-4%2F10-orange)](./QUALITY_ASSESSMENT.md)
[![Development Phase](https://img.shields.io/badge/Phase-3%20Semantic%20Enhancement-blue)](./ROADMAP.md)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8%2B-blue)](https://typescriptlang.org)

## Overview

AIPass-Code-Sniffer is a sophisticated codebase analysis framework designed to automatically extract, document, and visualize code abilities with the goal of matching or exceeding manual AI-assisted analysis quality. The project aims to provide semantic understanding, architectural insights, and business context recognition equivalent to direct AI code interpretation.

## 🎯 Project Goals

### Primary Objective
**Match Manual AI Analysis Quality**: Achieve semantic understanding, architectural insights, and business context recognition equivalent to direct AI code interpretation.

### Core Capabilities (Target)
- **Semantic Understanding**: Recognize code purpose, business domain, and architectural patterns
- **Pattern Recognition**: Detect React patterns, state management, safety systems, and design principles  
- **Quality Assessment**: Evaluate reusability, design patterns, and code quality metrics
- **Business Context**: Identify whether code represents AI tools, web frameworks, CLI utilities, etc.
- **Cross-file Analysis**: Understand component hierarchies, data flow, and architectural relationships

## 📊 Current Status

**Quality Level**: 4/10 (40% of target capability)

### ✅ Current Strengths
- **Rapid Discovery**: Fast function and class extraction (1000+ files in minutes)
- **Consistent Output**: Standardized documentation format
- **Multi-language Support**: Python, TypeScript, JavaScript analysis
- **Dependency Visualization**: DOT format graphs with local/external distinction
- **Scalability**: Handles large codebases efficiently

### ❌ Critical Limitations
- **No Semantic Understanding**: Cannot identify code purpose or business domain
- **Missing Pattern Recognition**: Ignores React patterns, architectural styles
- **Limited Type Analysis**: Surface-level TypeScript understanding only
- **No Business Context**: Cannot recognize AI tools vs web frameworks
- **No Quality Assessment**: Missing design pattern and reusability evaluation

*Based on comprehensive comparison with manual AI analysis of gemini-cli codebase*

## 🏗️ Project Structure

```
AIPass-Code-Sniffer/
├── README.md                    # This file
├── ROADMAP.md                   # Development roadmap and timeline
├── QUALITY_ASSESSMENT.md        # Detailed quality analysis report
├── SESSION_DIARY.md             # Development progress log
├── GEMINI.md                    # AI assistant context
│
├── src/                        # Main source code
│   ├── core/                   # Core analysis engines
│   │   ├── ability_extractor.py
│   │   ├── dependency_visualizer.py
│   │   ├── code_summarizer.py
│   │   └── tech_stack_detector.py
│   │
│   ├── analyzers/              # Language-specific analyzers
│   │   ├── typescript/
│   │   │   ├── ts_analyzer_cli.js
│   │   │   └── ts_analyzer.js
│   │   ├── python/
│   │   └── common/
│   │
│   ├── utils/                  # Utility modules
│   │   ├── project_mapper.py
│   │   └── index_updater.py
│   │
│   └── cli/                    # Command-line interface
│       ├── main.py
│       └── commands/
│
├── output/                     # Generated analysis outputs
│   ├── ability_cards/          # Generated ability cards
│   ├── dependency_graphs/      # DOT files and visualizations
│   └── reports/               # Analysis reports
│
├── research/                   # Research and reference materials
│   ├── code_sources/          # Research codebases (gemini-cli, etc.)
│   ├── benchmarks/            # Quality benchmarks
│   └── analysis_samples/      # Manual analysis examples
│
├── docs/                       # Documentation
│   ├── PROJECT_STRUCTURE.md   # Detailed structure documentation
│   ├── RESEARCH_PLAN.md       # Research methodology
│   └── TOOL_IDEAS.md          # Future enhancement ideas
│
├── config/                     # Configuration files
│   └── templates/             # Template files
│
└── scripts/                    # Build and utility scripts
    └── build/                 # Build artifacts
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** with TypeScript support
- **Git** for version control

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIPass-Code-Sniffer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt  # (when created)
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

### Basic Usage

```bash
# Extract abilities from a codebase
python src/cli/main.py extract /path/to/codebase --output ./output/ability_cards

# Generate dependency visualization
python src/cli/main.py visualize /path/to/codebase --output ./output/dependency_graphs

# Update abilities index
python src/cli/main.py index --analysis-dir ./output/ability_cards
```

### Example Analysis

```bash
# Analyze a TypeScript project
python src/cli/main.py extract ./research/code_sources/gemini-cli-main

# View generated ability cards
ls output/ability_cards/

# Generate dependency graph
python src/cli/main.py visualize ./research/code_sources/gemini-cli-main
```

## 📈 Development Roadmap

### Phase 3: Semantic Enhancement (Current - 4-6 weeks)
- [ ] **Enhanced TypeScript Analyzer**: Add semantic analysis beyond syntax parsing
- [ ] **Pattern Recognition System**: Detect React patterns, state management, architectural styles
- [ ] **Business Context Analysis**: Identify code domains (AI tools, web frameworks, CLI utilities)
- [ ] **Cross-file Relationship Analysis**: Understand component hierarchies and data flow
- [ ] **Quality Assessment Module**: Evaluate design patterns, reusability, and best practices

### Phase 4: Advanced Analysis (6-8 weeks)
- [ ] Architecture pattern detection (MVC, MVVM, Component-based)
- [ ] User experience workflow analysis
- [ ] Security pattern recognition
- [ ] Advanced type system analysis

### Phase 5: Advanced Features (8-12 weeks)
- [ ] Multi-language expansion (Go, Rust, Java)
- [ ] Real-time analysis capabilities
- [ ] Web-based visualization interface
- [ ] IDE integration plugins

## 📊 Quality Benchmark

Our quality standard is based on comprehensive analysis of the [gemini-cli](./research/code_sources/gemini-cli-main) research documentation, which demonstrates:

**Architecture Analysis:**
- Modular design recognition (CLI vs Core package separation)
- Tool ecosystem mapping (15+ specialized tools with purpose and security considerations)
- Safety-first architecture with sophisticated approval pipelines

**Pattern Recognition:**
- React terminal UI using Ink framework
- Advanced text buffer with Unicode support and undo/redo
- Custom patch format parser for structured code modifications
- Command safety assessment with multiple validation layers

**Business Context:**
- Clear identification as AI coding assistant
- Understanding of terminal UI paradigms, confirmation workflows, sandboxing
- Recognition of TypeScript best practices and testing strategies

## 🔬 Research Materials

The `research/code_sources/` directory contains reference codebases used for quality benchmarking:

- **gemini-cli-main**: Primary quality benchmark (AI coding assistant)
- **codex-main**: Test codebase for analysis validation
- **DesktopCommanderMCP-main**: TypeScript analysis validation
- **Additional projects**: Various AI tools and frameworks for pattern recognition

## 🤝 Contributing

### Development Setup

1. **Set up development environment**
   ```bash
   # Install development dependencies
   pip install -r requirements-dev.txt  # (when created)
   
   # Install pre-commit hooks
   pre-commit install  # (when configured)
   ```

2. **Run tests**
   ```bash
   python -m pytest tests/  # (when created)
   ```

3. **Code quality checks**
   ```bash
   # Type checking
   pyright src/
   
   # Linting
   flake8 src/
   ```

### Enhancement Priorities

Based on our quality assessment, contributions are most needed in:

1. **Semantic Analysis**: Adding business context and purpose recognition
2. **Pattern Recognition**: Implementing React, architectural, and design pattern detection
3. **Type System Analysis**: Enhancing TypeScript understanding beyond basic parsing
4. **Quality Assessment**: Creating design pattern and code quality evaluation
5. **Cross-file Analysis**: Building component relationship and data flow understanding

## 📚 Documentation

- **[ROADMAP.md](./ROADMAP.md)**: Detailed development phases and timeline
- **[QUALITY_ASSESSMENT.md](./QUALITY_ASSESSMENT.md)**: Comprehensive quality analysis and gap identification
- **[SESSION_DIARY.md](./SESSION_DIARY.md)**: Development progress and technical decisions
- **[docs/PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)**: Detailed project organization
- **[docs/RESEARCH_PLAN.md](./docs/RESEARCH_PLAN.md)**: Research methodology and approach

## 🎯 Success Metrics

**Target Quality Rating**: 8-10/10 (equal to or better than manual AI analysis)

**Key Performance Indicators**:
- **Semantic Understanding**: 90% accuracy in purpose and domain identification
- **Pattern Recognition**: 85% accuracy in architectural pattern detection  
- **Documentation Completeness**: 80% reduction in manual completion required
- **Analysis Speed**: Maintain sub-minute analysis for medium codebases (100-500 files)

## 📄 License

[License information to be added]

## 🙏 Acknowledgments

- **Gemini CLI Team**: For providing the quality benchmark through their comprehensive documentation
- **Open Source Community**: For the diverse codebases used in research and validation
- **TypeScript Team**: For the compiler API that enables our TypeScript analysis capabilities

---

**Current Status**: The project has completed foundational setup and quality assessment. We're now entering Phase 3 (Semantic Enhancement) to bridge the gap between current capabilities (4/10) and our target quality level (8-10/10).

For detailed progress tracking and technical decisions, see [SESSION_DIARY.md](./SESSION_DIARY.md).
