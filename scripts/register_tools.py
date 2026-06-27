from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

print("Connected Successfully")

print("Current User:")

print(w.current_user.me())