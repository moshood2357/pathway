from datetime import datetime, timedelta

from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from website.forms import LoginForm, AddSkillForm, CareerForm, ProfessionalForm, CommunityForm
from werkzeug.security import check_password_hash
from website.models import db, Admin, User, Skill, Career, Professional, Community
from functools import wraps

admin = Blueprint('admin', __name__)


# =============================
#   ADMIN AUTH DECORATOR
# =============================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('You must be logged in as admin.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


# Avoid caching admin pages after logout
@admin.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# =============================
#            LOGIN
# =============================
@admin.route('/admin', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        admin_user = Admin.query.filter(Admin.admin_email == email).first()

        if admin_user and check_password_hash(admin_user.admin_password, password):
            session['admin'] = admin_user.admin_email
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('admin.login'))

    return render_template('admin/admin_signin.html', form=form)


## =============================
#          DASHBOARD
# =============================
@admin.route('/admin/dashboard/', methods=['GET', 'POST'])
@admin_required
def dashboard():
    tab = request.args.get('tab', 'skills')

    total_users = User.query.count()

    # get new signups in last 7 days
    last_7_days = datetime.utcnow() - timedelta(days=7)
    new_signups = User.query.filter(User.reg_date >= last_7_days).count()

    # get daily active users (last 24 hours)
    last_24_hours = datetime.utcnow() - timedelta(days=1)
    dau = User.query.filter(User.last_login >= last_24_hours).count()

    # FORMS
    add_skill_form = AddSkillForm()
    add_career_form = CareerForm()
    add_professional_form = ProfessionalForm()
    add_community_form = CommunityForm()  # <-- NEW FORM

    add_professional_form.career_id.choices = [
        (c.career_id, c.career_name) for c in Career.query.all()
    ]

    add_community_form.career_id.choices = [
        (c.career_id, c.career_name) for c in Career.query.all()
    ]

    # DATA
    skills = Skill.query.all()
    careers = Career.query.all()
    professional = Professional.query.all()
    communities = Community.query.all()   # <-- COMMUNITY DATA

    # Handle Skill creation
    if add_skill_form.validate_on_submit() and add_skill_form.submit.data:
        new_skill = Skill(
            skill_name=add_skill_form.skill_name.data,
            category=add_skill_form.category.data
        )
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.dashboard', tab='skills'))

    # Handle Career creation
    if add_career_form.validate_on_submit() and add_career_form.submit.data:
        new_career = Career(
            career_name=add_career_form.career_name.data,
            description=add_career_form.description.data,
            demand_level=add_career_form.demand_level.data,
            average_salary=add_career_form.average_salary.data,
        )
        db.session.add(new_career)
        db.session.commit()
        flash('Career added successfully!', 'success')
        return redirect(url_for('admin.dashboard', tab='careers'))

    # Handle Professional creation
    if add_professional_form.validate_on_submit() and add_professional_form.submit.data:
        new_professional = Professional(
            first_name=add_professional_form.first_name.data,
            last_name=add_professional_form.last_name.data,
            email=add_professional_form.email.data,
            linkedin_id=add_professional_form.linkedin_id.data,
            career_id=add_professional_form.career_id.data
        )
        db.session.add(new_professional)
        db.session.commit()
        flash('Professional added successfully!', 'success')
        return redirect(url_for('admin.dashboard', tab='professionals'))

    # Handle Community Link creation  <-- NEW BLOCK
    if add_community_form.validate_on_submit() and add_community_form.submit.data:
        community_link = add_community_form.community_link.data.strip() or None

        new_community = Community(
            community_name=add_community_form.community_name.data.strip(),
            description=add_community_form.description.data.strip() or None,
            career_id=add_community_form.career_id.data,
            community_link=community_link
        )

        db.session.add(new_community)
        db.session.commit()
        flash(f'Communities "{add_community_form.community_name.data}" added successfully!', 'msg')

    return render_template(
        'admin/admin_dashboard.html',
        total_users=total_users,
        add_skill_form=add_skill_form,
        add_career_form=add_career_form,
        add_professional_form=add_professional_form,
        add_community_form=add_community_form,  # NEW
        skills=skills,
        careers=careers,
        professional=professional,
        communities=communities,  # NEW
        active_tab=tab,
        new_signups=new_signups,
        dau=dau
    )


# =============================
#          LOGOUT
# =============================
@admin.get('/loggedout/')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('views.home'))


# =============================
#       SKILLS CRUD
# =============================
@admin.route('/add_skill', methods=['GET', 'POST'])
@admin_required
def add_skill():
    form = AddSkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            skill_name=form.skill_name.data,
            category=form.category.data
        )
        db.session.add(new_skill)
        db.session.commit()
        flash(f'Skill "{form.skill_name.data}" added successfully!', 'msg')
    else:
        flash('Error adding skill. Please check your input.', 'errormsg')

    return redirect(url_for('admin.dashboard', tab='skillsTab'))


