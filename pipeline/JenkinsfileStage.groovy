pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.stage_aws"
        DATABASE_HOST = "sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com"
        DATABASE_NAME = "sinamecc_stage_2020"
        DATABASE_CREDS  = credentials('sinamecc-stage-dba')
        DATABASE_URL    = "postgres://${DATABASE_CREDS}@${DATABASE_HOST}:5432/${DATABASE_NAME}"
    }

    stages {
        stage("Build and Test") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials-us-east-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                    {
                        echo "Step: Updating requirements"
                        sh 'pip install -r requirements.txt'

                        echo "Step: Running Tests"
                        sh 'python manage.py test'

                        echo "Step: Running Migrations"
                        sh 'python manage.py migrate'                    
                    }
                }
            }
        }

        stage ("Building docker image") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    echo "Step: Building docker image"
                    sh 'docker build -t sinamecc_backend:stage .'
                }
            }   
        }

        stage ("Restarting docker container") {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials-us-east-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                {
                    echo "Step: Stopping current container"
                    sh 'test ! -z "`docker ps -a| grep sinamecc_backend_stage`" && (docker stop sinamecc_backend_stage && docker rm sinamecc_backend_stage) || echo "sinamecc_backend_stage does not exists"'

                    echo "Step: Running new container"
                    sh "docker run -d -e \"DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE\" -e \"DATABASE_URL=$DATABASE_URL\" -e \"AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\" -e \"AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\" --name sinamecc_backend_stage -p 8025:8015 sinamecc_backend:stage"
                }
            }   
        }
    }
}

