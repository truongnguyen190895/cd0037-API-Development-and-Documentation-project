import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        if request.method != "GET":
            abort(405)

        categories = Category.query.all()
        formatted_categories = {
            str(category.id): category.type for category in categories
        }
        categories_response = {"success": True, "categories": formatted_categories}
        return jsonify(categories_response)

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", default=1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        categories = Category.query.all()
        formatted_questions = [question.format() for question in questions[start:end]]
        formatted_categories = {
            str(category.id): category.type for category in categories
        }

        if len(formatted_questions) == 0:
            abort(404)

        response = {
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(questions),
            "categories": formatted_categories,
            "current_category": None,
        }

        return jsonify(response)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)
        try:
            db.session.delete(question)
            db.session.commit()
            return jsonify({"success": True, "question_id": question_id})
        except Exception as error:
            db.session.rollback()
            abort(500)

    @app.route("/questions", methods=["POST"])
    def create_question():
        payload = request.get_json()

        # search questions section

        if "searchTerm" in payload:
            search_term = payload["searchTerm"]
            if search_term:
                questions = Question.query.filter(
                    Question.question.ilike(f"%{search_term}%")
                ).all()
                formatted_questions = [question.format() for question in questions]
                total_questions = len(formatted_questions)
                return jsonify(
                    {
                        "success": True,
                        "total_questions": total_questions,
                        "questions": formatted_questions,
                    }
                )
            else:
                questions = Question.query.all()
                formatted_questions = [question.format() for question in questions]
                total_questions = len(formatted_questions)
                return jsonify(
                    {
                        "success": True,
                        "total_questions": total_questions,
                        "questions": formatted_questions,
                    }
                )

        # create new question section
        required_fields = ["question", "answer", "category", "difficulty"]

        for field in required_fields:
            if field not in payload or not payload[field]:
                abort(422)

        question_text = payload["question"]
        answer_text = payload["answer"]
        category = payload["category"]
        difficulty = payload["difficulty"]

        try:
            new_question = Question(
                question=question_text,
                answer=answer_text,
                category=category,
                difficulty=difficulty,
            )
            db.session.add(new_question)
            db.session.commit()
            return jsonify({"success": True, "created_question_id": new_question.id})
        except:
            db.session.rollback()
            abort(422)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=str(category_id)).all()

        if not questions:
            abort(404)

        formatted_questions = [question.format() for question in questions]
        total_questions = len(formatted_questions)

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "totalQuestions": total_questions,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        payload = request.get_json()

        if "quiz_category" not in payload or "previous_questions" not in payload:
            abort(400)
        quiz_category = payload["quiz_category"]
        category_id = quiz_category.get("id")
        previous_questions = payload["previous_questions"]

        if category_id is not None and category_id != 0:
            questions = Question.query.filter(
                Question.category == str(category_id)
            ).all()
        else:
            # If no category ID is provided, get all questions
            questions = Question.query.all()

        available_questions = [
            question for question in questions if question.id not in previous_questions
        ]

        if available_questions:
            random_question = random.choice(available_questions)
            formatted_question = random_question.format()
        else:
            formatted_question = None  # No available questions

        return jsonify({"success": True, "question": formatted_question})

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable Content"}
            ),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
            405,
        )

    @app.errorhandler(400)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad Request"}),
            400,
        )

    return app
