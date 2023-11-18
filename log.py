#!/usr/bin/env python3

import argparse
import os
import subprocess
import time

# ===================================================================================================================================================================================
# component Dictionary - Required for fetching out the directories for a particular component
# component Binaries   - Required for fetching function names in a CPP file for parsing CPP file.
# ===================================================================================================================================================================================
componentDict = {}
componentBin = {}
componentDict['<component name>'] = '<Path to Backend code for specified component>'
componentBin['<component name>'] = '<Path to so file for mentioned component>' 

componentDict['<component name>'] = '<Path to Backend code for specified component>'
componentBin['<component name>'] = '<Path to so file for mentioned component>'

componentDict['<component name>'] = '<Path to Backend code for specified component>'
componentBin['<component name>'] = '<Path to so file for mentioned component>'

componentDict['<component name>'] = ['<Path to Backend code for specified component>', '<Path to Backend code for specified component>']
componentBin['<component name>'] = '<path to so file>'

# ===================================================================================================================================================================================
# includeLogger - This is #include "Log.hpp" (To be placed at the top of each CPP file)
# ===================================================================================================================================================================================
includeLogger = '''// ====================================== Logger ======================================
#include <iostream>
#include <fstream>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <sstream>
#include <vector>
#include <chrono>
#include <unordered_map>

class Logger {
public:
    static void Log(const std::string& msg) {
        std::ostringstream oss{};
        std::unordered_map <std::string, long long> functionCalls = {};
        functionCalls[msg]++;
        readFromFile(functionCalls, msg); // Read from log file and popoulate unordered_map
        if(msg.find("Elapsed time : ") != std::string::npos) {
            oss << "[" << GetCurrentTime() << "] " << msg << std::endl;
        } else {
            oss << "[" << GetCurrentTime() << "] " << msg <<" | ("<< functionCalls[msg] << ")" << std::endl;
        }
        WriteToFile(oss.str()); // Write to file
    }

private:
    static std::string GetCurrentTime() {
        // Get current time from the clock, using microseconds resolution
        const boost::posix_time::ptime now = 
            boost::posix_time::microsec_clock::local_time();

        // Get the time offset in current day
        const boost::posix_time::time_duration td = now.time_of_day();
        boost::gregorian::date dateObj = now.date();
        std::string date = boost::gregorian::to_iso_string(dateObj);
        date = date.substr(0, 4) + "-" + date.substr(4,2) + "-" + date.substr(6, 2) + " ";
        
         int milliseconds = td.total_milliseconds() % 1000;
        int microseconds = td.total_microseconds() % 1000;

        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << td.hours() << ":"
            << std::setw(2) << td.minutes() << ":"
            << std::setw(2) << td.seconds() << "."
            << std::setw(3) << milliseconds << "."
            << std::setw(3) << microseconds;

        std::string formattedTime = oss.str();

        std::string currentTime =  date + formattedTime;

        return  currentTime;
    }

    static void WriteToFile(const std::string& log) {
        std::ofstream file("log.txt", std::ios::app); // Open log file in append mode
        if (file.is_open()) {
            file << log;
            file.close();
        }
    }

    static void readFromFile(std::unordered_map<std::string, long long> &functionCalls, const std::string& msg) {
        std::string logFilePath = "log.txt";  // Specify the path to your log file
        try {
            std::ifstream logFile(logFilePath); 

            if (logFile.is_open()) {
                std::string line;
                while (std::getline(logFile, line)) {
                    // Fetch the msg after time in log, to count the number of call sights.
                    auto it = std::find(line.begin(), line.end(), ' ');
                    int index = std::distance(line.begin(), it), spaceCount = 0;
                    while (it != line.end()) {
                        spaceCount++;

                        if (spaceCount == 2) {
                            index = std::distance(line.begin(), it);
                            break;
                        }

                        it = std::find(std::next(it), line.end(), ' ');
                    }
                    std::string lineSubstr = line.substr(index+1, line.size());
                    if(lineSubstr.find(msg) != std::string::npos) {
                        functionCalls[msg]++;
                    }
                }
                logFile.close();
            }
        } catch(...) { return; }
    }
};

class FunctionLogger {
public:
    FunctionLogger(const std::string& functionName, const std::string& fileName, const long long& lineNumber)
        : functionName(functionName), fileName(fileName), lineNumber(lineNumber) {
        start = std::chrono::high_resolution_clock::now();
        Logger::Log("Entering function: " + functionName + " in File: " + fileName + " at Line: " + std::to_string(lineNumber));
    }

    ~FunctionLogger() {
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() / 1000000.0;
        // std::cout << "Elapsed time: " << duration << " microseconds" << std::endl;
        Logger::Log("Exiting function : " + functionName + " in File: " + fileName + " at Line: " + std::to_string(lineNumber));
        Logger::Log("Elapsed time : " + std::to_string(duration) + " seconds.");
    }

private:
    std::string functionName;
    std::string fileName;
    long long lineNumber;
    std::chrono::time_point<std::chrono::high_resolution_clock> start;
};

#define LOG_FUNCTION() FunctionLogger functionLogger(__FUNCTION__, std::string(__builtin_FILE()), __builtin_LINE()-1)
// ====================================== Logger ======================================'''

