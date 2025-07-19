#!/usr/bin/env python3
"""
Setup script for AI-Enhanced Code Sniffer Phase 3.

This script helps set up the AI services and dependencies needed for
semantic analysis capabilities.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_dependencies():
    """Install required Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_node_dependencies():
    """Check Node.js and TypeScript dependencies."""
    print("\n🔍 Checking Node.js dependencies...")
    
    try:
        # Check Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
        else:
            print("❌ Node.js not found")
            return False
        
        # Check TypeScript
        result = subprocess.run(["npx", "tsc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ TypeScript {result.stdout.strip()} detected")
        else:
            print("⚠️ TypeScript not found, installing...")
            subprocess.check_call(["npm", "install", "-g", "typescript"])
        
        return True
    except Exception as e:
        print(f"❌ Node.js dependency check failed: {e}")
        return False


def setup_environment_file():
    """Create .env file template for API keys."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    print("\n🔑 Setting up environment configuration...")
    
    # Create .env.example
    env_example_content = """# AI Service API Keys
# Get your API keys from:
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/

OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Set preferred AI service
PREFERRED_AI_SERVICE=openai

# Optional: Set analysis level (basic, enhanced, premium)
DEFAULT_ANALYSIS_LEVEL=enhanced
"""
    
    with open(env_example, 'w') as f:
        f.write(env_example_content)
    print("✅ Created .env.example file")
    
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_example_content)
        print("✅ Created .env file (please add your API keys)")
    else:
        print("ℹ️ .env file already exists")
    
    return True


def test_basic_functionality():
    """Test basic functionality without AI services."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test CLI interface
        result = subprocess.run([
            sys.executable, "src/cli/main.py", "--help"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI interface working")
        else:
            print("❌ CLI interface test failed")
            return False
        
        # Test TypeScript analyzer
        test_file = "src/cli/main.py"  # Use Python file for basic test
        result = subprocess.run([
            sys.executable, "-c", 
            f"import sys; sys.path.insert(0, 'src'); "
            f"from core.dependency_visualizer import analyze_python_dependencies; "
            f"result = analyze_python_dependencies('{test_file}'); "
            f"print('✅ Basic analysis working:', len(result.get('imports', [])), 'imports found')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("❌ Basic analysis test failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_ai_services():
    """Test AI services if API keys are available."""
    print("\n🤖 Testing AI services...")
    
    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("⚠️ No AI API keys found in environment")
        print("   Add your API keys to .env file to enable AI features")
        return True  # Not a failure, just no AI services available
    
    try:
        # Test AI service initialization
        test_code = """
import sys
import os
sys.path.insert(0, 'src')
from core.ai_services import AIServiceManager

config = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "models": {"summarization": "gpt-4o-mini", "analysis": "gpt-4"}
    }
}

manager = AIServiceManager(config)
service = manager.get_service()
if service:
    print("✅ AI service initialized successfully")
else:
    print("⚠️ No AI services available (check API keys)")
"""
        
        result = subprocess.run([
            sys.executable, "-c", test_code
        ], capture_output=True, text=True)
        
        print(result.stdout.strip() if result.stdout else "AI service test completed")
        return True
        
    except Exception as e:
        print(f"⚠️ AI service test failed: {e}")
        return True  # Not critical for basic functionality


def create_test_analysis():
    """Create a test analysis to verify everything works."""
    print("\n📊 Creating test analysis...")
    
    try:
        # Test with a TypeScript file from research
        test_file = "research/code_sources/DesktopCommanderMCP-main/src/index.ts"
        
        if not os.path.exists(test_file):
            print("⚠️ Test TypeScript file not found, skipping test analysis")
            return True
        
        # Run enhanced analysis
        result = subprocess.run([
            sys.executable, "src/analyzers/typescript/semantic_analyzer.py", 
            test_file, "enhanced"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Test analysis completed successfully")
            if "Enhanced_AbilityCard_" in result.stdout:
                print("✅ Enhanced ability card generated")
        else:
            print("⚠️ Test analysis had issues (this is expected without AI API keys)")
            print("   Basic functionality should still work")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Test analysis failed: {e}")
        return True  # Not critical


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("🎉 AI-Enhanced Code Sniffer Setup Complete!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Add your AI API keys to the .env file:")
    print("   - OpenAI API key: https://platform.openai.com/api-keys")
    print("   - Anthropic API key: https://console.anthropic.com/")
    
    print("\n2. Test the enhanced analyzer:")
    print("   python src/cli/main.py extract [path] --analysis-level enhanced")
    
    print("\n3. Try the new semantic analysis:")
    print("   python src/analyzers/typescript/semantic_analyzer.py [typescript_file] premium")
    
    print("\n4. Available analysis levels:")
    print("   - basic: Syntax and dependencies only")
    print("   - enhanced: Basic + AI summaries")
    print("   - premium: Full AI analysis (semantic, patterns, quality)")
    
    print("\n5. Configuration:")
    print("   - Edit config/ai_config.json to customize AI settings")
    print("   - Edit .env to set API keys and preferences")
    
    print("\n🚀 Ready for Phase 3 semantic enhancement!")


def main():
    """Main setup function."""
    print("🔧 Setting up AI-Enhanced Code Sniffer (Phase 3)")
    print("="*50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install dependencies
    if success and not install_dependencies():
        success = False
    
    # Check Node.js dependencies
    if success and not check_node_dependencies():
        success = False
    
    # Setup environment
    if success and not setup_environment_file():
        success = False
    
    # Test basic functionality
    if success and not test_basic_functionality():
        success = False
    
    # Test AI services (non-critical)
    test_ai_services()
    
    # Create test analysis (non-critical)
    create_test_analysis()
    
    if success:
        print_next_steps()
    else:
        print("\n❌ Setup encountered errors. Please check the output above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
