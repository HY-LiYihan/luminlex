FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir streamlit openai -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health || exit 1

ENTRYPOINT ["sh", "-c", "pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ && streamlit run streamlit_app.py --server.port=8502 --server.address=0.0.0.0"]
