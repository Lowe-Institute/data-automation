# Code written by Aaron Xie, modified for script format by Abhi Uppal

import asyncio
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from lowe.locations.lookup import name2fips
from lowe.acs.ACSClient import ACSClient

# Primary and secondary colors
pri_color = "#961a30"
sec_color = "#e7c8ae"


# ------------------------------
# Plot Generation
# ------------------------------

# Fig 8: Total Household Income -- APPROVED


async def total_household_income(
    client: ACSClient,
    cities: list = [
        "cathedral city, ca",
        "coachella, ca",
        "desert hot springs, ca",
        "indian wells, ca",
        "indio, ca",
        "la quinta, ca",
        "palm desert, ca",
        "palm springs, ca",
        "rancho mirage, ca",
    ],
    year: str = "2019",
    save: bool = False,
    save_path: str = None,
):
    """
    Parameters
    ----------
    client: intialized ACS Client from lowe.acs.ACSClient
    city: name of the city eg.
    target
    year: str
        Year to get the data for
    save: bool
    True or False, whether or not you want to save
    save_path: str
    Path to save the file to
    """
    #     target_col = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Households Total"
    #     new_col_name = "Total Income"

    #     INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Total * INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Mean income (dollars)

    cols = {
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Total": "Families Total",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Mean income (dollars)": "Income Per",
    }

    loc_dicts = [{"city": city} for city in cities]
    loc_fips = [*map(name2fips, loc_dicts)]

    resp = await client.get_acs(
        vars=["S1901"], start_year=year, end_year=year, estimate="5", location=loc_fips
    )

    col_sub = [*list(cols.keys()), "state", "city"]
    resp = resp[col_sub]
    resp = resp.rename(columns=cols)

    resp["Total Income"] = resp["Families Total"].astype(str).astype(int) * resp[
        "Income Per"
    ].astype(str).astype(int)

    # Following is unique to each section

    categ = resp["city"]
    value = resp["Total Income"]

    plot_df = pd.DataFrame({"city": categ, "Value": value})
    plot_df.city = plot_df.city.str.title()  # Capitalize first letter in each city

    fig = px.bar(
        plot_df,
        x="city",
        y="Value",
        text=plot_df["Value"].apply(lambda x: "{0:,.0f}".format(x)),
    )
    fig.update_xaxes(type="category")

    fig.update_layout(
        font_family="Glacial Indifference",
        font_color="black",
        title_font_family="Glacial Indifference",
        title_font_color="black",
        legend_title_font_color="black",
        template="simple_white",
        xaxis_title="City",
        yaxis_title="Total Household Income",
    )

    fig.update_traces(marker_color=pri_color)

    if save:
        fig.write_image(save_path, format="png")
    return fig


# Fig 9: Median Household Income -- APPROVED


async def median_household_income(
    client: ACSClient,
    cities: list = [
        "cathedral city, ca",
        "coachella, ca",
        "desert hot springs, ca",
        "indian wells, ca",
        "indio, ca",
        "la quinta, ca",
        "palm desert, ca",
        "palm springs, ca",
        "rancho mirage, ca",
    ],
    year: str = "2019",
    save: bool = False,
    save_path: str = None,
):
    """
    DO NOT PASS CITIES PARAM (is a list of them); if one city just pass as list of 1
    Parameters
    ----------
    client: intialized ACS Client from lowe.acs.ACSClient
    city: name of the city eg.
    target
    year: str
        Year to get the data for
    save: bool
    True or False, whether or not you want to save
    save_path: str
    Path to save the file to
    """
    target_col = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Median income (dollars)"
    new_col_name = "Median Income"

    loc_dicts = [{"city": city} for city in cities]
    loc_fips = [*map(name2fips, loc_dicts)]

    resp = await client.get_acs(
        vars=["S1901"], start_year=year, end_year=year, estimate="5", location=loc_fips
    )

    col_sub = [target_col, "state", "city"]
    resp = resp[col_sub]
    resp = resp.rename(columns={target_col: new_col_name})

    # Following is unique to each section

    categ = resp["city"]
    value = resp["Median Income"].astype(str).astype(int)

    plot_df = pd.DataFrame({"Type": categ, "Value": value})
    plot_df.Type = plot_df.Type.str.title()  # Capitalize first letter in each city

    fig = px.bar(
        plot_df,
        x="Type",
        y="Value",
        text=plot_df["Value"].apply(lambda x: "{0:,.0f}".format(x)),
    )
    fig.update_xaxes(type="category")

    fig.update_layout(
        font_family="Glacial Indifference",
        font_color="black",
        title_font_family="Glacial Indifference",
        title_font_color="black",
        legend_title_font_color="black",
        template="simple_white",
        xaxis_title="City",
        yaxis_title="Median Household Income",
    )

    fig.update_traces(marker_color=pri_color)

    if save:
        fig.write_image(save_path, format="png")
    return fig


# Fig 10: Household Income By Class -- APPROVED


