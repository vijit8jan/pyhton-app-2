pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/your-repo/your-python-project.git'
        GIT_CREDENTIALS_ID = 'your-git-credentials-id'
        SONARQUBE_SCANNER_HOME = tool name: 'SonarQube Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
        SONARQUBE_SERVER = 'your-sonarqube-server-id'
        DOCKER_IMAGE_NAME = 'your-docker-image-name'
        DOCKER_CREDENTIALS_ID = 'your-docker-credentials-id'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: GIT_REPO_URL,
                        credentialsId: GIT_CREDENTIALS_ID
                    ]]
                ])
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh './venv/bin/pip install -r requirements.txt'
                    echo 'Build stage completed.'
                }
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SCANNER_HOME = "${SONARQUBE_SCANNER_HOME}"
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=your-project-key -Dsonar.sources=src/main/python -Dsonar.tests=src/test/python -Dsonar.host.url=${SONARQUBE_SERVER}"
                }
            }
        }

        stage('Code Coverage') {
            steps {
                script {
                    sh './venv/bin/coverage run -m pytest'
                    sh './venv/bin/coverage report'
                    sh './venv/bin/coverage xml'
                    echo 'Code coverage stage completed.'
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE_NAME} .'
                    echo 'Docker image built.'
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        sh "docker push ${DOCKER_IMAGE_NAME}"
                    }
                    echo 'Docker image pushed.'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
