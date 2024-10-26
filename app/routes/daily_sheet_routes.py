from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import daily_sheet_bp
from ..services.firebase_service import FirebaseService
from datetime import datetime

@daily_sheet_bp.route('/')
@login_required
def index():
    # Get all daily sheets
    sheets = FirebaseService.get_all_daily_sheets()
    return render_template('daily_sheets/list.html', sheets=sheets)

@daily_sheet_bp.route('/new', methods=['GET'])
@login_required
def new():
    employees = FirebaseService.get_all_employees()
    equipment = FirebaseService.get_available_equipment()
    return render_template('daily_sheets/new.html',
                         employees=employees,
                         equipment=equipment)

@daily_sheet_bp.route('/create', methods=['POST'])
@login_required
def create():
    try:
        # Get form data
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        # Create daily sheet
        sheet_data = {'date': date}
        sheet_id = FirebaseService.create_daily_sheet(sheet_data)
        
        # Process job sections
        job_sections = request.form.getlist('job_id[]')
        employee_ids = request.form.getlist('employee_ids[]')
        equipment_ids = request.form.getlist('equipment_ids[]')
        start_times = request.form.getlist('start_times[]')
        end_times = request.form.getlist('end_times[]')
        
        # Create job sections and assignments
        for i, job_id in enumerate(job_sections):
            section_data = {'job_id': job_id}
            section_id = FirebaseService.add_job_section(sheet_id, section_data)
            
            assignment_data = {
                'employee_id': employee_ids[i],
                'equipment_id': equipment_ids[i],
                'start_time': start_times[i],
                'end_time': end_times[i]
            }
            FirebaseService.add_assignment(section_id, assignment_data)
        
        flash('Daily sheet created successfully!', 'success')
        return redirect(url_for('daily_sheet.view', sheet_id=sheet_id))
        
    except Exception as e:
        flash(f'Error creating daily sheet: {str(e)}', 'error')
        return redirect(url_for('daily_sheet.new'))

@daily_sheet_bp.route('/<sheet_id>')
@login_required
def view(sheet_id):
    sheet = FirebaseService.get_daily_sheet(sheet_id)
    if not sheet:
        flash('Daily sheet not found', 'error')
        return redirect(url_for('daily_sheet.index'))
    return render_template('daily_sheets/view.html', sheet=sheet)