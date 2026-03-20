// //pipeline declaration
// pipeline{

//     //agent definition
//     agent {
//         agent { dockerfile { filename 'Dockerfile' } } // runs the pipeline inside Python 3.11 container
//     }


//     environment {
//         IMAGE_NAME = "flask-app"
//     }

//     stages{
//         stage('checkout') {
//             steps{
//                 checkout scm
//             }
//         }

//         stage('Test') {
//             steps {
//                 sh 'echo Running tests'
//                 sh 'python3 -m pip install --upgrade pip'
//                 sh 'python3 -m pip install -r requirements.txt'
//                 sh 'python3 -m pytest'
//             }
//         }

//         stage('Build') {
//             steps {
//                 sh "docker build -t ${IMAGE_NAME} ."
//             }
//         }

//         stage('Run Container') {
//             steps {
//                 sh "docker run -d -p 5000:5000 ${IMAGE_NAME}"
//             }
//         }

//     }
// }




pipeline {
  agent none

  environment {
    IMAGE_NAME = "flask-app:${env.BUILD_NUMBER}"
  }

  stages {

    stage('Smoke') {
      agent {
        docker {
          image 'python:3.14'
          args '--user root'
        }
      }
      steps {
        sh 'echo IN_CONTAINER=$(head -1 /etc/os-release)'
      }
    }

    stage('Checkout') {
      agent any
      steps {
        checkout scm
      }
    }

    stage('Test') {
      agent {
        docker {
          image 'python:3.14'
          args '--user root'
        }
      }
      steps {
        sh '''
          set -e
          echo "Running tests"
          python3 -m pip install -r requirements.txt
          python3 -m pytest
        '''
      }
    }

    stage('Build (Host Docker)') {
      agent {
        docker {
          image 'docker:24.0-cli'
          // USE HOST DOCKER
          args '-v //var/run/docker.sock:/var/run/docker.sock'
          reuseNode true
        }
      }
      steps {
        sh 'docker version'
        sh 'docker build -t "$IMAGE_NAME" .'
      }
    }

    stage('Run Container (Host Docker)') {
      agent {
        docker {
          image 'docker:24.0-cli'
          // USE HOST DOCKER
          args '-v //var/run/docker.sock:/var/run/docker.sock'
          reuseNode true
        }
      }
      steps {
        sh '''
          set -e
          docker ps -aqf "name=^flask-app$" | xargs -r docker rm -f || true
          docker run -d --name flask-app -p 5000:5000 "$IMAGE_NAME"
          docker ps
        '''
      }


