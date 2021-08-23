pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.ecs_aws"
        DATABASE_HOST = "sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com"
        DATABASE_NAME = "sinamecc_dev_2020"
        DATABASE_CREDS  = credentials('sinamecc-dev-dba')
        DATABASE_URL    = "postgres://${DATABASE_CREDS}@${DATABASE_HOST}:5432/${DATABASE_NAME}"

        BASE_ECR = "973157324549.dkr.ecr.us-east-2.amazonaws.com"
        ENVIRONMENT = "dev"
        APP = "sinamecc-backend"
        NGINX_TAG = "nginx-$ENVIRONMENT"
        ECS_CLUSTER_NAME = "sinamecc-cluster-$ENVIRONMENT"
        ECS_SERVICE_NAME = "sinamecc-backend-$ENVIRONMENT"
    }

    stages {
        stage("Build and Test") {
            steps {
                withPythonEnv('/bin/python3.7') {
                  echo "Step: Upgrading pip"
                  sh 'pip install --upgrade pip'

                  echo "Step: Updating requirements"
                  sh 'pip install -r requirements.txt'

                  echo "Step: Running Tests"
                  sh 'python manage.py test'

                  echo "Step: Running Migrations"
                  sh 'python manage.py migrate'
                }
            }
        }

        stage ("Building docker image") {
            steps {
                withPythonEnv('/bin/python3.7') {
                    echo "Step: Building docker image"
                    sh 'docker build -t $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT .'
                }
            }
        }
    }
}
