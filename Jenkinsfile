pipeline {
    agent { label 'Slave_ubuntu'}
    stages {
        stage("Pull changes from git"){
           steps{
                git 'http://github.com/tdworowy/DeepLearningStaff.git'
            }
        }
          stage("Run unit tests"){
           steps{
                dir("deep_learning_app"){
                    sh "pip install -r requirements.txt"
                     sh "pytest /tests/unit_tests/"
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
    }
}