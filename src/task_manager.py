import os
import datetime

from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

# .envから環境変数を取得する
load_dotenv()

class TaskManager:
    __TODOIST_TOKEN = os.getenv('TODOIST_API_TOKEN')

    def __init__(self) -> None:
        """
        コンストラクタ
        """
        self.__api = TodoistAPI(TaskManager.__TODOIST_TOKEN)

    def get_today_task(self) -> list[Task]:
        """
        タスクを取得して期限が今日までのものを選抜する
        """
        # 現在の時刻を取得
        date_now = datetime.datetime.today()
        # プロジェクトIDを取得
        project_id = os.getenv('TODOIST_PROJECT_ID')
        # プロジェクトからタスクを取得
        tasks = self.__api.get_tasks(project_id=project_id)

        today_tasks = [] # 期限が今日のタスク
        for task in tasks:
            # FIXME: 日付の表現形式にバグがあることのみ覚えている
            due_date = datetime.datetime.strptime(task.due.datetime, '%Y-%m-%dT%H:%M:%SZ')
            due_date += datetime.timedelta(hours=9)

            if due_date.month == date_now.month\
                and due_date.day == date_now.day:
                task.due.datetime = due_date.strftime('%Y-%m-%d %H:%M:%S')
                today_tasks.append(task)

        return(today_tasks)

if __name__ == '__main__':
    manager = TaskManager()
    tasks = manager.get_today_task()

    for task in tasks:
        print(task.content)
        print(task.due.datetime)