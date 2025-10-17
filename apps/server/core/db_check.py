import importlib
import sys


def check_db_driver() -> None:
    """Check for an installed PostgreSQL DB driver and print a helpful message.

    This will prefer psycopg (psycopg3). If neither psycopg nor psycopg2 is
    installed, raise RuntimeError with actionable guidance. This helps deploy
    logs quickly show why DB imports fail.
    """
    candidates = ["psycopg", "psycopg2"]
    found = []
    for mod in candidates:
        try:
            importlib.import_module(mod)
            found.append(mod)
        except Exception:
            pass

    if found:
        # Prefer psycopg if present
        if "psycopg" in found:
            print("DB driver check: found psycopg (psycopg3) installed")
        else:
            print("DB driver check: found psycopg2 installed")
        return

    # Nothing found — raise a clear error to fail fast with guidance
    msg = (
        "No PostgreSQL DB driver found in the environment.\n"
        "Install psycopg (psycopg3) by adding `psycopg[binary]==3.2.2` to your requirements\n"
        "or, if you must use psycopg2, ensure the Python runtime matches the compiled wheel.\n"
        "On Render: add a top-level runtime.txt (e.g. python-3.12.5), add a root requirements.txt\n"
        "that points to your app requirements, clear build cache, and redeploy.\n"
    )
    # Print to stdout to make it obvious in deploy logs before raising
    print("DB driver check: none found — failing with guidance:\n", msg)
    raise RuntimeError(msg)
