from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def count_nulls_neg_ones(df: DataFrame) -> DataFrame:
    """
    Count nulls and -1s in each column of a PySpark DataFrame.

    Parameters:
    df (DataFrame): Input PySpark DataFrame.

    Returns:
    DataFrame: A DataFrame with column names, count of nulls, and count of -1s.
    """
    column_stats = []
    
    for col in df.columns:
        null_count = df.filter(df[col].isNull()).count()
        neg_one_count = df.filter(df[col] == -1).count()
        column_stats.append((col, null_count, neg_one_count))
    
    return df.sparkSession.createDataFrame(column_stats, ["Column", "Null Count", "Negative One Count"])
