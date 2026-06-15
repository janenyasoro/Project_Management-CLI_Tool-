import sys
from storage import Storage
from models import User, Project, Task

DATA_FILE = "data/pm_tool_data.json"

class ProjectManagerCLI:
    def __init__(self):
        self.storage = Storage(DATA_FILE)

    def run(self):
        print("\n=== Project Management Tool ===")
        print("Type 'help' for commands, 'exit' to quit.\n")
        while True:
            try:
                cmd = input("pm> ").strip()
                if not cmd:
                    continue
                
                # Command routing
                if cmd == "exit":
                    self._handle_exit()
                    break
                elif cmd == "help":
                    self._show_help()
                elif cmd.startswith("user create "):
                    self._user_create(cmd)
                elif cmd == "user list":
                    self._user_list()
                elif cmd.startswith("project add "):
                    self._project_add(cmd)
                elif cmd.startswith("project list "):
                    self._project_list(cmd)
                elif cmd.startswith("task add "):
                    self._task_add(cmd)
                elif cmd.startswith("task list "):
                    self._task_list(cmd)
                elif cmd.startswith("task complete "):
                    self._task_complete(cmd)
                elif cmd == "save":
                    self.storage.save()
                else:
                    print("Unknown command. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nExiting...")
                self.storage.save()
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")

    # ---------- Helper Methods ----------
    def _handle_exit(self):
        self.storage.save()
        print("Goodbye!")

    def _show_help(self):
        print("""
Available commands:
  user create <name>          Create a new user
  user list                   List all users
  project add <user_id> <name>   Add a project to a user
  project list <user_id>      List projects for a user
  task add <project_id> <title> [contributor1,contributor2,...]
                              Add a task to a project (contributors are user IDs)
  task list <project_id>      List all tasks for a project
  task complete <task_id>     Mark a task as complete
  save                        Save data to file manually
  help                        Show this help
  exit                        Save and exit
        """)

    # ---------- User Commands ----------
    def _user_create(self, cmd):
        parts = cmd.split(maxsplit=2)
        if len(parts) < 3:
            print("Usage: user create <name>")
            return
        name = parts[2]
        uid = self.storage.get_next_id("user")
        new_user = User(uid, name)
        self.storage.users.append(new_user)
        self.storage.save()
        print(f"User '{name}' created with ID {uid}.")

    def _user_list(self):
        if not self.storage.users:
            print("No users found.")
            return
        print("\n=== Users ===")
        for u in self.storage.users:
            print(f"ID: {u.id} | Name: {u.name}")

    # ---------- Project Commands ----------
    def _project_add(self, cmd):
        parts = cmd.split(maxsplit=3)
        if len(parts) < 4:
            print("Usage: project add <user_id> <project_name>")
            return
        try:
            user_id = int(parts[2])
            proj_name = parts[3]
        except ValueError:
            print("Error: user_id must be a number.")
            return

        user = self.storage.find_user_by_id(user_id)
        if not user:
            print(f"User ID {user_id} not found.")
            return

        pid = self.storage.get_next_id("project")
        new_proj = Project(pid, proj_name, user_id)
        self.storage.projects.append(new_proj)
        self.storage.save()
        print(f"Project '{proj_name}' added to user '{user.name}' (project ID {pid}).")

    def _project_list(self, cmd):
        parts = cmd.split()
        if len(parts) != 3:
            print("Usage: project list <user_id>")
            return
        try:
            user_id = int(parts[2])
        except ValueError:
            print("Error: user_id must be a number.")
            return

        user = self.storage.find_user_by_id(user_id)
        if not user:
            print(f"User ID {user_id} not found.")
            return

        user_projs = self.storage.get_projects_by_user(user_id)
        if not user_projs:
            print(f"No projects for user '{user.name}'.")
            return

        print(f"\n=== Projects for {user.name} (ID {user.id}) ===")
        for p in user_projs:
            print(f"Project ID: {p.id} | Name: {p.name}")

    # ---------- Task Commands ----------
    def _task_add(self, cmd):
        # Format: task add <project_id> <title> [contrib1,contrib2,...]
        parts = cmd.split(maxsplit=3)
        if len(parts) < 4:
            print("Usage: task add <project_id> <title> [contributor1,contributor2,...]")
            return
        
        try:
            project_id = int(parts[2])
            title = parts[3].split("[")[0].strip()
            # Check for contributors
            contributors = []
            if "[" in cmd and "]" in cmd:
                contrib_part = cmd.split("[")[1].split("]")[0]
                if contrib_part.strip():
                    contributors = [int(x.strip()) for x in contrib_part.split(",") if x.strip().isdigit()]
        except ValueError:
            print("Error: project_id must be a number.")
            return

        project = self.storage.find_project_by_id(project_id)
        if not project:
            print(f"Project ID {project_id} not found.")
            return

        # Validate contributors (must be existing users)
        invalid = [c for c in contributors if not self.storage.find_user_by_id(c)]
        if invalid:
            print(f"Invalid contributor IDs: {invalid}. Users must exist first.")
            return

        tid = self.storage.get_next_id("task")
        new_task = Task(tid, title, project_id, contributors, completed=False)
        self.storage.tasks.append(new_task)
        self.storage.save()
        print(f"Task '{title}' added to project '{project.name}' (task ID {tid}).")

    def _task_list(self, cmd):
        parts = cmd.split()
        if len(parts) != 3:
            print("Usage: task list <project_id>")
            return
        try:
            project_id = int(parts[2])
        except ValueError:
            print("Error: project_id must be a number.")
            return

        project = self.storage.find_project_by_id(project_id)
        if not project:
            print(f"Project ID {project_id} not found.")
            return

        tasks = self.storage.get_tasks_by_project(project_id)
        if not tasks:
            print(f"No tasks for project '{project.name}'.")
            return

        print(f"\n=== Tasks for Project: {project.name} (ID {project.id}) ===")
        for t in tasks:
            status = "✓ Complete" if t.completed else "✗ Incomplete"
            contrib_names = []
            for uid in t.contributors:
                u = self.storage.find_user_by_id(uid)
                contrib_names.append(u.name if u else f"ID {uid}")
            contrib_str = f" | Contributors: {', '.join(contrib_names)}" if contrib_names else ""
            print(f"  Task ID: {t.id} | {t.title} [{status}]{contrib_str}")

    def _task_complete(self, cmd):
        parts = cmd.split()
        if len(parts) != 3:
            print("Usage: task complete <task_id>")
            return
        try:
            task_id = int(parts[2])
        except ValueError:
            print("Error: task_id must be a number.")
            return

        task = self.storage.find_task_by_id(task_id)
        if not task:
            print(f"Task ID {task_id} not found.")
            return

        if task.completed:
            print(f"Task '{task.title}' is already completed.")
        else:
            task.mark_complete()
            self.storage.save()
            print(f"Task '{task.title}' marked as complete.")