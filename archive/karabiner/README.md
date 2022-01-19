### Usage

- `python main.py YOUR_CSV_FILE --name YOUR_NAME`
- Example: `python main.py remap_keys.csv remap_system.csv --name remap`
- Open Karabiner-Elements, "Complex modifications" tab
- Click "Add rule" button and "Enable" on the rule with YOUR_NAME

### Remapping Explanation

- a: Original key
- b: New key
- mod_a: Optional modifiers for original key, e.g., "cmd", "shift" etc
- mod_b: Optional modifiers for new key

```
a,b,mod_a,mod_b
cmd_right,shift,,
```

- The above maps right command key to left shift key without modifiers
- If b is not a valid key, it will be treated as a shell command, eg `open -a Safari`

```
a,b,mod_a,mod_b
h,tab,['cmd'],"['ctrl','shift']"
```

- The above remaps left command + h key to ctrl + shift + tab
- See [remap_0.csv](remap_0.csv) for more examples
- See `Key` in [main.py](main.py) for available keys
