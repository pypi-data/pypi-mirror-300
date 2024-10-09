import ast

def get_function_info(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    functions_dict = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_info = {
                "name": node.name,
                "description": ast.get_docstring(node),
                "parameters": [],
                "return_type": None
            }

            for arg in node.args.args:
                param_info = {
                    "name": arg.arg,
                    "type": None
                }
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        param_info["type"] = arg.annotation.id
                    elif isinstance(arg.annotation, ast.Subscript):
                        param_info["type"] = ast.unparse(arg.annotation)
                function_info["parameters"].append(param_info)

            if node.returns:
                if isinstance(node.returns, ast.Name):
                    function_info["return_type"] = node.returns.id
                elif isinstance(node.returns, ast.Subscript):
                    function_info["return_type"] = ast.unparse(node.returns)

            functions_dict[function_info["name"]] = function_info

    return functions_dict