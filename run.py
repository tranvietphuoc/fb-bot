from apps import create_app, PORT


app = create_app()

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
