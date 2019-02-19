import paramiko
from scp import SCPClient

def get_ssh_client(myhost, myuser, mypassword = None, keyfile=None):
    k = None
    if keyfile:
        k = paramiko.RSAKey.from_private_key_file(keyfile)
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    if k:
        ssh_client.connect(hostname=myhost, username=myuser, pkey = k)
    else:
        ssh_client.connect(hostname=myhost, username=myuser, password=mypassword)
    return ssh_client

def ssh_command(myhost, myuser, mypassword, command):
    ssh_client = get_ssh_client(myhost, myuser, mypassword)
    _, stdout, _ = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status() # Channel.exit_status_ready for non-blocking call
    ssh_client.close()
    return exit_status

def ssh_hadoop_command(myhost, myuser, keyfile, command):
    ssh_client = get_ssh_client(myhost, myuser, None, keyfile)
#     pre_command = """
#     . ~/.profile;
#     . ~/.bashrc;
#     """

    #_, stdout, _ = ssh_client.exec_command('export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop;' + command)
    _, stdout, _ = ssh_client.exec_command('export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop;' + command)
    exit_status = stdout.channel.recv_exit_status() # Channel.exit_status_ready for non-blocking call
    ssh_client.close()
    return exit_status

def ssh_hadoop_command_big1(myhost, myuser, mypassword, command):
    ssh_client = get_ssh_client(myhost, myuser, mypassword)
#     pre_command = """
#     . ~/.profile;
#     . ~/.bashrc;
#     """

    #_, stdout, _ = ssh_client.exec_command('export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop;' + command)
    _, stdout, _ = ssh_client.exec_command('export HADOOP_CONF_DIR=/etc/hadoop/2.5.3.0-37/0/;' + command)
    exit_status = stdout.channel.recv_exit_status() # Channel.exit_status_ready for non-blocking call
    ssh_client.close()
    return exit_status

def ssh_copy(myhost, myuser, mypassword, localpath, remotepath):
    ssh_client = get_ssh_client(myhost, myuser, mypassword)
    sftp = ssh_client.open_sftp()
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh_client.close()
    
def scp_get(myhost, myuser, mypassword, src, dest):
    ssh_client = get_ssh_client(myhost, myuser, mypassword)
    with SCPClient(ssh_client.get_transport()) as scp:
        scp.get(src, local_path=dest, recursive=True)
    
def scp_put(myhost, myuser, mypassword, src, dest):
    ssh_client = get_ssh_client(myhost, myuser, mypassword)
    with SCPClient(ssh_client.get_transport()) as scp:
        scp.put(src, recursive=True, remote_path=dest)