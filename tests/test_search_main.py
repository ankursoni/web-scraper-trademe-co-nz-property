from pandas import DataFrame
import search.main


class TestSearchMain:

    DEFAULT_HIT_DELAY_SECONDS = 0

    def mock_property_search_fetch(domain_url, city, total_pages):
        return [search.main.PropertySearch(link="testlink", city=city)]

    def mock_property_detail_fetch(link, property_search):
        return search.main.PropertyDetail()

    def test_search_without_detail(_, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestSearchMain.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.main.property_search_fetch",
            TestSearchMain.mock_property_search_fetch,
        )
        spy_property_search_fetch = mocker.spy(search.main, "property_search_fetch")
        spy_property_detail_fetch = mocker.spy(search.main, "property_detail_fetch")

        # act
        result = search.main.search_without_detail(
            domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
        )

        # assert
        spy_property_search_fetch.assert_called_once_with(
            domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
        )
        spy_property_detail_fetch.assert_not_called()
        assert result != None
        assert result != []
        assert len(result) == 1

    def test_search_with_detail(_, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestSearchMain.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.main.property_search_fetch",
            TestSearchMain.mock_property_search_fetch,
        )
        mocker.patch(
            "search.main.property_detail_fetch",
            TestSearchMain.mock_property_detail_fetch,
        )
        spy_property_search_fetch = mocker.spy(search.main, "property_search_fetch")
        spy_property_detail_fetch = mocker.spy(search.main, "property_detail_fetch")

        # act
        result = search.main.search_with_detail(
            domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
        )

        # assert
        spy_property_search_fetch.assert_called_once_with(
            domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
        )
        spy_property_detail_fetch.assert_called_once_with(
            link="testlink",
            property_search=search.main.PropertySearch(
                link="testlink", city="auckland"
            ),
        )
        assert result != None
        assert result != []
        assert len(result) == 1

    def test_format_csv(_, mocker):
        # arrange
        item = type(
            "Item",
            (object,),
            {
                "__dict__": {
                    "test1": 1,
                    "test2": 2,
                }
            },
        )
        item_list = [item()]

        # act
        result = search.main.format_psv(property_list=item_list)

        # assert
        assert result == "sno|test1|test2\n1|1|2\n"
