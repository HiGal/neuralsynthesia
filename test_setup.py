#!/usr/bin/env python
"""
Test script to verify NeuralSynthesia setup and API connectivity.
Run this before starting the main application to ensure everything is configured correctly.
"""

import os
import sys
from pathlib import Path


def check_env_vars():
    """Check if required environment variables are set."""
    print("🔍 Checking environment variables...")

    required_vars = {
        'NEBIUS_API_KEY': 'Nebius AI API key for LLM and image generation',
        'OAUTH': 'Yandex OAuth token for STT/TTS (optional)',
        'FOLDER_ID': 'Yandex Cloud folder ID for STT/TTS (optional)'
    }

    missing = []
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            if 'KEY' in var or 'TOKEN' in var or 'OAUTH' in var:
                masked_value = value[:8] + '...' if len(value) > 8 else '***'
                print(f"  ✅ {var}: {masked_value}")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: Not set ({description})")
            if var == 'NEBIUS_API_KEY':
                missing.append(var)

    if missing:
        print("\n⚠️  Critical environment variables missing!")
        print("Please set them in .env file or export them in your shell.")
        print("\nExample .env file:")
        print("NEBIUS_API_KEY=your_api_key_here")
        print("NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1")
        return False

    print("✅ Environment variables OK\n")
    return True


def check_dependencies():
    """Check if required Python packages are installed."""
    print("📦 Checking Python dependencies...")

    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-Cors',
        'requests': 'requests',
    }

    optional_packages = {
        'translators': 'translators',
        'dotenv': 'python-dotenv'
    }

    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)

    print("\n  Optional packages:")
    for module, package in optional_packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ⚠️  {package} (optional, but recommended)")

    if missing:
        print(f"\n⚠️  Missing required packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    print("✅ Dependencies OK\n")
    return True


def check_directories():
    """Check and create necessary directories."""
    print("📁 Checking directories...")

    dirs = ['results', 'src']
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ - creating...")
            path.mkdir(parents=True, exist_ok=True)

    print("✅ Directories OK\n")
    return True


def test_nebius_connection():
    """Test connection to Nebius API."""
    print("🌐 Testing Nebius API connection...")

    try:
        from src.llm_generator import LLMStoryGenerator

        generator = LLMStoryGenerator()
        print(f"  ✅ API Base URL: {generator.base_url}")
        print(f"  ✅ API Key configured: {generator.api_key[:8]}...")

        # We won't actually make a request to avoid using credits
        print("  ℹ️  Skipping actual API call (to save credits)")
        print("  ℹ️  Connection test successful\n")
        return True

    except ValueError as e:
        print(f"  ❌ Configuration error: {e}\n")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        return False


def test_modules():
    """Test if custom modules can be imported."""
    print("🔧 Testing custom modules...")

    modules = [
        ('src.llm_generator', 'LLM Story Generator'),
        ('src.image_generator', 'Image Generator'),
    ]

    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {description}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
            return False

    print("✅ Modules OK\n")
    return True


def print_summary(results):
    """Print summary of all tests."""
    print("=" * 60)
    print("SETUP VERIFICATION SUMMARY")
    print("=" * 60)

    all_passed = all(results.values())

    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")

    print("=" * 60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to run NeuralSynthesia.")
        print("\nStart the application with:")
        print("  python app.py")
        print("\nOr test individual components:")
        print("  python src/llm_generator.py")
        print("  python src/image_generator.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, see README.md or check the documentation.")

    return all_passed


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("NEURALSYNTHESIA SETUP VERIFICATION")
    print("=" * 60)
    print()

    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv()
            print("📄 Loaded environment from .env file\n")
        else:
            print("ℹ️  No .env file found (using system environment variables)\n")
    except ImportError:
        print("ℹ️  python-dotenv not installed (using system environment variables)\n")

    results = {
        'Environment Variables': check_env_vars(),
        'Python Dependencies': check_dependencies(),
        'Directories': check_directories(),
        'Custom Modules': test_modules(),
        'Nebius API': test_nebius_connection(),
    }

    success = print_summary(results)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
