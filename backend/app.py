"""
Dental Materials Course Chatbot Backend - SMART VERSION
Flask server with intelligent chapter loading to avoid rate limits
"""

import os
import anthropic
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
KNOWLEDGE_BASE_DIR = Path(__file__).parent / 'knowledge_base'
INSTRUCTIONS_FILE = Path(__file__).parent / 'instructions.txt'

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Chapter keywords for smart loading
CHAPTER_KEYWORDS = {
    'Ch01': ['overview', 'introduction', 'history', 'oral cavity', 'teeth structure'],
    'Ch02': ['structure', 'matter', 'atomic', 'molecular', 'bonding', 'adhesion', 'chemistry'],
    'Ch03': ['physical properties', 'thermal', 'optical', 'color', 'solubility'],
    'Ch04': ['mechanical properties', 'stress', 'strain', 'elastic', 'strength', 'hardness', 'toughness'],
    'Ch05': ['composite', 'resin', 'filler', 'polymerization', 'shrinkage'],
    'Ch06': ['bonding', 'adhesive', 'etchant', 'primer', 'dentin bonding'],
    'Ch07': ['cement', 'luting', 'zinc', 'glass ionomer', 'resin cement'],
    'Ch08': ['amalgam', 'mercury', 'silver', 'creep', 'corrosion'],
    'Ch09': ['metal', 'alloy', 'gold', 'titanium', 'casting', 'wrought'],
    'Ch10': ['ceramic', 'porcelain', 'zirconia', 'alumina', 'glass ceramic', 'lithium disilicate'],
    'Ch11': ['denture', 'acrylic', 'pmma', 'prosthetic', 'polymer'],
    'Ch12': ['implant', 'osseointegration', 'titanium implant', 'abutment'],
    'Ch13': ['impression', 'gypsum', 'wax', 'alginate', 'silicone', 'stone', 'plaster'],
    'Ch14': ['casting', 'investment', 'sprue', 'burnout', 'lost wax'],
    'Ch15': ['digital', 'cad', 'cam', 'scanner', '3d printing', 'milling'],
    'Ch16': ['cutting', 'grinding', 'polishing', 'finishing', 'bur', 'abrasive'],
    'Ch17': ['biocompatibility', 'toxicity', 'allergy', 'cytotoxicity', 'safety'],
    'Ch18': ['in vitro', 'testing', 'research', 'laboratory'],
    'Ch19': ['clinical', 'in vivo', 'clinical trial', 'patient'],
    'Ch20': ['emerging', 'nanotechnology', 'biomimetic', 'smart materials', 'future']
}

def load_instructions():
    """Load the chatbot instructions from file"""
    if INSTRUCTIONS_FILE.exists():
        return INSTRUCTIONS_FILE.read_text()
    return "You are a helpful teaching assistant for a dental materials course."

def get_relevant_chapters(question):
    """Determine which Phillips chapters are relevant to the question"""
    question_lower = question.lower()
    relevant_chapters = []
    
    # Check each chapter's keywords
    for chapter, keywords in CHAPTER_KEYWORDS.items():
        for keyword in keywords:
            if keyword in question_lower:
                if chapter not in relevant_chapters:
                    relevant_chapters.append(chapter)
                break
    
    # If no specific chapters found, load just one general one
    if not relevant_chapters:
        relevant_chapters = ['Ch01']  # Just overview by default
    
    # Limit to max 3 chapters to avoid rate limits
    return relevant_chapters[:3]

def load_selective_knowledge(question):
    """Load only relevant files based on the question"""
    knowledge_files = []
    
    if not KNOWLEDGE_BASE_DIR.exists():
        return []
    
    # Get relevant Phillips chapters
    relevant_chapters = get_relevant_chapters(question)
    
    # Load all files
    for file_path in KNOWLEDGE_BASE_DIR.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md', '.csv']:
            try:
                filename = file_path.name
                
                # Always load non-Phillips files (syllabus, lectures, etc.)
                if not filename.startswith('Phillips_Ch'):
                    content = file_path.read_text(encoding='utf-8')
                    knowledge_files.append({
                        'name': filename,
                        'content': content
                    })
                # Only load relevant Phillips chapters
                else:
                    for chapter in relevant_chapters:
                        if chapter in filename:
                            content = file_path.read_text(encoding='utf-8')
                            knowledge_files.append({
                                'name': filename,
                                'content': content
                            })
                            break
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return knowledge_files

def build_context_message(question):
    """Build the context message with instructions and relevant knowledge"""
    instructions = load_instructions()
    knowledge_files = load_selective_knowledge(question)
    
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

@app.route('/info', methods=['GET'])
def info():
    """Get information about the knowledge base"""
    if not KNOWLEDGE_BASE_DIR.exists():
        return jsonify({
            'knowledge_base_exists': False,
            'files_count': 0
        })
    
    files = list(KNOWLEDGE_BASE_DIR.rglob('*.txt')) + list(KNOWLEDGE_BASE_DIR.rglob('*.md'))
    return jsonify({
        'knowledge_base_exists': True,
        'files_count': len(files),
        'files': [f.name for f in files]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        if not ANTHROPIC_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
        
        # Build context with only relevant chapters
        system_context = build_context_message(user_message)
        
        # Prepare messages for Claude
        messages = conversation_history + [
            {'role': 'user', 'content': user_message}
        ]
        
        # Call Claude API
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=1000,
            system=system_context,
            messages=messages
        )
        
        # Extract response text
        response_text = ''
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text
        
        return jsonify({
            'response': response_text,
            'model': 'claude-sonnet-4-20250514'
        })
        
    except anthropic.APIError as e:
        error_msg = f"API error: {str(e)}"
        print(f"Anthropic API error: {e}")
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"Error: {e}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("DENTAL MATERIALS CHATBOT - SMART BACKEND")
    print("=" * 60)
    print(f"Knowledge base directory: {KNOWLEDGE_BASE_DIR}")
    print(f"Instructions file: {INSTRUCTIONS_FILE}")
    print("")
    
    if KNOWLEDGE_BASE_DIR.exists():
        files = list(KNOWLEDGE_BASE_DIR.rglob('*.txt')) + list(KNOWLEDGE_BASE_DIR.rglob('*.md'))
        print(f"Found {len(files)} files in knowledge base")
        for f in files[:5]:  # Show first 5
            print(f"  - {f.name}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
    else:
        print("⚠️  Knowledge base directory not found!")
    
    print("")
    print("Starting server on http://0.0.0.0:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
