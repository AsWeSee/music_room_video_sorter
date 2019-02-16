import subprocess as sp
import os

command = ["python", 'main.py']

#proc = sp.run(command, stdout=sp.PIPE, universal_newlines=True) # shell=True,

pipe_read = sp.Popen(command, stdout = sp.PIPE, stderr = sp.DEVNULL, bufsize=1, universal_newlines=True) #

path = "D:\\mus 5 speed test\\correct\\"
out = ""
lastout = ""
i = 0
while not lastout == "finished\n":

    while pipe_read.poll() is None:

        out = pipe_read.stdout.readline()

        # try:
        #     outs, errs = pipe_read.communicate(timeout=5)
        # except sp.TimeoutExpired:
        #     outs, errs = pipe_read.communicate()

        print(out, end="")
        if out != "": lastout = out
        i += 1
        # if i%1000 ==0:
        #     print("read " + str(i))
        # if i==1000:
        #     break

    if lastout != "finished\n":
        print("process end with" + str(pipe_read.returncode))
        errorfile = lastout.split()[0]
        scr = path + errorfile
        dst = "D:\\mus 5 speed test\\errors\\" + errorfile
        os.rename(scr, dst)
        pipe_read = sp.Popen(command, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=1, universal_newlines=True)

print("reads " + str(i))
print("ENDED")