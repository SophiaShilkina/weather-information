from urls import app
import logging


HOST = "127.0.0.1"
PORT = 8000


if __name__ == '__main__':
    import uvicorn
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:    %(message)s')
    uvicorn.run(app, host=HOST, port=PORT)
