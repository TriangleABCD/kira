import os
import datetime

def detect_kira():
    current_path = os.getcwd()
    dir_path = os.path.join(current_path, '.kira')
    return os.path.isdir(dir_path)


class Project:
    def __init__(self):
        self.project_path = ''
        self.history_path = ''
        self.history = ''

    def new_project(self):
        self.project_path = os.getcwd()
        dir_path = os.path.join(self.project_path, '.kira')
        if detect_kira():
            os.rmdir(dir_path)
        os.mkdir(dir_path)
        self.history_path = os.path.join(dir_path, 'summary.md')

        with open(self.history_path, 'w') as f:
            f.write('project ' + os.path.basename(self.project_path) + ' chat history summary')

    def set_project(self):
        self.project_path = os.getcwd()
        dir_path = os.path.join(self.project_path, '.kira')
        self.history_path = os.path.join(dir_path, 'summary.md')

        with open(self.history_path, 'r', encoding ='utf-8') as f:
            lines = f.readlines()
        self.history = "".join(lines)

    def write_history(self, history):
        current_time = datetime.datetime.now()
        dir_path = os.path.join(self.project_path, '.kira')
        file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".md"
        file_path = os.path.join(dir_path, file_name)

        with open(file_path, 'w') as f:
            f.write(history)

    def write_history_summary(self, summary):
        dir_path = os.path.join(self.project_path, '.kira')
        file_path = os.path.join(dir_path, "summary.md")

        with open(file_path, 'a', encoding='utf-8') as f:
            current_time = datetime.datetime.now()
            time = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".md"
            f.write('\n\n' + time + '\n' + summary)
