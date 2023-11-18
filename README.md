## Logger - CPP microservices
![Email-Service](https://socialify.git.ci/suva007/logger/image?description=1&font=Bitter&issues=1&language=1&name=1&owner=1&pattern=Formal%20Invitation&theme=Dark)

## Features
<details>

<summary>1. Help</summary>

```ruby
  usage: log.py [-h] [-component COMPONENT [COMPONENT ...]] [-cleanUp]

  Logger for Microservices based Backend Components Components.

  optional arguments:
    -h, --help            show this help message and exit
    -component COMPONENT [COMPONENT ...]
                          Specify one or more Backend components ['WebSockets', 'Subscriber', 'Diff_checker']
    -cleanUp              Remove the changes in all the CPP filess [Requires '-component' argument].
```

</details>

<details>

<summary>2. Enabling logs</summary>

### Process CPP files inside mentioned component directory
```ruby
$ ./log.py -component Diff_Checker Subscriber
Components to process:  {'Diff_Checker', 'Subscriber'}

Processing Component:  Diff_Checker

Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>

Processing Component:  Subscriber

Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
.
.
.
```

</details>
<details>

<summary>3. Disable logs</summary>

### Remove the added code responsible for logging from CPP files
```ruby
$ ./log.py -component Diff_Checker Subscriber -cleanUp
==============================================================
Clean Up in Progress!!!!!
==============================================================
Components to process:  {'Diff_Checker', 'Subscriber'}

Processing Component:  Diff_Checker

Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>

Processing Component:  Subscriber

Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
Processing CPP file: <absolute path to CPP file on the path>
.
.
.
```

</details>

<details>
<summary>4. Build the code</summary>
  
### Build C++ code after enabling and disabling logging to reflect changes.

```ruby
  g++ -o output_filename file1.cpp file2.cpp file3.cpp
```
</details>

## Algorithm
- Step 1: Update the code-base with absolute path for each component in the MAP at the top of python file.
- Step 2: Update the binaries with absolute path for each component in the MAP at the top of python file.
- Step 3: The information hard-coded above will be used to figure out the list of files responsible for each component and for building an abstract syntax tree for parsing C++ file.
- Step 4: We write a boilerplate code at the top of each CPP file for a particular component, which is responsible in printing logs for each function inside CPP file. 
- Step 5: We traverse down the Abstract syntax tree of each CPP file and place a LOG_FUNCTION(); command at the start of each function in CPP file.
- Step 6: C++ Parsing is a hard problem in itself, therefore our parser might add some extra LOG_FUNCTION(); but the accurancy for our parser is around 99.1%.
- Step 7: After placing the boilerplate code and LOG_FUNCTION(); at the start of each function, we are ready to build the code and log information about functions in each of the mentioned component.

## What are we <a href="https://github.com/suva007/Logger/blob/main/log.txt" title="Link to notebook" style="background-color:#FFFFFF;color:#000000;text-decoration:none"> logging </a>?
1. [Current Time] Entering/Exiting function: <Name of the function> in File: <Absolute path of CPP file> at Line: <Line number> | (Number of times this function is executed as part of some operation run)

2. [Current Time] Elapsed Time: (In seconds)

* Current Time: Local time with microseconds precision.
* Entering / Exiting Function: Provides information about the set of functions executed as part of user operations.
* Name of the function: Coming up from LOG_FUNCTION(); added at the start of each function in a CPP file.
* Absolute path of CPP file: Responsible for business logic for a particular compenent.
* Number of times this function is executed: Helpful in resolving the performance and figuring out, if same function is executed multiple times as part of single user operation.
* Elapsed Time: Time taken by each function for its execution.

