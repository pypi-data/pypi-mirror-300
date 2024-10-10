from extras.scripts import Script
import os
import shutil
import uuid


class RobotTest(Script):

    def run(self, data, commit):
        robot_path = r'/tmp/robot' 
        if not os.path.exists(robot_path):
            os.makedirs(robot_path)
        project = uuid.uuid4().hex
        if not os.path.exists(os.path.join(robot_path, project)):
            os.makedirs(os.path.join(robot_path, project))
        project_path = os.path.join(robot_path, project)
        with open(os.path.join(project_path, 'test.robot'), 'w') as f:
            f.write("Testando a criação")
        shutil.rmtree(project_path)
        return "Hello World"