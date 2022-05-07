`python3 -m pytest tests/test_lowe/test_acs/test_acsclient.py`

This was developed using the conda environment

## Description of Test

- Check 3 tables with 1 and 5 years (6 tables)
- For each table check 3 different values
- Total of 3 tables * 2 estimate years * 3 different entries

Common Tables Used in Lowe
- S0801
- S2801 √
- S1901 √ √
- S1501 √
- DP05 √

Compare client pull with manual check eg. at https://data.census.gov/cedsci/table?q=coachella,%20ca%20S1501 

# Dev Notes and Questions
- The only of the city we look at that has 1 year estimate is indio, ca
- Use BetterComments (extension on VS Code) to help find the chunks of code

to find table that has 1 year est.

```
client = ACSClient()
await client.initialize()

for city in ['cathedral city, ca', 'coachella, ca', 'desert hot springs, ca', 'indian wells, ca', 'indio, ca', 'la quinta, ca', 'palm desert, ca', 'palm springs, ca', 'rancho mirage, ca']:
    for table in ["S0801", "S2801", "S1901", "S1501", "DP05"]:
        fip_code2 = search(city, codetype="city", search_on="name").iloc[0][1]

        locs = [{'city': fip_code2}]
        try:
            resp = await client.get_acs(vars = [table],
                                start_year='2019',
                                end_year='2019',
                                location=locs,
                                estimate="1")
            print(city, table)
        except:
            print("Failed")
        
```