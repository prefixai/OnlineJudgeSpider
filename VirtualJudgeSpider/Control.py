from VirtualJudgeSpider.Config import Problem

supports = ['Aizu', 'HDU', 'FZU', 'POJ', 'WUST', 'ZOJ']


class OJBuilder(object):
    @staticmethod
    def build_oj(name, *args, **kwargs):
        if name:
            try:
                module_meta = __import__('VirtualJudgeSpider.OJs.%sClass' % (name,), globals(), locals(),
                                         [name])
                class_meta = getattr(module_meta, name)
                oj = class_meta(*args, **kwargs)
                return oj
            except ModuleNotFoundError:
                pass
        return None


class Controller(object):
    def __init__(self, oj_name):
        remote_oj = Controller.get_real_remote_oj(oj_name)
        self._oj = OJBuilder.build_oj(remote_oj)
        self._origin_name = oj_name

    @staticmethod
    def get_real_remote_oj(name):
        """

        :param name: oj名称，可能与数据库里面保存的名称不一致，需要通过这个函数找到数据库名称
        :return: 数据库名称，或者不存在
        """
        for oj_name in supports:
            if str(name).upper() == str(oj_name).upper():
                return oj_name
        return None

    # 获取支持的OJ列表
    @staticmethod
    def get_supports():
        return supports

    # 判断当前是否支持
    @staticmethod
    def is_support(oj_name):
        if Controller.get_real_remote_oj(oj_name):
            return True
        return False

    def get_home_page_url(self):
        if not self._oj:
            return None
        return self._oj.home_page_url()

    # 获取题面
    def get_problem(self, pid, account, **kwargs):
        if not self._oj:
            problem = Problem()
            problem.remote_oj = self._origin_name
            problem.remote_id = pid
            problem.status = Problem.Status.STATUS_OJ_NOT_EXIST
            return problem
        return self._oj.get_problem(pid=pid, account=account, **kwargs)

    # 提交代码
    def submit_code(self, pid, account, code, language, **kwargs):
        if not self._oj:
            return None
        return self._oj.submit_code(account=account, code=code, language=language, pid=pid, **kwargs)

    # 获取结果
    def get_result(self, account, pid, **kwargs):
        if not self._oj:
            return None
        return self._oj.get_result(account=account, pid=pid, **kwargs)

    # 通过运行id获取结果
    def get_result_by_rid_and_pid(self, rid, pid):
        if not self._oj:
            return None
        return self._oj.get_result_by_rid_and_pid(rid, pid)

    # 获取源OJ语言
    def find_language(self, account, **kwargs):
        if not self._oj:
            return None
        return self._oj.find_language(account=account, **kwargs)

    # 判断是否是等待判题的返回结果，例如pending,Queuing,Compiling
    def is_waiting_for_judge(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_waiting_for_judge(verdict)

    # 判断源OJ的网络连接是否良好
    def check_status(self):
        if not self._oj:
            return None
        return self._oj.check_status()

    def is_accepted(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_accepted(verdict)

    def is_running(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_running(verdict)

    def is_compile_error(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_compile_error(verdict)
