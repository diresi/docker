import sys
sys.argv = ["run.py"]
import tasks.tasks
reload(tasks.tasks)
tasks.tasks.app.worker_main()
