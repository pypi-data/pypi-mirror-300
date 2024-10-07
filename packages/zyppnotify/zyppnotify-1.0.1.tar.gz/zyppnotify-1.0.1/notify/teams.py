import logging

import pandas as pd
import requests
from notify.types import DfsInfo
from pympler import asizeof


class NotifyTeams:
    def __init__(self, webhook: str):
        """

        Parameters
        ----------
        webhook: str
            url for sending the teams message
        """

        self.webhook = webhook
        self.msg = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "msteams": {"width": "Full"},
                        "version": "1.4",
                    },
                }
            ],
        }
        self.body = []

    @staticmethod
    def create_adaptive_card_dataframe(df: pd.DataFrame) -> dict:
        """
        Function to create a full dataframe used in adaptive cards in an adaptive card.
        """
        if df.shape[0] > 30:
            logging.warning(f"only first 30 records will be added.({df.shape[0]}> the limit of 30).")
            df = df.head(n=30)
        if df.shape[1] > 10:
            logging.warning("Only the first 10 columns will be shown")
            df = df.iloc[:, :10].copy()

        df_dict = df.to_dict("records")
        col_widths = []
        header_cells = []
        for col in df.columns:
            width = {"width": "auto"}
            col_widths.append(width)
            header_cell = {
                "type": "TableCell",
                "items": [
                    {
                        "type": "TextBlock",
                        "style": "emphasis",
                        "text": col,
                        "wrap": True,
                        "weight": "bolder",
                    }
                ],
            }
            header_cells.append(header_cell)
        header_row = {"type": "TableRow", "cells": header_cells}
        rows = [header_row]
        for row in df_dict:
            cells = []
            for key, value in row.items():
                cell = {
                    "type": "TableCell",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": value,
                            "wrap": True,
                        }
                    ],
                }
                cells.append(cell)
            row = {"type": "TableRow", "cells": cells}
            rows.append(row)
        table = {"type": "Table", "columns": col_widths, "rows": rows, "showGridLines": True}
        return table

    def add_full_dataframe(self, df: pd.DataFrame) -> None:
        """
        Function to add a full dataframe to the adaptive card.
        Parameters
        ----------
        df: pd.DataFrame
            Dataframe that will be added to the card.
        """
        table = self.create_adaptive_card_dataframe(df)
        self.body.append(table)

    def create_dataframe_report(self, dfs: DfsInfo) -> None:
        """
        Function to create a report of the dataframes that are processed.
        Parameters
        ----------
        dfs: dict
            Dataframes containing {name, df} as key value pairs
        """
        for df_name, df_shape in dfs.items():
            df_report = {
                "type": "Container",
                "style": "accent",
                "separator": True,
                "items": [
                    {
                        "type": "TextBlock",
                        "weight": "Bolder",
                        "text": f"{df_name}",
                        "wrap": "true",
                        "style": "heading",
                        "size": "Medium",
                    },
                    {
                        "type": "RichTextBlock",
                        "spacing": "Small",
                        "inlines": [
                            "In totaal ",
                            {"type": "TextRun", "text": f"{df_shape[0]}", "weight": "bolder"},
                            " records met ",
                            {"type": "TextRun", "text": f"{df_shape[1]}", "weight": "bolder"},
                            " kolommen verwerkt",
                        ],
                        "wrap": "true",
                        "size": "Small",
                    },
                ],
            }
            self.body.append(df_report)

    def create_buttons(self, buttons: dict) -> None:
        """

        Parameters
        ----------
        buttons: dict
            dictionairy containing button_name, button_link as key, value pairs.

        Returns
        -------
        None
            Adds the button(s) to the teams message

        """
        button_list = []
        for button_name, button_link in buttons.items():
            button = {"type": "Action.OpenUrl", "title": button_name, "url": button_link}
            button_list.append(button)
        self.msg["attachments"][0]["content"]["actions"] = button_list

    def create_message_header(self, title: str, subtitle: str = None):
        """
        Function to create the header of the Teams message containing the title, subtitle (optional) and Python-logo
        Parameters
        ----------
        title: str
            Title of the message
        subtitle: str
            Subtitle of the message (optional)
        """
        title_item = {
            "type": "TextBlock",
            "weight": "Bolder",
            "text": title,
            "wrap": "true",
            "style": "heading",
            "size": "Medium",
        }
        title_items = [title_item]
        if subtitle:
            subtitle_item = {
                "type": "TextBlock",
                "spacing": "Small",
                "text": subtitle,
                "isSubtle": "true",
                "wrap": "true",
                "size": "Small",
            }
            title_items.append(subtitle_item)

        message_header = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png",
                            "altText": "Python",
                            "style": "person",
                            "size": "small",
                            "horizontalAlignment": "Center",
                        }
                    ],
                    "width": "auto",
                    "verticalContentAlignment": "Center",
                },
                {"type": "Column", "items": title_items},
            ],
        }
        self.body.append(message_header)

    def create_simple_message(self, message: str):
        """
        Function to create a simple message block in the teams message. When <br> tags are included the enters are
        created by creating new text blocks.
        Parameters
        ----------
        message: str
            message that needs to be added to the card
        """
        if "<br>" in message:
            message_items = message.split("<br>")
            for message_item in message_items:
                message_item = {
                    "type": "TextBlock",
                    "text": message_item,
                    "wrap": "true",
                }
                self.body.append(message_item)

        else:
            message_item = {
                "type": "TextBlock",
                "text": message,
                "wrap": "true",
            }
            self.body.append(message_item)

    def create_warning_message(self, warning_message: str):
        """
        Function to create a warning message at the top of the teams message and under the heaader
        Parameters
        ----------
        warning_message: str
            warning message that will be added to the card with a warning symbol
        """
        warning = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://www.echopedia.org/images/c/cb/Warning.png",
                            "size": "medium",
                            "horizontalAlignment": "left",
                        }
                    ],
                    "width": "auto",
                },
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "size": "large",
                            "color": "attention",
                            "text": warning_message,
                            "wrap": "true",
                        }
                    ],
                    "verticalContentAlignment": "Center",
                },
            ],
        }
        self.body.append(warning)

    def add_extra_elements(self, extra: list):
        """
        Function to add extra elements to the message
        Parameters
        ----------
        extra: list
            list of dictionaries containing index and item as key values where item should be a dict containing the item to be
            added to the card.
        """
        for x in extra:
            assert set(list(x.keys())) == {"index", "item"}, "Extra should only contain position and item keys"
            assert "type" in x["item"].keys(), "Item should contain a type key"
            assert x["index"] <= len(self.body), "index should be smaller than the length of the body"
            assert x["index"] >= 0, "index should be a positive integer"
            if x["index"] == len(self.body):
                self.body.append(x["item"])
            else:
                self.body.insert(x["index"], x["item"])

    def basic_message(
        self,
        title: str,
        subtitle: str = None,
        message: str = None,
        buttons: dict = None,
        warning_message: str = None,
        df: pd.DataFrame = pd.DataFrame(),
        dfs: DfsInfo = None,
        extra: list = None,
    ):
        """
        This function posts a message, containing a section, in a Microsoft Teams channel

        Parameters
        ----------
        dfs: dict
            Dataframes dictionary, with keys as dataframe name and value as dataframe.
        df: pd.DataFrame
            df that will be added to a card section. length of dataframe should not exceed 10.
        title: str
            Title of the message
        subtitle: str
            Subtitle of the message (optional)
        message: str
            Content of the message (optional)
        buttons: dict
            dictionary of button_name, button_url as key value pairs
        warning_message: str
            warning message that will be added to the card
        extra: list
            dictionary containing index and item as key values where item should be a dict containing the item to be
            added to the card.
        Returns
        -------
        response
            sends a message in a teams channel, reporting col en records as information.
        """
        self.create_message_header(title, subtitle)

        if warning_message:
            self.create_warning_message(warning_message)

        if message:
            self.create_simple_message(message)

        if dfs:
            self.create_dataframe_report(dfs)

        if not df.empty:
            self.add_full_dataframe(df)

        if buttons:
            self.create_buttons(buttons)

        if extra:
            self.add_extra_elements(extra)
        self.msg["attachments"][0]["content"]["body"] = self.body
        body_size = asizeof.asizeof(self.body)
        if body_size > 40_000:
            raise ValueError(f"Body size is {body_size} bytes. This is will result in a Teams message above 28KB.")
        try:
            response = requests.post(url=self.webhook, json=self.msg)
            return response
        except Exception as e:
            logging.warning(f"Teams notification not sent! Error: {e}")
