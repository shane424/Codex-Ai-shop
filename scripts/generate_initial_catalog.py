#!/usr/bin/env python3
import csv, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select
from backend.database import SessionLocal, init_db
from backend.generation.bundle_generator import generate_bundle
from backend.generation.pdf_generator import generate_pdf
from backend.generation.sanitize import safe_slug
from backend.generation.spreadsheet_generator import generate_spreadsheet
from backend.models import Product
from backend.validation.artifacts import validate_pdf, validate_xlsx

NAMES=['Contractor Job Profit Tracker','Small Business Expense Tracker','Equipment Maintenance Log','Customer Follow-Up CRM','Quote Comparison Spreadsheet','Invoice Payment Tracker','Inventory Reorder Calculator','Mileage Log','Vendor Comparison Sheet','Simple Project Profitability Calculator','Pet Medication Tracker','Dog Daycare Daily Report','Kennel Cleaning Checklist','Pet Sitter Client Intake Pack','Reptile Feeding Tracker','Job Application Tracker','Recruiter CRM','Freelance Lead Tracker','Client Profitability Calculator','Proposal Follow-Up Tracker']
PDFS={'Kennel Cleaning Checklist','Dog Daycare Daily Report','Pet Sitter Client Intake Pack'}
BUNDLES={'Small Business Operations Pack':(3900,[0,1,3,5,6]),'Contractor Starter Pack':(2900,[0,2,4,7]),'Pet Business Operations Pack':(2900,[10,11,12,13,14]),'Job Search Command Center':(1900,[15,16,19]),'Freelancer Operations Pack':(2900,[17,18,19])}

def niche(i): return 'Small Business' if i<10 else ('Pet Business' if i<15 else 'Career & Freelance')
def main(root=Path('products/approved')):
    root.mkdir(parents=True,exist_ok=True); init_db(); db=SessionLocal(); paths=[]
    for i,name in enumerate(NAMES):
        slug=safe_slug(name); suffix='.pdf' if name in PDFS else '.xlsx'; path=root/f'{slug}{suffix}'
        if not path.exists(): (generate_pdf if suffix=='.pdf' else generate_spreadsheet)(path,name)
        result=validate_pdf(path) if suffix=='.pdf' else validate_xlsx(path)
        if not result.passed: raise RuntimeError(f'{name}: {result.reasons}')
        paths.append(path); product=db.scalar(select(Product).where(Product.slug==slug))
        values=dict(name=name,description=f'A practical {name.lower()} with clear instructions, reusable records, and an at-a-glance summary.',niche=niche(i),product_type=suffix[1:],price_cents=900 if suffix=='.pdf' else (1900 if 'Calculator' in name or 'Profit' in name else 1200),file_path=str(path.resolve()),keywords=[slug.replace('-',' '),niche(i).lower(),'downloadable template'],faqs=[{'question':'What is included?','answer':f'One reusable {suffix[1:].upper()} file with instructions.'},{'question':'Is this a subscription?','answer':'No. This is a one-time digital download.'}],related_slugs=[safe_slug(NAMES[x]) for x in range(max(0,i-1),min(20,i+2)) if x!=i],status='published',failure_reasons=[])
        if product:
            for k,v in values.items(): setattr(product,k,v)
        else: db.add(Product(slug=slug,**values))
    db.commit()
    for name,(price,indices) in BUNDLES.items():
        slug=safe_slug(name); path=root/f'{slug}.zip'
        if not path.exists(): generate_bundle(path,[paths[x] for x in indices],root)
        values=dict(name=name,description=f'Five related, practical templates collected in the {name}.',niche=niche(indices[0]),product_type='zip',price_cents=price,file_path=str(path.resolve()),keywords=[name.lower(),'template bundle'],faqs=[{'question':'What is included?','answer':'The related files shown in this bundle listing.'}],related_slugs=[safe_slug(NAMES[x]) for x in indices],status='published',failure_reasons=[])
        p=db.scalar(select(Product).where(Product.slug==slug))
        if p:
            for k,v in values.items(): setattr(p,k,v)
        else: db.add(Product(slug=slug,**values))
    db.commit(); db.close(); print('Catalog ready: 20 products and 5 bundles')
if __name__=='__main__': main()
