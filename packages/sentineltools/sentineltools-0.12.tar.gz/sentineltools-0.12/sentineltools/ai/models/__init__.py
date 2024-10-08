import os

DEFAULT_LOCAL_MODEL_DOWNLOAD = os.path.abspath(
    os.path.join("models", "pretrained"))


def assign_local_model_download(path: str = DEFAULT_LOCAL_MODEL_DOWNLOAD):
    os.environ['TORCH_HOME'] = path
