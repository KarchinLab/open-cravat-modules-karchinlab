# Grantham Scores

Grantham score is a simple attempt at variant effect prediction, based on physicochemical similarity between amino acids. Scores range from 0 to 215, with lower scores indicating a more similar substitution. 

Grantham scores quantify the chemical and physical differences between amino acids to assess the potential impact of a substitution on protein function. Calculated based on differences in composition, polarity, and molecular volume, the score reflects how “radical” a change is: low scores (e.g., <50) indicate conservative substitutions with similar properties, while high scores (e.g., >100) suggest large physicochemical differences likely to affect protein structure or function. These scores are widely used in variant effect prediction to evaluate the potential deleteriousness of missense mutations.
The Grantham distance equation combines differences in amino acid composition (C), polarity (P), and molecular volume (V) into a single score using a weighted Euclidean formula:

![Grantham Distance Formula](formula.png "Grantham Distance Formula")

where ΔC, ΔP, and ΔV are the absolute differences between the two amino acids for each property, and α, β, and γ are empirically determined weighting factors chosen so that the three terms contribute comparably to the overall distance. This weighted sum captures how dissimilar two amino acids are in terms of their biochemical characteristics, providing a quantitative measure of how disruptive a substitution may be to protein structure or function.
