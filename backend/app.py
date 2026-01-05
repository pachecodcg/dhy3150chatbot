"""
Dental Materials Course Chatbot Backend
Flask server that handles chat requests and interfaces with Claude API
"""

import os
import anthropic
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
KNOWLEDGE_BASE_DIR = Path(__file__).parent / 'knowledge_base'
INSTRUCTIONS_FILE = Path(__file__).parent / 'instructions.txt'

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def load_instructions():
    """Load the chatbot instructions from file"""
    if INSTRUCTIONS_FILE.exists():
        return INSTRUCTIONS_FILE.read_text()
    return "You are a helpful teaching assistant for a dental materials course."

def load_knowledge_base():
    """Load all course materials from the knowledge_base directory"""
    knowledge_files = []
    
    if not KNOWLEDGE_BASE_DIR.exists():
        KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
        return []
    
    # Support common file types
    supported_extensions = ['.txt', '.md', '.pdf', '.csv']
    
    for file_path in KNOWLEDGE_BASE_DIR.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                # For text-based files, read content directly
                if file_path.suffix.lower() in ['.txt', '.md', '.csv']:
                    content = file_path.read_text(encoding='utf-8')
                    knowledge_files.append({
                        'name': file_path.name,
                        'content': content
                    })
                # For PDFs, you'd need to add PDF processing here
                # For now, just note the file exists
                elif file_path.suffix.lower() == '.pdf':
                    knowledge_files.append({
                        'name': file_path.name,
                        'content': f"[PDF file: {file_path.name}]"
                    })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return knowledge_files

def build_context_message():
    """Build the context message with instructions and knowledge base"""
    instructions = load_instructions()
    knowledge_files = load_knowledge_base()
    
    context = f"{instructions}\n\n"
    
    if knowledge_files:
        context += "# Course Materials Available:\n\n"
        for file_info in knowledge_files:
            context += f"## {file_info['name']}\n{file_info['content']}\n\n"
    
    return context

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests from the frontend
    Expects JSON: { "message": "user question", "history": [] }
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build the context with instructions and knowledge base
        system_context = build_context_message()
        
        # Prepare messages for Claude
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # Add current user message
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # Call Claude API
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=4096,
            system=system_context,
            messages=messages
        )
        
        # Extract the response text
        assistant_message = response.content[0].text
        
        return jsonify({
            'response': assistant_message,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
        })
        
    except anthropic.APIError as e:
        print(f"Anthropic API error: {e}")
        return jsonify({'error': f'API error: {str(e)}'}), 500
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/info', methods=['GET'])
def info():
    """Return information about loaded knowledge base"""
    knowledge_files = load_knowledge_base()
    return jsonify({
        'files_loaded': len(knowledge_files),
        'files': [f['name'] for f in knowledge_files]
    })

if __name__ == '__main__':
    # Check for API key
    if not ANTHROPIC_API_KEY:
        print("WARNING: ANTHROPIC_API_KEY environment variable not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=5000)
