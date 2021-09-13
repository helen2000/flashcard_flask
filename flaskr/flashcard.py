from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flask import flash


from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("flashcard", __name__)


@bp.route("/")
def index():
    """Show all the users packs, most recent first."""
    db = get_db()
    packs = db.execute(
        "SELECT p.id, pname, public, created, author_id, username"
        " FROM pack p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("flashcards/home.html", packs=packs)

def get_pack(id, check_author=True):
    """Get a pack and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of pack to get
    :param check_author: require the current user to be the author
    :return: the pack with author information
    :raise 404: if a pack with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    pack = (
        get_db()
        .execute(
            "SELECT p.id, pname, created, author_id, username"
            " FROM pack p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if pack is None:
        abort(404, f"pack id {id} doesn't exist.")

    if check_author and pack["author_id"] != g.user["id"]:
        abort(403)

    return pack


@bp.route("/create-pack", methods=("GET", "POST"))
@login_required
def create():
    """Create a new pack for the current user."""
    if request.method == "POST":
        pname = request.form["pname"]
       
        error = None

        if not pname:
            error = "name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO pack (pname, author_id) VALUES (?, ?)",
                (pname, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("flashcard.index"))

    return render_template("flashcards/createPack.html")

@bp.route("/<int:id>-pack/edit", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a pack if the current user is the author."""
    pack = get_pack(id)

    if request.method == "POST":
        pname = request.form["pname"]
        error = None

        if not pname:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE pack SET pname = ? WHERE id = ?", (pname, id)
            )
            db.commit()
            return redirect(url_for("flashcard.index"))

    return render_template("flashcards/editPack.html", pack=pack)  

@bp.route("/<int:id>-pack/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a pack.

    Ensures that the pack exists and that the logged in user is the
    author of the pack.
    """
    get_pack(id)
    db = get_db()
    db.execute("DELETE FROM pack WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("flashcard.index"))


#card code is below

@bp.route("/<int:id>-pack-view}")
def packIndex(id):
    """Show all the cards in the pack, most recent first."""
    db = get_db()
    s = db.execute(
            "SELECT c.id, front, back, pname, public, pack_id"
            " FROM cards c JOIN pack p ON c.pack_id= p.id"
    ).fetchall()
    cards = (
        get_db()
        .execute(
            "SELECT c.id, front, back, pname, public, pack_id"
            " FROM cards c JOIN pack p ON c.pack_id= p.id"
            " WHERE pack_id = ?", 
            (id,),
        )
        .fetchall()
    )
    pack = (
        get_db()
        .execute(
            "SELECT p.id, pname, created, author_id, username"
            " FROM pack p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )
    print(pack)
    print(cards)
   

    return render_template("flashcards/packView.html", cards=cards, pack=pack)

def get_card(id, check_pack=True):
    """Get a card and its pack by id.
    """
    card = (
        get_db()
        .execute(
            "SELECT c.id, front, back, pname, public, pack_id"
            " FROM cards c JOIN pack p ON c.pack_id= p.id"
            " WHERE c.id = ?",
            (id,),
        )
        .fetchone()
    )

    if card is None:
        abort(404, f"card id {id} doesn't exist.")

    

    return card


@bp.route("/<int:id>-create-card", methods=("GET", "POST"))
@login_required
def card_create(id):
    """Create a new card for the current user."""
    if request.method == "POST":
        front=request.form["front-input"]
        back=request.form["back-input"]
        error = None

        if not front or not back:
            error = "front and back are both required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO cards (front, back, pack_id) VALUES (?, ?, ?)",
                (front, back, id),
            )
            db.commit()
            return redirect(url_for("flashcard.packIndex", id=id))

    return render_template("flashcards/createCard.html")

@bp.route("/<int:packid>-<int:cardid>-card/edit", methods=("GET", "POST"))
@login_required
def card_update( packid, cardid):
    """Update a pack if the current user is the author."""
    card = get_card(cardid)

    if request.method == "POST":
        front=request.form["front-input"]
        back=request.form["back-input"]
        error = None
      
        if not front or not back:
            error = "front and back are both required."

        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            db.execute(
                "UPDATE cards SET front = ?, back = ? WHERE id = ?", (front, back, cardid)
            )
            db.commit()
            return redirect(url_for("flashcard.packIndex", id=packid))
            

    return render_template("flashcards/editCard.html", card=card)  

@bp.route("/<int:packid>-<int:cardid>-card/delete", methods=("POST",))
@login_required
def card_delete(packid, cardid):
    """Delete a card.

    Ensures that the pack exists and that the logged in user is the
    author of the pack.
    """
    get_card(cardid)
    db = get_db()
    db.execute("DELETE FROM cards WHERE id = ?", (cardid,))
    db.commit()
    return redirect(url_for("flashcard.packIndex", id=packid))

@bp.route("/<string:pname>-<int:cardid>-card-front")
def play_front(pname, cardid):
    """plays a pack by showing the front
    """

    card = (
        get_db()
        .execute(
            "SELECT c.id, front, back, pname, public, pack_id"
            " FROM cards c JOIN pack p ON c.pack_id= p.id"
            " WHERE c.id = ? AND pname = ?",
            (cardid, pname,),
        )
        .fetchone() 
        
    )
    if card == None:
        flash("END OF PACK")
        return redirect(url_for("flashcard.index"))
        
    
    
    return render_template("flashcards/frontCard.html", card=card)

@bp.route("/<string:pname>-<int:cardid>-card-back")
def play_back(pname, cardid):
    """plays a pack by showing back
    """

    card = (
        get_db()
        .execute(
            "SELECT c.id, front, back, pname, public, pack_id"
            " FROM cards c JOIN pack p ON c.pack_id= p.id"
            " WHERE c.id = ? AND pname = ?",
            (cardid, pname,),
        )
        .fetchone() 
    )
    
    return render_template("flashcards/backCard.html", card=card)