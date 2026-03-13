"""
Test Environment Variables Script.

Verifies that all required API keys and tokens are properly configured.
Run this script to check your .env configuration before starting the server.

Usage:
    cd backend
    .venv\Scripts\activate
    python test_env.py
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import get_settings


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def check_env_var(name: str, description: str) -> bool:
    """Check if an environment variable is set."""
    value = os.environ.get(name)
    is_set = bool(value and value.strip())
    
    status = "✅ Yes" if is_set else "❌ No"
    preview = f"({value[:10]}...)" if is_set and len(value) > 10 else ""
    
    print(f"  {description}:")
    print(f"    Status: {status} {preview}")
    
    return is_set


def main():
    """Run environment variable checks."""
    print_section("Customer Success Digital FTE - Environment Check")
    
    # Load settings (this will also export to environment)
    try:
        print("\n  Loading configuration from .env...")
        settings = get_settings()
        print("  ✅ Configuration loaded successfully")
    except Exception as e:
        print(f"  ❌ Error loading configuration: {e}")
        print("\n  Make sure .env file exists in the backend directory.")
        return 1
    
    # Force export to environment
    settings.export_to_environment()
    
    # Check AI Provider Keys
    print_section("AI Provider Configuration")
    
    gemini_ok = check_env_var("GEMINI_API_KEY", "Gemini Key Detected")
    openrouter_ok = check_env_var("OPENROUTER_API_KEY", "OpenRouter Key Detected")
    openai_ok = check_env_var("OPENAI_API_KEY", "OpenAI Key Detected")
    
    # Check Channel Integration Keys
    print_section("Channel Integration Configuration")
    
    whatsapp_ok = check_env_var("ULTRAMSG_INSTANCE_ID", "WhatsApp Instance ID Detected")
    whatsapp_token_ok = check_env_var("ULTRAMSG_TOKEN", "WhatsApp Token Detected")
    gmail_ok = check_env_var("GMAIL_CLIENT_ID", "Gmail Client ID Detected")
    gmail_secret_ok = check_env_var("GMAIL_CLIENT_SECRET", "Gmail Secret Detected")
    
    # Check Other Services
    print_section("Other Services Configuration")
    
    context7_ok = check_env_var("CONTEXT7_API_KEY", "Context7 API Key Detected")
    database_ok = check_env_var("DATABASE_URL", "Database URL Detected")
    
    # Summary
    print_section("Summary")
    
    all_checks = [
        ("Gemini API Key", gemini_ok),
        ("OpenRouter API Key", openrouter_ok),
        ("WhatsApp Instance ID", whatsapp_ok),
        ("WhatsApp Token", whatsapp_token_ok),
        ("Gmail Client ID", gmail_ok),
        ("Gmail Client Secret", gmail_secret_ok),
        ("Context7 API Key", context7_ok),
        ("Database URL", database_ok),
    ]
    
    passed = sum(1 for _, ok in all_checks if ok)
    total = len(all_checks)
    
    print(f"\n  Checks Passed: {passed}/{total}")
    
    for name, ok in all_checks:
        status = "✅" if ok else "❌"
        print(f"    {status} {name}")
    
    # Recommendations
    if not gemini_ok:
        print("\n  ⚠️  WARNING: Gemini API Key is missing!")
        print("     The AI agent will not be able to generate responses.")
        print("     Add GEMINI_API_KEY to your .env file.")
    
    if not whatsapp_ok or not whatsapp_token_ok:
        print("\n  ⚠️  WARNING: WhatsApp configuration is incomplete!")
        print("     WhatsApp notifications will not work.")
        print("     Add ULTRAMSG_INSTANCE_ID and ULTRAMSG_TOKEN to your .env file.")
    
    if not gmail_ok or not gmail_secret_ok:
        print("\n  ⚠️  WARNING: Gmail configuration is incomplete!")
        print("     Gmail integration will not work.")
        print("     Add GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET to your .env file.")
    
    if passed == total:
        print("\n  🎉 All environment variables are configured correctly!")
        print("     You can now start the server with: uvicorn main:app --reload")
    
    print(f"\n{'='*60}\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
