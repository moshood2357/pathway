from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from website.auth import login_required
from website.models import User, db, User, Professional, Career, CareerRecommendation,Community
from website.forms import Question4, Question2
from datetime import datetime


views = Blueprint('views', __name__)


@views.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@views.route("/")
def home():
    return render_template("home.html")


@views.route('/about')
def about():
    return render_template('detailed_about_section.html')


@views.route("/contact")
def contact():
    return render_template("contact.html")




@views.route("/question2", methods=['GET', 'POST'])
def Second_question():
    form = Question2()

    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if user:
            user.education_level = form.currentlevel.data
            db.session.commit()
            return redirect(url_for('views.Third_question'))

    return render_template("question2.html", form=form)


@views.route("/question3")
def Third_question():
    return render_template("question3.html")


@views.route("/question4", methods=['GET', 'POST'])
def Fourth_question():
    form = Question4()

    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if user:
            user.career_goal = form.careergoal.data
            db.session.commit()
            return redirect(url_for('views.Fifth_question'))

    return render_template("question4.html", form=form)


@views.route("/question5")
def Fifth_question():
    return render_template("question5.html")


@views.route("/save-strengths", methods=['POST'])
def save_strengths():
    if 'user_id' not in session:
        # flash('Please log in to continue.', 'errormsg')
        return redirect(url_for('auth.Sign_in'))

    strengths = request.form.get('strengths', '')

    user = User.query.get(session['user_id'])
    if user:
        user.strength = strengths
        db.session.commit()
        # flash('Strengths saved successfully!', 'msg')
    # else:
    #     flash('User not found.', 'errormsg')

    return redirect(url_for('views.dashboard'))


# -------------------------------------
# AI-LIKE CAREER RECOMMENDATION LOGIC
# -------------------------------------
def score_career(career, user_keywords):
    """Assigns a score based on keyword matches."""
    score = 0
    career_keywords = (career.career_name or "").lower().split()

    for keyword in user_keywords:
        if keyword in career_keywords:
            score += 5  # strong match

        for ck in career_keywords:
            if keyword in ck:
                score += 2  # partial match

    return score


@views.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.Sign_in'))

    user = User.query.get(user_id)

    # Check if a recommendation already exists
    existing = CareerRecommendation.query.filter_by(user_id=user_id).first()
    if existing:
        recommended_career = existing.career.career_name if existing.career else ""
        flash(existing.recommendation_details, "info")
        return render_template(
            "dashboard.html",
            user=user,
            recommended_career=recommended_career
        )

    # Build user keywords
    keywords = []
    if user.career_goal:
        keywords += user.career_goal.lower().split()
    if user.strength:
        keywords += user.strength.lower().split()

    # If no profile data, prompt user to update
    if not keywords:
        flash("Complete your profile (career goal & strengths) to get personalized recommendations.", "warning")
        return render_template("dashboard.html", user=user, recommended_career="")

    # Fetch all careers
    careers = Career.query.all()
    if not careers:
        flash("No careers available for recommendation.", "warning")
        return render_template("dashboard.html", user=user, recommended_career="")

    # Function to score careers based on keyword match
    def score_career(career, keywords):
        text = f"{career.career_name} {career.description}"
        # Include skills if CareerSkill model exists
        if hasattr(career, "skills") and career.skills:
            text += " " + " ".join([skill.skill_name for skill in career.skills])
        text = text.lower()
        return sum(word in text for word in keywords)

    # Find the best matching career
    best_career = None
    best_score = -1
    for career in careers:
        score = score_career(career, keywords)
        if score > best_score:
            best_score = score
            best_career = career

    if not best_career:
        flash("No matching career found based on your profile.", "warning")
        return render_template("dashboard.html", user=user, recommended_career="")

    # Save recommendation
    reco_msg = (
        f"Recommended Career: {best_career.career_name}. "
        "You can edit your profile to change this recommendation anytime. This recommendation is just to  get you started, to get more personalized recommendation; kindly update your profile"
    )

    new_reco = CareerRecommendation(
        user_id=user.user_id,
        career_id=best_career.career_id,
        recommendation_details=reco_msg,
        date_generated=datetime.utcnow()
    )

    db.session.add(new_reco)
    db.session.commit()

    flash(reco_msg, "success")

    return render_template(
        "dashboard.html",
        user=user,
        recommended_career=best_career.career_name
    )



@views.route("/professional")
def professional():
    pro = Professional.query.all()
    return render_template("professional.html", pro=pro)




@views.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.Sign_in'))

    user = User.query.get(user_id)

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        career_goal = request.form.get("career_goal", "").strip()
        strength = request.form.get("strength", "").strip()
        education_level = request.form.get("education_level", "").strip()
        skills = request.form.get("skills", "").strip()  # Optional

        # --- Basic validation ---
        if not career_goal and not strength:
            flash("Please fill in at least your career goal or strengths.", "warning")
            return redirect(url_for("views.update_profile"))

        # --- Update user fields ---
        user.full_name = full_name or user.full_name
        user.career_goal = career_goal or user.career_goal
        user.strength = strength or user.strength
        user.education_level = education_level or user.education_level


        if hasattr(user, "skills"):
            user.skills = skills or user.skills

        db.session.commit()

        
        return redirect(url_for("views.dashboard"))
    
    
    return render_template(
        "update_profile.html",
        user=user
    )




@views.route("/community")
def community():
    communities=Community.query.limit(24).all()
    return render_template("community.html", communities=communities)




@views.route('/search_communities')
def search_communities():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify([])  # return empty if no query

    # search in name or description
    results = Community.query.filter(
        (Community.community_name.ilike(f'%{query}%')) |
        (Community.description.ilike(f'%{query}%'))
    ).all()

    communities = [
        {
            'community_name': c.community_name,
            'description': c.description,
            'community_link': c.community_link,
            
        } for c in results
    ]
    
    return jsonify(communities)