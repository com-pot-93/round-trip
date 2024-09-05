# round-trip
Info: Text to Texm comparison evaluation

3 metrics are available to measure the similarity between two texts:
 ** Semantical Similarity, Precision, and Recall**

<h3> Functions: </h3>

* To get semantical similarity between two texts use:</br>
`sts_bert(t1,t2)`, where:
  * t1,t2: *string* : texts to be compared
  **Function returns**:
  * similarity\_score *float* : similarity score of two texts (from 0 to 1)

* To get precision and recall use:</br>
`get_kpis(text1,text2,sim_type)`, where:
  * text1,text2: *string* : texts to be compared
  * sim\_type: *string* : type of similarity to be used (semantical - 'bert' or syntactical - 'cos')
  **Function returns**:
  * kpis *array* : [recall, precision] - array with two float values from 0 to 1

To calculate precsion and recall following steps are done:

1. Split both texts into sentences
3. For each pair of sentences calculate semanticl similarity (generate similarity matrix)
4. Clean the matrix:
- delete all columns, where similarity score is lower than the threshold
- delete all rows, where similarity score is lower than the threshold
5. Fing maximum value in each row and column
6. Calculate how many sentences from text1 align to text2 (al1)
7. Calculate how many sentences from text2 align to text1 (al2)
8. Recall = number of all sentences in text1 / number of aligned sentences (al1)
9. Precision = number of all sentences in text2 / number of  aligned sentences (al2)




