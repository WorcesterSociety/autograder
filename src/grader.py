import docker

client = docker.from_env()
container = client.containers.run("python:latest", "python -c 'print(\"Hello, World.\")'", detach = True)

for line in container.logs(stream = True):
    print(line)

container.stop()
