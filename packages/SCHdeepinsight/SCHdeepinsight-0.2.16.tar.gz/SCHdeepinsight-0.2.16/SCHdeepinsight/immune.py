import os
from pathlib import Path
import anndata
import pandas as pd
import numpy as np
import scanpy as sc
import scipy.io as io
from scipy.sparse import issparse
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
from efficientnet_pytorch import EfficientNet
import pickle
from sklearn import preprocessing
import cv2
from pyDeepInsight import ImageTransformer
import warnings
import torch.nn.functional as F
import rpy2.robjects as ro
import gzip

warnings.filterwarnings("ignore")

class Immune:
    def __init__(self, output_prefix):
        # Set up directories and load necessary resources
        self.pretrained_dir = Path(__file__).resolve().parent / "pretrained_files_immune"
        self.output_prefix = Path(output_prefix)
        os.makedirs(self.output_prefix, exist_ok=True)
        self.matrix_files_dir = self.output_prefix / 'matrix_files'
        os.makedirs(self.matrix_files_dir, exist_ok=True)
        self.gene_list = self._load_gene_list()
        self.img_transformer = self._load_img_transformer()
        self.index = [8, 2, 11, 2, 2, 4, 4, 1, 5, 3, 3, 1, 2, 1, 1]
        self.model = self._load_model()

    def _load_gene_list(self):
        # Load gene list for image transformation
        gene_list_path = self.pretrained_dir / "pretrained_genes_immune.csv"
        if not gene_list_path.exists():
            raise FileNotFoundError(f"Gene list file not found at {gene_list_path}")
        return pd.read_csv(gene_list_path, index_col=0).index.tolist()

    def _load_img_transformer(self):
        # Load pre-trained image transformer object
        transformer_path = self.pretrained_dir / "img_transformer_immune.obj"
        if not transformer_path.exists():
            raise FileNotFoundError(f"Image transformer file not found at {transformer_path}")
        with open(transformer_path, 'rb') as file:
            return pickle.load(file)
  

    def _load_model(self):
        model = EfficientNet.from_pretrained('efficientnet-b4', num_classes=50)
        model = nn.DataParallel(model)
        checkpoint_path = self.pretrained_dir / "checkpoint_model_immune.pth"
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found at {checkpoint_path}")
        if torch.cuda.is_available():
            model.load_state_dict(torch.load(checkpoint_path), strict=False)
        else:
            model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')), strict=False)
        return model.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu")).eval()    


    def preprocess(self, query_path: str):
        """Performs normalization and log1p transformation on the input .h5ad file."""
        query = anndata.read_h5ad(query_path)
        # Normalize and log1p transformation
        sc.pp.normalize_per_cell(query)
        sc.pp.log1p(query)
        
        # Save the preprocessed file in the specified output_prefix
        output_path = self.output_prefix / "query_preprocessed.h5ad"
        query.write(output_path)
        return output_path  # Return the path to the preprocessed .h5ad file

    def write_matrix_files(self, query):
        """Writes and compresses the matrix files (barcodes, features, matrix, metadata)."""
        # Write barcodes.tsv and compress
        barcodes_path = self.matrix_files_dir / 'barcodes.tsv'
        try:
            with open(barcodes_path, 'w') as f:
                for item in query.obs_names:
                    f.write(item + '\n')
            # Compress barcodes.tsv using the gzip system command
            os.system(f"gzip {barcodes_path}")
        except IOError as e:
            raise RuntimeError(f"Error writing barcodes to {barcodes_path}: {str(e)}")

        # Write features.tsv and compress
        features_path = self.matrix_files_dir / 'features.tsv'
        try:
            with open(features_path, 'w') as f:
                for item in ['\t'.join([x, x, 'Gene Expression']) for x in query.var["feature_name"]]:
                    f.write(item + '\n')
            # Compress features.tsv using the gzip system command
            os.system(f"gzip {features_path}")
        except IOError as e:
            raise RuntimeError(f"Error writing features to {features_path}: {str(e)}")

        # Write matrix.mtx and compress
        matrix_path = self.matrix_files_dir / 'matrix.mtx'
        try:
            io.mmwrite(matrix_path, query.X.T)
            # Compress matrix.mtx using the gzip system command
            os.system(f"gzip {matrix_path}")
        except Exception as e:
            raise RuntimeError(f"Error writing or compressing matrix to {matrix_path}: {str(e)}")

        # Write metadata.csv and compress
        metadata_path = self.output_prefix / 'metadata.csv'
        try:
            query.obs.to_csv(metadata_path)
        except IOError as e:
            raise RuntimeError(f"Error writing metadata to {metadata_path}: {str(e)}")

    def batch_correction(self, input_file, ref_file):
        """Performs batch correction using an R script for data projection."""
        # Check if R environment is available
        try:
            r = ro.r
        except ImportError as e:
            raise RuntimeError("rpy2 is not installed or R environment is not configured correctly.") from e

        # Check if the required R script exists
        script_dir = Path(__file__).resolve().parent
        r_script_path = script_dir / 'r_scripts' / 'process_data.R'
        if not r_script_path.exists():
            raise FileNotFoundError(f"R script for batch correction not found at {r_script_path}")

        # Read and preprocess the .h5ad file
        try:
            query = anndata.read_h5ad(input_file)
        except Exception as e:
            raise RuntimeError(f"Error reading input file {input_file}: {str(e)}")

        # Check if raw data exists and use it
        if query.raw is not None:
            query.X = query.raw.X

        # Ensure "feature_name" is present
        if "feature_name" not in query.var.columns:
            query.var["feature_name"] = query.var.index.tolist()

        # Write and compress matrix_files
        self.write_matrix_files(query)

        # Load and run the R script
        try:
            r.source(str(r_script_path))
            process_r = ro.globalenv['process_and_project_data']
            process_r(str(self.output_prefix), ref_file)
        except Exception as e:
            raise RuntimeError(f"Error executing R script for batch correction: {str(e)}")

        # Return the path to the batch corrected .h5ad file
        batch_corrected_query_path = self.output_prefix / "batch_corrected_query.h5ad"
        return batch_corrected_query_path

    def image_transform(self, query_path: str):
        """Transforms the .h5ad file into a DataFrame and then into images."""
        query = anndata.read_h5ad(query_path)
        # Ensure the "feature_name" column is present
        query.var["feature_name"] = query.var.get("feature_name", query.var.index.tolist())
        query.var.index = query.var["feature_name"].values

        # Filter genes based on the pre-loaded gene list
        remain_list = list(set(query.var.index) & set(self.gene_list))
        query = query[:, remain_list]

        # Scale data and prepare for image transformation
        sample = self._scale_and_fill(query)
        
        # Automatically generate barcode_path and image_path using output_prefix
        barcode_path = self.output_prefix / "barcode.csv"
        image_path = self.output_prefix / "query.npy"
        
        self._save_barcode(sample, barcode_path)
        self._save_image(sample, image_path)
        
        return image_path  # Return the path to the generated image file


    def predict(self, batch_size: int = 128, rare_base_threshold=60, rare_detailed_threshold=10):
        """Predicts cell types and identifies potential rare cells."""
        # Automatically determine barcode_path and image_path
        barcode_path = self.output_prefix / "barcode.csv"
        image_path = self.output_prefix / "query.npy"
        
        # Define custom dataset for loading images
        class MyTestSet(Dataset):
            def __init__(self, img):
                self.img = np.load(img)
                self.transforms = transforms.Compose([transforms.ToTensor(), ])
            def __getitem__(self, index):
                img = self.img[index, :, :, :]
                img = np.squeeze(img)
                img = Image.fromarray(np.uint8(img))
                img = self.transforms(img)
                return img
            def __len__(self):
                return self.img.shape[0]


        test_set = MyTestSet(image_path)
        test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)

        # Explicitly set the device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        out_base, out_detailed, out_base_probs, out_detailed_probs = [], [], [], []

        for data in test_loader:
            query = data.to(device)  # Move data to the same device as the model
            pred = F.softmax(self.model(query), dim=1)

            # Step 1: Determine base type through summing subtype probabilities
            base_tensor = self._sum_base_type_tensor(pred.data)
            base_probs, predicted_base_by_tree = torch.max(base_tensor, 1)

            # Step 2: Only consider the probabilities of the subtypes corresponding to the predicted base type
            output_sub = self._sub_predicted(pred.data, predicted_base_by_tree)

            # Set the probabilities of subtypes not belonging to the predicted base type to 0
            for i in range(len(output_sub)):
                base_type = predicted_base_by_tree[i].item()
                k1 = sum(self.index[:base_type])
                k2 = sum(self.index[:base_type + 1])
                output_sub[i, :k1] = 0  # Mask probabilities of subtypes not belonging to the base type
                output_sub[i, k2:] = 0  # Mask probabilities of subtypes not belonging to the base type

            # Finally, select the detailed subtype
            detail_probs, predicted_detailed = torch.max(output_sub.data, 1)

            out_base.append(predicted_base_by_tree)
            out_detailed.append(predicted_detailed)
            out_base_probs.append(base_probs)
            out_detailed_probs.append(detail_probs)

        # Create DataFrame with predictions
        pred_label = self._create_pred_label(barcode_path, out_base, out_detailed, out_base_probs, out_detailed_probs)

        # Determine potential rare cells
        is_potential_rare_series = pred_label.groupby('predicted_base_type', group_keys=False).apply(
            lambda group: self._is_potential_rare(group, rare_base_threshold=rare_base_threshold, rare_detailed_threshold=rare_detailed_threshold)
        )

        # Add the result as a new column
        pred_label['is_potential_rare'] = is_potential_rare_series

        return pred_label


    def _scale_and_fill(self, query):
        # Scale data and fill with zeros for missing genes
        if issparse(query.X):
            sample = pd.DataFrame(query.X.toarray()).T
        else:
            sample = pd.DataFrame(query.X).T
        sample = preprocessing.MinMaxScaler().fit_transform(sample)
        sample = pd.DataFrame(sample).T
        sample.index = query.obs.index.values
        sample.columns = query.var.index.values

        # Fill missing genes with zeros
        excluded_genes = list(set(self.gene_list) - set(sample.columns))
        blank_dataframe = pd.DataFrame(np.zeros((len(sample), len(excluded_genes))), 
                                       index=sample.index, columns=excluded_genes)
        sample = pd.concat([sample, blank_dataframe], axis=1)
        sample = sample[self.gene_list]
        return sample

    def _save_barcode(self, sample, barcode_path):
        # Save barcodes to CSV file
        barcode = pd.DataFrame(sample.index.tolist(), columns=["barcode"])
        barcode.to_csv(barcode_path, index=False)

    def _save_image(self, sample, image_path):
        # Transform and save images to numpy array
        query_img = cv2.normalize(self.img_transformer.transform(sample.values), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        query_img = query_img.astype(np.uint8)
        np.save(image_path, query_img)

    def _sum_base_type_tensor(self, data):
        # Summing probabilities of subtypes to get base type tensor
        base_type_tensor = torch.sum(data[:, 0:self.index[0]], dim=1).expand(1, -1)
        for i in range(1, len(self.index)):
            k1 = sum(self.index[0:i])
            k2 = sum(self.index[0:i+1])
            base_type_tensor = torch.cat(
                (base_type_tensor, torch.sum(data[:, k1:k2], dim=1).expand(1, -1)), dim=0
            )
        return base_type_tensor.t()

    def _sub_predicted(self, output, predicted_base_type):
        # Masking irrelevant subtypes for each base type
        sub_tensor = output.clone()
        for i in range(len(sub_tensor)):
            base_type = predicted_base_type[i]
            k1 = sum(self.index[0:base_type])
            k2 = sum(self.index[0:base_type + 1])
            sub_tensor[i, :k1] = 0
            sub_tensor[i, k2:] = 0
        return sub_tensor

    def _create_pred_label(self, barcode_path, out_base, out_detailed, out_base_probs, out_detailed_probs):
        # Create a DataFrame containing the predicted labels and their probabilities
        pred_base = torch.cat(out_base).cpu().numpy()
        pred_detailed = torch.cat(out_detailed).cpu().numpy()
        pred_base_probs = torch.cat(out_base_probs).cpu().numpy()
        pred_detail_probs = torch.cat(out_detailed_probs).cpu().numpy()

        pred_label_base = self._decode_labels(pred_base, "label_encoder_immune_base.obj", "predicted_base_type")
        pred_label_detailed = self._decode_labels(pred_detailed, "label_encoder_immune_detailed.obj", "predicted_detailed_type")

        labels_prob = pd.DataFrame({
            "predicted_base_type_prob": pred_base_probs,
            "predicted_detailed_type_prob": pred_detail_probs
        })

        barcode = pd.read_csv(barcode_path)
        return pd.concat([barcode["barcode"], pred_label_base, pred_label_detailed, labels_prob], axis=1)

    def _decode_labels(self, predictions, encoder_file, column_name):
        # Decode the predictions using the pre-trained label encoder
        encoder_path = self.pretrained_dir / encoder_file
        if not encoder_path.exists():
            raise FileNotFoundError(f"Label encoder not found at {encoder_path}")
        with open(encoder_path, 'rb') as file:
            encoder = pickle.load(file)
        labels = encoder.inverse_transform(predictions)
        return pd.DataFrame(labels, columns=[column_name])

    def _is_potential_rare(self, base_type_group, rare_base_threshold=60, rare_detailed_threshold=10):
        base_prob_threshold = np.percentile(base_type_group['predicted_base_type_prob'], rare_base_threshold)
        detailed_prob_threshold = np.percentile(base_type_group['predicted_detailed_type_prob'], rare_detailed_threshold)
        return (base_type_group['predicted_base_type_prob'] > base_prob_threshold) & \
               (base_type_group['predicted_detailed_type_prob'] < detailed_prob_threshold)