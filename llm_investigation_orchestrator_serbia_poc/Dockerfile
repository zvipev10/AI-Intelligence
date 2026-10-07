# AI-Intelligence analyst UI on i360. Build context: this directory.
#
#   docker build -t ai-intelligence .
#   docker run -p 8080:8080 -e HL_API_URL=http://platform-hl-api:8080 ai-intelligence
#
# Runtime is the Python 3.12 standard library only. The tests run during the build, in a
# separate stage, so a failing test fails the image build and no test tooling ships.

ARG PYTHON_IMAGE=python:3.12-slim

FROM ${PYTHON_IMAGE} AS test
# Node runs the UI tests (they evaluate slices of app.js); nothing else is installed.
RUN apt-get update \
 && apt-get install -y --no-install-recommends nodejs \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . .
RUN python -m unittest discover -s tests -t . \
 && python -m unittest discover -s . -p 'test_*.py' \
 && for test in test_*.cjs; do node "$test" > /dev/null || exit 1; done \
 && touch /tests-passed

FROM ${PYTHON_IMAGE}
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_HOST=0.0.0.0
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
WORKDIR /app
# Proof the test stage ran (BuildKit skips stages nothing depends on).
COPY --from=test /tests-passed /app/.tests-passed
COPY server.py analysis.py catalog_filters.py link_graph.py ./
COPY hl/ hl/
COPY mapping/ mapping/
COPY demo_profiles/ demo_profiles/
COPY index.html app.js styles.css polygon_draw.js demo_bootstrap.js help.html \
     investigation-user-flow.html system-capabilities-guide.html ./
COPY vendor/ vendor/
COPY assets/ assets/
USER 10001
EXPOSE 8080
CMD ["python", "server.py"]
