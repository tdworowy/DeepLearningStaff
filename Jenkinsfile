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
        stage("Static code analize backend"){
           steps{
               script {
                    sh(script: "python3 -m prospector --output-format json > prospector.json", returnStatus: true)
                  
               }
            }
        }
        stage("Static security analize backend"){
           steps{
               script {
                    sh(script: "python3 -m bandit -r . -v -f html -o bandit.html", returnStatus: true)
                    
               }
            }
        }
         stage("Static code analize frontend"){
           steps{
               script {
                   dir("dashboard/dashboard") {
                     sh(script: "npm install", returnStatus: true)
                     sh(script: "sudo npm install typescript -g", returnStatus: true)
                     sh(script: "sudo npm install tslint -g", returnStatus: true)
                     sh(script: "npm audit fix", returnStatus: true)
                     sh(script: "tslint -o tslint.txt './**/*.ts'", returnStatus: true)
                   }
               }
            }
        }
        stage("Run unit tests"){
          steps{
               script {
                    def unit_test_status = sh(script: "python3 -m pytest tests/unit_tests/ --html=unit_tests_report.html --self-contained-html", returnStatus: true)
                    if(unit_test_status !=0) {
                       unstable('unit tests failed!')
                    }                   
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
                         sh "mkdir -p data"
                         sh "docker pull mongo && docker run -d -p 27017:27017 --name mongo_db -v data:/data/db mongo"
                         sh "docker pull nats && docker run -d -p 4222:4222 -p 8222:8222 --name nats nats -V"
                         sh "docker run -d -p 4001:4001 -e logs_port=4001 --name node nullpointerexeption/deep_node"
                         sh "docker run -d -p 5000:5000 -p 4002:4002 -e logs_port=4002 --name api nullpointerexeption/deep_api"
                         sh "docker run -d -p 3000:3000 --name dashboard nullpointerexeption/deep_dashboard"
                       }
                }
        }
        stage("Run containers monitoring"){
           steps{
                script {
                    def containers = sh(script: "docker ps --format '{{.Names}}'", returnStdout: true)
                    containers = containers.replaceAll("\\s",",")
                    sh "python3 monitor_containers_logs.py $containers"
                }
            }
        }
        stage("Run integration tests"){
           steps{
                script {               
                   def integration_tests_status = sh(script: "python3 -m pytest tests/integration_tests/ --html=integration_tests_report.html --self-contained-html", returnStatus: true)
                   if(integration_tests_status !=0) {
                        unstable('integration tests failed!')
                   } 
                }
            }
        }
        stage("Run api tests"){
           steps{
                script {
                    def api_tests_status = sh(script: "python3 -m pytest tests/api_tests/ --log-cli-level --html=api_test_report.html --self-contained-html --reruns 3", returnStatus: true)
                    if(api_tests_status !=0) {
                        unstable('api tests failed!')
                    } 
                  
                }
            }
        }
        stage("Run front end tests"){
           steps{
                script {
                    dir("tests"){
                        sh "chmod 777 chromedriver/*"
                        sh "export PYTHONPATH=\$PYTHONPATH:\$(pwd)"
                            def front_tests_status = sh(script: "export PYTHONPATH=\$PYTHONPATH:\$(pwd) && cd front_end_tests && python3 -m behave -f allure_behave.formatter:AllureFormatter -o allure_dir", returnStatus: true)
                            if(front_tests_status !=0) {
                                unstable('front end tests failed!')
                                
                            } 
                        
                    } 
                }
            }
        }
    }
    post {
        always {
             script {
                archiveArtifacts artifacts: 'unit_tests_report.html', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'integration_tests_report.html', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'api_test_report.html', followSymlinks: false, allowEmptyArchive: true

                archiveArtifacts artifacts: 'dashboard/dashboard/tslint.txt', followSymlinks: false, allowEmptyArchive: true
                
                archiveArtifacts artifacts: 'tests/front_end_tests/logs/**/*', followSymlinks: false, allowEmptyArchive: true
                
                archiveArtifacts artifacts: 'mongo_db.log', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'nats.log', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'node.log', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'api.log', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'dashboard.log', followSymlinks: false, allowEmptyArchive: true

                archiveArtifacts artifacts: 'prospector.json', followSymlinks: false, allowEmptyArchive: true
                archiveArtifacts artifacts: 'bandit.html', followSymlinks: false, allowEmptyArchive: true

                sh 'docker kill $(docker ps -q)'
                sh 'docker rm $(docker ps -a -q)'
               
            }
        }
    }
}