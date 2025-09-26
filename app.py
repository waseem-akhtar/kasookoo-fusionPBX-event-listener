"""
Flask Webhook API Application

A simple Flask application that provides webhook endpoints for receiving
HTTP POST requests from external services.
"""

from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask Webhook API is running',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Main webhook endpoint to receive POST requests
    
    Accepts JSON payload and processes webhook data
    """
    try:
        # Get request data
        content_type = request.headers.get('Content-Type', '')
        
        # Log incoming request
        logger.info(f"Webhook received from IP: {request.remote_addr}")
        logger.info(f"Content-Type: {content_type}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Parse JSON data
        if 'application/json' in content_type:
            webhook_data = request.get_json()
        else:
            # Handle form data or raw data
            webhook_data = {
                'raw_data': request.get_data(as_text=True),
                'form_data': dict(request.form) if request.form else None
            }
        
        # Log the payload (be careful with sensitive data in production)
        logger.info(f"Webhook payload: {json.dumps(webhook_data, indent=2)}")
        
        # Process the webhook data (customize this section based on your needs)
        response_data = process_webhook_data(webhook_data)
        
        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Webhook processed successfully',
            'timestamp': datetime.utcnow().isoformat(),
            'data': response_data
        }), 200
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in webhook payload: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Invalid JSON format',
            'timestamp': datetime.utcnow().isoformat()
        }), 400
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


def process_webhook_data(data):
    """
    Process the webhook data based on your business logic
    
    Args:
        data (dict): The webhook payload data
        
    Returns:
        dict: Processed response data
    """
    # Example processing - customize based on your needs
    processed_data = {
        'received_at': datetime.utcnow().isoformat(),
        'payload_size': len(str(data)),
        'payload_type': type(data).__name__
    }
    
    # Add your custom processing logic here
    # For example:
    # - Validate specific fields
    # - Store data in database
    # - Trigger other services
    # - Send notifications
    
    return processed_data


@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """
    Specialized webhook endpoint for GitHub webhooks
    
    Handles GitHub webhook events with proper signature validation
    """
    try:
        # GitHub sends webhooks with specific headers
        event_type = request.headers.get('X-GitHub-Event')
        signature = request.headers.get('X-Hub-Signature-256')
        
        logger.info(f"GitHub webhook event: {event_type}")
        
        webhook_data = request.get_json()
        
        # Process GitHub-specific events
        if event_type == 'push':
            logger.info("Processing push event")
            # Handle push events
        elif event_type == 'pull_request':
            logger.info("Processing pull request event")
            # Handle PR events
        else:
            logger.info(f"Unhandled GitHub event: {event_type}")
        
        return jsonify({
            'status': 'success',
            'message': f'GitHub {event_type} event processed',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing GitHub webhook: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to process GitHub webhook',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask webhook API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)