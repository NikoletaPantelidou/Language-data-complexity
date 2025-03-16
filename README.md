# Language Complexity Analysis Across English, Greek, Catalan, and Spanish

## Project Overview

This project analyzes language complexity across **English, Greek, Catalan, and Spanish** using data from the **Grambank dataset**. The original R code, developed by **Hedvig Skirgård**, is used to calculate complexity scores based on two key metrics:

- **Fusion**: Measures the amount of morphology in a language.
- **Informativity**: Assesses the amount of obligatory grammatical information encoded.
  
## Methodology

- **Data Source**:
- 1.Grambank dataset with selected language values (document values.csv including only the relevant languages of this study)
- 2.Parameters file for fusion and informativity (parameters.csv) belongs to Hedvig Skirgård and no changes applied.
- **Fusion Score Calculation**:
  - Features with a Fusion weight of `1` contribute points to the Fusion score.
  - Features with a weight of `0` or `0.5` are ignored.
  - The final Fusion score is the mean of all valid Fusion points.
- **Informativity Score Calculation**:
  - Groups of grammatical features (e.g., singular, tense) are analyzed.
  - A language score if it marks at least one feature in each group.
  - The informativity score is the proportion of marked sets.

## Purpose

This study aims to compare how different languages encode complexity and whether **morphology (Fusion) and grammatical encoding (Informativity) vary systematically across these languages.**


## Future Work

- Expanding the analysis to **more languages**.
- Refining **Fusion and Informativity** metrics.
- Comparing spoken vs. written language complexity.

## References

📜 The code and the complexity analysis belongs to Hedvig Skirgård and can be found here https://github.com/HedvigS/rgrambank 

