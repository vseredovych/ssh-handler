#!/usr/bin/python3
import argparse
from shutil import copyfile

import csv
import sys

#=========================== Arguments ===========================#

parser = argparse.ArgumentParser(description='Great Description To Be Here')
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser('add')
parser_add.add_argument('-a', '--host', action='store', dest='host', required=True, help='hostname')
parser_add.add_argument('-d', '--description', action='store', dest='description', default="", help='description')
parser_add.add_argument('-u', '--user',  action='store', dest='user', required=True, help='username')

#parser_update = subparsers.add_parser('update')
#parser_update.set_defaults(func=update_config)

#parser.add_argument('-a', '--add', action='store_false', dest='description', help='description')

args = parser.parse_args()

hosts_read_path = "hosts.csv"
hosts_write_path = "hosts.csv"

completion_read_path = "./completion/ssh-completion.bash-templete"
completion_write_path = "./completion/ssh-completion.bash"

#src_completion_file="./completion/ssh-completion.bash"
etc_completion_file="/etc/bash_completion.d/ssh-completion.bash"

#=========================== Connection class ===========================#
class Connection:
  def __init__(self, username, hostname, description):
    self.hostname = hostname
    self.username = username
    self.description = description
  def __str__(self):
    return ','.join([ self.username, self.hostname, self.description ])

#=========================== Connections repository  ===========================#
class Connections:
  def __init__(self, filename):
    self.headers = [ 'username', 'hostname', 'description' ]
    self.connections = []
    self.__get_connections_from_hosts(filename)
  def __str__(self):
    return '\n'.join( [','.join(self.headers), '\n'.join([str(x) for x in self.connections])] )
  def get_usernames(self):
    return [ x.username for x in self.connections ]
  def get_quoted_usernames(self):
    return [ "\'{0}\'".format(x.username) for x in self.connections ]
  def get_hostnames(self):
    return [ x.hostname for x in self.connections ]
  def get_quoted_hostnames(self):
    return [ "\'{0}\'".format(x.hostname) for x in self.connections ]
  def get_descriptions(self):
    return [ x.description for x in self.connections ]
  def add_connection(self, username, hostname, description):
    self.add_connection_object(Connection(username, hostname, description))
  def add_connection_object(self, connection):
    if (connection.hostname not in self.get_hostnames()):
      self.connections.append(Connection(
          connection.username, 
          connection.hostname, 
          connection.description)
          )
    else:
      print("Given hostname is already exists!")
  def __get_connections_from_hosts(self, file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    headers = next(reader)
    if (not (headers == self.headers)):
      sys.exit(2)

    for row in reader:
      if (len(row) == 0):
        continue
      connection = Connection(row[0], row[1], row[2])
      self.add_connection_object(connection)


#=========================== Functions ===========================#

def update_hosts(connections):
    """
    Write to hosts.csv file
    """
    with open(hosts_write_path, "w+") as file:
      file.write(str(connections))

def update_config(connections):
  # new configuration file
  new_file = ""
  with open(completion_read_path, "r") as read_file:
    # configure templete file 
    for line in read_file:
      if ("#USERNAMES" in line):
        new_file += "users=({0})".format(" ".join(connections.get_quoted_usernames()))
        new_file += '\n'
        continue
      if ("#HOSTNAMES" in line):
        new_file += "hosts=({0})".format(" ".join(connections.get_quoted_hostnames()))
        new_file += '\n'
        continue
      new_file += line
      
  with open(completion_write_path, "w+") as write_file:
    # create new file from templete
    write_file.write(new_file)

  with open(etc_completion_file, "w+") as write_file:
    # create new file from templete
    write_file.write(new_file)

#    #update configuration file
#    copyfile(src_completion_file, dest_completion_file)


#=========================== Main ===========================#

if __name__ == "__main__":

  # all connections
  connections = ""
  with open(hosts_read_path, "r") as read_file:
    connections = Connections(read_file)

  connections.add_connection(args.user, args.host, args.description)
  update_hosts(connections)
  update_config(connections)