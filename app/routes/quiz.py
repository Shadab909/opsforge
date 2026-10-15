from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from app.routes.auth import login_required
from app.content_loader import get_topic, get_module, get_chunk, get_chunk_quiz
from app.database import save_quiz_attempt, get_chunk_progress

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/<topic_slug>/<module_slug>/<chunk_slug>/quiz", methods=["GET"])
@login_required
def take_quiz(topic_slug, module_slug, chunk_slug):
    topic = get_topic(topic_slug)
    module = get_module(topic_slug, module_slug)
    chunk = get_chunk(topic_slug, module_slug, chunk_slug)
    quiz_data = get_chunk_quiz(topic_slug, module_slug, chunk_slug)

    if not topic or not module or not chunk or not quiz_data:
        abort(404)

    username = session.get("username")
    progress = get_chunk_progress(username, topic_slug, module_slug, chunk_slug)

    questions = quiz_data.get("questions", [])
    passing_score = quiz_data.get("passing_score", 70)

    return render_template(
        "quiz.html",
        topic=topic,
        module=module,
        chunk=chunk,
        questions=questions,
        passing_score=passing_score,
        progress=progress
    )

@quiz_bp.route("/<topic_slug>/<module_slug>/<chunk_slug>/quiz", methods=["POST"])
@login_required
def submit_quiz(topic_slug, module_slug, chunk_slug):
    topic = get_topic(topic_slug)
    module = get_module(topic_slug, module_slug)
    chunk = get_chunk(topic_slug, module_slug, chunk_slug)
    quiz_data = get_chunk_quiz(topic_slug, module_slug, chunk_slug)

    if not topic or not module or not chunk or not quiz_data:
        abort(404)

    username = session.get("username")
    questions = quiz_data.get("questions", [])
    passing_score = quiz_data.get("passing_score", 70)

    total_q = len(questions)
    correct_count = 0
    results = []
    answers_saved = {}

    for idx, q in enumerate(questions):
        user_val = request.form.get(f"q_{idx}")
        expected = q.get("correct")
        
        # Normalize boolean for true_false
        if q.get("type") == "true_false":
            user_bool = (user_val == "true") if user_val in ("true", "false") else None
            is_correct = (user_bool == expected)
            user_display = "True" if user_bool is True else ("False" if user_bool is False else "No Answer")
            correct_display = "True" if expected is True else "False"
        else:
            is_correct = (user_val == expected)
            user_display = user_val or "No Answer"
            correct_display = expected

        if is_correct:
            correct_count += 1

        answers_saved[str(idx)] = user_val
        results.append({
            "index": idx + 1,
            "question": q.get("question"),
            "user_answer": user_display,
            "correct_answer": correct_display,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    score = round((correct_count / total_q) * 100) if total_q > 0 else 0
    passed = score >= passing_score

    # Save to user database
    save_quiz_attempt(
        username=username,
        topic_slug=topic_slug,
        module_slug=module_slug,
        chunk_slug=chunk_slug,
        score=score,
        total_questions=total_q,
        correct_count=correct_count,
        answers=answers_saved,
        passing_score=passing_score
    )

    return render_template(
        "quiz_result.html",
        topic=topic,
        module=module,
        chunk=chunk,
        score=score,
        total=total_q,
        correct_count=correct_count,
        passed=passed,
        passing_score=passing_score,
        results=results
    )
