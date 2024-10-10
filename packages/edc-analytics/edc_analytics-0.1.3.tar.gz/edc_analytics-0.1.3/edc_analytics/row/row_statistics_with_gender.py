import pandas as pd
from edc_constants.constants import FEMALE, MALE

from .row_statistics import RowStatistics


class RowStatisticsError(Exception):
    pass


class RowStatisticsFemale(RowStatistics):
    def __init__(
        self,
        df_numerator: pd.DataFrame = None,
        df_denominator: pd.DataFrame = None,
        **kwargs,
    ):
        if not df_numerator.empty:
            if not df_numerator["gender"].isnull().all():
                if (
                    df_numerator[df_numerator["gender"].notna()].count()
                    != df_numerator["gender"].value_counts()[FEMALE]
                ):
                    raise RowStatisticsError(
                        f"Expected Gender as a category of [{FEMALE}, {MALE}]. "
                        f"Expected `{FEMALE}`."
                    )
        super().__init__(
            df_numerator=df_numerator,
            df_denominator=df_denominator,
            **kwargs,
        )


class RowStatisticsMale(RowStatistics):
    def __init__(
        self,
        df_numerator: pd.DataFrame = None,
        df_denominator: pd.DataFrame = None,
        **kwargs,
    ):
        if not df_numerator.empty:
            if not df_numerator["gender"].isnull().all():
                if (
                    df_numerator[df_numerator["gender"].notna()].count()
                    != df_numerator["gender"].value_counts()[MALE]
                ):
                    raise RowStatisticsError(
                        f"Expected Gender as a category of [{FEMALE}, {MALE}]. "
                        f"Expected `{MALE}`."
                    )
        super().__init__(
            df_numerator=df_numerator,
            df_denominator=df_denominator,
            **kwargs,
        )


class RowStatisticsWithGender(RowStatistics):
    def __init__(
        self,
        columns: dict[str, tuple[str, int]] = None,
        gender_values: dict[str, str] = None,
        df_all: pd.DataFrame = None,
        coltotal: float | int | None = None,
        **kwargs,
    ):
        """
        custom row for displaying with gender columns: F, M, All
        :param colname:
        :param df_numerator:
        :param df_denominator:
        :param df_all:
        :param columns: dict of {col: (style name, places)} where col
               is "F", "M" or "All"
        :param gender_values: dict of {gender_label: gender_value} where
               gender_label is "F" or "M"

        Note: the default df["gender"] is "M" or "F".
        """

        female_style, female_places = columns[FEMALE]
        male_style, male_places = columns[MALE]
        all_style, all_places = columns["All"]

        # gender_values = gender_values or {"M": "Male", "F": "Female"}
        # female_value = gender_values["F"]
        # male_value = gender_values["M"]

        super().__init__(
            places=all_places,
            style=all_style,
            df_all=df_all,
            coltotal=coltotal,
            **kwargs,
        )

        self.m = RowStatisticsMale(
            places=male_places,
            style=male_style,
            coltotal=len(df_all[df_all["gender"] == MALE]),
            df_all=df_all,
            **kwargs,
        )
        self.f = RowStatisticsFemale(
            places=female_places,
            style=female_style,
            coltotal=len(df_all[df_all["gender"] == FEMALE]),
            df_all=df_all,
            **kwargs,
        )

    def values_list(self, style: str | None = None, places: int | None = None) -> list:
        values_list = super().values_list()
        return (
            list(self.formatted_cells().values())
            + self.f.values_list()
            + self.m.values_list()
            + values_list
        )

    def labels(self) -> list[str]:
        labels = super().labels()
        return (
            list(self.formatted_cells().keys())
            + [f"f{x}" for x in self.f.labels()]
            + [f"m{x}" for x in self.m.labels()]
            + labels
        )

    def row(self):
        return [self.formatted_cells()] + self.values_list()

    def formatted_cells(self) -> dict:
        formatted_cell = super().formatted_cell()
        return dict(
            F=self.f.formatted_cell(),
            M=self.m.formatted_cell(),
            All=formatted_cell,
        )
