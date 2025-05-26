from openai import OpenAI
import sys
import subprocess
from kira_utils import get_api_key, get_encrypted_api_key, multi_line_input, stream_output, stream_output_reason

class Model:
    def __init__(self, vendor_name='', url='', v3='', r1='', key_path='', key_key_path='', encrypt=False):
        self.vendor_name = vendor_name
        self.url = url
        self.model_v3_name = v3
        self.model_r1_name = r1

        self.api_key_path = key_path
        self.api_key_key_path = key_key_path
        self.api_key_encrypt = encrypt

        self.client = None
        self.init_client()

        self.message = [{
            "role": "system",
            "content": "你是领域专家，从专业角度回答用户问题，优先考虑专业性"
        }]

        self.history = []

    def init_client(self):
        api_key = None
        if self.api_key_encrypt:
            api_key = get_encrypted_api_key(self.api_key_path, self.api_key_key_path)
        else:
            api_key = get_api_key(self.api_key_path)

        self.client =  OpenAI(
            api_key = api_key,
            base_url = self.url
        )


    def chat_once(self, args, config):
        user_input = sys.stdin.read()
        if args.add:
            print(user_input)
        else:
            print('[' + self.vendor_name + '-' + config.models[config.model_choice]['v3'] + ' 🤖 ]:')
        pre_input = " ".join(args.non_option_args)
        user_input = pre_input + "\n" + user_input

        self.history.append(user_input)

        message = self.message
        message.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=config.models[config.model_choice]['v3'],
            messages=message,
            stream=args.stream
        )

        print('')
        
        if args.stream:
            content = stream_output(response)
            self.history.append(content)
        else:
            print(response.choices[0].message.content)
            self.history.append(response.choices[0].message.content)


    def chat(self, args, config):
        pre_input = " ".join(args.non_option_args)
        message = self.message
        while True:
            print('🥰:')
            user_input = multi_line_input()
            if user_input == 'exit' or user_input == 'quit' or user_input == 'q':
                break

            if user_input.startswith('!'):
                command = user_input[1:]
                pre_input = ''
                try:
                    print('命令执行成功')
                    result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
                    pre_input = result.stdout + '\n' + result.stderr
                    print(pre_input)
                    message.append({"refusal":None, "annotations": None, "audio": None, "function_call": None, "tool_calls": None, "role": "assistant", "content": pre_input})
                except subprocess.CalledProcessError as e:
                    print('命令执行失败:', e)
                continue

            user_input = pre_input + '\n' + user_input
            self.history.append(user_input)

            message = self.message
            message.append({"role": "user", "content": user_input})
            message.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=config.models[config.model_choice]['v3'],
                messages=message,
                stream=args.stream
            )

            print('')
            cur_content = ""

            if args.stream:
                print('[' + self.vendor_name + '-' + config.models[config.model_choice]['v3'] + ' 🤖 ]:')
                cur_content = stream_output(response)
                self.history.append(cur_content)
            else:
                cur_content = response.choices[0].message.content
                print(cur_content)
                self.history.append(cur_content)
            message.append({"refusal":None, "annotations": None, "audio": None, "function_call": None, "tool_calls": None, "role": "assistant", "content": cur_content})


    def reasonal_chat_once(self, args, config):
        user_input = sys.stdin.read()
        if args.add:
            print(user_input)
            print('')
        pre_input = " ".join(args.non_option_args)
        user_input = pre_input + "\n" + user_input

        self.history.append(user_input)

        message = self.message
        message.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=config.models[config.model_choice]['r1'],
            messages=message,
            stream=args.stream
        )
        
        if args.stream:
            content = stream_output_reason(response, self.vendor_name + '-' + config.models[config.model_choice]['r1'])
            self.history.append(content)
        else:
            print('[' + self.vendor_name + '-' + config.models[config.model_choice]['r1'] + ' 🤖🧐 ]:')
            print(response.choices[0].message.reasoning_content)
            print('')
            print('[' + self.vendor_name + '-' + config.models[config.model_choice]['r1'] + ' 🤖 ]:')
            print(response.choices[0].message.content)
            self.history.append(response.choices[0].message.content)


    def reasonal_chat(self, args, config):
        pre_input = " ".join(args.non_option_args)
        message = self.message
        while True:
            print('🥰:')
            user_input = multi_line_input()
            if user_input == 'exit' or user_input == 'quit' or user_input == 'q':
                break

            if user_input.startswith('!'):
                command = user_input[1:]
                pre_input = ''
                try:
                    print('命令执行成功')
                    result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
                    pre_input = result.stdout + '\n' + result.stderr
                    print(pre_input)
                    message.append({"refusal":None, "annotations": None, "audio": None, "function_call": None, "tool_calls": None, "role": "assistant", "content": pre_input})
                except subprocess.CalledProcessError as e:
                    print('命令执行失败:', e)
                continue

            user_input = pre_input + '\n' + user_input
            self.history.append(user_input)

            message.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model=config.models[config.model_choice]['r1'],
                messages=message,
                stream=args.stream
            )

            print('')
            cur_content = ""

            if args.stream:
                cur_content = stream_output_reason(response, self.vendor_name + '-' + config.models[config.model_choice]['r1'])
                self.history.append(cur_content)
            else:
                print('[' + self.vendor_name + '-' + config.models[config.model_choice]['r1'] + ' 🤖🧐 ]:')
                print(response.choices[0].message.reasoning_content)
                print('')
                print('[' + self.vendor_name + '-' + config.models[config.model_choice]['r1'] + ' 🤖 ]:')
                cur_content = response.choices[0].message.content
                print(cur_content)
                self.history.append(cur_content)

            message.append({"refusal":None, "annotations": None, "audio": None, "function_call": None, "tool_calls": None, "role": "assistant", "content": cur_content})
