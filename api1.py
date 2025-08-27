from flask import jsonify, request
from service import app
from model import ServiceManager

service_manager = ServiceManager()
allowed_services = ['SIM', 'FTTM', 'MYMS']

@app.route('/services', methods=['GET'])
def get_all_services():
    services = [s.to_dict() for s in service_manager.get_all()]
    return jsonify({'services': services})

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = service_manager.get_by_id(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service.to_dict())

@app.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    if data['ServiceName'] not in allowed_services:
        return jsonify({'error': f"ServiceName must be one of: {', '.join(allowed_services)}"}), 400
    service = service_manager.create(
        service_name=data['ServiceName'],
        description=data.get('Description'),
        service_time=data.get('ServiceTime')
    )
    return jsonify({'message': 'Service successfully created!', 'ServiceId': service.ServiceId}), 201

@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.get_json()
    if 'ServiceName' in data and data['ServiceName'] not in allowed_services:
        return jsonify({'error': f"ServiceName must be one of: {', '.join(allowed_services)}"}), 400

    service = service_manager.update(
        service_id,
        service_name=data.get('ServiceName'),
        description=data.get('Description'),
        service_time=data.get('ServiceTime')
    )
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify({'message': 'Service successfully updated!'})

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    success = service_manager.delete(service_id)
    if not success:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify({'message': 'Service successfully deleted!'})

@app.route('/services', methods=['DELETE'])
def delete_all_services():
    service_manager.delete_all()
    return jsonify({'message': 'All services deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
