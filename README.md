# DevOps Lab 1: DevOps Foundations & Continuous Integration

**Student:** Srishti Kainth | **Roll No.:** 2301730175 | **Email:** srishtikainth2@gmail.com
**Course:** DevOps and Automation (ENSP461)
**Environment:** Ubuntu 24.04 LTS, Git, GitHub, VS Code, Jenkins, Docker

A small Flask app that Jenkins builds, tests, packages and deploys on every push to `main`.

| File | Purpose |
|---|---|
| `app.py` | Flask app: `/`, `/health`, `/api/info`, `/api/add/<a>/<b>` |
| `test_app.py` | 5 pytest tests, published to Jenkins as a JUnit report |
| `requirements.txt` | Pinned dependencies (Flask, gunicorn, pytest) |
| `Dockerfile` | Python 3.12 slim image, non-root user, gunicorn |
| `deploy.sh` | Builds the image, replaces the running container, health-checks `/health` |
| `Jenkinsfile` | Pipeline: Checkout → Build → Test → Package → Deploy → Verify |

## Run locally

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -v
python3 app.py            # http://localhost:5000
./deploy.sh local         # deploy with Docker
```

## Jenkins setup (Ubuntu 24.04)

```bash
sudo apt install -y fontconfig openjdk-21-jre git python3-venv docker.io
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt update && sudo apt install -y jenkins
sudo usermod -aG docker jenkins && sudo systemctl restart jenkins
```

Job: **New Item → Pipeline → Pipeline script from SCM → Git**
- Repository URL: `https://github.com/srishhk/DevOps-LAB1.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`
- Build Triggers: *GitHub hook trigger for GITScm polling*

Plugins: Git, GitHub, Pipeline, Pipeline: Stage View, JUnit, Workspace Cleanup, Timestamper.
