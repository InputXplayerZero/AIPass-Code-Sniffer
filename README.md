# AIPass-Code-Sniffer

AI-powered semantic code analysis tool that provides intelligent understanding of codebases.

## Features

- **AI-Enhanced Analysis**: Semantic understanding, business context, and quality assessment
- **Multi-Language Support**: Python and TypeScript/JavaScript
- **Three Analysis Levels**: Basic → Enhanced → Premium
- **Quality Scoring**: Objective 0-10 scoring with recommendations
- **Pattern Recognition**: Architectural and design pattern detection

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Set API key
export OPENAI_API_KEY="your-api-key"

# Analyze single file
python src/cli/main.py analyze path/to/file.py --level premium

# Analyze entire codebase
python src/cli/main.py analyze . --level enhanced
```

## Analysis Levels

- **`basic`** - Fast syntax analysis, no AI required
- **`enhanced`** - AI-powered summaries and insights  
- **`premium`** - Full AI analysis with quality scoring and business context

## Output

Generated ability cards are saved to `output/ability_cards/` with comprehensive analysis including:
- Semantic understanding and purpose
- Business context and domain identification
- Quality assessment and recommendations
- Architectural patterns and design insights

## Archive

Project documentation and development materials are archived in `archive/` folder.
