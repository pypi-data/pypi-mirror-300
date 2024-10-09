"""Generate the report folder from a config file and model data
"""

import argparse


def main():

    # Provide the option to render the quarto
    parser = argparse.ArgumentParser("report_generator")
    parser.add_argument(
        "-f",
        "--config-file",
        required=True,
        help="Specify the config file describing the report",
    )
    parser.add_argument(
        "-r",
        "--render",
        help="Render the auto-generated quarto report",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="Remove the build directory for this report",
        action="store_true",
    )
    args = parser.parse_args()

    # Import packages here to avoid delay on help menu
    import shutil
    import subprocess
    import copy
    from pathlib import Path
    from jinja2 import Environment, FileSystemLoader
    import yaml
    import pickle
    from pyhbr import common
    import pandas as pd
    from loguru import logger as log

    # Read the configuration file
    with open(args.config_file) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Failed to load config file: {exc}")
            exit(1)

    # Load the config file
    config = common.read_config_file(args.config_file)
    analysis_name = config["analysis_name"]
    save_dir = config["save_dir"]
    now = common.current_timestamp()

    # Set up the log file output for plot/describe script
    log_file = (
        Path(save_dir) / Path(analysis_name + f"_generate_report_{now}")
    ).with_suffix(".log")
    log_format = "{time} {level} {message}"
    log_id = log.add(log_file, format=log_format)

    # Load the data files
    data, raw_data, data_path = common.load_most_recent_data_files(
        analysis_name, save_dir
    )

    # relative to the current working directory
    build_dir = Path(config["build_directory"])
    build_dir.mkdir(parents=True, exist_ok=True)

    # Make a subdirectory for this report
    report_dir = build_dir / Path(f"{analysis_name}_report")
    report_dir.mkdir(parents=True, exist_ok=True)

    # Optionally clean the subfolder
    if args.clean:
        shutil.rmtree(report_dir)

    # Make the output folder for images in the build directory
    image_dest_dir = report_dir / Path("images")
    image_dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy the config and adjust to create Jinja2 variables
    variables = copy.deepcopy(config)

    def copy_most_recent_image(image_name: str) -> Path:
        """Find the most recent image with the given name and copy it to the build directory.

        NOTE: uses image_dest_dir from outer scope

        Args:
            image_name: The image base name

        Returns:
            The path of the image relative to the project build subfolder
                that can be referenced in the report.
        """
        image_path = common.pick_most_recent_saved_file(image_name, save_dir, "png")
        image_file_name = image_path.name
        shutil.copy(image_path, image_dest_dir / image_file_name)
        return Path("images") / image_file_name

    def copy_most_recent_file(
        name: str, extension: str, save_dir: str, report_dir: Path, dest_dir: Path
    ) -> Path:
        """Find the most recent file with the given name and copy it to the destination

        Args:
            name: The base name of the file to copy
            extension: The file extension of the file to copy
            save_dir: The directory in which to locate the file
                to copy
            report_dir: The path to the report output directory relative to
                the working directory
            dest_dir: The destination directory name in which to place the file
                relative to the report directory

        Returns:
            The path to the copied item, relative to the report directory.
                This can be used as a string in the report to locate the item.
        """
        src_path = common.pick_most_recent_saved_file(name, save_dir, extension)

        # Create the destination directory if it does not exist
        (report_dir / dest_dir).mkdir(parents=True, exist_ok=True)

        dest_path = report_dir / dest_dir / src_path.name
        shutil.copy(src_path, dest_path)
        return dest_dir / src_path.name

    # Load the summary table so that it the data is available for text
    # in the report.
    summary_table, summary_table_path = common.load_item(
        f"{analysis_name}_summary", save_dir=save_dir
    )

    print(summary_table)
   
    without_trade_off = summary_table[~summary_table["model_key"].eq("trade_off")]
   
    outcome = "bleeding"
    df = without_trade_off[without_trade_off["outcome_key"].eq(outcome)]
    m = df[df["median_auc"].eq(df["median_auc"].max())]
    variables[f"best_{outcome}_model_auc"] = f"{m['median_auc'][0]:.2f}"
    variables[f"best_{outcome}_model_name"] = config["models"][m["model_key"][0]]["text"]

    df = without_trade_off[without_trade_off["outcome_key"].eq(outcome)]
    m = df[df["median_auc"].eq(df["median_auc"].min())]
    variables[f"worst_{outcome}_model_auc"] = f"{m['median_auc'][0]:.2f}"
    variables[f"worst_{outcome}_model_name"] = config["models"][m["model_key"][0]]["text"]

    outcome = "ischaemia"
    df = without_trade_off[without_trade_off["outcome_key"].eq(outcome)]
    m = df[df["median_auc"].eq(df["median_auc"].max())]
    variables[f"best_{outcome}_model_auc"] = f"{m['median_auc'][0]:.2f}"
    variables[f"best_{outcome}_model_name"] = config["models"][m["model_key"][0]]["text"]

    df = without_trade_off[without_trade_off["outcome_key"].eq(outcome)]
    m = df[df["median_auc"].eq(df["median_auc"].min())]
    variables[f"worst_{outcome}_model_auc"] = f"{m['median_auc'][0]:.2f}"
    variables[f"worst_{outcome}_model_name"] = config["models"][m["model_key"][0]]["text"]    

    # Convert the summary table to markdown and insert it directly in the document
    variables["summary_table"] = summary_table.drop(columns=["model_key", "outcome_key", "median_auc"]).to_markdown()

    # Copy the summary table to the folder for reference.
    variables["summary_table_file"] = copy_most_recent_file(
        f"{analysis_name}_summary", "pkl", save_dir, report_dir, Path("tables")
    )

    outcome_prevalences, outcome_prevalences_path = common.load_item(
        f"{analysis_name}_outcome_prevalences", save_dir=save_dir
    )

    # Convert the summary table to markdown and insert it directly in the document
    variables["outcome_prevalences"] = outcome_prevalences.reset_index().to_markdown(
        index=False
    )

    # Read the features and store them as markdown
    features_df = pd.DataFrame.from_dict(config["features"], orient="index")
    features_df.rename(
        columns={"text": "Feature", "docs": "Description", "category": "Data Source"},
        inplace=True,
    )
    variables["features_table"] = features_df.to_markdown(index=False)

    # Get the table of outcome prevalences
    variables["outcome_prevalences_file"] = copy_most_recent_file(
        f"{analysis_name}_outcome_prevalences",
        "pkl",
        save_dir,
        report_dir,
        Path("tables"),
    )

    # For reference
    variables["data_file"] = copy_most_recent_file(
        f"{analysis_name}_data", "pkl", save_dir, report_dir, Path("tables")
    )

    # Load the data (this is the same file copied above)
    #data, data_path = common.load_item(f"{analysis_name}_data", save_dir=save_dir)

    variables["index_start"] = raw_data["index_start"].strftime("%Y-%m-%d")
    variables["index_end"] = raw_data["index_end"].strftime("%Y-%m-%d")
    variables["num_index_spells"] = len(data["index_spells"])

    # Get the list of code groups for the appendix
    codes = raw_data["code_groups"]
    codes["group"] = codes["group"].map(variables["code_groups"])
    codes["code"] = codes["code"].str.upper()
    diagnosis_codes = (
        codes[codes["type"] == "diagnosis"][["code", "docs", "group"]]
        .rename(
            columns={
                "code": "ICD-10 Code",
                "docs": "Description",
                "group": "Code Group",
            }
        )
        .dropna()
    )
    variables["diagnosis_codes_table"] = diagnosis_codes.to_markdown(index=False)

    # General variables 
    variables["bleeding_secondary_cutoff"] = config["outcomes"]["bleeding"]["non_fatal"]["max_position"] - 1
    variables["ischaemia_secondary_cutoff"] = config["outcomes"]["ischaemia"]["non_fatal"]["max_position"] - 1
    variables["num_features"] = len(features_df)

    # Copy plots from the descriptive script
    variables["codes_hist_image"] = copy_most_recent_image(f"{analysis_name}_codes_hist")

    # Copy plots from the descriptive script
    variables["outcome_survival_image"] = copy_most_recent_image(f"{analysis_name}_survival")

    # Copy plots from the descriptive script
    variables["arc_survival_image"] = copy_most_recent_image(f"{analysis_name}_arc_survival")    

    # Copy the most recent version of each figure into the
    # build directory
    for name, model in variables["models"].items():

        # Copy the model file
        model["file"] = copy_most_recent_file(
            f"{analysis_name}_{name}", "pkl", save_dir, report_dir, Path("models")
        )

        # Save the test set proportion (every model is the same,
        # so overwriting is fine)
        model_data, model_data_path = common.load_item(
            f"{analysis_name}_{name}", save_dir=save_dir
        )
        variables["test_proportion"] = model_data["config"]["test_proportion"]

        # ROC curves
        model["roc_curves_image"] = copy_most_recent_image(
            f"{analysis_name}_{name}_roc"
        )

        # Feature importances
        model["feature_importance_image"] = copy_most_recent_image(
            f"{analysis_name}_{name}_feature_importance"
        )

        # Bleeding/ischaemia trade-off
        model["trade_off_image"] = copy_most_recent_image(
            f"{analysis_name}_{name}_trade_off"
        )

        plots = ["stability", "calibration"]
        outcomes = ["bleeding", "ischaemia"]
        for outcome in outcomes:
            for plot in plots:
                model[f"{plot}_{outcome}_image"] = copy_most_recent_image(
                    f"{analysis_name}_{name}_{plot}_{outcome}"
                )

        # Extract data from the summary table
        bleeding_row = f"{model['abbr']}-B"
        ischaemia_row = f"{model['abbr']}-I"
        model["roc_auc_bleeding"] = summary_table.loc[bleeding_row, "ROC AUC"]
        model["roc_auc_ischaemia"] = summary_table.loc[ischaemia_row, "ROC AUC"]
        model["instability_bleeding"] = summary_table.loc[
            bleeding_row, "Spread of Instability"
        ]
        model["instability_ischaemia"] = summary_table.loc[
            ischaemia_row, "Spread of Instability"
        ]
        model["risk_uncertainty_bleeding"] = summary_table.loc[
            bleeding_row, "Estimated Risk Uncertainty"
        ]
        model["risk_uncertainty_ischaemia"] = summary_table.loc[
            ischaemia_row, "Estimated Risk Uncertainty"
        ]

    # Copy static files to output folder
    shutil.copy(config["bib_file"], report_dir / Path("ref.bib"))
    shutil.copy(config["citation_style"], report_dir / Path("style.csl"))
    shutil.copy(args.config_file, report_dir / Path("config.yaml"))

    # Set up the Jinja2 templates
    environment = Environment(loader=FileSystemLoader(config["templates_folder"]))

    # Render the report template and write it to the build directory
    report_template = environment.get_template(config["report_template"])
    doc = report_template.render(variables)
    (report_dir / Path("report.qmd")).write_text(doc, encoding="utf-8")

    # Render the readme template
    readme_template = environment.get_template("README.md")
    doc = readme_template.render(variables)
    (report_dir / Path("README.md")).write_text(doc, encoding="utf-8")

    # Optionally render the quarto
    if args.render:
        subprocess.run(["quarto", "render", "report.qmd"], cwd=report_dir)
