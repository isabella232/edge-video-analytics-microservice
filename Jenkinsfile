pipeline {

    agent {
         node {
            label 'aws-ec2'
         }
    }

    environment {
         MC_URL = 'https://esh-mc.intel.com' // API url to validate branch exists in mc
        MODULE_ID = '619ce395ff6f230021e442eb' // ID associated with the Service Layer
        MODULE_NAME    = 'Edge Video Analytics Resources' // Name which goes to Service Layer
        MODULE_FILE_NAME = 'Edge_Video_Analytics_Resources' //Installation file name associated in the repo
        CURRENT_DATE = sh(script: 'date +%Y%m%d', returnStdout: true).trim()
        AWS_S3_BUCKET = 'eshs3bucket'    // AWS S3 BUCKET NAME
        AWS_S3_REGION = 'us-west-2' // AWS REGION NAME
        AWS_S3_SOURCE = 'esh/jenkins' // AWS SOURCE Path for Jenkins upload
        GITLAB_LOGIN = credentials('Intel-Gitlab')
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    echo "--------------------------------------------"
                    echo " Agent setup "
                    echo "--------------------------------------------"
                    while pgrep apt > /dev/null; do
                        sleep 11
                    done
                    sudo apt-get update
                    echo "--------------------------------------------"
                '''
            }
        }

        stage('Install certs') {
                steps {
                    sh '''
                        wget https://gitlab.devtools.intel.com/dse-public/devops-scripts/-/raw/master/install-certs.sh --no-check-certificate
                        chmod a+x install-certs.sh
                        ./install-certs.sh
                    '''
                    }
            }

        stage('Linting') {
            steps {
                sh '''#!/bin/bash
                        echo "--------------------------------------------"
                        echo " Running linting for ${MODULE_NAME} "
                        echo "--------------------------------------------"
                        pip3 install flake8
                        pip3 install bandit
    
                        echo "-------------Running Style check---------------"
                        ${HOME}/.local/bin/flake8 . --tee --output-file=pep8_output.txt
                        #if [ -s pep8_output.txt ]; then
                        #    exit 1
                        #fi
                        #echo "---------------Running Tests-----------------"
                        #${HOME}/.local/bin/tox -e py3
    
                        echo "---------------Running Bandit-----------------"
                        ${HOME}/.local/bin/bandit -r ${PWD} -f txt -o bandit_report.txt || true
                        #if [ -s bandit_report.txt ]; then
                        #    exit 1
                        #fi
                        echo "--------------------------------------------"
                    '''
            }
        }


        stage('Create Package') {
            steps {
                sh '''#!/bin/bash
                    echo "--------------------------------------------"
                    echo " Creating ${MODULE_NAME} zip"
                    echo "--------------------------------------------"
                    echo "Module Name: ${MODULE_NAME}"
                    echo "Module ID: ${MODULE_ID}"
                    echo "Module File: ${MODULE_FILE_NAME}"
                    python3 compile.py build_ext --inplace
                    mv *.so esb_install.so
                    rm -rf .git* build run.sh docker-compose-build.yml esb_install.so

                    echo "-------------Copy dependencies--------------"
                    #rsync -av \
                    #--exclude={${MODULE_FILE_NAME}.py, ${MODULE_FILE_NAME}.c, 'compile.py', '__pycache__', \
                    #'__init__.py', 'Jenkinsfile', 'README.md', 'tests', 'install.log', 'pep8_output.txt', 'bandit_report.txt'} \
                    #. ${MODULE_ID}
                    rsync -av --exclude ${MODULE_FILE_NAME}.py --exclude ${MODULE_FILE_NAME}.c --exclude compile.py --exclude evas/ \
                              --exclude '*.rst' --exclude '*.md' --exclude install.log --exclude Jenkinsfile --exclude pep8_output.txt \
                              --exclude bandit_report.txt --exclude __init__.py --exclude __pycache__ --exclude tests --exclude eii/ \
                              --exclude README.md --exclude Dockerfile \
                              --exclude IntelSHA2RootChain-Base64 --exclude __MACOSX --exclude IntelSHA2RootChain-Base64.zip \
                              --exclude '*.crt' --exclude '*certs*' ./ ${MODULE_ID}  

                    cd ${MODULE_ID}
                    echo "---------------Create zip-------------------"
                    zip -r ${MODULE_ID}.zip .
                    retval=$?
                    if [ $retval -ne 0 ]; then
                        echo "Failed create module zip"
                        exit $retval
                    fi
                    echo "--------------------------------------------"
                '''
            }
        }
        stage('Push to S3'){
            steps{
                script {
                  def res = "";
                  withAWS(region:"${AWS_S3_REGION}",credentials:'AWS_S3_Upload') {
                      def identity=awsIdentity();//Log AWS credentials
                      def ZIP_FILE_PATH = pwd();
                      echo "--------------------------------------------"
                      echo " Uploading ${MODULE_NAME} to S3"
                      echo "--------------------------------------------"
                      echo "${MODULE_NAME} : ${MODULE_ID}.zip"

                      def MC_VERSION = sh(script: "wget --server-response --method POST --timeout=0 --header 'Content-Type: application/json' \
                          --ca-directory=/etc/ssl/certs/ --no-proxy --no-check-certificate \
                          --body-data '{\"id\":\"'$MODULE_ID'\",\"version\":\"'$GIT_BRANCH'\"}' \
                            \${MC_URL}/ingredient/validateVersion 2>&1 | grep \"HTTP/\" | awk '{print \$2}'", returnStdout: true).trim();

                      echo "ID: $MODULE_ID, version: $GIT_BRANCH"
                      if ( MC_VERSION != '200' ) {
                        echo "-------Push to S3 skipped-------"
                        echo "--------------------------------------------"
                        sh(script: "exit 0")
                      }

                      echo ZIP_FILE_PATH;
                      res = s3Upload(file:"${ZIP_FILE_PATH}/${MODULE_ID}/${MODULE_ID}.zip", bucket:"${AWS_S3_BUCKET}", path:"esh/jenkins/${MODULE_ID}.zip");
                  }
                  if ( res != "s3://${AWS_S3_BUCKET}/esh/jenkins/${MODULE_ID}.zip" ) {
                      error("AWS S3 Upload Failed.");
                  }

                  echo "-----------Generate MD5sum------------------"
                  def MD5SUM = sh(script: "md5sum \${MODULE_ID}/\${MODULE_ID}.zip | cut -d ' ' -f1",returnStdout:true).trim();
                  if ( !MD5SUM ){
                      error("Failed to generate md5sum")
                  }
                  echo "original md5sum: ${MD5SUM}"
                }
            }
        }
        stage('Update MD5Sum'){
            steps{
                script {
                  def ZIP_FILE_PATH = pwd();

                  withAWS(region:"${AWS_S3_REGION}",credentials:'AWS_S3_Upload') {
                      def identity=awsIdentity();//Log AWS credentials
                      echo "--------------------------------------------"
                      echo " Downloading ${MODULE_NAME} from S3"
                      echo "--------------------------------------------"
                      echo "${MODULE_NAME} : ${MODULE_ID}.zip"
                      sh(script: "sudo mkdir -p \${ZIP_FILE_PATH}/\${MODULE_ID}/download",returnStdout:true);
                      res = s3Download(file:"${ZIP_FILE_PATH}/${MODULE_ID}/download/${MODULE_ID}.zip", bucket:"${AWS_S3_BUCKET}", path:"esh/jenkins/${MODULE_ID}.zip", force:true)
                  }
                  echo "-----------Generate MD5sum------------------"
                  def MD5SUM = sh(script: "md5sum \${MODULE_ID}/download/\${MODULE_ID}.zip | cut -d ' ' -f1",returnStdout:true).trim();
                  if ( !MD5SUM ){
                    error("Failed to generate md5sum")
                  }
                  echo "md5sum(s3): ${MD5SUM}"

                  echo "--------------Post MD5sum-------------------"
                  def RETVAL = sh(script: "wget --method POST --timeout=0 --header 'Content-Type: application/json' --body-data '{\"id\":\"'$MODULE_ID'\",\"hashValue\":\"'$MD5SUM'\"}' \${MC_URL}/ingredient/updateMD5Hash --ca-directory=/etc/ssl/certs/ --no-proxy --no-check-certificate",returnStatus:true);
                  if ( RETVAL != 0 ) {
                      error("Failed to post md5sum");
                  }
                  echo "--------------------------------------------"
                }
            }
        }
    }

    post {
        success {
            emailext(
                attachmentsPattern: "bandit_report.txt, pep8_output.txt",
                replyTo: '$DEFAULT_REPLYTO',
                subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
                body: "${env.BUILD_URL} has result ${currentBuild.result}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
            updateGitlabCommitStatus state: 'success'
        }

        failure {
            emailext(
                replyTo: '$DEFAULT_REPLYTO',
                subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
                body: "${env.BUILD_URL} has result ${currentBuild.result}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
            updateGitlabCommitStatus state: 'failed'
        }
    }

}
