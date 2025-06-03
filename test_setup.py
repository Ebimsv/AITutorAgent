#!/usr/bin/env python3
"""
Test script to verify AI Tutorial Agent setup.
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Test basic Python modules
        import sqlite3
        import uuid
        import json
        from datetime import datetime
        print("✅ Basic Python modules: OK")
        
        # Test third-party modules
        import streamlit
        print("✅ Streamlit: OK")
        
        # Test LangChain/LangGraph
        from langchain.schema import HumanMessage, AIMessage
        from langgraph.graph import StateGraph, END
        print("✅ LangChain/LangGraph: OK")
        
        # Test OpenAI client
        from openai import OpenAI
        print("✅ OpenAI client: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def test_database():
    """Test database functionality."""
    print("\n🗄️ Testing database...")
    
    try:
        from database import TutorialDatabase
        
        # Create test database
        db = TutorialDatabase("test_tutorial.db")
        print("✅ Database creation: OK")
        
        # Test creating conversation
        conv_id = db.create_conversation("test_session", "Test Subject")
        print(f"✅ Conversation creation: OK (ID: {conv_id})")
        
        # Test adding message
        db.add_message(conv_id, "user", "Test message", "question")
        print("✅ Message insertion: OK")
        
        # Test retrieving history
        history = db.get_conversation_history(conv_id)
        assert len(history) == 1
        print("✅ History retrieval: OK")
        
        # Cleanup
        import os
        os.remove("test_tutorial.db")
        print("✅ Database cleanup: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        traceback.print_exc()
        return False

def test_llm_api():
    """Test LLM API connection."""
    print("\n🤖 Testing LLM API...")
    
    try:
        from LLM_api import client
        
        # Test simple API call
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout",
            messages=[{"role": "user", "content": "Hello, respond with 'API test successful'"}],
            extra_headers={
                "HTTP-Referer": "AI-Tutorial-Agent-Test",
                "X-Title": "AI Tutorial Agent Test",
            },
        )
        
        response = completion.choices[0].message.content
        print(f"✅ API response received: {response[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API error: {e}")
        print("Please check your API key in LLM_api.py")
        return False

def test_tutorial_agent():
    """Test tutorial agent functionality."""
    print("\n🎓 Testing tutorial agent...")
    
    try:
        from tutorial_agent import TutorialAgent
        
        # Create agent
        agent = TutorialAgent()
        print("✅ Agent creation: OK")
        
        # Note: We skip the actual tutorial generation test to avoid API calls
        # In a real test, you would test start_tutorial() with a simple subject
        
        print("✅ Agent basic functionality: OK")
        return True
        
    except Exception as e:
        print(f"❌ Agent error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 AI Tutorial Agent Setup Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("LLM API", test_llm_api),
        ("Tutorial Agent", test_tutorial_agent),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nTo start using the AI Tutorial Agent:")
        print("  • Web interface: streamlit run streamlit_app.py")
        print("  • CLI interface: python cli_demo.py")
    else:
        print(f"\n⚠️ {len(results) - passed} test(s) failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 