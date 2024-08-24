format:
	black . && isort . && autoflake .

run:
	podman-compose up

remove:
	podman-compose down
	podman volume prune -f
	podman rmi -a
	podman network prune -f
