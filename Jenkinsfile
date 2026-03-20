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

  stages {
    stage('Smoke') {
      agent {
        docker {
          image 'python:3.14'
          args '--user root' // run as root to avoid pip permission issues
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
          args '--user root' // root so pip can install to system site-packages
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

    stage('Build') {
      agent {
        docker {
          image 'docker:24.0-cli'
          // Connect to the dind sidecar over TLS on the 'jenkins' network
          args '''
            --network jenkins
            -e DOCKER_HOST=tcp://docker:2376
            -e DOCKER_CERT_PATH=/certs/client
            -e DOCKER_TLS_VERIFY=1
            -v jenkins-docker-certs:/certs/client:ro
          '''
          reuseNode true
        }
      }
      environment {
        IMAGE_NAME = "flask-app:${env.BUILD_NUMBER}"
      }
      steps {
        sh 'docker version'
        sh 'docker build -t "$IMAGE_NAME" .'
      }
    }

    stage('Run Container') {
      agent {
        docker {
          image 'docker:24.0-cli'
          args '''
            --network jenkins
            -e DOCKER_HOST=tcp://docker:2376
            -e DOCKER_CERT_PATH=/certs/client
            -e DOCKER_TLS_VERIFY=1
            -v jenkins-docker-certs:/certs/client:ro
          '''
          reuseNode true
        }
      }
      environment {
        IMAGE_NAME = "flask-app:${env.BUILD_NUMBER}"
      }
      steps {
        // Stop any prior container if needed
        sh 'docker ps -aqf "name=^flask-app$" | xargs -r docker rm -f || true'
        sh 'docker run -d --name flask-app -p 5000:5000 "$IMAGE_NAME"'
      }
    }
  }
}

