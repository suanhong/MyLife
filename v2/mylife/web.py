from __future__ import annotations

from datetime import date

from flask import Blueprint, abort, jsonify, request

from .repository import DiaryEntry, DiaryRepository


def create_diary_blueprint(repo: DiaryRepository) -> Blueprint:
    bp = Blueprint("diary", __name__)

    @bp.get("/api/diaries")
    def list_diaries():
        try:
            limit = int(request.args.get("limit", "30"))
        except ValueError:
            abort(400)
        if limit < 1 or limit > 365:
            abort(400)
        return jsonify(entries=[{"date": entry.diary_date.isoformat(), "text": entry.text,
                                 "image_ids": list(entry.image_ids)} for entry in repo.recent(limit)])

    @bp.get("/api/diaries/<diary_date>")
    def get_diary(diary_date: str):
        try:
            day = date.fromisoformat(diary_date)
        except ValueError:
            abort(400)
        entry = repo.get(day)
        if entry is None:
            abort(404)
        return jsonify(date=entry.diary_date.isoformat(), text=entry.text,
                       image_ids=list(entry.image_ids))

    @bp.put("/api/diaries/<diary_date>")
    def put_diary(diary_date: str):
        try:
            day = date.fromisoformat(diary_date)
        except ValueError:
            abort(400)
        payload = request.get_json(silent=True) or {}
        text = payload.get("text")
        if not isinstance(text, str):
            abort(400)
        repo.save(DiaryEntry(day, text, tuple(payload.get("image_ids") or ())))
        return jsonify(status="saved"), 200

    @bp.delete("/api/diaries/<diary_date>")
    def delete_diary(diary_date: str):
        try:
            day = date.fromisoformat(diary_date)
        except ValueError:
            abort(400)
        return ("", 204) if repo.delete(day) else abort(404)

    return bp
