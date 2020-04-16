pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.stage_aws"
    }

    stages {

        stage("Build and Test") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    echo "Step: Updating requirements"
                    sh 'pip install -r requirements.txt'

                    echo "Step: Running Tests"
                    //sh 'python manage.py test'

                    echo "Step: Running Migrations"
                    sh 'python manage.py migrate'
                }
            }
        }

        stage ("Building docker image") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    echo "Step: Building docker image"
                    sh 'docker build -t sinamecc_backend:latest .'
                }
            }   
        }

        stage ("Restarting docker container") {
            steps {
                echo "Step: Stopping current container"
                sh '[[ ! -z `docker ps | grep sinamecc_backend_dev` ]] && (docker stop sinamecc_backend_dev && docker rm sinamecc_backend_dev) || echo "sinamecc_backend_dev does not exists"'

                echo "Step: Running new container"
                sh 'docker run -d -e "DJANGO_SETTINGS_MODULE=config.settings.stage_aws" --name sinamecc_backend_dev sinamecc_backend:latest'
            }   
        }
    }
}