# Real Estate Classification and Categorization using AI

This project aims to classify and categorize real estate properties using a combination of image and text data. The goal is to build a machine learning model that can automatically classify properties into categories such as type (house, apartment, land), architectural style, condition, location, and more.

## Table of Contents
- [Project Overview](#project-overview)
- [Data Collection](#data-collection)
- [Data Preprocessing](#data-preprocessing)
  - [Text Data](#text-data)
  - [Image Data](#image-data)
- [Feature Engineering](#feature-engineering)
- [Model Selection](#model-selection)
- [Training](#training)
- [Evaluation](#evaluation)
- [Deployment](#deployment)
- [Maintenance](#maintenance)
- [Tools and Libraries](#tools-and-libraries)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The project involves training an AI model to classify and categorize real estate properties using both image and text data. The process includes:

- Collecting data from real estate platforms.
- Preprocessing and feature engineering for both text and image data.
- Training multimodal machine learning models.
- Evaluating and deploying the model for real-world use.

## Data Collection
Data is collected from real estate platforms such as OLX, and Imóveis Web. The data includes:

- **Text Data:** Property descriptions, titles, and metadata.
- **Image Data:** Photos of properties (e.g., interiors, exteriors, landscapes).

Tools used for data collection:

- Web scraping libraries: `Scrapy`, `Selenium`.
- APIs provided by real estate platforms (if available).

## Data Preprocessing
### Text Data
- **Cleaning:** Remove stop words, punctuation, and special characters.
- **Tokenization:** Split text into words or sentences.
- **Normalization:** Convert text to lowercase, lemmatization, etc.
- **Vectorization:** Use techniques like TF-IDF, Word2Vec, or BERT embeddings.

### Image Data
- **Resizing:** Resize images to a standard size (e.g., 224x224).
- **Normalization:** Normalize pixel values to the range [0, 1].
- **Data Augmentation:** Apply techniques like rotation, flipping, etc., to increase dataset size.

## Feature Engineering
- **Text Features:** Extract features such as word frequencies, embeddings, etc.
- **Image Features:** Use pre-trained CNNs (e.g., ResNet, VGG, Inception) to extract features.
- **Multimodal Features:** Combine text and image features for multimodal models.

## Model Selection
- **Text Models:** LSTM, GRU, BERT, or traditional classifiers like SVM and Random Forest.
- **Image Models:** CNNs like ResNet, VGG, or EfficientNet.
- **Multimodal Models:** Combine text and image features using architectures like CLIP, ViLT, or custom fusion models.

## Training
- **Data Splitting:** Split data into training (70%), validation (15%), and test (15%) sets.
- **Training Process:** Train models using frameworks like TensorFlow or PyTorch.
- **Hyperparameter Tuning:** Use Grid Search or Random Search for optimization.
- **Regularization:** Apply techniques like dropout and early stopping to prevent overfitting.

## Evaluation
- **Metrics:** Evaluate models using accuracy, precision, recall, F1-score, etc.
- **Confusion Matrix:** Analyze classification errors.
- **Model Adjustments:** Fine-tune models based on evaluation results.

## Deployment
- **API Development:** Use Flask or FastAPI to create an API for the model.
- **User Interface:** Develop a simple UI for users to interact with the model.
- **Monitoring:** Monitor model performance in production and update as needed.

## Maintenance
- **Continuous Data Collection:** Regularly collect new data to keep the model up-to-date.
- **Re-training:** Periodically retrain the model with new data.
- **Updates:** Make adjustments based on user feedback and changing requirements.

## Tools and Libraries
- **Python:** Primary programming language.
- **TensorFlow/PyTorch:** For deep learning model development.
- **Scikit-learn:** For traditional machine learning models.
- **NLTK/Spacy:** For natural language processing.
- **OpenCV/PIL:** For image processing.
- **Pandas/Numpy:** For data manipulation.
- **Flask/FastAPI:** For API development.

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Setup with Anaconda

1. Install Anaconda or Miniconda from https://docs.conda.io/en/latest/miniconda.html

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd real-estate-ml
   ```

3. Create and activate the conda environment:
   ```bash
   make create_environment
   conda activate real-estate-ml
   ```

4. Install Python dependencies:
   ```bash
   make requirements
   ```

## Development Commands

- Format code: `make format`
- Check code style: `make lint`
- Clean compiled files: `make clean`
- Update environment: `make update_environment`
- Process dataset: `make data`

View all available commands:
```bash
make help
```
