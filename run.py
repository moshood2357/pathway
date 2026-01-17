import os
from website import create_app

# Create the Flask app
app = create_app()

# Determine debug mode from environment variable (default False)
debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)




# This script is the entry point for running the web application.# It imports the Flask application instance from the 'website' package
# and starts the development server on port 8000 with debug mode enabled.
