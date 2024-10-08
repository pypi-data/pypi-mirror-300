import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from kytest.utils.log import logger
from kytest.core.adr.driver import Driver


class Elem(object):
    """
    安卓控件定义
    https://github.com/openatx/uiautomator2
    """

    def __init__(self, driver: Driver = None, watch: list = None, **kwargs):
        """
        @param driver: 安卓驱动
        @param watch: 需要处理的异常弹窗定位方式列表
        """
        self._kwargs = kwargs
        self._driver = driver
        self._xpath = kwargs.get('xpath', None)
        self._watch = watch

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    # 公共方法
    def watch_handler(self):
        """
        异常弹窗处理
        @return:
        """
        logger.info("开始弹窗检测")
        ctx = self._driver.d.watch_context()
        for loc in self._watch:
            ctx.when(loc).click()
        ctx.wait_stable()
        ctx.close()
        logger.info("检测结束")

    def find(self, timeout=5, n=3):
        """
        增加截图的方法
        @param timeout: 每次查找时间
        @param n：失败后重试的次数
        @return:
        """
        logger.info(f"查找: {self._kwargs}")
        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath is not None else self._driver.d(**self._kwargs)

        retry_count = n
        if _element.wait(timeout=timeout):
            logger.info(f"查找成功")
            return _element
        else:
            if retry_count > 0:
                for count in range(1, retry_count + 1):
                    logger.info(f"第{count}次重试...")
                    if self._watch:
                        self.watch_handler()
                    if _element.wait(timeout=timeout):
                        logger.info(f"查找成功")
                        return _element

            logger.info("查找失败")
            self._driver.shot("查找失败")
            raise Exception(f"控件: {self._kwargs}, 查找失败")

    # 属性获取
    def get_text(self, timeout=5):
        logger.info("获取文本")
        _elem = self.find(timeout=timeout)
        if isinstance(_elem, XPathSelector):
            elems = _elem.all()
        else:
            elems = list(_elem)
        text = []
        for elem in elems:
            text.append(elem.get_text())

        if len(text) == 1:
            text = text[0]
        return text

    def exists(self, timeout=5):
        logger.info("是否存在")
        result = False
        try:
            _element = self.find(timeout=timeout, n=0)
            result = True
        except:
            result = False
        finally:
            return result

    def count(self, timeout=5):
        logger.info("获取定位到的控件数量")
        return self.find(timeout=timeout).count

    def info(self, timeout=5):
        logger.info("获取控件信息")
        return self.find(timeout=timeout).info

    def center(self, timeout=5, *args, **kwargs):
        return self.find(timeout=timeout).center(*args, **kwargs)

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector],
                      offset=(0.5, 0.5)):
        """
        修正控件中心坐标
        """
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    # 操作
    def click(self, timeout=5):
        logger.info("点击")
        element = self.find(timeout=timeout)
        x, y = self._adapt_center(element)
        self._driver.util.click(x, y)

    def long_click(self, timeout=5):
        logger.info("长按")
        element = self.find(timeout=timeout)
        x, y = self._adapt_center(element)
        self._driver.long_click(x, y)

    def input(self, text, timeout=5, pwd_check=False):
        logger.info("输入")
        self.click(timeout=timeout)
        if pwd_check is True:
            self._driver.d(focused=True).set_text(text)
        else:
            self._driver.util.input(text)

    def clear_text(self, timeout=5, *args, **kwargs):
        logger.info("清空")
        self.find(timeout=timeout).clear_text(*args, **kwargs)

    def screenshot(self, file_path, timeout=5):
        logger.info("截屏")
        self.find(timeout=timeout).screenshot().save(file_path)

    def drag_to(self, timeout=5, *args, **kwargs):
        logger.info("拖动")
        self.find(timeout=timeout).drag_to(*args, **kwargs)


if __name__ == '__main__':
    pass







