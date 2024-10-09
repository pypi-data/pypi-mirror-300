The external function (tool) set can be parsed by FastMindAPI in the form of a package, allowing the LLM to invoke these functions through natural language.

## 1 File Structure

### 1.1 Directory

A function set should be organized like this:

```
Custom_Python_Package/
	__init__.py
	requirements.txt
	tools.json
	ModuleA/
		__init__.py
		submodule1.py
	ModuleB/
	...
```

The root directory name is used as the `tool_package_name`.

### 1.2 tools.json

The file `tools.json` in the root directory is necessary for storing some metadata.

The "path" field provides the relative path of the function's file; please refer to the format in the following example.

```json
{
  "TestFunc":{
    "path": "ModuleA/submodule1.py"
  },
  ...
}
```

### 1.3 Custom Function (tool)

The functions need to have:

- Docstrings; (`Name`,  `Description`, `Parameters`, `Returns`)
- Type hints for input parameters. (Only native Python types are supported for parameters.)

Tips:

- The naming convention for Python functions mainly follows the PEP 8 style guide, using snake_case.

```python
# In ModuleA/submodule1.py

def test_func(Param1: str, Param2: List[int]):
    """
    Name: test_func
    Description: ...
    Parameters:
        Param1: str, ...
        Param2: List[int], ...
    Returns:
        Output1: dict, ...
    Other Information
    """
    return Output1
```

## 2 Local Debugging

`pip install fastmindapi`

### 2.1 Load Sets

```python
from fastmindapi.modules import FunctionModule

Tool_Set_List = [
  ".../Tool_Package_1",
  ".../Tool_Package_2"
]

func_module = FunctionModule(Tool_Set_List)
```

### 2.2 Get Info

The format of tool information is the same as OpenAI's.

```python
func_module.get_all_tool_names_list()
func_module.get_tool_information_text_list(['Tool_Package_1/Tool_1', 'Tool_Package_2/Tool_1'])

```

### 2.3 Call a Function

```python
# Method 1
func_module.exec_tool_calling("Tool_Package_1/Tool_1(...)")
# Method 2
func_module.tool_pool_dict["Tool_Package_1"].call_tool("Tool_1",[])

# Example
func_module.exec_tool_calling("chem_lib/get_element_properties(element='Au')")
func_module.tool_pool_dict["chem_lib"].call_tool("get_element_properties",["Au"])
```

