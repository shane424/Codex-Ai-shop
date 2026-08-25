from pathlib import Path
from openpyxl import Workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from .sanitize import safe_text

HEADERS=['Date','Item / Project','Category','Quantity','Revenue','Cost','Status','Notes']
def generate_spreadsheet(path: Path, title: str, headers: list[str]|None=None) -> Path:
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); headers=headers or HEADERS
    wb=Workbook(); ins=wb.active; ins.title='Instructions'
    ins.append([safe_text(title)]); ins.append(['How to use']); ins.append(['Add one record per row on Data Entry. Use Dashboard for totals. Currency values are entered in dollars.'])
    data=wb.create_sheet('Data Entry'); data.append([safe_text(x) for x in headers])
    for row in range(2,102):
        data.cell(row,6,f'=IFERROR(C{row}*D{row},0)') if headers==HEADERS else None
    data.auto_filter.ref=f'A1:H101'; data.freeze_panes='A2'
    dv=DataValidation(type='list',formula1='"Open,In progress,Complete,Paused"'); data.add_data_validation(dv); dv.add('G2:G101')
    dash=wb.create_sheet('Dashboard'); dash.append(['Summary','Value']); dash.append(['Total revenue',"=SUM('Data Entry'!E2:E101)"]); dash.append(['Total cost',"=SUM('Data Entry'!F2:F101)"]); dash.append(['Profit','=B2-B3']); dash.append(['Profit margin','=IFERROR(B4/B2,0)']); dash['B5'].number_format='0.0%'
    for ws in wb:
        ws.freeze_panes=ws.freeze_panes or 'A2'; ws.sheet_view.showGridLines=False
        for cell in ws[1]: cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='243B53'); cell.alignment=Alignment(wrap_text=True)
        for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=min(42,max(12,max(len(str(c.value or'')) for c in col)+2))
    wb.save(path); return path
