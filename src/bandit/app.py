import json

from flask import Flask, request
import numpy as np
import logging
import os


def create_app(model):
    """App factory pattern"""
    app = Flask(__name__)

    @app.route('/v1/models/<model_name>')
    def readiness(model_name):
        return {"name": "custom", "ready": True, "version": os.environ.get("VERSION")}

    @app.route("/v1/models/<model_name>:predict", methods=["post"])
    def predict(model_name):
        app.logger.info(model)
        data = request.data
        app.logger.info("predicting on %s", data)
        coefs = np.array([3, 4])
        return {"predictions": coefs}

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app