from pathlib import Path

from loguru import logger
import pandas as pd
import typer
from ydata_profiling import ProfileReport

from real_estate_ml.config import PROCESSED_DATA_DIR, REPORTS_DIR

app = typer.Typer()

@app.command()
def main(
    train_path: Path = PROCESSED_DATA_DIR / "train.csv",
    test_path: Path = PROCESSED_DATA_DIR / "test.csv",
    output_dir: Path = REPORTS_DIR / "profiling",
):
    """Generate profiling reports for the datasets"""
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate report for training data
    logger.info("Generating profiling report for training data...")
    train_df = pd.read_csv(train_path)
    train_profile = ProfileReport(
        train_df, 
        title="Training Dataset Profiling Report",
        explorative=True
    )
    train_profile.to_file(output_dir / "train_profile.html")
    
    # Generate report for test data
    logger.info("Generating profiling report for test data...")
    test_df = pd.read_csv(test_path)
    test_profile = ProfileReport(
        test_df,
        title="Test Dataset Profiling Report",
        explorative=True
    )
    test_profile.to_file(output_dir / "test_profile.html")
    
    # Generate comparison report
    logger.info("Generating comparison report...")
    comparison_profile = train_profile.compare(test_profile)
    comparison_profile.to_file(output_dir / "comparison_profile.html")
    
    logger.success("Profiling reports generated successfully!")

if __name__ == "__main__":
    app()