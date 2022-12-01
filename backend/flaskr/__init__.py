import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated(request, selection):
    page = request.args.get("page", 1, type=int)
    # calculate the start and end of the required questions
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # format the selection
    questions = [question.format() for question in selection]
    # requested questions
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app) # Allow CORS for all domains on all routes.
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        # True means allow cookies
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        # Query the categories
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in selection}
        
        if len(categories) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(Category.query.all())
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=['GET'])
    def get_questions():
        try:
            # Query the categories
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {category.id: category.type for category in categories}

            # Query the questions
            current_questions = []
            questions = Question.query.order_by(Question.id).all()
            #print("questions: {}".format(questions))
            if questions == []:
                abort(422)
            
            current_questions = paginated(request, questions)
            #print("current_questions: {}".format(current_questions))
            if current_questions == []:
                abort(422)
                
            return jsonify({
                "success": True,
                "total_questions": len(Question.query.all()),
                "questions": current_questions,
                "categories": formatted_categories,
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
  
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            # Query the category_id's type
            current_category = Category.query.filter(Category.id==category_id).one_or_none() #returns obj
            # Query the questions of the category_id
            questions = Question.query.filter(Question.category==category_id).all()
            current_questions = paginated(request, questions)
          
            if not current_category or not questions:
                abort(404)
        
            return jsonify({
                "success": True,
                "total_questions": len(questions),
                "questions": current_questions,
                "categories": current_category.type
            })
        except Exception as error:
            print(error)
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
                }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "unprocessable"
                }),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "bad request"
                }), 
            400
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405, 
                "message": "method not allowed"
                }), 
            405
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "internal error"
                }), 
            500
        )
    return app
    

