import pandas as pd
import zipfile

class Dataset:
    def __init__(self, zip_path, filename):
        self.zip_path = zip_path
        self.filename = filename

    def __repr__(self):
        return f"Dataset('{self.zip_path}', '{self.filename}')"

    def to_frame(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            with zf.open(self.filename) as file:
                if self.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif self.filename.endswith('.xlsx'):
                    df = pd.read_excel(file)
                elif self.filename.endswith('.tsv'):
                    df = pd.read_csv(file, sep='\t')
                else:
                    raise ValueError("Unsupported file format.")
        return df

class DatasetZip:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.files = self._load_datasets()

    def _load_datasets(self):
        datasets = []
        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            for filename in zf.namelist():
                if filename.endswith(('.csv', '.xlsx', '.tsv')):
                    datasets.append(Dataset(self.zip_path, filename))
        return datasets

    def __repr__(self):
        return f"DatasetZip('{self.zip_path}')"

# Usage example
dataset_zip = DatasetZip('/mnt/sabrent2/data/amazon-product-dataset-2020.zip')
print(dataset_zip.files)

# Assuming you want to load the first dataset into a DataFrame
if dataset_zip.files:
    df = dataset_zip.files[0].to_frame()
    print(df.head())  # Display the first few rows of the DataFrame
else:
    print("No supported dataset files found.")
