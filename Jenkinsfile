//pipeline declaration
pipeline{

    //agent definition
    agent any


    environment {
        IMAGE_NAME = "flask-app"
    }

    stages{
        stage('checkout') {
            steps{
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'echo Running tests'
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m pytest'
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                sh "docker run -d -p 5000:5000 ${IMAGE_NAME}"
            }
        }

    }
}