"""
Dataset analyzers for inspecting and understanding data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class DatasetStats:
    """Statistics about a dataset."""
    num_rows: int
    num_cols: int
    memory_usage: int
    column_types: Dict[str, str]
    missing_values: Dict[str, int]
    missing_percentages: Dict[str, float]
    numeric_stats: Dict[str, Dict[str, float]]
    categorical_stats: Dict[str, Dict[str, Any]]
    duplicates: int
    potential_issues: List[str]


class DatasetAnalyzer:
    """Analyze datasets and provide insights."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.df: pd.DataFrame = None
        self.stats: DatasetStats = None
    
    def load_data(self) -> None:
        """Load the dataset based on file extension."""
        suffix = self.file_path.suffix.lower()
        
        if suffix == '.csv':
            self.df = pd.read_csv(self.file_path, sep=None, engine = "python")
        elif suffix in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path)
        elif suffix == '.json':
            self.df = pd.read_json(self.file_path)
        elif suffix == '.parquet':
            self.df = pd.read_parquet(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def analyze(self) -> DatasetStats:
        """Perform comprehensive dataset analysis."""
        if self.df is None:
            self.load_data()
        
        # Basic info
        num_rows, num_cols = self.df.shape
        memory_usage = self.df.memory_usage(deep=True).sum()
        
        # Column types
        column_types = {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        
        # Missing values
        missing_values = self.df.isnull().sum().to_dict()
        missing_percentages = {
            col: (count / num_rows * 100) if num_rows > 0 else 0
            for col, count in missing_values.items()
        }
        
        # Numeric statistics
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_stats = {}
        for col in numeric_cols:
            numeric_stats[col] = {
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'median': float(self.df[col].median()),
                'q25': float(self.df[col].quantile(0.25)),
                'q75': float(self.df[col].quantile(0.75)),
            }
        
        # Categorical statistics
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        categorical_stats = {}
        for col in categorical_cols:
            unique_count = self.df[col].nunique()
            categorical_stats[col] = {
                'unique_count': unique_count,
                'most_common': self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else None,
                'most_common_freq': int(self.df[col].value_counts().iloc[0]) if unique_count > 0 else 0,
            }
        
        # Duplicates
        duplicates = self.df.duplicated().sum()
        
        # Detect potential issues
        potential_issues = self._detect_issues(
            missing_percentages, numeric_stats, categorical_stats, duplicates, num_rows
        )
        
        self.stats = DatasetStats(
            num_rows=num_rows,
            num_cols=num_cols,
            memory_usage=memory_usage,
            column_types=column_types,
            missing_values=missing_values,
            missing_percentages=missing_percentages,
            numeric_stats=numeric_stats,
            categorical_stats=categorical_stats,
            duplicates=duplicates,
            potential_issues=potential_issues,
        )
        
        return self.stats
    
    def _detect_issues(
        self,
        missing_percentages: Dict[str, float],
        numeric_stats: Dict[str, Dict[str, float]],
        categorical_stats: Dict[str, Dict[str, Any]],
        duplicates: int,
        num_rows: int,
    ) -> List[str]:
        """Detect potential data quality issues."""
        issues = []
        
        # High missing values
        for col, pct in missing_percentages.items():
            if pct > 50:
                issues.append(f"Column '{col}' has {pct:.1f}% missing values")
            elif pct > 20:
                issues.append(f"Column '{col}' has {pct:.1f}% missing values (moderate)")
        
        # High cardinality categoricals
        for col, stats in categorical_stats.items():
            if stats['unique_count'] > num_rows * 0.9:
                issues.append(f"Column '{col}' has very high cardinality ({stats['unique_count']} unique values)")
        
        # Potential outliers in numeric columns
        for col, stats in numeric_stats.items():
            iqr = stats['q75'] - stats['q25']
            if iqr > 0:
                lower_bound = stats['q25'] - 3 * iqr
                upper_bound = stats['q75'] + 3 * iqr
                if stats['min'] < lower_bound or stats['max'] > upper_bound:
                    issues.append(f"Column '{col}' may contain outliers")
        
        # Duplicates
        if duplicates > 0:
            dup_pct = (duplicates / num_rows * 100) if num_rows > 0 else 0
            issues.append(f"Dataset contains {duplicates} duplicate rows ({dup_pct:.1f}%)")
        
        # Small dataset
        if num_rows < 100:
            issues.append(f"Small dataset ({num_rows} rows) - may not be sufficient for training")
        
        return issues
    
    def suggest_preprocessing(self) -> List[str]:
        """Suggest preprocessing steps based on analysis."""
        if self.stats is None:
            self.analyze()
        
        suggestions = []
        
        # Missing values
        for col, pct in self.stats.missing_percentages.items():
            if pct > 50:
                suggestions.append(f"Consider dropping column '{col}' (>{pct:.1f}% missing)")
            elif pct > 0:
                if col in self.stats.numeric_stats:
                    suggestions.append(f"Impute missing values in '{col}' (numeric) with median/mean")
                else:
                    suggestions.append(f"Impute missing values in '{col}' (categorical) with mode or 'unknown'")
        
        # Duplicates
        if self.stats.duplicates > 0:
            suggestions.append(f"Remove {self.stats.duplicates} duplicate rows")
        
        # Scaling
        if self.stats.numeric_stats:
            suggestions.append("Scale/normalize numeric features (StandardScaler or MinMaxScaler)")
        
        # Encoding
        if self.stats.categorical_stats:
            suggestions.append("Encode categorical features (OneHotEncoder or LabelEncoder)")
        
        # High cardinality
        for col, stats in self.stats.categorical_stats.items():
            if stats['unique_count'] > 50:
                suggestions.append(f"Consider feature hashing or target encoding for '{col}' (high cardinality)")
        
        # Outliers
        for col in self.stats.numeric_stats:
            if any(f"Column '{col}' may contain outliers" in issue for issue in self.stats.potential_issues):
                suggestions.append(f"Handle outliers in '{col}' (clip, remove, or transform)")
        
        # Train-test split
        suggestions.append("Split data into train/validation/test sets (e.g., 70/15/15)")
        
        return suggestions
    
    def suggest_models(self) -> Dict[str, List[str]]:
        """Suggest suitable ML/DL models based on dataset characteristics."""
        if self.stats is None:
            self.analyze()
        
        suggestions = {
            'classification': [],
            'regression': [],
            'general': [],
        }
        
        num_rows = self.stats.num_rows
        num_features = self.stats.num_cols
        
        # Determine task type (this is a heuristic)
        has_categorical_target = False
        has_numeric_target = False
        
        # Check if last column might be target
        last_col = list(self.stats.column_types.keys())[-1] if self.stats.column_types else None
        if last_col:
            if last_col in self.stats.categorical_stats:
                unique_count = self.stats.categorical_stats[last_col]['unique_count']
                if unique_count < 20:  # Likely classification
                    has_categorical_target = True
            elif last_col in self.stats.numeric_stats:
                has_numeric_target = True
        
        # Classification models
        if has_categorical_target or num_rows < 10000:
            suggestions['classification'] = [
                "Logistic Regression (baseline)",
                "Random Forest Classifier",
                "XGBoost Classifier",
                "LightGBM Classifier",
                "CatBoost Classifier",
            ]
            
            if num_rows > 1000:
                suggestions['classification'].append("Neural Network (MLP)")
        
        # Regression models
        if has_numeric_target or not has_categorical_target:
            suggestions['regression'] = [
                "Linear Regression (baseline)",
                "Ridge/Lasso Regression",
                "Random Forest Regressor",
                "XGBoost Regressor",
                "LightGBM Regressor",
            ]
            
            if num_rows > 1000:
                suggestions['regression'].append("Neural Network (MLP)")
        
        # General recommendations
        if num_rows < 1000:
            suggestions['general'].append("Dataset is small - use simple models and cross-validation")
        elif num_rows < 10000:
            suggestions['general'].append("Medium dataset - tree-based models (RF, XGBoost) work well")
        else:
            suggestions['general'].append("Large dataset - consider deep learning or gradient boosting")
        
        if num_features > 50:
            suggestions['general'].append("High-dimensional data - consider feature selection or PCA")
        
        if self.stats.categorical_stats:
            suggestions['general'].append("Has categorical features - CatBoost handles these natively")
        
        return suggestions


def analyze_dataset(file_path: Path) -> Tuple[DatasetStats, List[str], Dict[str, List[str]]]:
    """
    Analyze a dataset and return statistics, preprocessing suggestions, and model recommendations.
    
    Args:
        file_path: Path to the dataset file
        
    Returns:
        Tuple of (stats, preprocessing_suggestions, model_suggestions)
    """
    analyzer = DatasetAnalyzer(file_path)
    stats = analyzer.analyze()
    preprocessing = analyzer.suggest_preprocessing()
    models = analyzer.suggest_models()
    
    return stats, preprocessing, models
