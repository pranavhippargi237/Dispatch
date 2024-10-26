from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

class FirebaseService:
    @staticmethod
    def get_all_employees():
        return [doc.to_dict() for doc in db.collection('employees').stream()]
    
    @staticmethod
    def get_all_equipment():
        return [doc.to_dict() for doc in db.collection('equipment').stream()]
    
    @staticmethod
    def get_available_equipment():
        return [doc.to_dict() for doc in 
                db.collection('equipment')
                .where('status', '==', 'available')
                .stream()]
    
    @staticmethod
    def create_daily_sheet(data):
        daily_sheet_ref = db.collection('daily_sheets').document()
        daily_sheet_data = {
            'date': data['date'],
            'created_at': datetime.now(),
            'status': 'active'
        }
        daily_sheet_ref.set(daily_sheet_data)
        return daily_sheet_ref.id
    
    @staticmethod
    def add_job_section(daily_sheet_id, job_data):
        section_ref = db.collection('job_sections').document()
        section_data = {
            'daily_sheet_id': daily_sheet_id,
            'job_id': job_data['job_id'],
            'created_at': datetime.now()
        }
        section_ref.set(section_data)
        return section_ref.id
    
    @staticmethod
    def add_assignment(section_id, assignment_data):
        assignment_ref = db.collection('daily_assignments').document()
        assignment_data.update({
            'job_section_id': section_id,
            'created_at': datetime.now()
        })
        assignment_ref.set(assignment_data)
        return assignment_ref.id