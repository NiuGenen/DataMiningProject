# DataMiningProject

- 交通拥堵预测

---

# Preprocessing

### step one

- Combine txt files into one csv file
- Remove column 'roadtype' 'length'
- Convert label into integer
    - unknown : -1
    - no : 0
    - light : 1
    - medium : 2
    - high : 3
    
### step two

- Convert 'direction' 'linkid' into integer
- And store the mapping

### step three

- Remove all the data of some linkid, which contains too much unknown
- Fill the remaining unknown data
    - Using the data from the other time at the same day
    - Using the data from the same time at the other day
    - Average

### step four

- Convert into training format

---

# Train

- DecisionTree
- Neural Network

---

# Prediction

- Select half an hour's data as input data
- Preprocessing input data
- predicting