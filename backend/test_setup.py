#!/usr/bin/env python3
"""
Test script to verify the chatbot is working correctly
Run this after setup to check if everything is configured properly
"""

import os
import sys
import requests
import json

def test_api_key():
    """Check if API key is set"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key'")
        return False
    
    if not api_key.startswith('sk-ant-'):
        print("❌ API key format looks incorrect")
        print("   Should start with 'sk-ant-'")
        return False
    
    print("✅ API key is set")
    return True

def test_dependencies():
    """Check if required packages are installed"""
    try:
        import anthropic
        import flask
        import flask_cors
        print("✅ All Python dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def test_knowledge_base():
    """Check if knowledge base files exist"""
    kb_dir = os.path.join(os.path.dirname(__file__), 'knowledge_base')
    if not os.path.exists(kb_dir):
        print("❌ knowledge_base/ directory not found")
        return False
    
    files = [f for f in os.listdir(kb_dir) if not f.startswith('.')]
    if not files:
        print("⚠️  No files in knowledge_base/")
        print("   Add your course materials to knowledge_base/")
        return False
    
    print(f"✅ Found {len(files)} files in knowledge_base/")
    for f in files[:5]:  # Show first 5
        print(f"   - {f}")
    if len(files) > 5:
        print(f"   ... and {len(files) - 5} more")
    return True

def test_backend():
    """Test if backend server is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=2)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"⚠️  Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running")
        print("   Start it with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def test_chat():
    """Test a simple chat interaction"""
    try:
        response = requests.post(
            'http://localhost:5000/chat',
            json={
                'message': 'Hello, can you help me with this course?',
                'history': []
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"   Response preview: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Chat returned error: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing chat: {e}")
        return False

def main():
    print("🦷 Testing Dental Materials Chatbot Setup")
    print("=" * 50)
    print()
    
    tests = [
        ("API Key", test_api_key),
        ("Dependencies", test_dependencies),
        ("Knowledge Base", test_knowledge_base),
        ("Backend Server", test_backend),
        ("Chat Functionality", test_chat),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        print("-" * 50)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed! Your chatbot is ready to use.")
        print()
        print("Next steps:")
        print("1. Open frontend/index.html in a browser")
        print("2. Start asking questions!")
    else:
        print("⚠️  Some tests failed. Review the errors above.")
        print()
        print("Common fixes:")
        print("- Make sure backend is running: python app.py")
        print("- Set API key: export ANTHROPIC_API_KEY='your-key'")
        print("- Install dependencies: pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
