from fastapi import FastAPI, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from sqlalchemy import create_engine, Column, String, Integer, Float, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import enum


app = FastAPI()

# Database setup in the same file
DATABASE_URL = "sqlite:///./patients.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    others = "others"

class PatientORM(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

# Pydantic models
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def orm_to_pydantic(orm_obj: PatientORM) -> Patient:
    return Patient(
        id=orm_obj.id,
        name=orm_obj.name,
        city=orm_obj.city,
        age=orm_obj.age,
        gender=orm_obj.gender.value,
        height=orm_obj.height,
        weight=orm_obj.weight,
    )

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view(db: Session = Depends(get_db)):
    patients = db.query(PatientORM).all()
    return {p.id: orm_to_pydantic(p).model_dump(exclude={'id'}) for p in patients}

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001'),
                 db: Session = Depends(get_db)):
    patient = db.query(PatientORM).filter(PatientORM.id == patient_id).first()
    if patient:
        return orm_to_pydantic(patient).model_dump(exclude={'id'})
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
                  order: str = Query('asc', description='sort in asc or desc order'),
                  db: Session = Depends(get_db)):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    patients = db.query(PatientORM).all()
    p_list = [orm_to_pydantic(p) for p in patients]
    reverse = True if order == 'desc' else False
    sorted_data = sorted(p_list, key=lambda x: getattr(x, sort_by), reverse=reverse)
    return [p.model_dump(exclude={'id'}) for p in sorted_data]

@app.post('/create')
def create_patient(patient: Patient, db: Session = Depends(get_db)):
    existing = db.query(PatientORM).filter(PatientORM.id == patient.id).first()
    if existing:
        raise HTTPException(status_code=400, detail='Patient already exists')
    patient_orm = PatientORM(
        id=patient.id,
        name=patient.name,
        city=patient.city,
        age=patient.age,
        gender=GenderEnum(patient.gender),
        height=patient.height,
        weight=patient.weight
    )
    db.add(patient_orm)
    db.commit()
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(PatientORM).filter(PatientORM.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'gender' and value is not None:
            setattr(patient, key, GenderEnum(value))
        else:
            setattr(patient, key, value)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(PatientORM).filter(PatientORM.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    db.delete(patient)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'patient deleted'})