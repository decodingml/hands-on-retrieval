from typing import Optional

import pandas as pd


def parse_stars(stars: str) -> Optional[float]:
    """Parse the stars rating from a string to a float value between 0 and 5.

    Args:
        stars: String containing the star rating (e.g., "4.2 out of 5 stars", "4,2 de 5 estrellas")

    Returns:
        Float value between 0 and 5, or None if parsing fails
    """

    if pd.isna(stars):
        return None
    stars_str = str(stars).replace(",", ".")  # Handle European number format
    try:
        return float(stars_str.split()[0])
    except (ValueError, IndexError):
        return None


def parse_ratings(ratings: str) -> Optional[int]:
    """Parse the number of ratings from a string to a float value.

    Args:
        ratings: String containing the number of ratings (e.g., "1,116 ratings", "90 valoraciones")

    Returns:
        Int value representing the number of ratings, or None if parsing fails
    """

    if pd.isna(ratings):
        return None
    try:
        # Remove commas and get first number
        ratings_str = str(ratings).split()[0].replace(",.", "")
        return int(ratings_str)
    except (ValueError, IndexError):
        return None


def parse_price(price: str) -> Optional[float]:
    """Parse the price from a string to a float value.

    Args:
        price: String containing the price (e.g., "$9.99", "25,63€")

    Returns:
        Float value representing the price, or -10 if parsing fails or price is NaN
    """
    if pd.isna(price):
        return None

    try:
        # Remove currency symbols and convert to float
        price_str = str(price).replace("$", "").replace("€", "").replace(",", ".")
        return min(float(price_str), 1000.0)
    except ValueError:
        return None


def process_product_data(df: pd.DataFrame, sample: bool = True) -> pd.DataFrame:
    """Process raw product data into a standardized format.

    This function takes a DataFrame containing raw product data and processes it to ensure
    consistent data types and formats across all fields.

    Args:
        df: Input DataFrame containing raw product data with columns:
            - asin (str): Amazon Standard Identification Number
            - type (str): Product type
            - title (str): Product title
            - description (str): Product description
            - stars (str): Star rating
            - ratings (str): Number of ratings
            - price (str): Product price

    Returns:
        Processed DataFrame with the following columns and types:
            - asin (str): Unchanged
            - type (str): Unchanged
            - title (str): Unchanged
            - description (str): Unchanged
            - review_rating (float): Value between 0 and 5
            - review_count (float): Number of ratings
            - price (float): Price value
    """

    # Create a copy to avoid modifying the original DataFrame
    df_processed = df.copy()

    # Keep only required columns
    columns_to_keep = [
        "asin",
        "type",
        "title",
        "description",
        "stars",
        "ratings",
        "price",
    ]
    df_processed = df_processed[columns_to_keep]

    # Apply transformations
    df_processed["review_rating"] = df_processed["stars"].apply(parse_stars)
    df_processed["review_count"] = df_processed["ratings"].apply(parse_ratings)
    df_processed["price"] = df_processed["price"].apply(parse_price)

    df_processed = df_processed.dropna(
        subset=["review_rating", "review_count", "price"]
    ).astype(
        {
            "asin": str,
            "type": str,
            "title": str,
            "description": str,
            "review_rating": float,
            "review_count": int,
            "price": float,
        }
    )

    if sample:
        df_processed = df_processed.head(300)

    return df_processed
