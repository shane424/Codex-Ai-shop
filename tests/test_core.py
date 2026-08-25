from pathlib import Path
from zipfile import ZipFile
import pytest
from sqlalchemy.orm import sessionmaker
from backend.agents.opportunity_agent import is_safe, score
from backend.database import Base, make_engine
from backend.generation.bundle_generator import generate_bundle
from backend.generation.pdf_generator import generate_pdf
from backend.generation.spreadsheet_generator import generate_spreadsheet
from backend.models import Product
from backend.scheduler.automation_loop import action_for
from backend.validation.artifacts import validate_pdf, validate_xlsx

def test_weighted_score_and_safety():
    assert score(dict(utility=100,purchase_intent=80,automation=70,margin=60,niche_specificity=50))==78
    assert not is_safe({'problem':'official Pokemon profit guaranteed'})
    assert is_safe({'problem':'specific equipment maintenance record'})
def test_generation_validation_and_bundle(tmp_path):
    root=tmp_path/'approved'; x=generate_spreadsheet(root/'tracker.xlsx','Tracker'); p=generate_pdf(root/'check.pdf','Checklist')
    assert validate_xlsx(x).passed; assert validate_pdf(p).passed
    bundle=generate_bundle(root/'bundle.zip',[x,p],root)
    assert ZipFile(bundle).namelist()==['tracker.xlsx','check.pdf']
    outside=tmp_path/'private.txt'; outside.write_text('secret')
    with pytest.raises(ValueError): generate_bundle(root/'bad.zip',[outside],root)
def test_database_price_constraints(tmp_path):
    engine=make_engine(f'sqlite:///{tmp_path}/x.db'); Base.metadata.create_all(engine); db=sessionmaker(bind=engine)()
    db.add(Product(slug='unique',name='One',description='Useful',niche='Business',product_type='pdf',price_cents=500,file_path='/safe',status='draft')); db.commit()
    assert db.query(Product).one().price_cents==500
def test_automation_thresholds():
    assert action_for(500,0)=='kill'; assert action_for(250,0)=='improve'; assert action_for(100,2)=='scale'; assert action_for(10,0)=='observe'
