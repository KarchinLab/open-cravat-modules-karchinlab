# MISTIC - MISsense deleTeriousness predICtor

MISTIC uses a supervised machine-learning model dedicated to the prediction of deleterious missense variants. MISTIC incorporates a Soft Voting system using the machine-learning algorithms Random Forest and Logistic Regression. The algorithms were trained to distinguish deleterious from benign missense variants based on a selection of 113 missense features. Examples of these features include multi-ethnic minor allele frequencies and evolutionary conservation, and physiochemical and biochemical properties of amino acids.

## Scores

The Soft Voting system generates a score from 0 to 1 and represents the probability of a given missense variant to be classified as deleterious. By default, missense variants with scores >0.5 are classified as deleterious and missense variants with scores <0.5 are classified as benign.

Information from https://lbgi.fr/mistic/