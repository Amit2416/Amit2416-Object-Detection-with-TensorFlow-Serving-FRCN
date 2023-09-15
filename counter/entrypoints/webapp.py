from io import BytesIO
from flask import Flask, request, jsonify
from counter import config

from utils.logging_utils import configure_logging
logger = configure_logging()

app = Flask(__name__)

count_action = config.get_count_action()

@app.route('/object-count', methods=['POST'])
def object_detection():
    try:
        logger.info('Received object detection request with old service end point')

        uploaded_file = request.files['file']
        threshold = float(request.form.get('threshold', 0.5))
        image = BytesIO()
        uploaded_file.save(image)
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)
    
    except Exception as e:

        logger.exception('Error in object detection')
        return jsonify({'error': 'Error detecting objects'}), 500


#added new service point
@app.route('/new-service-endpoint', methods=['POST'])
def predict_objects():
    try:
        logger.info('Received object detection request with new service end point')

        uploaded_file = request.files['file']
        threshold = float(request.form.get('threshold', 0.5))
        image = BytesIO()
        uploaded_file.save(image)
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)
    
    except Exception as e:

        logger.exception('Error in object detection')
        return jsonify({'error': 'Error detecting objects'}), 500

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
