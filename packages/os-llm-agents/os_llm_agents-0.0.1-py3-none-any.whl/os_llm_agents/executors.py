import re
import json

from typing import Any, Dict

from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    FunctionMessage,
    HumanMessage
)


class AgentExecutor:
    def __init__(self, llm, tools: list, system_prompt: str):
        """

        Example tool:
        
        def multiply(**kwargs) -> int:
            # Multiply two integers together.
            print(kwargs)
            n1, n2 = kwargs["n1"], kwargs["n2"]
            return n1 * n2
            
        multiply_tool = {
            "name": "multiply",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "n1": {
                        "type": "int",
                        "description": "Number one",
                    },
                    "n2": {
                        "type": "int",
                        "description": "Number two",
                    },
                },
                "required": ["n1", "n2"],
            },
            "implementation": multiply,  # Attach the function implementation
        }
        """
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        
        tool_description = """Use the function '{name}' to {description}:
{tool_json}"""
        tool_descriptions = [tool_description.format(
            name=tool["name"],
            description=tool["description"],
            tool_json=json.dumps(tool["parameters"])
        ) for tool in tools]
        self.tool_prompt = self._generate_tool_prompt(tool_descriptions)

    def _generate_tool_prompt(self, tool_descriptions: list) -> str:
        tools_text = "\n".join(tool_descriptions)
        return f"""
        {self.system_prompt}
        
        You have access to the following functions:

        {tools_text}

        Don't call the function if there is no need for that

        If you choose to call a function ONLY reply in the following format with no prefix or suffix:

        <function=example_function_name>{{"example_name": "example_value"}}</function>

        Reminder:
        - Function calls MUST follow the specified format, start with <function= and end with </function>
        - Required parameters MUST be specified
        - Only call one function at a time
        - Put the entire function call reply on one line

        If there is no function call available, answer the question **like normal with your current knowledge and do not tell the user about function calls**
        """

    def invoke(self, user_input: str, chat_history: list = None) -> Any:
        if chat_history is None:
            chat_history = []
            # Introduce system prompt to the chat history
            chat_history.append(SystemMessage(content=self.tool_prompt))
        else:
            # if no system prompt available
            if not isinstance(chat_history[0], SystemMessage):
                chat_history = [
                    SystemMessage(content=self.tool_prompt)
                ] + chat_history
        
        # Invoke the LLM
        response = self.llm.invoke(user_input, chat_history=chat_history)
        chat_history.append(HumanMessage(content=user_input))
        
        # Parse and execute the response
        parsed_response = self.parse_tool_response(response)
        if parsed_response:
            response = FunctionMessage(
                content=str(self.execute_tool(parsed_response)),
                name=parsed_response["function"]
            )
        else:
            response = AIMessage(content=response)

        chat_history.append(response)
        
        return {"response": response, "chat_history": chat_history}

    def parse_tool_response(self, response: str) -> Dict[str, Any]:
        function_regex = r"<function=(\w+)>(.*?)</function>"
        match = re.search(function_regex, response)

        if match:
            function_name, args_string = match.groups()
            try:
                args = json.loads(args_string)
                return {
                    "function": function_name,
                    "arguments": args,
                }
            except json.JSONDecodeError as error:
                print(f"Error parsing function arguments: {error}")
                return None
        return None

    def execute_tool(self, parsed_response: Dict[str, Any]) -> Any:
        available_functions = {tool['name']: tool for tool in self.tools}
        
        fun_name = parsed_response["function"]
        arguments = parsed_response["arguments"]
        
        if fun_name in available_functions:
            tool_function = available_functions[fun_name]["implementation"]
            return tool_function(**arguments)
        
        print(f"Function {fun_name} not available.")
        return None