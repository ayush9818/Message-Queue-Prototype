pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'c8053ebe-8270-4c79-bab6-e3d8b69d22e9', url: 'https://github.com/ayush9818/Message-Queue-Prototype.git']]])

            }
        }
        stage("Build"){
            steps{
                git branch: 'main', credentialsId: 'c8053ebe-8270-4c79-bab6-e3d8b69d22e9', url: 'https://github.com/ayush9818/Message-Queue-Prototype.git'
            }
        }
        stage("Testing"){
            steps{
                sh 'ls'
                sh 'pip install -r requirements.txt'
                dir('./testing'){
                    sh 'pwd'
                    sh 'python tests.py'
                }

                echo "Testing Done"
            }
        }
    }
}
