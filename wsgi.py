import os

from bandit.app import create_app

# model = pickle.load((os.environ.get("MODEL_STORAGE_PATH"))
model = f'I am a model {os.environ.get("MODEL_STORAGE_PATH")}'
app = create_app(model)