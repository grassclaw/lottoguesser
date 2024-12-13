# Packages
    ```

    conda create -n lottery_analysis python=3.10 -y
    conda activate lottery_analysis

    conda install pandas numpy matplotlib scikit-learn -y
    pip install pdfplumber
    ```

# Create conda from yml
    ```
    conda env create -f lottery_analysis_env.yml
    ```