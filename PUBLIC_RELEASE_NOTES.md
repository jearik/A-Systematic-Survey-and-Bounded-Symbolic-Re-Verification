# Public release preparation notes

Source package: `Survey_FV_CrossDomain_IIoT_ACCESS_Supplementary_Artifacts_v17_1_20260720.zip`.

Preparation actions:

1. extracted the validated 387-file payload;
2. removed tool-installation logs containing user-specific environment paths;
3. removed the nested duplicate `S3_ABLATION_FULL_LOGS.zip` while retaining its text and CSV evidence;
4. replaced absolute Windows, WSL, and Linux home paths in text logs with placeholders;
5. added current reproducible vector-figure inputs and exports;
6. corrected three truncated/OCR-damaged bibliographic titles without changing coding fields;
7. added repository metadata, citation metadata, dependencies, and validation tooling;
8. applied CC BY 4.0 to data/documentation and MIT to original code/model sources;
9. regenerated `MANIFEST_SHA256.csv` for the public directory.

These actions create a sanitized derivative for public distribution. The validated submission ZIP remains the immutable provenance package.
