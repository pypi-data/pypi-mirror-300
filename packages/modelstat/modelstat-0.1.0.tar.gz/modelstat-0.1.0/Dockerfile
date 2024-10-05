FROM python:3.12.2-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements_apt /tmp/requirements_apt
COPY requirements_pip /tmp/requirements_pip
COPY requirements.txt /tmp/requirements.txt
RUN groupadd -r user && useradd -m -r -g user user
RUN apt-get clean \
    && apt-get update \
    && xargs -a /tmp/requirements_apt apt-get install -y \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r /tmp/requirements_pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements_*
RUN mkdir -p /home/user/.vscode-server \
    && chown -R user:user /home/user/.vscode-server
WORKDIR /home/user/work
COPY --chown=user:user . .
USER user
WORKDIR /home/user/work/
CMD ["tail", "-f", "/dev/null"]
