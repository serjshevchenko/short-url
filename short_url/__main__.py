import uvicorn

from short_url.config import config
from short_url.api.application import create_application

app = create_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)  # noqa
