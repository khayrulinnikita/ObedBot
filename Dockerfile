FROM python:3.8-slim
RUN groupadd --gid 2000 worker \
  && useradd --uid 2000 --gid worker --shell /bin/bash --create-home worker
USER worker
WORKDIR /bot
COPY --chown=worker:worker requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=worker:worker main.py photo.jpg /bot/

ENTRYPOINT ["python", "main.py"]