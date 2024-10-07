import json
import logging
import os
import subprocess
from typing import List

from libtokit.path import check_file_exists

UNLIMITED = -1
VERSION = 0x020101

RESULT_SUCCESS = 0
RESULT_WRONG_ANSWER = -1
RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
RESULT_MEMORY_LIMIT_EXCEEDED = 3
RESULT_RUNTIME_ERROR = 4
RESULT_SYSTEM_ERROR = 5

ERROR_INVALID_CONFIG = -1
ERROR_FORK_FAILED = -2
ERROR_PTHREAD_FAILED = -3
ERROR_WAIT_FAILED = -4
ERROR_ROOT_REQUIRED = -5
ERROR_LOAD_SECCOMP_FAILED = -6
ERROR_SETRLIMIT_FAILED = -7
ERROR_DUP2_FAILED = -8
ERROR_SETUID_FAILED = -9
ERROR_EXECVE_FAILED = -10
ERROR_SPJ_ERROR = -11


logger = logging.getLogger('judger')

lib_path = os.getenv('LIB_JUDGER_SO', '/usr/lib/judger/libjudger.so')
err, msg = check_file_exists(lib_path)
if err:
    msg = f"lib_path: {lib_path}, err: {err}, msg: {msg}"
    logger.error(msg)
    raise ValueError(msg)


class ComDo:
    UNLIMITED = -1
    VERSION = 0x020101
    RESULT_SUCCESS = 0
    RESULT_WRONG_ANSWER = -1
    RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
    RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
    RESULT_MEMORY_LIMIT_EXCEEDED = 3
    RESULT_RUNTIME_ERROR = 4
    RESULT_SYSTEM_ERROR = 5
    ERROR_INVALID_CONFIG = -1
    ERROR_FORK_FAILED = -2
    ERROR_PTHREAD_FAILED = -3
    ERROR_WAIT_FAILED = -4
    ERROR_ROOT_REQUIRED = -5
    ERROR_LOAD_SECCOMP_FAILED = -6
    ERROR_SETRLIMIT_FAILED = -7
    ERROR_DUP2_FAILED = -8
    ERROR_SETUID_FAILED = -9
    ERROR_EXECVE_FAILED = -10
    ERROR_SPJ_ERROR = -11

    @classmethod
    def do(cls, proc_args: List[str] = None):
        logger.debug(f"ComDo: {proc_args}")
        proc = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        logger.debug(f"ComDo out: {out}, err {err}")
        if err:
            raise ValueError("Error occurred while calling judger: {}".format(err))
        data = json.loads(out.decode("utf-8"))
        logger.debug(f"ComDo return: {data}")
        return data


class Judger(ComDo):
    lib_path = lib_path
    str_list_vars = ["args", "env"]
    int_vars = ["max_cpu_time", "max_real_time",
                "max_memory", "max_stack", "max_output_size",
                "max_process_number", "uid", "gid", "memory_limit_check_only"]
    str_vars = ["exe_path", "input_path", "output_path", "error_path", "log_path"]

    @classmethod
    def check_str_list_vars(cls, local_args: dict = None, proc_args: List[str] = None):
        for var in cls.str_list_vars:
            value = local_args[var]
            if not isinstance(value, list):
                raise ValueError("{} must be a list".format(var))
            for item in value:
                if not isinstance(item, str):
                    raise ValueError("{} item must be a string".format(var))
                proc_args.append("--{}={}".format(var, item))
        return proc_args

    @classmethod
    def check_str_vars(cls, local_args: dict = None, proc_args: List[str] = None):
        for var in cls.str_vars:
            value = local_args[var]
            if not isinstance(value, str):
                raise ValueError("{} must be a string".format(var))
            proc_args.append("--{}={}".format(var, value))
        return proc_args

    @classmethod
    def check_int_vars(cls, local_args: dict = None, proc_args: List[str] = None):
        for var in cls.int_vars:
            value = local_args[var]
            if not isinstance(value, int):
                raise ValueError("{} must be an int".format(var))
            if value != UNLIMITED:
                proc_args.append("--{}={}".format(var, value))
        return proc_args

    @classmethod
    def run(cls, max_cpu_time, max_real_time, max_memory, max_stack, max_output_size, max_process_number,
            exe_path, input_path, output_path, error_path, args, env, log_path, seccomp_rule_name, uid, gid,
            memory_limit_check_only=0, debug: bool = False):
        # 传入的所有变量进入到local()中
        local_args = locals()
        proc_args = [cls.lib_path]
        proc_args = cls.check_str_list_vars(local_args=local_args, proc_args=proc_args)
        proc_args = cls.check_int_vars(local_args=local_args, proc_args=proc_args)
        proc_args = cls.check_str_vars(local_args=local_args, proc_args=proc_args)
        if not isinstance(seccomp_rule_name, str) and seccomp_rule_name is not None:
            raise ValueError("seccomp_rule_name must be a string or None")
        if seccomp_rule_name:
            proc_args.append("--seccomp_rule={}".format(seccomp_rule_name))
        if debug:
            return proc_args
        return cls.do(proc_args=proc_args)


def main():
    result = Judger.run(
        max_cpu_time=1000,
        max_real_time=3000,
        max_memory=128 * 1024 * 1024,
        max_stack=128 * 1024 * 1024,
        max_output_size=1024 * 1024,
        max_process_number=UNLIMITED,
        exe_path='/path/to/executable',
        input_path='/path/to/input',
        output_path='/path/to/output',
        error_path='/path/to/error',
        args=['arg1', 'arg2'],
        env=['ENV_VAR=value', 'ANOTHER_VAR=another_value'],
        log_path='/path/to/log',
        seccomp_rule_name='default',
        uid=1000,
        gid=1000,
        debug=True,
    )
    print(f'Result: {result}')


# 使用示例
if __name__ == "__main__":
    main()
