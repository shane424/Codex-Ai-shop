from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from .sanitize import safe_text

def generate_pdf(path: Path, title: str, sections: list[tuple[str,str]]|None=None) -> Path:
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); styles=getSampleStyleSheet()
    sections=sections or [('How to use','Print or save this checklist. Complete each item, add notes, and review before closing the task.'),('Checklist','Use the rows below to record owner, due date, completion, and notes.')]
    story=[Paragraph(safe_text(title),styles['Title']),Spacer(1,.2*inch)]
    for heading,body in sections: story += [Paragraph(safe_text(heading),styles['Heading2']),Paragraph(safe_text(body),styles['BodyText']),Spacer(1,.15*inch)]
    rows=[['Done','Task / record','Owner','Date','Notes']]+[['□','', '', '', ''] for _ in range(18)]
    table=Table(rows,colWidths=[.45*inch,2.4*inch,1.1*inch,.9*inch,1.5*inch],rowHeights=[.3*inch]*len(rows),repeatRows=1)
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.black),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(table); SimpleDocTemplate(str(path),pagesize=letter,rightMargin=.4*inch,leftMargin=.4*inch,topMargin=.5*inch,bottomMargin=.5*inch).build(story); return path
