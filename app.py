from website import create_app

app = create_app()

# Only when the main function is run, the app will run; So if the package is imported, it doesn't run the whole app
if __name__ == '__main__':
    app.run(debug=True) # debug: Whenever sth is changed, the app reruns to update / debug