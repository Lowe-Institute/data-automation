import pytest
from lowe.acs.ACSClient import ACSClient
from lowe.locations.lookup import search


@pytest.mark.asyncio
class TestSearch_and_Get:
    """
    tests:
    - ACSClient Initialization
    - client.get_acs()

    needs working:
    - lowe.locations.lookup search()
    """

    async def test_add(self):
        assert 1 + 1 == 2

    # ! S2801 + 5 year
    async def test_5year_s2801_1(self):
        # Initialize client
        client = ACSClient()
        await client.initialize()

        # Find City Code
        fip_code = search("cathedral city, ca", codetype="city", search_on="name").iloc[
            0
        ][1]

        # fip_code2 = search('coachella, ca', codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        # Get whole table
        resp = await client.get_acs(
            vars=["S2801"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )

        # Get specific data
        col_name = "TYPES OF COMPUTERS AND INTERNET SUBSCRIPTIONS Estimate Percent Total households TYPE OF INTERNET SUBSCRIPTIONS With an Internet subscription: Broadband of any type"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        # Get data matches with hand-pulled from table
        assert value == 82.2

    async def test_5year_s2801_2(self):
        client = ACSClient()
        await client.initialize()
        fip_code = search("cathedral city, ca", codetype="city", search_on="name").iloc[
            0
        ][1]

        # fip_code2 = search('coachella, ca', codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S2801"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )
        col_name = "TYPES OF COMPUTERS AND INTERNET SUBSCRIPTIONS Estimate Percent Total households TYPES OF COMPUTER Has one or more types of computing devices: Desktop or laptop"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 75.3

    async def test_5year_s2801_3(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code2 = search("coachella, ca", codetype="city", search_on="name").iloc[0][
            1
        ]

        locs = [{"city": fip_code2}]

        resp = await client.get_acs(
            vars=["S2801"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )
        col_name = "TYPES OF COMPUTERS AND INTERNET SUBSCRIPTIONS Estimate Total Total households TYPE OF INTERNET SUBSCRIPTIONS With an Internet subscription: Broadband of any type"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 11273

    async def test_5year_s2801_4(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code2 = search("coachella, ca", codetype="city", search_on="name").iloc[0][
            1
        ]

        locs = [{"city": fip_code2}]

        resp = await client.get_acs(
            vars=["S2801"],
            start_year="2017",
            end_year="2017",
            location=locs,
            estimate="5",
        )
        col_name = "TYPES OF COMPUTERS AND INTERNET SUBSCRIPTIONS Estimate Total Total households TYPE OF INTERNET SUBSCRIPTIONS With an Internet subscription: Broadband of any type"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 8138

    # ! DP05 + 5 year
    async def test_5year_DP05_1(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code2 = search("coachella, ca", codetype="city", search_on="name").iloc[0][
            1
        ]

        locs = [{"city": fip_code2}]

        resp = await client.get_acs(
            vars=["DP05"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )

        col_name = "ACS DEMOGRAPHIC AND HOUSING ESTIMATES Percent SEX AND AGE Total population Under 5 years"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 5.7

    async def test_5year_DP05_2(self):
        client = ACSClient()
        await client.initialize()
        fip_code = search("cathedral city, ca", codetype="city", search_on="name").iloc[
            0
        ][1]

        # fip_code2 = search('coachella, ca', codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["DP05"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )

        col_name = "ACS DEMOGRAPHIC AND HOUSING ESTIMATES Estimate HISPANIC OR LATINO AND RACE Total population Hispanic or Latino (of any race) Puerto Rican"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 125

    async def test_5year_DP05_3(self):
        client = ACSClient()
        await client.initialize()
        fip_code = search("cathedral city, ca", codetype="city", search_on="name").iloc[
            0
        ][1]

        # fip_code2 = search('coachella, ca', codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["DP05"],
            start_year="2017",
            end_year="2017",
            location=locs,
            estimate="5",
        )

        col_name = "ACS DEMOGRAPHIC AND HOUSING ESTIMATES Estimate CITIZEN, VOTING AGE POPULATION Citizen, 18 and over population Female"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 15033

    # S1901
    async def test_5year_S1901_1(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code2 = search("coachella, ca", codetype="city", search_on="name").iloc[0][
            1
        ]

        locs = [{"city": fip_code2}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2020",
            end_year="2020",
            location=locs,
            estimate="5",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families Total $75,000 to $99,999"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 15.6

    async def test_5year_S1901_2(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code2 = search("coachella, ca", codetype="city", search_on="name").iloc[0][
            1
        ]

        locs = [{"city": fip_code2}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2020",
            end_year="2020",
            location=locs,
            estimate="5",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households PERCENT ALLOCATED Nonfamily income in the past 12 months"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 55.4

    async def test_5year_S1901_3(self):
        client = ACSClient()
        await client.initialize()
        # fip_code = search('cathedral city, ca', codetype="city", search_on="name").iloc[0][1]

        # fip_code2 = search('coachella, ca', codetype="city", search_on="name").iloc[0][1]

        fip_code3 = search(
            "desert hot springs, ca", codetype="city", search_on="name"
        ).iloc[0][1]

        locs = [{"city": fip_code3}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="5",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $100,000 to $149,999"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 3.5

    # 1 Year - S1901
    async def test_1year_S1901_1(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Nonfamily households Total $10,000 to $14,999"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 7.2

    async def test_1year_S1901_2(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Families PERCENT ALLOCATED Family income in the past 12 months"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 41.2

    async def test_1year_S1901_3(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1901"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) Estimate Households Total $150,000 to $199,999"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 11.4

    # 1 Year - S1501
    async def test_1year_S1501_1(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1501"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "EDUCATIONAL ATTAINMENT Estimate Percent Male POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL Less than high school graduate"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 10.4

    async def test_1year_S1501_2(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1501"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "EDUCATIONAL ATTAINMENT Estimate Percent RACE AND HISPANIC OR LATINO ORIGIN BY EDUCATIONAL ATTAINMENT Hispanic or Latino Origin High school graduate or higher"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 72.7

    async def test_1year_S1501_3(self):
        client = ACSClient()
        await client.initialize()

        fip_code = search("indio, ca", codetype="city", search_on="name").iloc[0][1]

        locs = [{"city": fip_code}]

        resp = await client.get_acs(
            vars=["S1501"],
            start_year="2019",
            end_year="2019",
            location=locs,
            estimate="1",
        )

        col_name = "EDUCATIONAL ATTAINMENT Estimate Male AGE BY EDUCATIONAL ATTAINMENT Population 25 years and over Associate's degree"
        col_sub = [col_name, "state", "city"]
        if len(resp[col_sub]) != 1:
            assert False

        value = float(resp[col_sub][col_name].iloc[0])

        assert value == 1879
