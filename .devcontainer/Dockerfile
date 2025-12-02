# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-trixie

# Install system dependencies, including git and ngspice
RUN apt-get update \
    && apt-get install -y --no-install-recommends ngspice \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define the user and group (VS Code convention)
ARG USERNAME=vscode
ARG GROUPNAME=vscode
ARG UID=1000
ARG GID=1000

# Generic default value, shoulds be overwritten in devcontainer.json
ARG PROJECT_ROOT=/workspaces/project-name
ENV APP_HOME=${PROJECT_ROOT}

RUN addgroup --gid $GID $GROUPNAME \
    && adduser --uid $UID --gid $GID --disabled-password $USERNAME \
    && mkdir -p $APP_HOME \
    && chown -R $USERNAME:$GROUPNAME $APP_HOME

WORKDIR ${APP_HOME}

# Switch to the non-root user for security
USER $USERNAME