async def household_income_by_class(
    client: ACSClient,
    cities: list = ["coachella, ca", "desert hot springs, ca"],
    save: bool = False,
    save_path: str = None,
    year: str = "2019",
):
    """
    DO NOT PASS CITIES PARAM (is a list of them); if one city just pass as list of 1
    Parameters
    ----------
    client: intialized ACS Client from lowe.acs.ACSClient
    city: name of the city eg.
    target
    year: str
        Year to get the data for
    save: bool
    True or False, whether or not you want to save
    save_path: str
    Path to save the file to
    """
    # NOTE: &#36; is a $ -- needed in any label with 2 dollar signs. Without this, plotly tries to render it as LaTeX (math)
    cols = {
        # old col name: new name
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total Less than $10,000": "Less than $10,000",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $10,000 to $14,999": "&#36;10,000-&#36;14,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $15,000 to $24,999": "&#36;15,000-&#36;24,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $25,000 to $34,999": "&#36;25,000-&#36;34,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $35,000 to $49,999": "&#36;35,000-&#36;49,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $50,000 to $74,999": "&#36;50,000-&#36;74,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $75,000 to $99,999": "&#36;75,000-&#36;99,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $100,000 to $149,999": "&#36;100,000-&#36;149,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $150,000 to $199,999": "&#36;150,000-&#36;199,999",
        "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $200,000 or more": "$200,000+",
    }

    loc_dicts = [{"city": city} for city in cities]
    loc_fips = [*map(name2fips, loc_dicts)]

    resp = await client.get_acs(
        vars=["S1901"], start_year=year, end_year=year, estimate="5", location=loc_fips
    )

    col_sub = [*list(cols.keys()), "state", "city"]
    resp = resp[col_sub]
    resp = resp.rename(columns=cols)

    # Following is unique to each section

    categ = resp.columns[0:10].astype(str)
    bar_value = resp.iloc[1][0:10].astype(str).astype(float)
    line_value = resp.iloc[0][0:10].astype(str).astype(float)

    bar_df = pd.DataFrame({"Type": categ, "Percentage": bar_value})
    line_df = pd.DataFrame({"Type": categ, "Percentage": line_value})

    fig = px.line(
        line_df,
        x="Type",
        y="Percentage",
        color=px.Constant("Coachella Valley"),
        color_discrete_sequence=[sec_color],
    )
    fig.add_bar(
        x=bar_df["Type"],
        y=bar_df["Percentage"],
        name="Desert Hot Spring",
        text=bar_df["Percentage"].apply(lambda x: "{0:,.1f}%".format(x)),
    )

    fig.update_layout(
        font_family="Glacial Indifference",
        font_color="black",
        title_font_family="Glacial Indifference",
        title_font_color="black",
        legend_title_font_color="black",
        legend_title_text="Region",
        template="simple_white",
        xaxis_title="City",
        yaxis_title="Percent of Households",
    )

    fig.update_traces(marker_color=pri_color)

    if save:
        fig.write_image(save_path, format="png")
    return fig


# Table 1: Residence and Work Location -- WIP


async def residence_and_work_loc(
    client: ACSClient,
    cities: list = ["desert hot springs, ca"],
    year: str = "2019",
    save: bool = False,
    save_path: str = None,
):
    """
    Parameters
    ----------
    client: intialized ACS Client from lowe.acs.ACSClient
    city: name of the city eg.
    target
    year: str
        Year to get the data for
    save: bool
    True or False, whether or not you want to save
    save_path: str
    Path to save the file to
    """
    cols = {
        # old col name: new name
        "COMMUTING CHARACTERISTICS BY SEX Estimate Total PERCENT ALLOCATED Place of work": "% Allocated Place of Work",
        "COMMUTING CHARACTERISTICS BY SEX Estimate Total Workers 16 years and over PLACE OF WORK Not living in 12 selected states": "Count, live outside state",
        "COMMUTING CHARACTERISTICS BY SEX Estimate Total Workers 16 years and over PLACE OF WORK Worked in state of residence Worked outside county of residence": "Count, outside of county",
        "COMMUTING CHARACTERISTICS BY SEX Estimate Total Workers 16 years and over PLACE OF WORK Worked in state of residence Worked in county of residence": "Count, inside county",
    }

    loc_dicts = [{"city": city} for city in cities]
    loc_fips = [*map(name2fips, loc_dicts)]

    resp = await client.get_acs(
        vars=["S0801"], start_year=year, end_year=year, estimate="5", location=loc_fips
    )

    col_sub = [*list(cols.keys()), "state", "city"]
    resp = resp[col_sub]
    resp = resp.rename(columns=cols)

    ans = [
        ["Living/Working", resp.iloc[0]["city"]],
        [resp.columns[1], resp.iloc[0][1]],
        [resp.columns[2], resp.iloc[0][2]],
        [resp.columns[3], resp.iloc[0][3]],
    ]
    fig = ff.create_table(
        ans, colorscale=[[0, pri_color], [0.5, "#ffffff"], [1, "#ffffff"]]
    )

    return fig


# ------------------------------
# Testing Code
# ------------------------------


async def main():
    client = ACSClient()
    await client.initialize()
    try:
        test = await residence_and_work_loc(client=client)
    finally:
        await client.close()
    test.show()
    return test


if __name__ == "__main__":
    asyncio.run(main())