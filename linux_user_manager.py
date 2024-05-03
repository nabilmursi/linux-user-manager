import os
import subprocess
import cmd
import sys

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

class LinuxUserManager(cmd.Cmd):
    intro = 'Welcome to Linux User Manager. Available commands:'
    prompt = '(lum) '
    
    def __init__(self):
        super(LinuxUserManager, self).__init__()
        if os.geteuid() != 0:
            sys.exit("This script must be run as root (or with sudo).")
        self.print_options()

    def print_options(self):
        print("\nAvailable Options:")
        print("1 - List all users: Show a list of all system users.")
        print("2 - List all groups: Display all groups on the system.")
        print("3 - Add a new user: Add a user with specified username.")
        print("4 - Delete a user: Remove a user with specified username.")
        print("5 - Add a new group: Create a new group with specified group name.")
        print("6 - Delete a group: Remove a group with specified group name.")
        print("7 - Add a user to a group: Add specified user to a specified group.")
        print("8 - Remove a user from a group: Remove specified user from a specified group.")
        print("9 - Check for files with risky permissions: Find files with permissions set to 777.")
        print("10 - Show options: Redisplay this options list.")
        print("0 - Exit: Quit the Linux User Manager.")
        print("\nPlease select an option by entering the number.")

    def do_1(self, arg):
        'List all users on the system'
        print(run_command("cut -d: -f1 /etc/passwd"))

    def do_2(self, arg):
        'List all groups on the system'
        print(run_command("cut -d: -f1 /etc/group"))

    def do_3(self, arg):
        'Add a new user'
        print(run_command(f"sudo useradd {arg}"))

    def do_4(self, arg):
        'Delete a user'
        print(run_command(f"sudo userdel {arg}"))

    def do_5(self, arg):
        'Add a new group'
        print(run_command(f"sudo groupadd {arg}"))

    def do_6(self, arg):
        'Delete a group'
        print(run_command(f"sudo groupdel {arg}"))

    def do_7(self, arg):
        'Add a user to a group'
        username, groupname = arg.split()
        print(run_command(f"sudo usermod -a -G {groupname} {username}"))

    def do_8(self, arg):
        'Remove a user from a group'
        username, groupname = arg.split()
        print(run_command(f"sudo gpasswd -d {username} {groupname}"))

    def do_9(self, arg):
        'Check for files with risky permissions'
        risky_files = run_command("find / -perm 0777 -type f")
        if risky_files.strip():
            print("Risky permissions found on the following files:")
            print(risky_files)
        else:
            print("No risky permissions found.")

    def do_10(self, arg):
        'Show this options list again'
        self.print_options()

    def do_0(self, arg):
        'Exit the Linux User Manager'
        print("Exiting...")
        return True

if __name__ == '__main__':
    LinuxUserManager().cmdloop()
