# ==================================================================================================
# --- Imports
# ==================================================================================================
# Standard library imports

# ==================================================================================================
# --- Class for job submission
# ==================================================================================================
class SubmissionStatement:
    def __init__(self, sub_filename, path_job_folder, context):
        self.sub_filename = sub_filename
        self.path_job_folder = (
            path_job_folder[:-1] if path_job_folder[-1] == "/" else path_job_folder
        )

        # GPU configuration
        if context in ["cupy", "opencl"]:
            self.request_GPUs = 1
            self.slurm_queue_statement = ""
        else:
            self.request_GPUs = 0
            self.slurm_queue_statement = "#SBATCH --partition=slurm_hpc_acc"


class LocalPC(SubmissionStatement):
    def __init__(self, sub_filename, path_job_folder, context=None):
        super().__init__(sub_filename, path_job_folder, context)

        self.head = "# Running on local pc"
        self.body = f"bash {self.path_job_folder}/run.sh &"
        self.tail = "# Local pc"
        self.submit_command = self.get_submit_command(sub_filename)

    @staticmethod
    def get_submit_command(sub_filename):
        return f"bash {sub_filename}"


class Slurm(SubmissionStatement):
    def __init__(self, sub_filename, path_job_folder, context):
        super().__init__(sub_filename, path_job_folder, context)

        self.head = "# Running on SLURM "
        self.body = f"sbatch --ntasks=2 {self.slurm_queue_statement.split(' ')[1] if self.slurm_queue_statement != '' else self.slurm_queue_statement} --output=output.txt --error=error.txt --gres=gpu:{self.request_GPUs} {self.path_job_folder}/run.sh"
        self.tail = "# SLURM"
        self.submit_command = self.get_submit_command(sub_filename)

    @staticmethod
    def get_submit_command(sub_filename):
        return f"bash {sub_filename}"


class SlurmDocker(SubmissionStatement):
    def __init__(self, sub_filename, path_job_folder, context, path_image, fix=False):
        super().__init__(sub_filename, path_job_folder, context)

        # ! Ugly fix, will need to be removed when INFN is fixed
        if fix:
            to_replace = "/storage-hpc/gpfs_data/HPC/home_recovery"
            replacement = "/home/HPC"
            self.path_job_folder = self.path_job_folder.replace(to_replace, replacement)
            path_image = path_image.replace(to_replace, replacement)
            self.sub_filename = self.sub_filename.replace(to_replace, replacement)
            self.str_fixed_run = (
                f"sed -i 's/{to_replace}/{replacement}/' {self.path_job_folder}/run.sh\n"
            )

        self.head = (
            "#!/bin/bash\n"
            + "# This is a SLURM submission file using Docker\n"
            + self.slurm_queue_statement
            + "\n"
            + f"#SBATCH --output={self.path_job_folder}/output.txt\n"
            + f"#SBATCH --error={self.path_job_folder}/error.txt\n"
            + "#SBATCH --ntasks=2\n"
            + f"#SBATCH --gres=gpu:{self.request_GPUs}"
        )
        self.body = f"singularity exec {path_image} {self.path_job_folder}/run.sh"
        self.tail = "# SLURM Docker"
        self.submit_command = self.get_submit_command(sub_filename)

    @staticmethod
    def get_submit_command(sub_filename):
        return f"sbatch {sub_filename}"


class HTC(SubmissionStatement):
    def __init__(self, sub_filename, path_job_folder, context, htc_flavor="espresso"):
        super().__init__(sub_filename, path_job_folder, context)

        self.head = (
            "# This is a HTCondor submission file\n"
            + "error  = error.txt\n"
            + "output = output.txt\n"
            + "log  = log.txt"
        )
        self.body = (
            f"initialdir = {self.path_job_folder}\n"
            + f"executable = {self.path_job_folder}/run.sh\n"
            + f"request_GPUs = {self.request_GPUs}\n"
            + f"+JobFlavour  = {htc_flavor}\n"
            + "queue"
        )
        self.tail = "# HTC"
        self.submit_command = self.get_submit_command(sub_filename)

    @staticmethod
    def get_submit_command(sub_filename):
        return f"condor_submit {sub_filename}"


class HTCDocker(SubmissionStatement):
    def __init__(self, sub_filename, path_job_folder, context, path_image, htc_flavor="espresso"):
        super().__init__(sub_filename, path_job_folder, context)

        self.head = (
            "# This is a HTCondor submission file using Docker\n"
            + "error  = error.txt\n"
            + "output = output.txt\n"
            + "log  = log.txt\n"
            + "universe = vanilla\n"
            + "+SingularityImage ="
            + f' "{path_image}"'
        )
        self.body = (
            f"initialdir = {self.path_job_folder}\n"
            + f"executable = {self.path_job_folder}/run.sh\n"
            + f"request_GPUs = {self.request_GPUs}\n"
            + f"+JobFlavour  = {htc_flavor}\n"
            + "queue"
        )
        self.tail = "# HTC Docker"
        self.submit_command = self.get_submit_command(sub_filename)

    @staticmethod
    def get_submit_command(sub_filename):
        return f"condor_submit {sub_filename}"
