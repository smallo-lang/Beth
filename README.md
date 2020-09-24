# Beth

Beth is an assembler + VM bundle for SmallO assembly. She can run your SmallO
assembly code with no extra steps and dependencies. The only thing you need is
Python3.



## Architecture

### <a name="loader"></a> Loader

The loader is supposed to 

1. Read input file(s);
2. Clean the code of redundant data (e.g. empty lines, comments, whitespace);
3. Pass it onto the [preprocessor](preprocessor).


### <a name="preprocessor"></a> Preprocessor

The preprocessor is supposed to

1. Receive code from the [loader](loader);
2. Check for label duplicates;
3. Compose the label map;
4. Compile the instructions list.


> Preprocessor must also check for duplicated labels and raise syntax error in
> case duplicates have been detected.

Learn more about internals like label map below.


### Virtual Machine Internals

> Beth utilises its own VM written in Python. It is slower than [Rick] and is
> also different in terms of architecture.

[Rick]: https://github.com/smallo-lang/Rick

#### State

The VM contains the following internal structures:

1. Label map;
2. Instructions list;
3. Variable map;
4. Return locations stack;
5. Opcodes map.

> Opcode methods are to be surrounded with `_underscores_` which will separate
> them visually from the rest of internal VM methods.

#### Methods

1. Fetch;
2. Decode;
3. Execute;
4. Tick - utilizes all above methods.

> In this regard, SmallO VM is very traditional and does not seek to deviate
> from the long-lived standard of processing.



## License

This project is licensed under the **Mozilla Public License Version 2.0** --
see the [LICENSE](LICENSE) file for details.

Please note that this project is distributred as is,
**with absolutely no warranty of any kind** to those who are going to deploy
and/or use it. None of the authors and contributors are responsible (liable)
for **any damage**, including but not limited to, loss of sensitive data and
machine malfunction.
