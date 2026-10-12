
import subprocess
import sys


steps = [
    ("Extract data", "src.extract"),
    ("Transform data", "src.transform"),
    ("Validate data", "src.validate"),
    ("Load data into MySQL", "src.load"),
    ("Refresh data warehouse", "src.refresh_warehouse"),
]


for step_name, module_name in steps:
    print(f"\n{'=' * 50}")
    print(f"STEP: {step_name}")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        check=False
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped: {step_name} failed.")
        sys.exit(result.returncode)

print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")


