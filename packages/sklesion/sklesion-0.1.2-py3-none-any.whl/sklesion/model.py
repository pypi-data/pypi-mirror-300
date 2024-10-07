import tensorflow as tf
import pickle
import os
import importlib
import pandas as pd
import numpy as np


# Python class for the skin cancer classifier
class SkinLesionClassifier:
    # ---> Construct instance
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Path to the file with Keras model
        self.model_path = os.path.join(current_dir, "model.keras")
        # Path to file with model properties' dictionary
        self.model_props_path = os.path.join(current_dir, "model_props.pkl")
        # Path to file with ProbToLabel Keras layer (for getting labels from predicted
        # probabilities)
        self.prob_to_label_path = os.path.join(current_dir, "prob_to_label.py")
        # Path to file with detailed description of the diagnosis classes
        self.cl_info_path = os.path.join(current_dir, "cl_info.pkl")
        # The model itself
        self.model = self.load_model()
        # Model properties dictionary
        self.model_props = self.load_model_props()
        # ProbToLabel layer
        self.prob_to_label = self.load_prob_to_label()
        # Detailed description of the diagnosis classes
        self.cl_info = self.load_cl_info()
        # List of diagnosis classes
        self.cl = self.get_cl()
        # List of benign diagnosis classes
        self.cl_ben = self.get_cl_ben()
        # List of the malign diagnosis classes
        self.cl_mal = self.get_cl_mal()

    # ---> Load model from file
    def load_model(self):
        if os.path.exists(self.model_path):
            return tf.keras.models.load_model(self.model_path)
        else:
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

    # ---> Load model properties dictionary from file
    def load_model_props(self):
        if os.path.exists(self.model_props_path):
            with open(self.model_props_path, "rb") as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(
                f"Model properties' file not found: {self.model_props_path}"
            )

    # ---> Load ProbToLabel Keras layer from file (for getting labels from predicted
    # probabilities)
    def load_prob_to_label(self):
        if os.path.exists(self.prob_to_label_path):
            spec = importlib.util.spec_from_file_location(
                "prob_to_label.py", self.prob_to_label_path
            )
            file = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(file)
            ProbToLabel = file.ProbToLabel
            return ProbToLabel(self.model_props["i_cl_map"])
        else:
            raise FileNotFoundError(
                f"ProbToLabel file not found: {self.prob_to_label_path}"
            )

    # ---> Load detailed description of the diagnosis classes from file
    def load_cl_info(self):
        if os.path.exists(self.cl_info_path):
            with open(self.cl_info_path, "rb") as f:
                return pickle.load(f)
        else:
            raise FileNotFoundError(f"Classes' file not found: {self.cl_info_path}")

    # ---> Get the codenames of the diagnosis classes
    def get_cl(self) -> list:
        cl = list(self.cl_info.keys())
        return cl

    # ---> Get the codenames of the benign diagnosis classes
    def get_cl_ben(self) -> list:
        cl_ben = [
            cl_i for cl_i in self.cl if self.cl_info[cl_i]["severity"] == "Benign"
        ]
        return cl_ben

    # ---> Get the codenames of the malign diagnosis classes
    def get_cl_mal(self) -> list:
        cl_mal = [
            cl_i for cl_i in self.cl if self.cl_info[cl_i]["severity"] == "Malign"
        ]
        return cl_mal

    # ---> Pre-process features
    def preprocess(self, x: dict) -> tf.data.Dataset:

        # Create TensorFlow tensor from image (bytes object)
        image = tf.image.decode_jpeg(x["image"], channels=3)

        # Create pandas DataFrame from meta dictionary
        meta = pd.Series(x["meta"]).to_frame().transpose()

        # Re-scale image image
        image = tf.image.resize(image, self.model_props["img_shape"])

        # Handle the possibility of age missing its value
        meta["age_missing"] = meta["age"].isnull().astype(int)
        meta["age"].fillna(self.model_props["age_mean"], inplace=True)

        # One-hot encode nominal meta features (sex and location)
        meta["sex"] = meta["sex"].map(
            {key: value for (key, value) in self.model_props["oh_map"]["sex"].items()}
        )
        meta["location"] = meta["location"].map(
            {key: value for (key, value) in self.model_props["oh_map"]["loc"].items()}
        )

        # Normalize numeral meta feature age
        meta["age"] = meta["age"] / self.model_props["age_max"]

        # Combine the different meta features to define an overall feature vector
        meta = (
            meta["sex"]
            + meta["location"]
            + meta["age"].apply(lambda x: [x])
            + meta["age_missing"].apply(lambda x: [x])
        )

        # Define TensorFlow Dataset from image and metadata
        x = tf.data.Dataset.zip(
            (
                (
                    tf.data.Dataset.from_tensor_slices(image),
                    tf.data.Dataset.from_tensor_slices(meta.to_list()),
                ),
            )
        ).batch(1)

        return x

    # ---> Predict diagnosis probabilities
    def predict_P(self, x: dict) -> np.ndarray:
        x_pre = self.preprocess(x)
        P = self.model.predict(x_pre)
        return P

    # ---> Get diagnosis probability dictionaries from diagnosis probabilities
    def get_P_info_from_P(self, P: np.ndarray) -> np.ndarray:
        P_info = np.array(
            [
                {cl_i: P_j[i] for (i, cl_i) in self.model_props["i_cl_map"].items()}
                for P_j in P
            ]
        )
        return P_info

    # ---> Predict diagnosis probabilities in the form of dictionaries
    def predict_P_info(self, x: dict) -> np.ndarray:
        P = self.predict_P(x)
        P_info = self.get_P_info_from_P(P)
        return P_info

    # ---> Predict diagnoses (i.e. most probable diagnoses)
    def predict_y(self, x: dict) -> np.ndarray:
        P = self.predict_P(x)
        y = self.prob_to_label(P).numpy().astype(str)
        return y

    # ---> Get probabilities of the most probable diagnoses from diagnosis probabilities
    def get_P_y_from_P(self, P_info: np.ndarray) -> np.ndarray:
        P_y = P_info.max(axis=1)
        return P_y

    # ---> Get probabilities of the most probable diagnoses from diagnosis probability
    # dictionaries
    def get_P_y_from_P_info(self, P_info: np.ndarray) -> np.ndarray:
        P_y = P_info.max(axis=1)
        return P_y

    # ---> Predict diagnoses from diagnosis probabilities
    def get_y_from_P(self, P: np.ndarray) -> np.ndarray:
        y = self.prob_to_label(P).numpy().astype(str)
        return y

    # ---> Predict diagnoses from diagnosis probability dictionaries
    def get_y_from_P_info(self, P_info: np.ndarray) -> np.ndarray:
        P = np.array([list(P_info_i.values()) for P_info_i in P_info])
        y = self.get_y_from_P(P)
        return y

    # ---> Get probabilities of benign diseases from diagnosis probability dictionaries
    def get_P_ben_from_P_info(self, P_info: np.ndarray) -> np.ndarray:
        P_ben = np.array([P_info[cl_i] for cl_i in self.cl_ben])
        return P_ben

    # ---> Get probabilities of malign diseases from diagnosis probability dictionaries
    def get_P_mal_from_P_info(self, P_info: np.ndarray) -> np.ndarray:
        P_mal = np.array([P_info[cl_i] for cl_i in self.cl_mal])
        return P_mal

    # ---> Get probabilities of benign diseases from diagnosis probabilities
    def get_P_ben_from_P(self, P: np.ndarray) -> np.ndarray:
        P_info = self.get_P_info_from_P(P)
        P_ben = self.get_P_ben_from_P_info(P_info)
        return P_ben

    # ---> Get probabilities of malign diseases from diagnosis probabilities
    def get_P_mal_from_P(self, P: np.ndarray) -> np.ndarray:
        P_info = self.get_P_info_from_P(P)
        P_mal = self.get_P_mal_from_P_info(P_info)
        return P_mal
