from app.models import Case
from app import db

class CaseService:
    
    # fetch all therapy cases in db
    @staticmethod
    def get_all_cases():
        cases = Case.query.all()
        return [{"name": case.name, "description": case.description} for case in cases]

    # add a new case 
    @staticmethod   
    def add_case(name, description):
        new_case = Case(name=name, description=description)
        db.session.add(new_case)
        db.session.commit()
        return {"message": "Case has been added successfully."}, 201