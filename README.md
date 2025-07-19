# AIPass-Code-Sniffer

AI-powered semantic code analysis tool that provides intelligent understanding of codebases.

## Features

- **AI-Enhanced Analysis**: Semantic understanding, business context, and quality assessment
- **Multi-Language Support**: Python and TypeScript/JavaScript
- **Three Analysis Levels**: Basic → Enhanced → Premium
- **Quality Scoring**: Objective 0-10 scoring with recommendations
- **Pattern Recognition**: Architectural and design pattern detection

## 🚀 **Installation & Setup**

### **1. Clone & Navigate**
```bash
# Clone the repository
git clone https://github.com/your-username/AIPass-Code-Sniffer.git
cd AIPass-Code-Sniffer

# Or if you already have it
cd C:\AIPass-Code-Sniffer  # Windows
cd /path/to/AIPass-Code-Sniffer  # Linux/Mac
```

### **2. Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for TypeScript analysis)
npm install

# Verify installation
python --version  # Should be 3.8+
node --version    # Should be 14+
```

### **3. Environment Setup** (Optional - Only for AI Analysis)
```bash
# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here
set ANTHROPIC_API_KEY=your-anthropic-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
$env:ANTHROPIC_API_KEY="your-anthropic-key-here"

# Linux/Mac (Bash)
export OPENAI_API_KEY="your-api-key-here"
export ANTHROPIC_API_KEY="your-anthropic-key-here"

# Or create .env file in project root
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "ANTHROPIC_API_KEY=your-anthropic-key-here" >> .env
```

### **4. Quick Test**
```bash
# Test the CLI (should show help)
python src/cli/main.py --help

# Test skill discovery (no API key needed)
python src/cli/main.py discover-skills . --output ./test_output

# Check if it worked
ls ./test_output  # Linux/Mac
dir .\test_output  # Windows
```

## 🚀 **CLI Commands**

### **1. Skill Discovery** (Recommended - Zero Cost)
```bash
# Discover all extractable skills in codebase
python src/cli/main.py discover-skills [PATH] [OPTIONS]

# Options:
--output, -o     Output directory (default: ./output/skill_reports)

# Examples:
python src/cli/main.py discover-skills .                    # Current directory
python src/cli/main.py discover-skills /path/to/project     # Specific project
python src/cli/main.py discover-skills . -o ./my_reports    # Custom output
```
**Output**: Category-based skill catalog with clickable file links, zero token usage

### **2. AI-Enhanced Analysis** (Requires API Key)
```bash
# Analyze with AI-powered semantic understanding
python src/cli/main.py analyze [PATH] [OPTIONS]

# Options:
--level, -l      Analysis level: basic|enhanced|premium (default: enhanced)
--output, -o     Output directory (default: ./output/ability_cards)
--budget, -b     Token budget limit (e.g., 20000)
--sample, -s     Sample percentage (e.g., "10%" or "50")
--incremental, -i Skip already analyzed files
--skills, -sk    Include skill detection

# Examples:
python src/cli/main.py analyze file.py --level premium     # Single file, full AI
python src/cli/main.py analyze . --level basic            # Basic syntax only
python src/cli/main.py analyze . --budget 10000          # With token limit
python src/cli/main.py analyze . --sample "25%"          # Sample 25% of files
```
**Output**: Detailed ability cards with AI insights, token usage tracking

### **3. Dependency Visualization**
```bash
# Generate dependency graphs
python src/cli/main.py visualize [PATH] [OPTIONS]

# Options:
--output, -o     Output directory (default: ./output/dependency_graphs)

# Examples:
python src/cli/main.py visualize .                        # Current directory
python src/cli/main.py visualize /path/to/project         # Specific project
```
**Output**: Dependency graphs and analysis reports

### **4. Index Management**
```bash
# Update abilities index
python src/cli/main.py index [OPTIONS]

# Options:
--directory, -d  Directory with ability cards (default: ./output/ability_cards)

# Examples:
python src/cli/main.py index                              # Default directory
python src/cli/main.py index -d ./custom/cards           # Custom directory
```
**Output**: Updated index files for ability cards

### **5. Legacy Commands**
```bash
# Legacy extract command (redirects to analyze)
python src/cli/main.py extract [PATH] [OPTIONS]           # Use 'analyze' instead
```

## 📊 **Analysis Levels**

| Level | Description | Cost | Use Case |
|-------|-------------|------|----------|
| **`basic`** | Fast syntax analysis | FREE | Quick overview, large codebases |
| **`enhanced`** | AI summaries + insights | ~$0.0008/file | Balanced analysis |
| **`premium`** | Full AI semantic analysis | ~$0.002/file | Deep understanding |

## 📁 **Output Types**

### **Skill Discovery Reports** (`discover-skills`)
```
output/skill_reports/
├── SKILL_DISCOVERY_REPORT.md    # Category-based overview with file links
├── skill_analysis.json          # Structured skill data
└── summary_stats.txt            # Quick statistics
```

### **AI-Enhanced Ability Cards** (`analyze`)
```
output/ability_cards/[PROJECT]_[TIMESTAMP]/
├── Enhanced_AbilityCard_[file].md    # AI-powered analysis
├── analysis_summary.json            # Token usage & costs
└── index.md                         # Navigation index
```

### **Dependency Graphs** (`visualize`)
```
output/dependency_graphs/
├── dependency_graph.json
├── dependency_report.md
└── visualization.html
```

## 💡 **Usage Examples**

### **Quick Skill Overview** (Recommended First Step)
```bash
# Get zero-cost overview of all skills in your codebase
python src/cli/main.py discover-skills . --output ./reports

