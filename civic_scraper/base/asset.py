import csv
import datetime
import mimetypes
import os
from pathlib import Path

import requests


class Asset:
    """
    Args:
        url (str): URL to download an asset.
        asset_name (str): Title of an asset. Ex:  City Council Regular Meeting
        committee_name (str): Name of committee that generated the asset. Ex: City Council
        place (str): Name of place associated with the asset.
            Lowercase with spaces and punctuation removed. Ex: menlopark
        state_or_province (str):  Two-letter abbreviation for state or province
            associated with an asset. Ex: ca
        asset_type (str): One of SUPPORTED_ASSET_TYPES. Ex: agenda
        meeting_date (datetime.datetime): Date of meeting or None if no date given
        meeting_time (datetime.time): Time of meeting or None
        meeting_id (str): Unique meeting ID. For example, cominbation of scraper type,
            subdomain and numeric ID or date. Ex: civicplus-nc-nashcounty-05052020-382
        scraped_by (str): civic_scraper.__version__
        content_type (str): File type of the asset as given by HTTP headers. Ex: 'application/pdf'
        content_length (str): Asset size in bytes

    Public methods:
        download: downloads an asset to a given target_path
    """

    def __init__(
        self,
        url: str,
        asset_name: str = None,
        committee_name: str = None,
        place: str = None,
        state_or_province: str = None,
        asset_type: str = None,
        meeting_date: datetime.datetime = None,
        meeting_time: datetime.time = None,
        meeting_id: str = None,
        scraped_by: str = None,
        content_type: str = None,
        content_length: str = None,
    ):
        self.url = url
        self.asset_name = asset_name
        self.committee_name = committee_name
        self.place = place
        self.state_or_province = state_or_province
        self.asset_type = asset_type
        self.meeting_date = meeting_date
        self.meeting_time = meeting_time
        self.meeting_id = meeting_id
        self.scraped_by = scraped_by
        self.content_type = content_type
        self.content_length = content_length

    def __repr__(self):
        return f"Asset({self.url})"

    def download(self, target_dir, session=None):
        """
        Downloads an asset to a target directory.

        Args:
            target_dir (str): target directory name

        Returns:
            Full path to downloaded file
        """
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        file_extension = mimetypes.guess_extension(self.content_type)
        file_name = "{}_{}{}".format(
            # meeting id reflects date and numeric identifier
            self.meeting_id,
            self.asset_type,
            file_extension,
        )
        if session:
            response = session.get(self.url, allow_redirects=True)
        else:
            response = requests.get(self.url, allow_redirects=True)
        full_path = os.path.join(target_dir, file_name)
        with open(full_path, "wb") as outfile:
            outfile.write(response.content)
        return full_path


class AssetCollection(list):

    def to_os(self, target_dir):
        rows = [asset.__dict__ for asset in self]
        events = {}
        for row in rows:
            print(row)
            if row["meeting_id"] in events:
                event = events[row["meeting_id"]]
            else:
                if row['meeting_time']:
                    event_day = row['meeting_date'].strftime("%Y-%m-%d")
                    event_time = row['meeting_time'].strftime("%H:%M:%S")
                    event_date = f"{event_day} {event_time}"
                else:
                    event_date = row["meeting_date"].strftime("%Y-%m-%d")
                event = Event(
                    name=row['asset_name'], location_name=row['place'], start_date=event_date
                )

            event.add_document(row["asset_type"], row["url"], media_type=row["content_type"], on_duplicate="ignore")

            if row["committee_name"]:
                event.add_participant(
                    row["committee_name"],
                    type="committee",
                    note="host",
                )
            
            event.extras["meeting_id"] = row["meeting_id"]
            events[row["meeting_id"]] = event
                
            print(event)
            print(event.extras["meeting_id"])

        for key in events:
            event = events[key]
            fname = f"{target_dir}/{event.extras['meeting_id']}.json"
            with open(fname, "w") as outfile:
                json.dump(event.as_dict(), outfile)
        return events

    def to_csv(self, target_dir):
        """
        Write metadata about the asset list to a csv.

        Args:
            targer_dir (str):  Path to directory where metadata file should be written.

        Output: csv with metadata

        Returns:
            Path to file written.
        """
        headers = [
            "place",
            "state_or_province",
            "meeting_date",
            "meeting_time",
            "committee_name",
            "meeting_id",
            "asset_name",
            "asset_type",
            "url",
            "scraped_by",
            "content_type",
            "content_length",
        ]
        tstamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M")
        file_name = f"civic_scraper_assets_meta_{tstamp}z.csv"
        path = os.path.join(target_dir, file_name)
        rows = [asset.__dict__ for asset in self]
        # Ensure output dir exists
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        # Write the file
        with open(path, "w") as out:
            writer = csv.DictWriter(out, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        return path
