# Annotation Tool

This folder contains a simple annotation tool implemented as a Streamlit web application. The tool is designed for annotating questions as part of a multi-stage annotation process.

## Installation

To get started, install the required dependencies:

```bash
pip install streamlit PyYAML
```

## Usage

### Stage 1 Annotation

1. Navigate to the `Annotation_Tool` directory:
   ```bash
   cd Annotation_Tool
   ```

2. Run the Stage 1 annotation tool:
   ```bash
   streamlit run Stage_1_Annotator.py
   ```

3. A web application will launch in your default browser. Use this interface for the first stage of question annotations.

### Stage 2 Annotation

After completing the first stage of annotations, proceed to the second stage to determine whether a question is Indic or not.

1. Run the Stage 2 annotation tool:
   ```bash
   streamlit run Stage_2_Annotator.py
   ```

2. As with Stage 1, this will open a web application for the second stage of annotations.

## Notes

- Ensure you are in the correct directory (`Annotation_Tool`) before running the Streamlit commands.
- The tools are designed to follow the sequential annotation process: Stage 1 followed by Stage 2.

If you encounter any issues or have questions about the tool, feel free to reach out!