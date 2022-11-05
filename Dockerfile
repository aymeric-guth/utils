# syntax=docker/dockerfile:1.4
ARG DOCKER_IMAGE

FROM $DOCKER_IMAGE AS base-layer
ARG PROJECT_NAME
ENV PROJECT_NAME=$PROJECT_NAME
ENV WORKSPACE=/$PROJECT_NAME
COPY . $WORKSPACE
WORKDIR $WORKSPACE


FROM base-layer AS stagging-common
RUN python3 -m pip install --no-cache-dir \
    virtualenv \
    setuptools \
    build
RUN python3 -m virtualenv .venv
RUN . .venv/bin/activate


FROM stagging-common AS stagging
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -c "print('coucou')"
#RUN python3 -m build . --wheel
