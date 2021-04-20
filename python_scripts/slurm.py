import os
import subprocess
from scheduler import scheduler

class slurm(scheduler):
  def __init__(self,scheduler_type):
     self.type = scheduler_type

  def createHeaders(self,test):
    for headerType in ["build","test"]:
      if(headerType == "build"):
        file_out = test.fb
      else:
        file_out = test.ft
      file_out.write("#!/bin/sh -l\n")
      file_out.write("#SBATCH --account={}\n".format(test.account))
      if(headerType == "build"):
        file_out.write("#SBATCH -o {}_%j.o\n".format(test.b_filename))
        file_out.write("#SBATCH -e {}_%j.e\n".format(test.b_filename))
        file_out.write("#SBATCH --time={}\n".format(test.build_time))
      else:
        file_out.write("#SBATCH -o {}_%j.o\n".format(test.t_filename))
        file_out.write("#SBATCH -e {}_%j.e\n".format(test.t_filename))
        file_out.write("#SBATCH --time={}\n".format(test.test_time))
      if(test.partition != "None"):
        file_out.write("#SBATCH --partition={}\n".format(test.partition))
      if(test.cluster != "None"):
        file_out.write("#SBATCH --cluster={}\n".format(test.cluster))
      file_out.write("#SBATCH --qos={}\n".format(test.queue))
      file_out.write("#SBATCH --nodes=1\n")
      file_out.write("#SBATCH --ntasks-per-node={}\n".format(test.cpn))
      file_out.write("#SBATCH --exclusive\n")
      file_out.write("export JOBID=$SLURM_JOBID\n")

  def submitJob(self,test,subdir,mpiver,branch):
    batch_build = "sbatch {}".format(test.b_filename)
    jobnum= subprocess.check_output(batch_build,shell=True).strip().decode('utf-8').split()[3]
    monitor_cmd_build = "python3 {}/python_scripts/get-results.py {} {} {} {} {} {} {} {}".format(test.mypath,jobnum,subdir,test.machine_name,self.type,test.script_dir,test.artifacts_root,mpiver,branch)
    print(monitor_cmd_build)
    proc = subprocess.Popen(monitor_cmd_build, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    # submit the second job to be dependent on the first
    batch_test = "sbatch --depend=afterok:{} {}".format(jobnum,test.t_filename)
    print("Submitting test_batch with command: {}".format(batch_test))
    jobnum= subprocess.check_output(batch_test,shell=True).strip().decode('utf-8').split()[3]
    monitor_cmd_test = "python3 {}/python_scripts/get-results.py {} {} {} {} {} {} {} {}".format(test.mypath,jobnum,subdir,test.machine_name,self.type,test.script_dir,test.artifacts_root,mpiver,branch)
    print(monitor_cmd_test)
    proc = subprocess.Popen(monitor_cmd_test, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    test.createGetResScripts(monitor_cmd_build,monitor_cmd_test)
