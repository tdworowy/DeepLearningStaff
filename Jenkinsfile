pipeline {
    agent { label 'Slave_ubuntu'}
    stages {
        stage("Clean Workspace"){
           steps{
               cleanWs()
            }
        }
        stage("Pull changes from git"){
           steps{
                git 'http://github.com/tdworowy/DeepLearningStaff.git'
            }
        }
        stage("Prepare env"){
           steps{
               script {
                    sh "pip3 install -r tests/requirements.txt"
                    sh "export PYTHONPATH=\$PYTHONPATH:\$(pwd)"
               }
            }
        }
        stage("Update config"){
           steps{
                script {
                    def ip = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true)
                    sh "python3 update_config.py $ip"
                }
            }
        }
        stage("Run unit tests"){
          steps{
               script {
                    sh "python3 -m pytest tests/unit_tests/"
               } 
           }
        }
        stage('Build Docker Images') {
            steps {
                script {
                         sh "docker build -t nullpointerexeption/deep_node -f DockerfileNode ."
                         sh "docker build -t nullpointerexeption/deep_api -f DockerfileApi ."
                         dir("dashboard") {
                             sh "docker build -t nullpointerexeption/deep_dashboard ."
                        }
                }
            }
        }
        stage('Run containers') {
            steps {
                script {
                         sh "mkdir -p ~/data"
                         sh "docker pull mongo && docker run -d -p 27017:27017 -v ~/data:/data/db mongo"
                         sh "docker pull nats && docker run -d -p 4222:4222 -p 8222:8222 nats"
                         sh "docker run -d nullpointerexeption/deep_node"
                         sh "docker run -d -p 5000:5000 nullpointerexeption/deep_api"
                         sh "docker run -d -p 3000:3000 nullpointerexeption/deep_dashboard"

                        }
                }
            }
        stage("Run integration tests"){
           steps{
                script {               
                    sh "python3 -m pytest tests/integration_tests/"
                    
                }
            }
        }
        stage("Run api tests"){
           steps{
                script {
                    sh "python3 -m pytest tests/api_tests/"
                }
            }
        }
        stage("Run front end tests"){
           steps{
                script {
                    dir("tests"){
                        sh "./run_front_end_tests.sh"
                    } 
                }
            }
        }
        
    }
    post {
        always {
             script {
                sh 'docker kill $(docker ps -q)'
               // sh 'docker rm $(docker ps -a -q)'
               
            }
        }
    }
}