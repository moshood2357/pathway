from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_email = db.Column(db.String(100), unique=True, nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('super', 'moderator'), default='super')


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    education_level = db.Column(db.Enum('Secondary', 'Diploma', 'BSc', 'MSc', 'PhD'), nullable=True)
    career_goal = db.Column(db.String(100), nullable=True)
    current_role = db.Column(db.String(255), nullable=True)
    current_level = db.Column(db.String(255), nullable=True)
    strength = db.Column(db.String(255), nullable=True)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # relationships
    skills = db.relationship('UserSkill', back_populates='user', cascade='all, delete-orphan')
    interests = db.relationship('UserInterest', back_populates='user', cascade='all, delete-orphan')
    recommendations = db.relationship('CareerRecommendation', back_populates='user', cascade='all, delete-orphan')
    communities = db.relationship('UserCommunity', back_populates='user', cascade='all, delete-orphan')

class Career(db.Model):
    __tablename__ = 'career'

    career_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    career_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    demand_level = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=False)
    average_salary = db.Column(db.Numeric(12, 2), nullable=True)

    # relationships
    professionals = db.relationship('Professional', back_populates='career')
    skills = db.relationship('CareerSkill', back_populates='career', cascade='all, delete-orphan')
    user_interests = db.relationship('UserInterest', back_populates='career', cascade='all, delete-orphan')
    recommendations = db.relationship('CareerRecommendation', back_populates='career', cascade='all, delete-orphan')
    communities = db.relationship('Community', back_populates='career', cascade='all, delete-orphan')


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.Enum('Technical', 'Soft', 'Other'), nullable=False)

    # relationships
    careers = db.relationship('CareerSkill', back_populates='skill', cascade='all, delete-orphan')
    users = db.relationship('UserSkill', back_populates='skill', cascade='all, delete-orphan')


class UserInterest(db.Model):
    __tablename__ = 'user_interest'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('career.career_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # relationships
    user = db.relationship('User', back_populates='interests')
    career = db.relationship('Career', back_populates='user_interests')


class CareerSkill(db.Model):
    __tablename__ = 'career_skill'

    career_id = db.Column(db.Integer, db.ForeignKey('career.career_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # relationships
    career = db.relationship('Career', back_populates='skills')
    skill = db.relationship('Skill', back_populates='careers')


class UserSkill(db.Model):
    __tablename__ = 'user_skill'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # relationships
    user = db.relationship('User', back_populates='skills')
    skill = db.relationship('Skill', back_populates='users')


class CareerRecommendation(db.Model):
    __tablename__ = 'career_recommendation'

    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('career.career_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date_generated = db.Column(db.DateTime, default=datetime.utcnow)
    prof_id = db.Column(db.Integer, nullable=True)
    recommendation_details = db.Column(db.String(255), nullable=True)

    # relationships
    user = db.relationship('User', back_populates='recommendations')
    career = db.relationship('Career', back_populates='recommendations')


class Professional(db.Model):
    __tablename__ = 'professional'

    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    linkedin_id = db.Column(db.String(100), unique=True, nullable=True)
    career_id = db.Column(db.Integer, db.ForeignKey('career.career_id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)

    # relationships
    career = db.relationship('Career', back_populates='professionals')


class EducationLevel(db.Model):
    __tablename__ = 'education_level'

    edulevel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edulevel_name = db.Column(db.String(45), nullable=False)


# -------------------- Community --------------------
class Community(db.Model):
    __tablename__ = 'community'

    community_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    career_id = db.Column(db.Integer, db.ForeignKey('career.career_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    community_link = db.Column(db.String(2083), nullable=True)


    # relationships
    career = db.relationship('Career', back_populates='communities')
    users = db.relationship('UserCommunity', back_populates='community', cascade='all, delete-orphan')


# -------------------- UserCommunity --------------------
class UserCommunity(db.Model):
    __tablename__ = 'user_community'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # relationships
    user = db.relationship('User', back_populates='communities')
    community = db.relationship('Community', back_populates='users')