# -*- coding: utf-8 -*-
import string

from .jsonConcat import JsonConcat
from . import h5CommandManager, h5UserAPI


class CommandProcessor(object):
    def __init__(self, managerType):
        if managerType == 'h5':
            self.manager = h5CommandManager.H5CommandManager()
            self.userAPI = h5UserAPI
            self.concat = JsonConcat('h5')

    '''
    通过id查找，则传入{"id":id},
    通过name查找，传入{"name":"name","index",index}
    通过Xpath查找，传入{"xpath":"//*[@id=\"dctlist\""}
    '''

    def doCommandWithElement(self, byType, actionType, text=None, **domType):
        jsActionType = self.manager.getJsAction(actionType, None)
        if jsActionType is not None:

            # 找到控件dom
            domTemplate = self.manager.getElement(byType)
            domTemplateType = string.Template(domTemplate)
            domResult = domTemplateType.substitute(**domType)
            # 使用xpath找控件,需要先转义成\\\",在json中会转义成\",在js中执行"
            if byType == self.userAPI.ByType.XPATH:
                domResult = domResult.replace('"', '\\\"')
            # 组装json命令
            if actionType == self.userAPI.ActionType.TEXT:
                if text is None:
                    raise TypeError('请输入要设置的text值')
                jsActionTemplate = string.Template(jsActionType)
                jsActionResult = jsActionTemplate.substitute({"text": text})
            else:
                jsActionResult = jsActionType
            jsCommand = domResult + jsActionResult
            params = {"expression": jsCommand}
            jsonResult = self.concat.concat(actionType, **params)
            return jsonResult
        else:
            raise TypeError('ActionType错误')

    '''
     不需要找到控件的command，比如滑动，获得html，获得node等。参数根据不同的actionType传入。
     比如当actionType为SCROLL,参数为
     {
       "x": "x", "y": "y","xDistance": "xDistance", "yDistance": "yDistance"
     }
     也可以是CLOSE_WINDOW等不需要参数的actionType
    '''

    def doCommandWithoutElement(self, actionType, **kw):
        kwResult = self.manager.getExpression(actionType, None)
        if kwResult is not None:
            # getValue的时候会传入value值
            if kw is not None:
                paramsCat = string.Template(kwResult)
                kwResult = paramsCat.substitute(**kw)
            params = dict()
            params["expression"] = kwResult
            jsonResult = self.concat.concat(actionType, **params)
        else:
            jsonResult = self.concat.concat(actionType, **kw)
        return jsonResult


if __name__ == "__main__":
    pass
