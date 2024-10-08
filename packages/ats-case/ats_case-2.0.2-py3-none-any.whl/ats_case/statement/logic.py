from ats_base.common import func
from ats_base.log.logger import logger

from ats_case.case import command
from ats_case.case.context import Context


def monitoring_control(func):
    """
    逻辑控制语句监测和控制
    :param func:
    :return:
    """

    def wrap(self, index):
        # 执行前
        self._context.runtime.step = self._steps[index]

        is_jump = False
        if _is_condition_step(self._context):
            if not _condition_is_true(self._context):
                # 条件False -> 跳到控制语句结束步骤
                is_jump = True

        # 执行步骤
        if not is_jump:
            _log_in_loop(self._context)
            func(self, index)

        # 执行后
        if _is_end_step(self._context):
            if not _loop_is_over(self._context):
                # 循环没有结束 -> 跳到循环开始第一步
                is_jump = True
            else:  # 控制语句结束 -> 跳到下一步
                try:
                    is_jump = True
                    self._context.runtime.step = self._steps[self._steps.index(self._context.runtime.step) + 1]
                except:  # 溢出 - 例如if的结束步骤是这个用例的最后一步
                    # is_jump = False
                    pass

        if is_jump:
            index = self._steps.index(self._context.runtime.step)
        else:
            index = self._steps.index(self._context.runtime.step) + 1

        return index

    return wrap


def _is_condition_step(context: Context):
    """
    步骤是否带有条件判断
    :param context:
    :return:
    """
    return context.runtime.step in context.runtime.conditions


def _condition_is_true(context: Context):
    """
    条件判断
    :param context:
    :return:
    """
    # if条件
    ifBody = context.runtime.logicBody.get("IF_S_{}".format(context.runtime.step))
    if ifBody is not None and isinstance(ifBody, dict):
        try:
            ci = int(ifBody.get("condition"))
        except:
            ci = int(context.runtime.glo.get(ifBody.get("condition"), 1))

        if ci == 0:  # 条件判断False
            start = ifBody.get("start")
            end = ifBody.get("end")

            context.runtime.step = end
            for i in range(start, end + 1):
                context.runtime.sos.update({i: func.to_dict(result=None)})

            return False

    # loop条件 - 实例化currentLoop
    loopBody = context.runtime.logicBody.get("LOOP_S_{}".format(context.runtime.step))
    if loopBody is not None and isinstance(loopBody, dict):
        start = loopBody.get("start", 0)
        end = loopBody.get("end", 0)
        count = loopBody.get("count", 0)

        if count <= 0:
            context.runtime.step = end
            for i in range(start, end + 1):
                context.runtime.sos.update({i: func.to_dict(result=None)})
            return False

        if context.runtime.currentLoop is None:
            context.runtime.currentLoop = _new_loop(context, start=start, end=end, count=count)
            _log(context)
        else:
            # 新的循环
            if context.runtime.currentLoop.start != start:
                newLoop = _new_loop(context, start=start, end=end, count=count)

                # 判断新的循环是否有父循环
                if context.runtime.currentLoop.start < newLoop.start \
                        and newLoop.end <= context.runtime.currentLoop.end:
                    newLoop.parent = context.runtime.currentLoop
                else:
                    if context.runtime.currentLoop.parent is not None:
                        if context.runtime.currentLoop.parent.start < newLoop.start \
                                and newLoop.end <= context.runtime.currentLoop.parent.end:
                            newLoop.parent = context.runtime.currentLoop.parent

                context.runtime.currentLoop = newLoop
                _log(context)

    return True


def _is_end_step(context: Context):
    """
    控制语句结束步骤
    :param context:
    :return:
    """
    return context.runtime.step in context.runtime.endSteps


def _loop_is_over(context: Context, is_over=True):
    """
    循环结束
    :param context:
    :return:
    """
    if context.runtime.currentLoop is not None:
        context.runtime.currentLoop.index += 1
        if context.runtime.currentLoop.index < context.runtime.currentLoop.count:
            context.runtime.step = context.runtime.currentLoop.start
            is_over = False
        else:
            # 循环结束 - 输出日志
            _log(context, level=1)

            if context.runtime.currentLoop.parent is not None \
                    and context.runtime.step == context.runtime.currentLoop.parent.end_step:
                context.runtime.currentLoop = context.runtime.currentLoop.parent
                is_over = _loop_is_over(context)

        if is_over:
            context.runtime.currentLoop = None

    return is_over


def _new_loop(context: Context, start=0, end=0, count=0):
    context.runtime.loop_sn += 1
    return CurrentLoop(sn=context.runtime.loop_sn, start=start, end=end, count=count)


def _log_in_loop(context: Context):
    if context.runtime.currentLoop is not None:
        _log(context, 2)


def _log(context: Context, level=0):
    if level == 0:
        logger.info('~ @TCC-LOOP-> loops[#{}] start. -range {}:{}  -count {}'.format(
            context.runtime.currentLoop.sn, context.runtime.currentLoop.start,
            context.runtime.currentLoop.end, context.runtime.currentLoop.count))

        command.client().message('[#{}]循环开始 - 步骤范围[{}-{}], 共{}次'.format(
            context.runtime.currentLoop.sn, context.runtime.currentLoop.start,
            context.runtime.currentLoop.end, context.runtime.currentLoop.count)).show(context)

    if level == 1:
        command.client().message("[#{}]循环结束...".format(context.runtime.currentLoop.sn)).show(context)
        logger.info('~ @TCC-LOOP-> loops[#{}] end.'.format(context.runtime.currentLoop.sn))

    if level == 2:
        logger.info('~ @TCC-LOOP-> loops[#{}], -count {}, -index {}'.format(
            context.runtime.currentLoop.sn, context.runtime.current.count,
            context.runtime.currentLoop.index + 1))
        command.client().message('[#{}]循环 - 共{}次, 当前执行第{}次'.format(
            context.runtime.currentLoop.sn, context.runtime.currentLoop.count,
            context.runtime.currentLoop.index + 1)).show(context)


# class CurrentIf(object):
#     def __init__(self):
#         self._sn = ""
#         self._start_step = 0
#         self._end_step = 0
#         self._condition = 0
#         self._parent = None
#         self._next_branch = None


class CurrentLoop(object):
    def __init__(self, sn=0, start=0, end=0, count=0):
        self._sn = sn
        self._start = start
        self._end = end
        self._count = count
        self._index = 0
        self._parent = None

    @property
    def sn(self):
        return self._sn

    @sn.setter
    def sn(self, value):
        self._sn = value

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def count(self):
        return self._count

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

# def decorator(func):
#     def wrapper(self, index):
#         # 在装饰器中可以访问self
#         print("Accessing self:", self._p)
#         # 调用被装饰的方法
#         func(self, index)
#
#         return 1
#
#     return wrapper
#
#
# class MyClass:
#     def __init__(self, p: int):
#         self._p = p
#
#     @decorator
#     def my_method(self, index):
#         print("Executing my_method with param:", index)
#
#
# if __name__ == '__main__':
#     obj = MyClass(1)
#     print(obj.my_method(10))
