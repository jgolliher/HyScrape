import requests as rq
from bs4 import BeautifulSoup
import re
import pandas as pd
from hyscrape import to_seconds


class WebResult:
    def __init__(self, url: str):
        """Initialize a WebResult object"""
        response = rq.get(url)
        if response.status_code != 200:
            raise ValueError(f"Invalid response code {response.status_code}")
        self.content = BeautifulSoup(response.content, features="html.parser")
        self.raw_results = self.content.find("pre").text.splitlines()

    def parse_data(self):
        """Parses either Psych/Prelims/Finals"""
        # Determine round
        round = self._determine_round()
        if round == "Psych":
            print("NO CODE FOR PROCESSING PSYCH SHEET")
        elif round == "Prelims":
            return self._parse_prelims()
        elif round == "Finals":
            return self._parse_finals()
        else:
            return ValueError(f"Round was {round} which is not Psych/Prelims/Finals")

    def _determine_round(self):
        """Determines the round type (Psych, Prelims, or Finals) from a list of strings."""
        for row in self.raw_results:
            row = row.strip()
            if "Psych Sheet" in row:
                return "Psych"
            elif "Preliminaries" in row:
                return "Prelims"
            elif "Finals" in row:
                return "Finals"
        return None

    def _parse_prelims(self):
        """Parses prelims and return a Pandas DataFrame"""
        round_type = "Prelims"
        swimmer_data = []
        for row in self.raw_results:
            match = re.search(pattern=r"^\s*\d{1,3}\s.*", string=row)
            if match:
                place = row[0:4].strip()  # Place
                name = row[4:21].strip()  # Name
                year = row[21:24].strip()  # School year
                team = row[24:38].strip()  # School
                time1 = row[40:50].strip()  # Time 1
                time2 = row[50:61].strip()  # Time
                swimmer_data.append([place, name, year, team, time1, time2])

        df = pd.DataFrame(
            swimmer_data,
            columns=["Place", "Name", "Year", "Team", "Psych", "Prelims"],
        )

        df.loc[df["Psych"] == "NT", "Psych"] = "0"
        df.loc[df["Prelims"] == "NT", "Prelims"] = "0"

        df["Prelims"] = df["Prelims"].str.replace("J", "")
        df["Prelims"] = df["Prelims"].str.replace("M", "")
        df["Prelims"] = df["Prelims"].str.replace("P", "")

        df["PsychSS"] = df["Psych"].apply(to_seconds)
        df["PrelimsSS"] = df["Prelims"].apply(to_seconds)
        return df

    def _parse_finals(self):
        """Parse finals and return a Pandas DataFrame"""
        round_type = "Finals"
        swimmer_data = []
        for row in self.raw_results:
            match = re.search(pattern=r"^\s*\d{1,3}\s.*", string=row)
            if match:
                place = row[0:4].strip()  # Place
                name = row[4:21].strip()  # Name
                year = row[21:24].strip()  # School year
                team = row[24:38].strip()  # School
                time1 = row[40:50].strip()  # Time 1
                time2 = row[50:60].strip()  # Time
                points = row[68:72].strip()
                swimmer_data.append([place, name, year, team, time1, time2, points])

        test = pd.DataFrame(
            swimmer_data,
            columns=[
                "Place",
                "Name",
                "Year",
                "Team",
                "Prelims",
                "Finals",
                "Points",
            ],
        )

        test.loc[test["Prelims"] == "NT", "Prelims"] = "0"
        test.loc[test["Finals"] == "NT", "Finals"] = "0"

        test["Prelims"] = test["Prelims"].str.replace("J", "")
        test["Prelims"] = test["Prelims"].str.replace("M", "")
        test["Prelims"] = test["Prelims"].str.replace("P", "")
        test["Prelims"] = test["Prelims"].str.replace("S", "")

        test["Finals"] = test["Finals"].str.replace("M", "")
        test["Finals"] = test["Finals"].str.replace("S", "")
        test["Finals"] = test["Finals"].str.replace("P", "")

        test["PrelimsSS"] = test["Prelims"].apply(to_seconds)
        test["FinalsSS"] = test["Finals"].apply(to_seconds)
        return test
