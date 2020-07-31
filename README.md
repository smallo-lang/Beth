# SmallO Interpreter

Simple syntax. Infinite opportunities.



## Type System

SmallO supports two simple types: `number` and `string` where `number` also
serves as `boolean`. The `string` type can be interpreted as `boolean` using its
length (empty `string` gives `false`, non-empty one gives `true`).



## General Operational Principles

SmallO supports two syntactic structures: *instruction* and *label*. I believe
these are self-explanatory. Instructions differ in terms of their operand number
such that there are methods that don't need any operands (e.g. `end`) while some
take up to 3 operands (normally two values and a variable to store the result).



## Operations

### Instruction Set

```asm
@ assignment
put val var

@ binary numerical operations
    @ arithmetic
add num num var
sub num num var
mul num num var
div num num var
mod num num var
    @ comparisons
gth num num var @ greater than
lth num num var @ less than
geq num num var @ greater than or equal to
leq num num var @ less than or equal to

@ binary general operations
eq val val var  @ equality check (type-crytical)
neq val val var @ inequality check (type-crytical)

@ I/O operations
inn var     @ input number (type-crytical)
ins var     @ input string (type-crytical)
out val     @ output value (type-blind)

@ string operations
con val val var @ concatenate 2 values as strings (type-blind)
stn val var @ string-to-number conversion (type-blind)

@ boolean operations
not val var
and val val var
or val val var

@ labels
jump_location:

@ control flow
jump *      @ unconditional jump
jmpt val *  @ jump if val is true
jmpf val *  @ jump if val is false
back        @ return to previous branch point
err val num @ exit program with error message (type-blind) and exit code num
end         @ exit program
```


### Symbol Map

| Symbol | Meaning             |
|:------:|:--------------------|
| #      | number literal      |
| $      | string literal      |
| var    | variable identifier |
| num    | number (# or var)   |
| val    | value               |
| *      | label identifier    |
| @      | comment             |

> The `val` represents constant literal (`#` or `$`) or variable identifier
> (`var`). It's used in commands that support auto-conversion.



## Virtual Machine Architecture

### <a name="loader"></a> Loader

The loader is supposed to 

1. Read input file(s);
2. Clean the code of redundant data (e.g. empty lines);
3. Pass it onto the [preprocessor](preprocessor).

> Loader must also check for duplicated labels and raise syntax error in case
> duplicates have been detected.


### <a name="preprocessor"></a> Preprocessor

The preprocessor is supposed to

1. Receive code from the [loader](loader);
2. Check for label duplicates;
3. Compose the label map;
4. Compile the instructions list.

> Learn more about internals like label map below.


### Internals

#### State

The VM contains the following internal structures:

1. Label map;
2. Instructions list;
3. Variable map;
4. Return locations stack;
5. Instructions map.

> Instructions methods are to be named with an \_underscore prefix.

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
