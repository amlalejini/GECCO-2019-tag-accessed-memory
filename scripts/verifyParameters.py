'''
Script: verifyParameters.py

I use this script to test whether or not I've correctly set the parameters for a
given set of runs.
'''

import argparse, os, copy, errno, csv

general_parameters = ["set PROG_POP_SIZE 500"]

expected_mut_parameters = {
    "MUT_5": ["set PROG_MUT__PER_BIT_FLIP 0.5", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.5"],
    "MUT_1": ["set PROG_MUT__PER_BIT_FLIP 0.1", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.1"],
    "MUT_075": ["set PROG_MUT__PER_BIT_FLIP 0.075", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.075"],
    "MUT_05": ["set PROG_MUT__PER_BIT_FLIP 0.05", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.05"],
    "MUT_025": ["set PROG_MUT__PER_BIT_FLIP 0.025", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.025"],
    "MUT_01": ["set PROG_MUT__PER_BIT_FLIP 0.01", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.01"],
    "MUT_0075": ["set PROG_MUT__PER_BIT_FLIP 0.0075", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.0075"],
    "MUT_005": ["set PROG_MUT__PER_BIT_FLIP 0.005", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.005"],
    "MUT_0025": ["set PROG_MUT__PER_BIT_FLIP 0.0025", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.0025"],
    "MUT_001": ["set PROG_MUT__PER_BIT_FLIP 0.001", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.001"],
    "MUT_0001": ["set PROG_MUT__PER_BIT_FLIP 0.0001", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.0001"],
    "MUT_00001": ["set PROG_MUT__PER_BIT_FLIP 0.00001", "set PROG_MUT__PER_NUMERIC_ARG_SUB 0.00001"],
}

expected_arg_parameters = {
    "ARGS_TAG_BF": ["set PROGRAM_ARGUMENT_MODE 0", "Adding default TAG-BASED ARGUMENT instructions WITHOUT TYPE SEARCHING."],
    "ARGS_NUM": ["set PROGRAM_ARGUMENT_MODE 1", "Adding default NUMERIC ARGUMENT instructions."]
}

expected_problem_parameters = {
    "PROBLEM_for-loop-index": ["set GENERATIONS 300", "set PROBLEM for-loop-index", "set PROG_EVAL_TIME 256", "set MAX_PROG_SIZE 128", "Loaded TRAINING set size = 100"],
    "PROBLEM_grade": ["set GENERATIONS 300", "set PROBLEM grade", "set PROG_EVAL_TIME 128", "set MAX_PROG_SIZE 128", "Loaded TRAINING set size = 200"],
    "PROBLEM_median": ["set GENERATIONS 300", "set PROBLEM median", "set PROG_EVAL_TIME 64", "set MAX_PROG_SIZE 64", "Loaded TRAINING set size = 100"],
    "PROBLEM_number-io": ["set GENERATIONS 100", "set PROBLEM number-io", "set PROG_EVAL_TIME 32", "set MAX_PROG_SIZE 32", "Loaded TRAINING set size = 25"],
    "PROBLEM_smallest": ["set GENERATIONS 300", "set PROBLEM smallest", "set PROG_EVAL_TIME 64", "set MAX_PROG_SIZE 64", "Loaded TRAINING set size = 100"]
}

def main():
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str, help="Target experiment directory.")

    args = parser.parse_args()

    data_directory = args.data_directory

    # Get a list of all runs
    runs = [d for d in os.listdir(data_directory) if "__" in d]
    runs.sort()

    compliant_runs = 0
    noncompliant_runs = 0
    total_runs = len(runs)
    for run in runs:
        run_dir = os.path.join(data_directory, run)
        run_id = run.split("__")[-1]
        run_name = "__".join(run.split("__")[:-1])
        run_log = None

        with open(os.path.join(run_dir, "run.log"), "r") as fp:
            run_log = fp.read().strip()

        noncompliant = []
        # Check general_parameters
        for param in general_parameters:
            if param not in run_log:
                noncompliant.append(param)

        # Check expected_mut_parameters
        for treatment in expected_mut_parameters:
            if treatment in run_name:
                for param in expected_mut_parameters[treatment]:
                    if param not in run_log:
                        noncompliant.append(param)

        # Check expected_arg_parameters
        for treatment in expected_arg_parameters:
            if treatment in run_name:
                for param in expected_arg_parameters[treatment]:
                    if param not in run_log:
                        noncompliant.append(param)

        # Check expected_problem_parameters
        for treatment in expected_problem_parameters:
            if treatment in run_name:
                for param in expected_problem_parameters[treatment]:
                    if param not in run_log:
                        noncompliant.append(param)

        if len(noncompliant):
            print(f"{run_name}_{run_id} is not compliant with: {noncompliant}")
            noncompliant_runs += 1
        else:
            compliant_runs += 1
    print(f"# Compliant runs = {compliant_runs}; # Non-compliant runs = {noncompliant_runs}; Total runs: {total_runs}")


if __name__ == "__main__":
    main()