# Load necessary libraries
process_and_project_data <- function(output_prefix, ref_file) {
  # Check for necessary libraries
  required_packages <- c("Seurat", "SeuratDisk", "ProjecTILs", "Matrix")
  
  missing_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]
  
  if (length(missing_packages) > 0) {
    stop(paste("The following required packages are missing. Please install them before running this script:", 
               paste(missing_packages, collapse = ", ")))
  }
  
  # Load the required packages
  lapply(required_packages, require, character.only = TRUE)
  
  # Read the matrix files
  cat("Reading matrix files...\n")
  raw_data <- Read10X(file.path(output_prefix, "matrix_files"))
  
  # Use read.csv to read metadata
  metadata <- read.csv(file.path(output_prefix, "metadata.csv"))
  
  # Create Seurat object
  cat("Creating Seurat object...\n")
  seurat_data <- CreateSeuratObject(counts = raw_data, meta.data = metadata)
  
  # Normalize data 
  cat("Normalizing data\n")
  seurat_data <- NormalizeData(object = seurat_data, normalization.method = "LogNormalize", scale.factor = 10000)
  
  # Project using ProjecTILs
  cat("Projecting using ProjecTILs...\n")
  reference <- readRDS(ref_file)
  query_projected <- Run.ProjecTILs(seurat_data, ref = reference, filter.cell = FALSE, skip.normalize = TRUE)
  # Adjust expression values before saving
  query_raw <- GetAssayData(seurat_data, layer = "counts")
  
  # Align gene order
  query_raw <- query_raw[rownames(query_projected), ]
  
  # Extract projected data
  query_df <- GetAssayData(query_projected, layer = "data")
  
  # Retain the values in query_df at positions where query_raw is non-zero
  # Use sparse matrix multiplication directly to avoid element-wise filling
  query_raw@x[query_raw@x != 0] <- 1  # Set non-zero elements in query_raw to 1
  query_df <- query_df * as.matrix(query_raw)  # Perform matrix multiplication to retain values at non-zero positions
  
  # Update the projected object with the adjusted data
  query_projected <- SetAssayData(query_projected, new.data = as.matrix(query_df))
  
  # Save as .h5seurat and convert to .h5ad
  cat("Saving the results...\n")
  query_projected@assays[["RNA"]] <- NULL
  SaveH5Seurat(query_projected, file.path(output_prefix, "batch_corrected_query.h5seurat"), assay="integrated")
  Convert(file.path(output_prefix, "batch_corrected_query.h5seurat"), dest = "h5ad")
  
  cat("Batch correction process completed successfully,..\n")
  cat("the corrected file was saved as query_projected.h5ad in the assigned folder.\n")
  
}
