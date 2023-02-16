import os

def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    assert test_app.config["SECRET_KEY"] == "change_me"
    assert test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("TEST_DB_URI")
