import os

from reflex import constants
from reflex.reflex import _run


def main():
    # 环境：dev / prod（默认 prod）
    env_str = os.getenv("RX_ENV", "prod").lower()
    env = constants.Env.DEV if env_str == constants.Env.DEV.value else constants.Env.PROD

    # 前后端运行开关（与 CLI 语义一致）
    frontend_only = os.getenv("REFLEX_FRONTEND_ONLY", "").lower() in ("1", "true", "yes")
    backend_only = os.getenv("REFLEX_BACKEND_ONLY", "").lower() in ("1", "true", "yes")

    # 端口与主机
    frontend_port = os.getenv("REFLEX_FRONTEND_PORT")
    backend_port = os.getenv("REFLEX_BACKEND_PORT")
    backend_host = os.getenv("REFLEX_BACKEND_HOST")

    frontend_port = int(frontend_port) if frontend_port else None
    backend_port = int(backend_port) if backend_port else None

    # 单端口模式（仅在 prod 可用）
    single_port = os.getenv("REFLEX_SINGLE_PORT", "").lower() in ("1", "true", "yes")

    _run(
        env=env,
        frontend=not backend_only,
        backend=not frontend_only,
        frontend_port=frontend_port,
        backend_port=backend_port,
        backend_host=backend_host,
        single_port=single_port,
    )


if __name__ == "__main__":
    main()