# ===================================================================================================================================================================================
# log function call - To be placed as the first line of all the functions in a CPP file
# ===================================================================================================================================================================================
log_function = "LOG_FUNCTION();"

# ===================================================================================================================================================================================
# write log_function as the first line for each CPP function
# ===================================================================================================================================================================================
def writeLogAtTheTop(component, fileName):
    # Path to the CPP file
    import re
    import subprocess

    command = f"nm -D --defined-only {componentBin[component]} | awk '$2 ~ /[tT]/ {{print $3}}' | c++filt"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # Decode the output from bytes to string and split it into a list by new lines
    output_list = output.decode('utf-8').split('\n')

    # List of function names
    function_names = [item.split('(')[0].split('::')[-1] for item in output_list]

    # Open the file
    with open(fileName, 'r') as file:
        content = file.readlines()

    # Check if log_function already exist
    for line in content:
        if 'LOG_FUNCTION();' in line:
            return

    new_content = []
    inside_function = False
    open_arg = False
    close_arg = False
    for line in content:
        # Check if the line contains a function name
        function_found = any(func in line for func in function_names)
        if function_found:
            inside_function = True
        if inside_function and '(' in line:
            open_arg = True
        if inside_function and open_arg and ')' in line:
            close_arg = True

        if ';' in line or 'if' in line or 'for' in line or 'while' in line or 'do' in line or 'else' in line or 'else if' in line or 'switch' in line:
            # TODO: Make sure all the keywords are taken care
            inside_function = False;
            open_arg = False
            close_arg = False
            new_content.append(line)

        elif close_arg and '{' in line:
            new_content.append(line.replace('{', '{LOG_FUNCTION();'))
            inside_function = False
            open_arg = False
            close_arg = False
        else:
            new_content.append(line)

    # Get the current file permissions
    file_permissions = os.stat(fileName).st_mode

    # Set the write permission
    new_permissions = file_permissions | 0o200

    # Change the file permissions to make it writable
    os.chmod(fileName, new_permissions)

    # Write the modified content back to the file
    with open(fileName, 'w') as file:
        file.writelines(new_content)

# ===================================================================================================================================================================================
# Check for invalid component Names
# ===================================================================================================================================================================================
def checkComponentList(components):
    for comp in components:
        if comp not in componentDict:
            raise ValueError("Invalid Component Name! Allowed list of components: ", componentDict.keys())

# ===================================================================================================================================================================================
# write includeLogger at the top of a given filename
# ===================================================================================================================================================================================
def writeAtTheTop(fileName):
    try:
        bookmark = "// ====================================== Logger ======================================" 
        # Get the current file permissions
        file_permissions = os.stat(fileName).st_mode

        # Set the write permission
        new_permissions = file_permissions | 0o200

        # Change the file permissions to make it writable
        os.chmod(fileName, new_permissions)

        # Read the existing content of the CPP file
        with open(fileName, "r") as file:
            content = file.read()

        if bookmark not in content:
            # Write the long string at the top and append the existing content
            with open(fileName, "w") as file:
                file.write(includeLogger.strip() + "\n\n" + content)
    except Exception as ex:
        raise ValueError("Warning! Exception caught inside writeAtTheTop. Mostly, the file is now corrupted!!\n", fileName, ex)

# ===================================================================================================================================================================================
# run_command will help in running sbmake for all the supplied components
# ===================================================================================================================================================================================
def run_command(command):
    # Run the command and capture the output
    print(command, "in progress!!!")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Print the output line by line
    for line in iter(process.stdout.readline, b''):
        print(line.decode().rstrip())

    # Wait for the process to finish
    process.wait()

