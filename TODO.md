- [x] Review memory optimisations

## Code Review Findings & Recommendations

### 🚨 Critical Issues
- **Syntax Error in Python < 3.12 (`ollama_setup.py`):** Fix the double-quote string formatting inside the `f-string` on line 25 (`logger.debug(f"Ollama version : {resp.json()['version']}")`).

### 🛠️ Architecture & Best Practices
- **Logging Initialization Order (`main.py`):** Ensure `init_logging()` is executed before any logging calls or starting the asyncio loop.
- **Deprecated Asyncio Execution (`main.py`):** Replace `asyncio.get_event_loop().run_until_complete(async_main())` with the modern `asyncio.run(async_main())`.
- **Argparse Structure (`main.py`):** Move global arguments like `--debug` before the `add_subparsers(...)` definition.
- **Use of Built-in `exit()` (`main.py`):** Import `sys` and replace `exit()` with `sys.exit()` for safe program termination.

### 🧹 Code Quality & Typing
- **Missing Type Hint (`documents.py`):** Add the missing `int` type hint to the `port` parameter in the `load_from_directory` function signature.
- **Subparser Command Routing (`main.py`):** Consider using `.set_defaults(func=...)` for commands instead of the growing `if args.command == ...` block.