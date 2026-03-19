# 🚀 Flask App CI/CD Pipeline with Docker and Jenkins

This project demonstrates a fully containerised Flask application built and tested through a Jenkins CI pipeline.

The environment uses **Docker-in-Docker (dind)** to provide a clean and isolated Docker daemon for Jenkins, allowing the pipeline to build images without relying on host-level Docker access.

---

## 📦 Project Structure
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── README.md


---

## 🧰 Technologies Used

- **Python / Flask** — simple web application  
- **Docker** — containerisation for the application  
- **Docker-in-Docker (dind)** — isolated Docker daemon for Jenkins  
- **Jenkins Pipeline (Declarative)** — automated CI build stages  
- **GitHub** — source control and Jenkins integration  

---

## 🔧 Running the Flask App Locally (Optional)

Install dependencies and run the app:

```bash
pip install -r requirements.txt
python app.py

Visit in your browser: http://localhost:5000

🐳 Building the Docker Image Manually

From the root of the project:

docker build -t flask-app -f Dockerfile .

Run the container:

docker run -d -p 5000:5000 --name flask-app-container flask-app

⚙️ Jenkins CI/CD Pipeline

This project includes a Jenkinsfile that:

Checks out the repository

Connects to the remote Docker daemon (dind)

Runs a Docker sanity check

Builds the Docker image

Example Pipeline Stages

pipeline {
    agent any

    environment {
        DOCKER_HOST       = 'tcp://docker:2376'
        DOCKER_TLS_VERIFY = '1'
        DOCKER_CERT_PATH  = '/certs/client'
    }

    stages {
        stage('Docker Sanity') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t flask-app -f Dockerfile .'
            }
        }
    }
}

🏗️ Jenkins + Docker-in-Docker Setup (Controller)

This project expects Jenkins to run from a custom image that includes the Docker CLI.

Example Jenkins Controller Dockerfile

FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y lsb-release curl && \
    curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc https://download.docker.com/linux/debian/gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli

USER jenkins

Docker-in-Docker Service

Run a dedicated Docker daemon for Jenkins: docker run -d \
  --name jenkins-docker \
  --privileged \
  --network jenkins \
  --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --publish 2376:2376 \
  docker:dind \
  --storage-driver overlay2


🔗 Connecting Jenkins to GitHub

Configure your Jenkins job as:

Type: Pipeline → Pipeline script from SCM

SCM: Git

Repository URL:

https://github.com/yourusername/flask-app.git

Branch: main

Script Path: Jenkinsfile

✔️ Future Enhancements

Add automated testing (e.g., pytest)

Add deployment stages

Push Docker images to Docker Hub or GHCR

Add GitHub webhooks for automatic build triggers


📄 License

This project is open source and licensed under the MIT License.


---

If you want, I can also upgrade this with:
- CI/CD diagram (great for portfolios)
- GitHub badges (build status, Docker pulls)
- A “production-ready” version with deploy stage (e.g., Kubernetes or EC2)

Just tell me 👍

