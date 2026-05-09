

# AWS CI Pipeline Demo 🚀

This project demonstrates how to build a simple Continuous Integration (CI) pipeline using AWS services, Docker, and a Flask application.

The pipeline automatically detects changes pushed to GitHub, triggers a build using AWS CodeBuild, containerizes the Flask application with Docker, and pushes the image to Docker Hub.

The main goal of this project was to gain hands-on experience with:

- AWS CodePipeline
- AWS CodeBuild
- AWS Systems Manager Parameter Store
- IAM roles and permissions
- Docker containerization
- CI workflow automation
- Secure secrets management

---

# Project Architecture

```text
GitHub Push → CodePipeline → CodeBuild → Docker Build → Docker Hub
```

Workflow overview:

1. Developer pushes code to GitHub
2. CodePipeline detects the repository change
3. CodePipeline triggers CodeBuild automatically
4. CodeBuild retrieves Docker credentials securely from AWS Parameter Store
5. Docker image is built inside CodeBuild
6. Docker image is pushed to Docker Hub

This removes the need for manual Docker builds and image pushes.

---

# Technologies Used

- Python 3.11
- Flask
- Docker
- AWS CodeBuild
- AWS CodePipeline
- AWS Systems Manager Parameter Store
- IAM
- Docker Hub
- GitHub

---

# Project Structure

```bash
aws-ci-tools-demo/
│
├── app.py
├── Dockerfile
├── buildspec.yml
├── requirement.txt
└── README.md
```

---

# Flask Application

The application is a lightweight Flask API with three routes.

## app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my DevOps Journey"

@app.route('/about')
def about():
    return "Mustapha is a fast, curious learner with a can do attitude. In pursuit of being a cracked Engineer!"

@app.route('/DevOps')
def devops():
    return "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and deliver software faster."


if __name__ == '__main__':
    app.run(debug=True)
```

Available routes:

| Route | Description |
|---|---|
| `/` | Home page |
| `/about` | About section |
| `/DevOps` | DevOps description |

---

# Docker Configuration

The Flask application is containerized using Docker.

## Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

## What This Dockerfile Does

- Uses a lightweight Python base image
- Creates `/app` as the working directory
- Copies dependency files into the container
- Installs Python dependencies
- Copies application source code
- Exposes Flask on port 5000
- Starts the Flask application automatically

---

# Python Dependencies

Your `requirement.txt` file should contain Python packages only.

## requirement.txt

```txt
Flask==3.0.3
```

Note:
Your original `requirement.txt` content appears to accidentally contain Dockerfile instructions instead of Python dependencies. The example above is the correct format for the file.

---

# AWS CodeBuild Configuration

The build process is defined in `buildspec.yml`.

## buildspec.yml

```yaml
version: 0.2

env:
  parameter-store:
    DOCKER_USERNAME: /app/docker/username
    DOCKER_PASSWORD: /app/docker/password
    DOCKER_URL: /app/docker/url

phases:
  install:
    runtime-versions:
      python: 3.11

  pre_build:
    commands:
      - echo "Installing dependencies..."
      - pip install -r aws-ci-tools-demo/requirement.txt

  build:
    commands:
      - echo "Running tests..."
      - cd aws-ci-tools-demo/
      - echo "Building Docker image..."
      - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "$DOCKER_URL"
      - docker build -t "$DOCKER_URL/$DOCKER_USERNAME/aws-ci-tools-demo:latest" .
      - docker push "$DOCKER_URL/$DOCKER_USERNAME/aws-ci-tools-demo:latest"

  post_build:
    commands:
      - echo "Build completed successfully!"
```

---

# Important CodeBuild Requirement

CodeBuild must run in Privileged Mode for Docker builds to work.

When creating the CodeBuild project:

- Environment Image: Managed Image
- Operating System: Ubuntu
- Runtime: Standard
- Enable: Privileged Mode

Without Privileged Mode enabled, Docker commands inside CodeBuild will fail.

---

# Why Parameter Store Matters

One of the biggest lessons learned during this project was proper secrets management.

Hardcoding Docker credentials directly inside `buildspec.yml` works temporarily, but it creates security risks and makes credential rotation difficult.

Instead, Docker credentials are stored securely inside AWS Systems Manager Parameter Store using `SecureString` values.

Benefits:

- Keeps credentials out of source control
- Improves security practices
- Makes secret rotation easier
- Keeps build configuration cleaner

---

# Setting Up AWS Parameter Store

Create the following parameters inside AWS Systems Manager Parameter Store:

| Parameter Name | Type |
|---|---|
| `/app/docker/username` | SecureString |
| `/app/docker/password` | SecureString |
| `/app/docker/url` | String |

Example values:

```text
/app/docker/username = your-dockerhub-username
/app/docker/password = your-dockerhub-password
/app/docker/url = docker.io
```

---

# IAM Permissions for CodeBuild

The IAM role attached to CodeBuild must have permission to retrieve parameters from AWS Systems Manager Parameter Store.

Example policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameters",
        "ssm:GetParameter"
      ],
      "Resource": "*"
    }
  ]
}
```

Additional permissions are typically required for:

- CloudWatch Logs
- Amazon S3
- CodeBuild
- Docker image operations

---

# Setting Up CodeBuild

## Step 1 — Create a Build Project

Inside AWS CodeBuild:

1. Create a new build project
2. Choose GitHub as the source provider
3. Connect your repository
4. Select a managed Ubuntu image
5. Enable Privileged Mode
6. Use the repository buildspec file

CodeBuild will now use `buildspec.yml` automatically during builds.

---

# Setting Up CodePipeline

## Step 1 — Create a Pipeline

Inside AWS CodePipeline:

1. Create a new pipeline
2. Select GitHub as the source provider
3. Connect the repository
4. Enable automatic change detection
5. Add CodeBuild as the build provider
6. Select the existing CodeBuild project

Once configured, every push to GitHub automatically triggers the CI pipeline.

---

# Running the Project Locally

## Clone the Repository

```bash
git clone <your-repository-url>
cd aws-ci-tools-demo
```

## Install Dependencies

```bash
pip install -r requirement.txt
```

## Run the Flask Application

```bash
python app.py
```

Application URL:

```text
http://127.0.0.1:5000
```

---

# Running with Docker Locally

## Build Docker Image

```bash
docker build -t aws-ci-tools-demo .
```

## Run Docker Container

```bash
docker run -p 5000:5000 aws-ci-tools-demo
```

---

# Example CI Workflow

```text
Developer pushes code to GitHub
        ↓
CodePipeline detects repository changes
        ↓
CodeBuild starts automatically
        ↓
Parameter Store injects Docker credentials
        ↓
Docker image is built
        ↓
Docker image is pushed to Docker Hub
```

---

# What I Learned

This project helped strengthen my understanding of:

- CI/CD automation
- AWS service integration
- Docker image workflows
- Secure credential management
- IAM role permissions
- End-to-end pipeline orchestration

It also reinforced the importance of not hardcoding secrets directly into configuration files.

---

