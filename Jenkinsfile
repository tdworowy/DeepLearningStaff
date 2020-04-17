pipeline {
    agent { label 'Slave_ubuntu'}
    stages {
        stage("Pull changes from git"){
           steps{
                git 'http://github.com/tdworowy/DeepLearningStaff.git'
            }
        }
      stage("Install requirements"){
           steps{
               script {
                    sh "pip3 install -r requirements.txt"
               }
            }
        }
          stage("Run unit tests"){
           steps{
               script {
                dir("deep_learning_app"){
                    sh "pip3 install -r requirements.txt"
                    sh "python3 -m pytest tests/unit_tests"
                } 
            }
           }
        }
        stage('Build Docker Images') {
            steps {
                script {
                         sh "docker build -t nullpointerexeption/deep_node -f DockerfileNode ."
                         sh "docker build -t nullpointerexeption/deep_api -f DockerfileApi ."
                         dir("dashboard/dashboard") {
                             sh "docker build -t nullpointerexeption/deep_dashboard ."
                        }
                }
            }
        }
        stage('Build containers') {
            steps {
                script {
                         sh "mkdir ~/data"
                         sh "docker pull mongo && docker run -d -p 27017:27017 -v ~/data:/data/db mongo"
                         sh "docker pull nats && docker run nats"
                         sh "docker run nullpointerexeption/deep_node"
                         sh "docker run nullpointerexeption/deep_api"
                         sh "docker run nullpointerexeption/deep_dashboard"
                        
                        }
                }
            }
        stage("Run integration tests"){
           steps{
                script {               
                    dir("deep_learning_app"){
                        sh "python3 -m pytest tests/integration_tests"
                    } 
                }
            }
        }
       stage("Run api tests"){
           steps{
                script {
                    dir("deep_learning_app"){
                        sh "python3 -m pytest tests/api_tests"
                    } 
                }
            }
        }
      stage("Run front end tests"){
           steps{
                script {
                    dir("deep_learning_app/tests"){
                        sh "./run_front_end_tests.sh"
                    } 
                }
            }
        }
        
    }
}