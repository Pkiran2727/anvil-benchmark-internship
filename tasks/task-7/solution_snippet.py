"""Solution for Task 7: modify get_items to support ?q= search."""

# Replace the get_items function with:
@app.route("/api/items", methods=["GET"])
def get_items():
    q = request.args.get("q", "").strip()
    if q:
        items = Item.query.filter(Item.name.ilike(f"%{q}%")).all()
    else:
        items = Item.query.all()
    return jsonify([i.to_dict() for i in items]), 200
