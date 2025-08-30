from authx import AuthX, AuthXConfig
import os
import logging

logging.basicConfig(level=logging.INFO)

config = AuthXConfig()
config.JWT_ALGORITHM="HS256"
config.JWT_SECRET_KEY=os.getenv("SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "mindForgeCookie"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)
