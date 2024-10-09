import os
import sys
import re

from ...utils.file import read_JSON
from .parser import get_function_info
# from .param import get_tool_param


def parse_docstring(input_string: str) -> dict | str:
    # 使用正则表达式解析字符串
    pattern = re.compile(
        r'Name:\s*(?P<name>.*?)\n'
        r'Description:\s*(?P<description>.*?)\n'
        r'Parameters:\n(?P<parameters>.*?)\n'
        r'Returns:\n(?P<returns>.*?)(?=\n[A-Za-z]|$)', re.DOTALL)
    match = pattern.match(input_string)

    if match:
        # 提取匹配的内容
        name = match.group('name')
        description = match.group('description')
        parameters = match.group('parameters').strip().split('\n')
        returns = match.group('returns').strip().split('\n')

        return {
            "Name": name,
            "Description": description,
            "Parameters": parameters,
            "Returns": returns
            }
    else:
        return "No match found."


class FunctionPool:
    def __init__(self, code_dir_path):
        self.code_dir_path = code_dir_path
        self.code_father_dir_path = "/".join(self.code_dir_path.strip().rstrip("/").split("/")[:-1])
        if self.code_father_dir_path not in sys.path:
            sys.path.append(self.code_father_dir_path)
        self.tool_package_name = self.code_dir_path.strip().rstrip("/").split("/")[-1]

        self.meta_data = read_JSON(os.path.join(self.code_dir_path, "tools.json"))
        self.toolrawinfo = {}
        self.get_toolrawinfo_from_metapath()
        self.toolinfo = {}
        self.process_toolinfo()

    def get_toolrawinfo_from_metapath(self):
        for tool_name in self.meta_data:
            tool_relative_path = self.meta_data[tool_name]["path"]
            self.toolrawinfo[tool_name] = get_function_info(os.path.join(self.code_dir_path,tool_relative_path))[tool_name]

    def process_toolinfo(self):
        for tool_name in self.toolrawinfo:
            print("Getting Tool Info: ", tool_name)
            raw_info = self.toolrawinfo[tool_name]
            doc_string = parse_docstring(raw_info['description'])
            tool_info = {}
            tool_info["name"] = raw_info['name']
            tool_info["description"] = doc_string['Description']
            tool_info["parameters"] = {"type": "object", "properties":{}}
            param_description_dict = {}
            for param_text in doc_string["Parameters"]:
                param_name = param_text.split(":")[0]
                param_description = param_text[len(param_name)+1:].strip()
                param_description_dict[param_name.strip()] = param_description
            for raw_param_dict in raw_info['parameters']:
                param_name = raw_param_dict["name"]
                tool_info["parameters"]["properties"][param_name] = {}
                tool_info["parameters"]["properties"][param_name]["type"] = raw_param_dict["type"]
                if param_name in param_description_dict:
                    tool_info["parameters"]["properties"][param_name]["description"] = param_description_dict[param_name][len(raw_param_dict["type"])+1:].strip()
            self.toolinfo[tool_name] = tool_info

    def call_tool(self, tool_name: str, parameters_list: list):
        tool_path = self.meta_data[tool_name]["path"]
        import_cmd = "from "+self.tool_package_name+"."+tool_path.split(".py")[0].replace("/",".")+" import "+tool_name
        exec(import_cmd)
        calling_cmd = tool_name+"("+",".join([str(param) if type(param) is not str else '"'+param+'"' for param in parameters_list])+")"
        calling_result = eval(calling_cmd)
        # calling_result = post_process_execution_result(calling_result)
        return calling_result
        # try:
        #     return eval(calling_cmd)
        # except:  # noqa: E722
        #     return "Calling Tool Failed."
