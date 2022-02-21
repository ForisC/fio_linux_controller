def remote = [:]
remote.name = "node-1"
remote.host = params.client
remote.user = 'ec2-user'
remote.allowAnyHosts = true
currentBuild.description = env.Description

node {
    withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu_clinet', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
        remote.user = userName
        remote.identityFile = identity
        stage("Env Preparing"){
            
            sshCommand remote: remote, command: "sudo yum -y install fio"
            sshCommand remote: remote, command: "sudo pkill fio || true"
            sshCommand remote: remote, command: "sudo ps -x|grep fio>p || true"
            sshCommand remote: remote, command: "sudo cat p"
            sshCommand remote: remote, command: "sudo find . -empty -name p | grep ."
        }
        
        
        stage("FIO random read") {
            command = "sudo echo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=randread -ioengine=psync -bs=16k -size=${env.TestSize}G -numjobs=30 -runtime=1000 -group_reporting -name=randread>randread"
            sshCommand remote: remote, command: command
        }
        stage("FIO sequential read") {
            command = "sudo echo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=read -ioengine=psync -bs=16k -size=${env.TestSize}G -numjobs=30 -runtime=1000 -group_reporting -name=read>read"
            sshCommand remote: remote, command: command
        }
        stage("FIO random write") {
            command = "sudo echo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=randwrite -ioengine=psync -bs=16k -size=${env.TestSize}G -numjobs=30 -runtime=1000 -group_reporting -name=randwrite>read"
            sshCommand remote: remote, command: command
        }
        stage("FIO sequential write") {
            command = "sudo echo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=write -ioengine=psync -bs=16k -size=${env.TestSize}G -numjobs=30 -runtime=1000 -group_reporting -name=write>write"
            sshCommand remote: remote, command: command
        }
        stage("create cva"){
            sh 'echo -e "1000,1500">>data.csv'
            sh 'cat data.csv'

        }
        stage("plot"){
            plot csvSeries: [[
                            file: 'data.csv',
                            exclusionValues: '',
                            displayTableFlag: false,
                            inclusionFlag: 'OFF',
                            url: '']],
            csvFileName: "plot-iops.csv",
            group: 'Plot Group',
            title: 'FIO test',
            style: 'line',
            exclZero: false,
            keepRecords: false,
            logarithmic: false,
            numBuilds: '10',
            useDescr: true,
            yaxis: 'iops',
            yaxisMaximum: '',
            yaxisMinimum: ''
            }
    }
}