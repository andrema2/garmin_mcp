"""
Helpers para executar chamadas bloqueantes do Garmin Connect em thread.

Motivação:
- A maioria das APIs do `garminconnect`/`requests` é bloqueante.
- Os tools do MCP rodam em ambiente async; bloquear o event loop degrada
  performance e pode travar múltiplas chamadas concorrentes.

Este módulo centraliza o padrão `anyio.to_thread.run_sync(...)`.
"""

from __future__ import annotations

from typing import Any

import anyio  # type: ignore


async def call_garmin(method_name: str, *args: Any, **kwargs: Any) -> Any:
    """
    Executa um método do cliente Garmin (bloqueante) em uma thread.

    Args:
        method_name: Nome do método em `garminconnect.Garmin`
        *args/**kwargs: Argumentos passados ao método

    Returns:
        O retorno do método do cliente Garmin
    """

    def _call() -> Any:
        # Import lazy para evitar custo de import e ciclos.
        from garmin_mcp.server import get_garmin_client

        client = get_garmin_client()
        method = getattr(client, method_name)
        return method(*args, **kwargs)

    return await anyio.to_thread.run_sync(_call)


