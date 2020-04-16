pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.stage_aws"
    }

    stages {
        withPythonEnv('/usr/bin/python3.6') {
            stage("Build and Test") {
                steps {
                    
                    echo "Step: Running Migrations"
                    sh 'python manage.py migrate'

                    echo "Step: Running Tests"
                    sh 'python manage.py migrate'

                }
            }

            stage ("Execute migrations") {
                steps {
                    echo "Step: Build and Test"
                }   
            }

            stage ("Restarting service") {
                steps {
                    echo "Step: Build and Test"
                }   
            }
        }
    }
}