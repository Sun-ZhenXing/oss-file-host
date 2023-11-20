FROM python:3.10-bookworm as builder

WORKDIR /app

ARG PYPI_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY . ./

RUN pip -V \
    && pip config set global.index-url ${PYPI_MIRROR_URL} \
    && python -m pip install -U pip \
    && pip install Cython \
    && python setup.py build_ext -b lib \
    && cp -rf requirements.txt lib/

FROM python:3.10-slim-bookworm

WORKDIR /app

COPY --from=builder /app/lib /app

RUN pip -V \
    && pip config set global.index-url ${PYPI_MIRROR_URL} \
    && python -m pip install -U pip \
    && pip install -r requirements.txt

EXPOSE 8000

CMD [ "sanic", "server:app", "--host=0.0.0.0", "--port=8000", "--fast" ]
