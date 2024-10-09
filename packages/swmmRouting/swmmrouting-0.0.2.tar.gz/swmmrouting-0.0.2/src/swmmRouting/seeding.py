import numpy as np
import pandas as pd
import random
import logging

logger = logging.getLogger("seeder")


class Seeder:
    def __init__(self, df_seeding_population, hourly_probability):
        self.seed_population = None
        self.seed_pattern = None

        self.set_seed_population(df_seeding_population)
        self.set_seed_pattern(hourly_probability)
        return

    def set_seed_population(self, df_seeding_population):
        """
        Takes a DataFrame with a column "node" and a column "pop" for the information
        which nodes have what seeding population.
        Args:
            df_seeding_population (pd.DataFrame): DataFrame with seeding population.

        Returns:

        """
        self.seed_population = df_seeding_population
        logger.info(f"Seed population set")
        return

    def set_seed_pattern(self, hourly_probability):
        """
        Takes an array with 24 values with the probability of a seed occuring each hour.
        Sum equates to average seeds/day.
        Args:
            hourly_probability (np.array): Array of hourly probabilities.

        Returns:

        """
        self.seed_pattern = hourly_probability
        logger.info(f"Seed pattern set to {hourly_probability}")
        return

    def generate_seeds(self, start, end):
        """
        Creates an initial routing table with nodes for columns and each seed is a row with the origin time for the
        origin node. The rest is NaN.
        Args:
            start (pd.Timestamp): Starting timestamp.
            end (pd.Timestamp): Ending timestamp.

        Returns:
            pd.DataFrame: Routing Table with initial seeds.
        """
        # hours during which to create seeds
        hours = pd.date_range(start, end, freq='H')
        # weights for each hour
        hour_weights = [self.seed_pattern[hour.hour] for hour in hours]
        # create list of seeds from the nodes
        seeds = random.choices(self.seed_population["node"], weights=self.seed_population["pop"],
                               k=np.around(self.seed_population["pop"].sum() * sum(hour_weights)).astype(int))
        # choose an origin hour for each seed
        seed_hours = [random.choices(hours, hour_weights)[0] for _ in seeds]
        # choose a random time within the hour for each seed
        seed_times = [seed_hour + pd.to_timedelta(random.randint(0, 3599), unit='s') for seed_hour in seed_hours]
        seeds = pd.DataFrame.from_dict({"nodes": seeds,
                                        "times": seed_times}).pivot(columns='nodes').droplevel(0, axis=1)
        logger.info(f"{len(seeds)} seeds created for {len(seeds.columns)} nodes "
                    f"between {start:'%Y-%m-%d %H:%M'} and {end}:'%Y-%m-%d %H:%M'")
        return seeds


if __name__ == "__main__":
    # main()
    pass
