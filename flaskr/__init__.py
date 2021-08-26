import os


from flask import Flask, render_template, request, redirect
from flaskr.models import Pack
from flaskr.models import Cards

from flaskr.database import init_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )



    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a home page
    @app.route('/', methods=['POST', 'GET'])
    def home():
        packs=Pack.query.all()
        print(packs)
        return render_template('home.html', packs=packs)

    @app.route('/<int:id>', methods=['POST', 'GET'])
    def packDisplaSy(id):
        print(Pack.query.filter(Pack.id == id).first())
        print(Cards.query.filter(Cards.pack_id==id).all())
        try:
            return render_template('packView.html',  pack= Pack.query.filter(Pack.id == id).first(), cards = Cards.query.filter(Cards.pack_id==id).all())
        except:
            return "it was not possible to go into this pack"

    @app.route('/newpack', methods=['POST', 'GET'])
    def makeNewPack():
        
        if request.method =='POST':
            print("HERE")
            
            pack_name = request.form['pname']
            new_pack = Pack(name=pack_name)
            print(pack_name)
            print("NEW PACK", new_pack)
            try:
                init_db()
                from flaskr.database import db_session
                db_session.add(new_pack)
                db_session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                return ' there was an issue adding this to your database'
        else:
            return render_template('createPack.html')

    @app.route('/deletePack/<int:id>')
    def deletePack(id):
        pack_to_delete = Pack.query.filter(Pack.id == id).first()
        try:
            cards_to_delete = Pack.query.filter(Cards.pack_id==id).all()
            init_db()
            from flaskr.database import db_session
            db_session.delete(pack_to_delete)
            for each in cards_to_delete:
                db_session.delete(each)
            db_session.commit()
            return redirect('/')
        except:
            return "there is a problem deleting this pack"
    
    @app.route('/editPack/<int:id>', methods=['POST', 'GET'])
    def editPack(id):
        pack_to_edit = Pack.query.filter(Pack.id == id).first()
        if request.method =='POST':
            print("HERE")
            pack_to_edit.name = request.form['pname']
            
            try:
                init_db()
                from flaskr.database import db_session
                db_session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                return ' there was an issue editing your database'
        else:
            return render_template('editPack.html', pack = pack_to_edit)



    return app

   
    
            

''' @app.route('/<int:id>', methods=['POST', 'GET'])
    def packDisplay(id):
        pack_to_open = Pack.query.get_or_404(id)
        try:
            return render_template('packView.html',  pack= pack_to_open, card = Cards.query.filter(Cards.pack_id==id).all())
        except:
            return "it was not possible to go into this pack"
   
    from flaskr.database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app'''