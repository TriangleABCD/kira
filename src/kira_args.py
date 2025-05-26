import argparse


# models_const = {
#     'api_chose': {
#         'r1': 'model_r1',
#         'v3': 'model_v3'
#     }
# }
# api_chose = 'api_chose'

class Args:
    def __init__(self, model=None, chat=False, add=False, stream=False, init=False, non_option_args=None):
        self.model = model
        self.chat = chat
        self.add = add
        self.stream = stream
        self.init = init
        self.non_option_args = non_option_args if non_option_args is not None else []


class ArgumentParserWrapper:
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)
        self.add_arguments()
    
    def add_arguments(self):
        self.parser.add_argument('-r', '--r1', action='store_const',
                                 const=models_const[api_chose]['r1'],
                                 default=models_const[api_chose]['v3'],
                                 dest='model', help="使用 deepseek-reasoner 模型")
        self.parser.add_argument('-c', '--chat', action='store_true', dest='chat', help="对话形式")
        self.parser.add_argument('-a', '--add', action='store_true', dest='add', help="输出原文")
        self.parser.add_argument('-s', '--stream', action='store_true', dest='stream', help="流式输出")
        self.parser.add_argument('--init', action='store_true', dest='init', help="初始化")
        self.parser.add_argument('non_option_args', nargs='*')

    def parse_args(self):
        parsed_args = self.parser.parse_args()
        args = Args(
            model=parsed_args.model,
            chat=parsed_args.chat,
            add=parsed_args.add,
            stream=parsed_args.stream,
            init=parsed_args.init,
            non_option_args=parsed_args.non_option_args
        )
        return args


def get_args():
    arg_parser = ArgumentParserWrapper(
        description='kira(Knowledge Interactive Response Agent), 命令行大模型 Agent 工具'
    )
    args = arg_parser.parse_args()
    return args

