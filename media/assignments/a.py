import subprocess
from subprocess import call

a = "test"
subprocess.run(["tree", a, "capture_output=True"])
f = open("out.txt" , "w")
print(sys.stdout, f)
