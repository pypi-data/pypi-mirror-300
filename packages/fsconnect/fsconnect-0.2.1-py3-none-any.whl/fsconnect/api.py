from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')

    # Mock summary logic (replace with your AI model logic)
    summary = f"Summary of: {text[:50]}..." if text else "No text provided."
    
    return jsonify({"summary": summary})

@api_blueprint.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    # Mock generation logic (replace with your AI model logic)
    generated_content = f"Generated content based on: {prompt}"
    
    return jsonify({"generated_content": generated_content})
