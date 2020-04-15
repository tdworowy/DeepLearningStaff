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
                    dir("services") {
                        app = docker.build("nullpointerexeption/deep_node")
                    }
                     dir("services") {
                        app = docker.build("nullpointerexeption/deep_node")
                    }
                     dir("api") {
                        app = docker.build("nullpointerexeption/deep_api")
                    }
                     dir("dashboard/dashboard") {
                        app = docker.build("nullpointerexeption/deep_dashboard")
                    }
                  }
                }
            }
    }
}