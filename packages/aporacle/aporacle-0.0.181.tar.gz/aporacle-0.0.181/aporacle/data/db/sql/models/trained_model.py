from komoutils.core.time import the_time_in_iso_now_is
from sqlalchemy import Index, Column, Integer, String, Float, JSON, inspect

from aporacle.data.db.sql.models import Base


class TrainedModel(Base):
    __tablename__ = "TrainedModel"
    __table_args__ = (Index("os_chain_feed_name_target_index", "chain", "feed", "name", "target"),)

    id = Column(String(255), primary_key=True, nullable=False)
    chain = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    feed = Column(String(255), nullable=False)
    symbols = Column(JSON, nullable=False)
    model_type = Column(String(255), nullable=False)
    r2 = Column(Float, nullable=False)
    rmse = Column(Float, nullable=False)
    feature_count = Column(Float, nullable=True)
    target = Column(Integer, nullable=True)
    scaler_mean = Column(JSON, nullable=True)
    scaler_scale = Column(JSON, nullable=True)
    coefficients = Column(JSON, nullable=True)
    intercept = Column(Float, nullable=True)
    performance = Column(JSON, nullable=True, default={})
    ranking = Column(Integer, nullable=True, default=0)
    last_evaluation_voting_round = Column(Integer, nullable=True, default=0)
    last_evaluation_time = Column(String(255), nullable=True, default='')
    running = Column(Integer, nullable=True, default=0)
    predicting = Column(Integer, nullable=True, default=0)
    # Metrics columns
    running_r_squared = Column(Float, nullable=True, default=0)  # R² (R-squared) - Running evaluation metric
    directional_accuracy = Column(Float, nullable=True)  # Directional Accuracy
    overestimation_frequency = Column(Float, nullable=True)  # Overestimation Frequency
    underestimation_frequency = Column(Float, nullable=True)  # Underestimation Frequency
    average_overestimation_degree = Column(Float, nullable=True)  # Average Overestimation Degree
    average_underestimation_degree = Column(Float, nullable=True)  # Average Underestimation Degree

    correction_factor = Column(Float, nullable=True)  # Running Correction Factor (if applicable)
    avg_correction_error = Column(Float, nullable=True)  # Average Correction Error
    avg_last_n_corrections = Column(Float, nullable=True)  # Average of Last N Corrections

    mae = Column(Float, nullable=True)  # Mean Absolute Error (MAE)
    rmse_metric = Column(Float, nullable=True)  # Root Mean Squared Error (RMSE)
    mape = Column(Float, nullable=True)  # Mean Absolute Percentage Error (MAPE)
    prediction_stability = Column(Float, nullable=True)  # Prediction Stability (e.g., standard deviation)
    complexity_penalty = Column(Float, nullable=True)  # Complexity Penalty (if applicable)
    timestamp = Column(String(255), nullable=False, default=the_time_in_iso_now_is())

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
