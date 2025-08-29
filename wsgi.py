from app import create_app

application = create_app()

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # dev run
    application.run(host="0.0.0.0", port=5000, debug=True)
