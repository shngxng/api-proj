from app import create_app

app = create_app()

# Run application
if __name__ == '__main__':
    app.run(debug=True)