# Output: Clean category-based report with direct file links
# Cost: $0 (no AI tokens used)
# Time: ~30 seconds for 200 files
```

### **Deep AI Analysis** (When You Need Details)
```bash
# Analyze specific high-value files with AI
python src/cli/main.py analyze src/core/important_module.py --level premium

# Output: Detailed ability card with business context, quality scoring
# Cost: ~$0.002 per file
# Time: ~10 seconds per file
```

### **Budget-Controlled Analysis**
```bash
# Analyze with token budget to control costs
python src/cli/main.py analyze . --budget 50000 --sample "10%"

# Output: AI analysis of 10% sample within budget
# Cost: Capped at ~$0.10 (50k tokens)
# Time: Varies based on sample size
```

## 💻 **Complete Terminal Guide**

### **Basic Workflow - Start Here**
```bash
# 1. Navigate to your project
cd C:\AIPass-Code-Sniffer

# 2. Get overview of your codebase (FREE)
python src/cli/main.py discover-skills . --output ./reports

# 3. View the results
# Windows:
notepad .\reports\SKILL_DISCOVERY_REPORT.md
# Linux/Mac:
cat ./reports/SKILL_DISCOVERY_REPORT.md

# 4. (Optional) AI analysis of specific files
python src/cli/main.py analyze src/core/important_file.py --level enhanced
```

### **Analyze Different Project Types**
```bash
# Analyze current directory
python src/cli/main.py discover-skills .

# Analyze specific project folder
python src/cli/main.py discover-skills C:\path\to\your\project
python src/cli/main.py discover-skills /home/user/my-project

# Analyze with custom output location
python src/cli/main.py discover-skills . --output C:\MyReports
python src/cli/main.py discover-skills . --output ~/my-reports
```

### **AI Analysis Examples**
```bash
# Single file analysis (detailed)
python src/cli/main.py analyze myfile.py --level premium
python src/cli/main.py analyze src/utils/helper.js --level enhanced

# Whole project with budget control
python src/cli/main.py analyze . --level enhanced --budget 20000

# Sample analysis (10% of files)
python src/cli/main.py analyze . --sample "10%" --level enhanced

# Incremental analysis (skip already analyzed)
python src/cli/main.py analyze . --incremental --level basic
```

### **View Results**
```bash
# View skill discovery report
# Windows:
type .\output\skill_reports\SKILL_DISCOVERY_REPORT.md
start .\output\skill_reports\SKILL_DISCOVERY_REPORT.md

# Linux/Mac:
cat ./output/skill_reports/SKILL_DISCOVERY_REPORT.md
less ./output/skill_reports/SKILL_DISCOVERY_REPORT.md

# View AI analysis results
# Windows:
dir .\output\ability_cards
start .\output\ability_cards

# Linux/Mac:
ls ./output/ability_cards
open ./output/ability_cards
```

### **Troubleshooting Commands**
```bash
# Check if Python is working
python --version
python -c "import sys; print(sys.path)"

# Check if dependencies are installed
pip list | grep openai
npm list typescript

# Test CLI without running analysis
python src/cli/main.py --help
python src/cli/main.py discover-skills --help
python src/cli/main.py analyze --help

# Check environment variables
# Windows:
echo %OPENAI_API_KEY%
# Linux/Mac:
echo $OPENAI_API_KEY

# Run with debug output
python -v src/cli/main.py discover-skills . --output ./debug_test
```

### **Common Use Cases**
```bash
# 1. Quick project overview (most common)
python src/cli/main.py discover-skills . --output ./project_overview

# 2. Analyze specific high-value files
python src/cli/main.py analyze src/core/ --level premium

# 3. Budget-controlled full analysis
python src/cli/main.py analyze . --budget 50000 --sample "20%"

# 4. Generate dependency graphs
python src/cli/main.py visualize . --output ./dependencies

# 5. Update analysis index
python src/cli/main.py index --directory ./output/ability_cards
```

## Archive

Project documentation and development materials are archived in `archive/` folder.
