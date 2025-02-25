from flask import Flask, render_template, redirect, url_for, request, flash
from db import mysql
from flask import session

app = Flask(__name__)

# REVIEWS
def model_reviews():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT tbl_review.id_review, tbl_review.review_text, tbl_review.rating, tbl_user.name, tbl_profile.profile_picture
        FROM tbl_review
        JOIN tbl_user ON tbl_review.id_user = tbl_user.id_user
        LEFT JOIN tbl_profile ON tbl_user.id_user = tbl_profile.id_user
        ORDER BY tbl_review.id_review DESC
    """)
    reviews = cur.fetchall()
    cur.close()

    return render_template('user/buyer/review.html', data_reviews=reviews)

# ADD REVIEW
def model_add_review():
    if request.method == "POST":
        review_text = request.form['review_text']
        rating = request.form['rating']

        # Ensure rating is a valid integer
        try:
            rating = int(rating)
        except ValueError:
            flash("Invalid rating. Please enter a number between 1 and 5.", "danger")
            return redirect(url_for('write_review'))

        # Check if rating is within 1-5
        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.", "danger")
            return redirect(url_for('write_review'))
        if "loggedin" in session:
            id_user = session['id_user']
        else:
            flash("You must be logged in to write a review.", "danger")
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO tbl_review (id_user, review_text, rating)
            VALUES (%s, %s, %s)
        """, (id_user, review_text, rating))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('reviews'))

    return render_template('user/buyer/write_review.html')