# ===================================================================================================================================================================================
# remove includeLogger from the top of a given filename
# ===================================================================================================================================================================================
def removeFromTheTop(fileName):
    try:
        bookmark = "// ====================================== Logger ======================================"
        # Read the existing content of the CPP file
        with open(fileName, "r") as file:
            lines = file.readlines()

        # Find the start and end line numbers of the added code
        start_line = None
        end_line = None
        for i, line in enumerate(lines):
            if bookmark in line:
                if start_line is None:
                    start_line = i
                else:
                    end_line = i
                    break

        # Remove the lines containing the added code
        if start_line is not None and end_line is not None:
            del lines[start_line : end_line + 2]

        #Get the current file permissions
        file_permissions = os.stat(fileName).st_mode

        # Set the write permission
        new_permissions = file_permissions | 0o200

        # Change the file permissions to make it writable
        os.chmod(fileName, new_permissions)

        # Write the modified content back to the CPP file
        with open(fileName, "w") as file:
            file.writelines(lines)
    except Exception as ex:
        raise ValueError("Warning! Exception caught inside removeFromTop. Mostly, the file is now corrupted!!\n", fileName, ex)

# ===================================================================================================================================================================================
# remove LOG_FUNCTION from the top of each function in a given fileName
# ===================================================================================================================================================================================
def removeLogFromTheTop(fileName):
    try:
        bookmark = "LOG_FUNCTION();"
        # Read the existing content of the CPP file
        with open(fileName, "r") as file:
            lines = file.readlines()

        # Create a new list that doesn't include the line to remove
        new_content = [line.replace(bookmark, '') for line in lines]

        # Get the current file permissions
        file_permissions = os.stat(fileName).st_mode

        # Set the write permission
        new_permissions = file_permissions | 0o200

        # Change the file permissions to make it writable
        os.chmod(fileName, new_permissions)

        # Write the new content back to the file
        with open(fileName, 'w') as file:
            file.writelines(new_content)
    except Exception as ex:
        raise ValueError("Warning! Exception caught inside removeFromTop. Mostly, the file is now corrupted!!\n", fileName, ex)

# ===================================================================================================================================================================================
# Find CPP files in a directory and it's sub-directories
# ===================================================================================================================================================================================
def find_cpp_files(component, directory, cleanUp = False):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cpp"):
                fileName = os.path.join(root, file)
                print("Processing CPP file:", fileName)
                if cleanUp:
                    removeFromTheTop(fileName)
                    removeLogFromTheTop(fileName)
                else:
                    writeLogAtTheTop(component, fileName)
                    writeAtTheTop(fileName)

# ===================================================================================================================================================================================
# Main logic: Populate the directories with code base
# ===================================================================================================================================================================================
def loggerManager(components, cleanUp = False):
    if cleanUp:
        print("==============================================================")
        print("Clean Up in Progress!!!!!")
        print("==============================================================")

    print("Components to process: ", components)
    for comp in components:
        print("\nProcessing Component: ", comp)
        print()
        directory = componentDict[comp]
        if isinstance(directory, list):
            for direct in directory:
                # Make Changes to CPP files
                find_cpp_files(comp, direct, cleanUp)
        else:
            # Make Changes to CPP files
            find_cpp_files(comp, directory, cleanUp)
# ===================================================================================================================================================================================
# Check if user is at SB root or not
# ===================================================================================================================================================================================
def checkSandboxRoot():
    required_directories = ["home", "user", "config"]
    found_directories = []

    for dir_name in required_directories:
        dir_path = os.path.join(os.getcwd(), dir_name)
        if os.path.isdir(dir_path):
            found_directories.append(dir_name)

    if len(found_directories) != len(required_directories):
        raise ValueError("Invalid Path! Please go back to Sandbox root path in order to proceed.")

# ===================================================================================================================================================================================
# Logic for Argument validation
# ===================================================================================================================================================================================

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Logger for Microservices based Backend Components.")

# Add the component argument with nargs='+' to accept multiple values
helpMessage = f"Specify one or more Backend Components {list(componentDict.keys())}"
parser.add_argument('-component', nargs='+', help=helpMessage)

# Cleanup - Helps in cleaning up the CPP files in list of components.
parser.add_argument("-cleanUp", action="store_true", help="Remove the changes in all the CPP filess [Requires '-component' argument].")

# Parse the command-line arguments
args = parser.parse_args()

# ===================================================================================================================================================================================
# Check if correct arguments are provided
# ===================================================================================================================================================================================
if args.component:
    # 1. Use Only Unique Elements
    args.component = set(args.component)
    
    # 2. Check for Invalid Supplied Components
    checkComponentList(args.component)

    # 3. Check for Sandbox root path
    checkSandboxRoot()

    # 4. Main Logic: Populate the CPP Files in all the subdirectories with codeBase and Log Function call
    loggerManager(args.component, args.cleanUp)
else:
    # Print help message if no arguments are provided
    parser.print_help()
