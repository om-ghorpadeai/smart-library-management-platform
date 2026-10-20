from flask import Flask, jsonify, render_template


def create_app():
    app = Flask(__name__)

    books = [
        {
            "id": 1,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "available": True
        },
        {
            "id": 2,
            "title": "Python Crash Course",
            "author": "Eric Matthes",
            "available": True
        },
        {
            "id": 3,
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "available": True
        },
        {
            "id": 4,
            "title": "Introduction to Algorithms",
            "author": "Thomas H. Cormen",
            "available": True
        },
        {
            "id": 5,
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "available": True
        }
    ]

    @app.route("/")
    def home():
        return render_template("index.html", books=books)

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "UP",
            "service": "Smart Library Management Platform"
        }), 200

    @app.route("/api/books")
    def get_books():
        return jsonify(books), 200

    @app.route("/api/books/<int:book_id>/borrow", methods=["POST"])
    def borrow_book(book_id):
        book = next(
            (item for item in books if item["id"] == book_id),
            None
        )

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        if not book["available"]:
            return jsonify({"error": "Book is already borrowed"}), 409

        book["available"] = False

        return jsonify({
            "message": "Book borrowed successfully",
            "book": book
        }), 200

    @app.route("/api/books/<int:book_id>/return", methods=["POST"])
    def return_book(book_id):
        book = next(
            (item for item in books if item["id"] == book_id),
            None
        )

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        book["available"] = True

        return jsonify({
            "message": "Book returned successfully",
            "book": book
        }), 200

    return app
