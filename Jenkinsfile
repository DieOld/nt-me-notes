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
        stage('Deploy') {
            steps {
                sh 'ssh -tf ubuntu@52.45.181.56 "ls -la"'
            }
        }
    }
}