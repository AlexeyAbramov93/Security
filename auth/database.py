TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://sql_app.db"
    },
    "apps": {
        "contact": {
            "models": [
                "auth.models", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}