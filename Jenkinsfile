// DevOps Lab 1 - Declarative CI/CD pipeline
// Student: Srishti Kainth (2301730175)
// Jenkins job: "Pipeline script from SCM"
//   Repository: https://github.com/srishhk/DevOps-LAB1.git, Branch: */main, Script Path: Jenkinsfile

pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 20, unit: 'MINUTES')
    }

    triggers {
        // GitHub webhook trigger (needs the GitHub plugin). Poll as a fallback
        // when Jenkins is not reachable from the internet.
        githubPush()
        pollSCM('H/5 * * * *')
    }

    environment {
        APP_VERSION = '1.0.0'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip -q
                    pip install -r requirements.txt -q
                    python -m py_compile app.py
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/lab1-app-${BUILD_NUMBER}.tar.gz app.py requirements.txt Dockerfile deploy.sh
                    sha256sum dist/*.tar.gz
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                sh 'chmod +x deploy.sh && ./deploy.sh ${BUILD_NUMBER}'
            }
        }

        stage('Verify') {
            steps {
                sh 'curl -fs http://localhost:5000/ && echo && curl -fs http://localhost:5000/api/info'
            }
        }
    }

    post {
        success { echo "Build #${BUILD_NUMBER} passed and was deployed." }
        failure { echo "Build #${BUILD_NUMBER} failed. Check the stage logs above." }
        always  { cleanWs(deleteDirs: true, notFailBuild: true) }
    }
}
