ARG BASE_IMAGE=docker.io/python:3.8.7-slim-buster
ARG SOURCE_DIR_PATH=/location-guessing-game-telegram-bot


# hadolint ignore=DL3006
FROM $BASE_IMAGE as build

RUN apt-get update \
    && apt-get install --no-install-recommends --yes ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home build

USER build
RUN pip install --user --no-cache-dir pipenv==2020.11.15

ARG SOURCE_DIR_PATH
COPY --chown=build Pipfile Pipfile.lock $SOURCE_DIR_PATH/
WORKDIR $SOURCE_DIR_PATH
ENV PIPENV_CACHE_DIR=/tmp/pipenv-cache \
    PIPENV_VENV_IN_PROJECT=yes-please \
    PATH=/home/build/.local/bin:$PATH
RUN pipenv install --deploy \
    && pipenv graph \
    && pipenv run pip freeze \
    && rm -rf $PIPENV_CACHE_DIR
COPY --chown=build . $SOURCE_DIR_PATH
RUN chmod -cR a+rX .

# workaround for broken multi-stage copy
# > failed to copy files: failed to copy directory: Error processing tar file(exit status 1): Container ID ... cannot be mapped to a host ID
USER 0
RUN chown -R 0:0 $SOURCE_DIR_PATH
USER build


# hadolint ignore=DL3006
FROM $BASE_IMAGE

RUN apt-get update \
    && apt-get install --no-install-recommends --yes ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && find / -xdev -type f -perm /u+s -exec chmod -c u-s {} \; \
    && find / -xdev -type f -perm /g+s -exec chmod -c g-s {} \;

USER nobody

ARG SOURCE_DIR_PATH
COPY --from=build $SOURCE_DIR_PATH $SOURCE_DIR_PATH
ENV PATH=$SOURCE_DIR_PATH/.venv/bin:$PATH
WORKDIR $SOURCE_DIR_PATH
CMD ["python", "location_guessing_game_telegram_bot.py"]
