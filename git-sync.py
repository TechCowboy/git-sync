import os
import subprocess

# get directories

debug = 1

print("Finding local git repositories...")
cwd = os.getcwd()

if debug:
    cwd = os.path.abspath(os.path.join(cwd, os.pardir))
    os.chdir(cwd)

all_dirs = os.listdir(cwd)
git_dirs = []

for dir in all_dirs:
    if os.path.isdir(dir):
        if os.path.exists(os.path.join(dir, ".git")):
            git_dirs.append(os.path.abspath(dir))

total_dirs = len(git_dirs)
print(f"{total_dirs} git directories found")
print("Getting the latest status on each remote repositories...")
status_size = 45
for dir in git_dirs:
    os.chdir(dir)
    count = f"{total_dirs}"
    print(f"{count:3} {dir:70}\r", end='')
    result = subprocess.run(['git', 'remote','-v','update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    total_dirs -= 1
print(f"{' ':75}\r")

pull_info = ''
total_up_to_date=0

latest_but_modified = 'Lastest from remote but local files modified'

for dir in git_dirs:
    os.chdir(dir)
    result = subprocess.run(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    behind = output.find("Your branch is behind") >= 0
    modified = output.find("modified:") >= 0
    untracked = output.find("Untracked files:") >= 0
    uptodate = output.find("Your branch is up to date with") >= 0
    
    if uptodate:
        if modified:
            but_modified = "but modified"
            print(f"{latest_but_modified:45} {dir}")
        else:
            but_modified = ""
            total_up_to_date += 1
        
    else:
        
        if behind:           
            if modified:
                print(f"{'Behind but files modified':45} {dir}")
                result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)
                pull_info += result.stdout.decode('utf-8')
                print(pull_info)
            else:
                print(f"{'Pulling lastest files':45} {dir}")
                result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)
                pull_info += result.stdout.decode('utf-8')
                print(pull_info)
        else:
            total_up_to_date += 1

print()
print(f"{total_up_to_date} repositories are up to date")        