@admin.route('/edit_skill/<int:id>', methods=['POST'])
@admin_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)

    skill.skill_name = request.form.get('skill_name')
    skill.category = request.form.get('category')

    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='skillsTab'))


@admin.route('/delete_skill/<int:skill_id>')
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='skillsTab'))


# =============================
#        CAREER CRUD
# =============================
@admin.route('/add_career', methods=['GET', 'POST'])
@admin_required
def add_career():
    forms = CareerForm()

    if forms.validate_on_submit():
        new_career = Career(
            career_name=forms.career_name.data,
            description=forms.description.data,
            demand_level=forms.demand_level.data,
            average_salary=forms.average_salary.data
        )
        db.session.add(new_career)
        db.session.commit()

        flash(f'Career "{forms.career_name.data}" added successfully!', 'msg')
    else:
        flash('Error adding career. Please check your input.', 'errormsg')

    return redirect(url_for('admin.dashboard', tab='careersTab'))


@admin.route('/edit_career/<int:career_id>', methods=['POST'])
@admin_required
def edit_career(career_id):
    career = Career.query.get_or_404(career_id)

    career.career_name = request.form.get('career_name')
    career.description = request.form.get('description')
    career.demand_level = request.form.get('demand_level')
    career.average_salary = request.form.get('average_salary')

    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='careersTab'))


@admin.route('/delete_career/<int:career_id>')
@admin_required
def delete_career(career_id):
    career = Career.query.get_or_404(career_id)
    db.session.delete(career)
    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='careersTab'))


# =============================
#     PROFESSIONAL CRUD
# =============================
@admin.route('/add_professional', methods=['GET', 'POST'])
@admin_required
def add_professional():
    form = ProfessionalForm()

    form.career_id.choices = [
        (c.career_id, c.career_name)
        for c in Career.query.all()
    ]

    if form.validate_on_submit():
        new_professional = Professional(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            linkedin_id=form.linkedin_id.data,
            career_id=form.career_id.data
        )

        db.session.add(new_professional)
        db.session.commit()

        flash(f'Professional "{form.first_name.data} {form.last_name.data}" added successfully!', 'msg')
        return redirect(url_for('admin.dashboard', tab='professionalsTab'))

    if form.errors:
        flash('Error adding professional. Please check your input.', 'errormsg')

    return redirect(url_for('admin.dashboard', tab='professionalsTab'))


@admin.route('/edit_professional/<int:professional_id>', methods=['POST'])
@admin_required
def edit_professional_route(professional_id):
    professional = Professional.query.get_or_404(professional_id)

    professional.first_name = request.form.get('first_name')
    professional.last_name = request.form.get('last_name')
    professional.email = request.form.get('email')
    professional.linkedin_id = request.form.get('linkedin_id')
    professional.career_id = request.form.get('career_id')

    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='professionalsTab'))


@admin.route('/delete_professional/<int:professional_id>')
@admin_required
def delete_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    db.session.delete(professional)
    db.session.commit()
    return redirect(url_for('admin.dashboard', tab='professionalsTab'))



# =============================
#       COMMUNITY CRUD
# =============================
@admin.route('/add_community', methods=['GET', 'POST'])
@admin_required
def add_community():
    form = CommunityForm()

    # Dynamically load career choices (required for WTForms validation)
    form.career_id.choices = [(c.career_id, c.career_name) for c in Career.query.all()]

    if form.validate_on_submit():
        # Handle empty string for community_link
        community_link = form.community_link.data.strip() or None

        new_community = Community(
            community_name=form.community_name.data.strip(),
            description=form.description.data.strip() or None,
            career_id=form.career_id.data,
            community_link=community_link
        )

        db.session.add(new_community)
        db.session.commit()
        # flash(f'Community "{form.community_name.data}" added successfully!', 'msg')
    else:
        # Show detailed errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "errormsg")

    return redirect(url_for('admin.dashboard', tab='communityTab'))



# ------- Edit Community -------
@admin.route('/edit_community/<int:id>', methods=['POST'])
@admin_required
def edit_community(id):
    community = Community.query.get_or_404(id)

    # Update fields
    community.community_name = request.form.get('community_name')
    community.description = request.form.get('description')
    community.career_id = request.form.get('career_id')
    community.community_link = request.form.get('community_link')

    db.session.commit()
    # flash("Community updated successfully!", "msg")

    return redirect(url_for('admin.dashboard', tab='communityTab'))


# ------- Delete Community -------
@admin.route('/delete_community/<int:id>')
@admin_required
def delete_community(id):
    community = Community.query.get_or_404(id)

    db.session.delete(community)
    db.session.commit()
    # flash("Community deleted successfully!", "msg")

    return redirect(url_for('admin.dashboard', tab='communityTab'))
