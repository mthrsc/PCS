from io import BytesIO
import pytest
from imageLogic.card_handling import Card_handling
from imageLogic.image_modification import Image_modification
from web_scraping.scraper import Scraper
import json
import tkinter as tk


def test_get_card_name(reader, mock_rs):
    assert reader.get_card_name(mock_rs) == "Darkrai"


def test_get_card_code(reader, mock_rs):
    assert reader.get_card_code(mock_rs) == "167/264"


def test_reach_1024(imod):

        page2 = MockPage2()
        file_path = "./test_data/test_image.jpg"

        # Run method with mock data
        result_image = imod.reach_1024(file_path, page2)

        # Test the image size
        buffer = BytesIO()
        result_image.save(buffer, 'jpeg')
        image_size_kb = buffer.tell() / 1024

        assert image_size_kb < 1024


def test_pre_query_website():
    page2 = MockPage2()
    scraper = Scraper(page2)
    scraper.pre_query_website()
    result = page2.table[0][3].get("1.0", "end").strip()
    assert "Darkrai" in result
    assert "167" in result


# Use a fixture to load mock data
@pytest.fixture
def mock_rs():
    with open('./test_data/test.json') as file:
        return json.load(file)


# Use a fixture to create the reader object
@pytest.fixture
def reader():
    return Card_handling("")


@pytest.fixture
def imod():
    return Image_modification()


# Create a mini mock for page2 that has only variables needed for testing
class MockPage2:
    def __init__(self):
        self.break_thread = False
        self.status = "pricing"

        # Creating a mock table
        entry_name = tk.Entry()
        entry_name.insert(0, "Darkrai")

        entry_code = tk.Entry()
        entry_code.insert(0, "167/264")

        self.table = [[tk.Label(), entry_name, entry_code, tk.Text(state="disabled")]]

