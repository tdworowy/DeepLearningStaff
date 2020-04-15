pipeline {
    agent { label 'Slave_ubuntu'}
    stages {
        stage("Pull changes from git"){
           steps{
                git 'http://github.com/tdworowy/DeepLearningStaff.git'
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                         sh "docker build nullpointerexeption/deep_node -f DockerFileNode ."
                         sh "docker build nullpointerexeption/deep_api -f DockerFileApi ."
                         dir("dashboard/dashboard") {
                             app = docker.build("nullpointerexeption/deep_dashboard")
                        }
            }
        }
        }
    }
}