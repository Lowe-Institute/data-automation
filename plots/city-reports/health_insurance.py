# Code written by Aaron Onate, slight modifications for production made by Abhi Uppal

import asyncio
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from lowe.acs.ACSClient import ACSClient
from lowe.locations.lookup import name2fips

# Primary, secondary, and tertiary colors
pri_color = "#961a30"
sec_color = "#e7c8ae"
ter_color = "#e6aeb7"


# ------------------------------
# Plot Generation
# ------------------------------

# Fig 27: Health Insurance -- APPROVED
async def health_insurance(
    client: ACSClient,
    city: str = "indian wells, ca",
    year: str = "2019",
    save: bool = False,
    save_path: str = None,
):
    """
    Parameters
    ----------
    city: name of the city as a list eg. ['cathedral city, ca'] or ['coachella, ca'] etc.
    save: bool
    True or False, whether or not you want to save
    save_path: str
    Path to save the file to
    """

    # Pull data for city
    loc = name2fips({"city": city})
    resp = await client.get_acs(
        vars=["S2701"], start_year="2015", end_year=year, estimate="5", location=loc
    )

    # pull data for united states
    resp1 = await client.get_acs(
        vars=["S2701"],
        start_year="2015",
        end_year=year,
        location={},  # united states
        estimate="5",
    )

    # pull data for california
    resp2 = await client.get_acs(
        vars=["S2701"],
        start_year="2015",
        end_year=year,
        location={"state": "06"},  # california
        estimate="5",
    )

    target_cols = [
        "SELECTED CHARACTERISTICS OF HEALTH INSURANCE COVERAGE IN THE UNITED STATES Estimate Percent Insured Civilian noninstitutionalized population",
        "location_key",
    ]

    cityname = (
        city.title()[:-1] + city[-1].upper()
    )  # Ensures the state is fully capitalized

    renamed_colCalifornia = {target_cols[0]: "California"}
    renamed_colCity = {target_cols[0]: cityname}
    renamed_colUS = {target_cols[0]: "United States"}

    # format city dataframe
    df_resp = resp[target_cols]
    df_resp = df_resp.apply(pd.to_numeric, errors="ignore")
    df_resp = df_resp.rename(columns=renamed_colCity)

    # format us dataframe
    df_resp1 = resp1[target_cols]
    df_resp1 = df_resp1.apply(pd.to_numeric, errors="ignore")
    df_resp1 = df_resp1.rename(columns=renamed_colUS)

    # format california dataframe
    df_resp2 = resp2[target_cols]
    df_resp2 = df_resp2.apply(pd.to_numeric, errors="ignore")
    df_resp2 = df_resp2.rename(columns=renamed_colCalifornia)

    # combine all three dataframes

    df_final = pd.concat([df_resp[cityname], df_resp1["United States"]], axis=1)
    df_final = pd.concat([df_final, df_resp2["California"]], axis=1)

    # plot data
    fig = px.line()

    fig.add_trace(
        go.Scatter(
            x=df_final.index,
            y=df_final[cityname] / 100,
            name=cityname,
            line=dict(color="#961a30"),
            text=df_final[cityname].apply(lambda x: "{0:1.1f}%".format(x)),
            mode="lines+markers+text",
            textposition="top center",
            legendrank=3,
            textfont=dict(family="Glacial Indifference", size=14, color=pri_color),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_final.index,
            y=df_final["California"] / 100,
            name="California",
            line=dict(color="#cc690f"),
            # text= df_final['California'].apply(lambda x: '{0:1.1f}%'.format(x)),
            # mode="lines+markers+text",
            # textposition = 'top center',
            legendrank=2,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_final.index,
            y=df_final["United States"] / 100,
            name="United States",
            line=dict(color=ter_color),
            # text= df_final['United States'].apply(lambda x: '{0:1.1f}%'.format(x)),
            # textposition = 'bottom center',
            # mode="lines+markers+text",
            legendrank=1,
        )
    )

    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")

    fig.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5
        ),
        template="plotly_white",
        font=dict(family="Glacial Indifference", size=14, color="Black"),
        yaxis=dict(tickformat=".0%", hoverformat="closest"),
        yaxis_title="Percentage of Population with Health Insurance",
    )

    if save:
        fig.write_image(save_path)
    return fig


# ------------------------------
# Testing Code
# ------------------------------


async def main():
    client = ACSClient()
    await client.initialize()
    try:
        test = await health_insurance(client=client)
    finally:
        await client.close()
    test.show()
    return test


if __name__ == "__main__":
    asyncio.run(main())