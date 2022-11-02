import os
import subprocess

# get directories

debug = 1

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


print("Getting latest status from remote sites ")
total_dirs = len(git_dirs)
for dir in git_dirs:
    os.chdir(dir)
    count = f"{total_dirs}"
    print(f"{count} remaining    ")
    result = subprocess.run(['git', 'remote','-v','update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    total_dirs -= 1
print()
pull_info = ''
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
        else:
            but_modified = ""
        print(f"Up to date {but_modified:15} {dir}")
    else:
        
        if behind:
            
            if modified:
                print(f"Files modified, can't pull {dir}")
            else:
                print(f"Pulling {dir}")
                result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)
                pull_info += result.stdout.decode('utf-8')

        
        
    
"""
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   examples/adam-smartkeys/Makefile
	modified:   examples/adam-smartkeys/src/main.c
	modified:   src/smartkeys.h
	modified:   src/smartkeys_putc.c
	modified:   src/smartkeys_puts.c
	modified:   src/smartkeys_sound_init.c
	modified:   src/smartkeys_sound_play.c

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	build/
	examples/adam-smartkeys/adam-smartkeys
	examples/adam-smartkeys/adam-smartkeys.ddp
	examples/adam-smartkeys/adam-smartkeys.map
	examples/adam-smartkeys/adam-smartkeys_BOOTSTRAP.bin
	examples/adam-smartkeys/build/
	smartkeys.lib
"""
