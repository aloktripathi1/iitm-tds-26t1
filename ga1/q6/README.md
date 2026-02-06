# IoT Sensor Data Processing

Monitor temperature sensors to detect anomalies

## Task

This Python project has a bug in `utils.py`. Your job is to:

1. Extract the ZIP file
2. Run `python main.py` to see the current (incorrect) output
3. Debug and fix the bug in `utils.py`
4. Run `python main.py` again to get the correct output
5. Submit the OUTPUT line from your fixed code

## Tips

- Use an AI coding agent like **GitHub Copilot** to help identify the bug
- The bug is subtle but will produce incorrect results
- Read the code carefully and compare expected vs actual behavior
- The correct code should process all sensor readings correctly

## Running the Code

```bash
# Extract the ZIP file
unzip python_debug.zip
cd python_debug

# Run the script
python main.py

# Or use uv (faster)
uv run main.py
```

The output will show statistics about sensor readings above the threshold.
The final line will be: `OUTPUT: count,total,average`

Submit this OUTPUT line as your answer.

## Debugging with AI

Try asking your AI coding agent:
- "Is there a bug in this code?"
- "Why might this function give incorrect results?"
- "Compare this implementation with the expected behavior"
- "What could cause an off-by-one error here?"

Good luck! 🐛🔍
