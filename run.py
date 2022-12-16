from blog import create_app, db
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # disable debug mode when deploy on server
        # This tells your operating system to listen on all public IPs.
        app.run(host='0.0.0.0')

