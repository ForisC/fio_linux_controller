def remote = [:]
remote.name = "node-1"
remote.host = params.client
remote.user = 'ubuntu'
remote.allowAnyHosts = true
currentBuild.description = env.Description

node {
    withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu_clinet', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
        // remote.user = userName
        remote.identityFile = identity
        stage("Env Preparing"){
            sshCommand remote: remote, command: "sudo pkill fio || true"
            // sshCommand remote: remote, command: "sudo ps -x|grep fio>p || true"
            // sshCommand remote: remote, command: "sudo cat p"
            // sshCommand remote: remote, command: "sudo find . -empty -name p | grep ."
            // sshCommand remote: remote, command: "sudo yum -y install fio"
        }
        
        
        stage("FIO random read") {
            command = "sudo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=randread -ioengine=psync -bs=16k -size=${env.TestSize} -numjobs=30 -runtime=1000 -group_reporting -name=randread --output=randread.json --output-format=json"
            sshCommand remote: remote, command: command
        }
        stage("FIO sequential read") {
            command = "sudo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=read -ioengine=psync -bs=16k -size=${env.TestSize} -numjobs=30 -runtime=1000 -group_reporting -name=read --output=read.json --output-format=json"
            sshCommand remote: remote, command: command
        }
        stage("FIO random write") {
            command = "sudo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=randwrite -ioengine=psync -bs=16k -size=${env.TestSize} -numjobs=30 -runtime=1000 -group_reporting -name=randwrite --output=randwrite.json --output-format=json"
            sshCommand remote: remote, command: command
        }
        stage("FIO sequential write") {
            command = "sudo fio -filename=${env.drive} -direct=1 -iodepth 1 -thread -rw=write -ioengine=psync -bs=16k -size=${env.TestSize} -numjobs=30 -runtime=1000 -group_reporting -name=write --output=write.json --output-format=json"
            sshCommand remote: remote, command: command
        }
        stage("collect data"){
            sshGet remote: remote, from: 'write.json', into: 'write.json', override: true
            sshGet remote: remote, from: 'randread.json', into: 'randread.json', override: true
            sshGet remote: remote, from: 'randwrite.json', into: 'randwrite.json', override: true
            sshGet remote: remote, from: 'read.json', into: 'read.json', override: true
            sh "cat read.json"
            sh "cat write.json"
            sh "cat randread.json"
            sh "cat randwrite.json"

        }
    //     stage("plot"){
    //         plot csvSeries: [[
    //                         file: 'data.csv',
    //                         exclusionValues: '',
    //                         displayTableFlag: false,
    //                         inclusionFlag: 'OFF',
    //                         url: '']],
    //         csvFileName: "plot-iops.csv",
    //         group: 'Plot Group',
    //         title: 'FIO test',
    //         style: 'line',
    //         exclZero: false,
    //         keepRecords: false,
    //         logarithmic: false,
    //         numBuilds: '10',
    //         useDescr: true,
    //         yaxis: 'iops',
    //         yaxisMaximum: '',
    //         yaxisMinimum: ''
    //         }
    }
}