format:
	black . && isort . && autoflake .

run:
	podman-compose up

remove:
	podman-compose down
	podman volume prune -f
	podman image --all --force
	podman network prune -f
