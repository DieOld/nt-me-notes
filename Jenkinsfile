pipeline {
    agent {
        docker { image 'dieold/buildbox:1.0' }
    }
    stages {
        stage('Linter') {
            steps {
                sh 'flake8'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "here must be tests.."'
            }
        }
    }
}