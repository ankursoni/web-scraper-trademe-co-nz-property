import search.main


class TestPropertySearch:

    property_search_result = None

    DEFAULT_HIT_DELAY_SECONDS = 0

    def mock_property_search_001_requests_get(url):
        f = open("tests/data/property_search_001.html", "r")
        response = type(
            "requests.models.Response",
            (object,),
            dict(content=f.read(), status_code=200),
        )
        return response

    def mock_property_detail_001_requests_get(url):
        f = open("tests/data/property_detail_001.html", "r")
        response = type(
            "requests.models.Response",
            (object,),
            dict(content=f.read(), status_code=200),
        )
        return response

    def mock_property_detail_002_requests_get(url):
        f = open("tests/data/property_detail_002.html", "r")
        response = type(
            "requests.models.Response",
            (object,),
            dict(content=f.read(), status_code=200),
        )
        return response

    def mock_property_detail_003_requests_get(url):
        f = open("tests/data/property_detail_003.html", "r")
        response = type(
            "requests.models.Response",
            (object,),
            dict(content=f.read(), status_code=200),
        )
        return response

    def test_property_search_001_fetch(self, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestPropertySearch.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.property_search.requests.get",
            TestPropertySearch.mock_property_search_001_requests_get,
        )
        spy_requests_get = mocker.spy(search.property_search.requests, "get")

        # act
        result = search.main.property_search_fetch(
            domain_url="https://www.trademe.co.nz", city="auckland", total_pages=1
        )

        # assert
        spy_requests_get.assert_called_once_with(
            url="https://www.trademe.co.nz/a/property/residential/sale/auckland?page=1"
        )
        assert result != None
        assert result != []
        assert len(result) == 22

        assert result[0].city == "auckland"
        assert (
            result[0].link
            == "https://www.trademe.co.nz/a/property/residential/sale/auckland/rodney/gulf-harbour/listing/3640441947"
        )
        assert result[0].title == "ADORABLE, AFFORDABLE, ABSOLUTLY GEM!"
        assert result[0].address == "71 Nautilus Drive, Gulf Harbour, Rodney"
        assert result[0].number_of_bedrooms == "3"
        assert result[0].number_of_bathrooms == "2"
        assert result[0].number_of_parking_lots == None
        assert result[0].number_of_living_areas == None
        assert result[0].floor_area_sqm == "155 m2"
        assert result[0].land_area_sqm == "132  m2"
        assert result[0].asking_price == "Deadline sale"

        assert result[-1].city == "auckland"
        assert (
            result[-1].link
            == "https://www.trademe.co.nz/a/property/residential/sale/auckland/rodney/gulf-harbour/listing/3611361622"
        )
        assert result[-1].title == "Substantial Family Residence"
        assert result[-1].address == "9 Belle-Mer Place, Gulf Harbour, Rodney"
        assert result[-1].number_of_bedrooms == "5"
        assert result[-1].number_of_bathrooms == "3"
        assert result[-1].number_of_parking_lots == None
        assert result[-1].number_of_living_areas == None
        assert result[-1].floor_area_sqm == "308 m2"
        assert result[-1].land_area_sqm == "921  m2"
        assert result[-1].asking_price == "Price by negotiation"

        TestPropertySearch.property_search_result = result

    def test_propertydetail_001_fetch(self, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestPropertySearch.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.property_detail.requests.get",
            TestPropertySearch.mock_property_detail_001_requests_get,
        )
        spy_requests_get = mocker.spy(search.property_detail.requests, "get")

        # act
        result = search.main.property_detail_fetch(
            link="https://www.trademe.co.nz/a/property/residential/sale/auckland/manukau-city/the-gardens/listing/3615355083",
            property_search=TestPropertySearch.property_search_result[19]
            if TestPropertySearch.property_search_result
            else None,
        )

        # assert
        spy_requests_get.assert_called_once_with(
            url="https://www.trademe.co.nz/a/property/residential/sale/auckland/manukau-city/the-gardens/listing/3615355083"
        )
        assert result != None

        assert result.city == "auckland"
        assert (
            result.link
            == "https://www.trademe.co.nz/a/property/residential/sale/auckland/manukau-city/the-gardens/listing/3615355083"
        )
        assert result.title == "Your Treasure in the Gardens"
        assert result.address == "19 Manara Place, The Gardens, Manukau City"
        assert result.number_of_bedrooms == "4"
        assert result.number_of_bathrooms == "2"
        assert result.number_of_parking_lots == "2"
        assert result.number_of_living_areas == None
        assert result.floor_area_sqm == "270 m2"
        assert result.land_area_sqm == "644  m2"
        assert result.asking_price == "$1,680,000"
        # new attributes
        assert result.property_type == "House"
        assert result.rateable_value == None
        assert result.parking_type == None
        assert (
            result.in_the_area
            == "Schools: Primary / Intermediate School: The Gardens School. Secondary School: Alfriston College"
        )
        assert result.property_id == None
        assert result.agency_reference == "RIS10054"
        assert result.broadband_options == "Fibre, ADSL, VDSL, Wireless"
        assert (
            result.description
            == """Finding the right home can be a challenge, especially a home which can satisfy all members of the family. This treasured home in The Gardens could be the one for you! 
This charming home has a number of standout features such as attention to detail and the layout. The house includes an outstanding 270 sqm of floor area comprising of 4 bedrooms and 2 bathrooms, generous amounts of living space and ample storage on both floors.
The ground floor is designed to be enjoyed by the entire family as you can utilize every corner to suit the purpose of each member. You'll find the master bedroom with a walk-in wardrobe including an ensuite and a double bedroom located away from the main living area where kids can run around and for teenagers to have their own space. Parents can relax and enjoy the outdoors by creating the most amazing garden landscape. A kitchen is the key element of a home and represents unity, love and wealth. It is tucked away privately once you’ve spent time welcoming your guests so your wealth is always fulfilled but protected in a safe place. 
On the second floor, you'll find another two generous bedrooms with a separate bathroom and toilet. You also benefit from having an additional living room, which you can transform to suit your family’s needs. You will no longer have to worry about the weather. Rain or shine, you can drive into the internal garage and enter your home in comfort and ease. 
The Gardens is a wonderful and renowned neighbourhood. It will take you less than 3 mins to visit the serene Botanic Garden and provides convenient access to the motorway and local shops.
This sensational home is waiting for its new owner so don't wait. Contact me today at 021 308 797 and bring your family along to my open homes.
PLEASE NOTE: Specified floor and land area size have been obtained from but not limited to multiple sources: Property Smarts, Property-Guru, or Title documents. Advertised areas have not been measured by the Salesperson or Next Gen Real Estate Limited. We...
"""
        )

    def test_propertydetail_002_fetch(self, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestPropertySearch.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.property_detail.requests.get",
            TestPropertySearch.mock_property_detail_002_requests_get,
        )
        spy_requests_get = mocker.spy(search.property_detail.requests, "get")

        # act
        result = search.main.property_detail_fetch(
            link="https://www.trademe.co.nz/a/property/residential/sale/auckland/rodney/gulf-harbour/listing/3611361622",
            property_search=TestPropertySearch.property_search_result[21]
            if TestPropertySearch.property_search_result
            else None,
        )

        # assert
        spy_requests_get.assert_called_once_with(
            url="https://www.trademe.co.nz/a/property/residential/sale/auckland/rodney/gulf-harbour/listing/3611361622"
        )
        assert result != None

        assert result.city == "auckland"
        assert (
            result.link
            == "https://www.trademe.co.nz/a/property/residential/sale/auckland/rodney/gulf-harbour/listing/3611361622"
        )
        assert result.title == "Substantial Family Residence"
        assert result.address == "9 Belle-Mer Place, Gulf Harbour, Rodney"
        assert result.number_of_bedrooms == "5"
        assert result.number_of_bathrooms == "3"
        assert result.number_of_parking_lots == None
        assert result.number_of_living_areas == None
        assert result.floor_area_sqm == "308 m2"
        assert result.land_area_sqm == "921  m2"
        assert result.asking_price == "Price by negotiation"
        # new attributes
        assert result.property_type == "House"
        assert result.rateable_value == "$1,600,000"
        assert result.parking_type == "off street parking"
        assert result.in_the_area == None
        assert result.property_id == None
        assert result.agency_reference == "MLY30171"
        assert result.broadband_options == "Fibre, ADSL, VDSL, Wireless"
        assert (
            result.description
            == """Situated in one of Gulf Harbour's premier locations this desirable address and executive residence is a winning combination. Designed for family and entertaining this heartwarming home is a show stopper with 5 bedrooms, 3 bathrooms, 2 living and inground pool, not to mention the triple car garaging.
Spread over two levels and positioned in a secluded setting for privacy and peaceful living. Impeccable layout and fabulous flow makes this a winner for families who love to entertain, with an open plan kitchen and dining area, separate formal dining, and 2 separate lounges. The main family lounge is wired for entertainment with projector screen and projector included, with the second lounge perfectly positioned for summers around the pool or cosy nights around the gas fire in the cooler months. 
On the ground floor there is a bathroom, separate WC and laundry and two large bedrooms, one off the lounge used as a 5th bedroom or large home office. 
Upstairs the large Master with walk-in wardrobe and large ensuite enjoys views. A further two large bedrooms, are serviced by a family bathroom.
With fantastic indoor / outdoor flow to two entertaining areas; The kids favourite will be the swimming pool and inground spa plus an outdoor shower for when you come home from the beach or time spent in the pool. The north facing BBQ area flows seamlessly from the kitchen ideal for entertaining with family and friends.
Fully fenced and with large gates at the entrance of the section, it will provide plenty of security for the large parking area and the toys that you can house in the large triple car garage. A Building Report is available on request.
The Gulf Harbour lifestyle is right on your doorstep, with a choice of coastal walks throughout the suburb, local schools, Shakespear Regional Park and two golf courses. Gulf Harbour Village, Gulf Harbour Marina and Ferry service to Auckland CBD are all close by as well. 
A very unique property in a fantastic location, this is a must view, call Sharon now!
"""
        )

    def test_propertydetail_003_fetch(self, mocker):
        # arrange
        mocker.patch.object(
            search.main,
            "DEFAULT_HIT_DELAY_SECONDS",
            TestPropertySearch.DEFAULT_HIT_DELAY_SECONDS,
        )
        mocker.patch(
            "search.property_detail.requests.get",
            TestPropertySearch.mock_property_detail_003_requests_get,
        )
        spy_requests_get = mocker.spy(search.property_detail.requests, "get")

        # act
        result = search.main.property_detail_fetch(
            link="https://www.trademe.co.nz/a/property/new-homes/house-land/auckland/rodney/milldale/listing/3615362032",
            property_search=TestPropertySearch.property_search_result[18]
            if TestPropertySearch.property_search_result
            else None,
        )

        # assert
        spy_requests_get.assert_called_once_with(
            url="https://www.trademe.co.nz/a/property/new-homes/house-land/auckland/rodney/milldale/listing/3615362032"
        )
        assert result != None

        assert result.city == "auckland"
        assert (
            result.link
            == "https://www.trademe.co.nz/a/property/new-homes/house-land/auckland/rodney/milldale/listing/3615362032"
        )
        assert result.title == "16 Karapara Rd - buy direct from Sensation!"
        assert result.address == "16 Karapapa Road, Milldale, Rodney"
        assert result.number_of_bedrooms == "4"
        assert result.number_of_bathrooms == "2"
        assert result.number_of_parking_lots == "4"
        assert result.number_of_living_areas == "2"
        assert result.floor_area_sqm == "208 m2"
        assert result.land_area_sqm == "468  m2"
        assert result.asking_price == "Price by negotiation"
        # new attributes
        assert result.property_type == "House"
        assert result.rateable_value == None
        assert result.parking_type == None
        assert result.in_the_area == "Shops, school, cafe"
        assert result.property_id == "HSZ447"
        assert result.agency_reference == None
        assert result.broadband_options == None
        assert (
            result.description
            == """Our home at 18 Ruxton Road (off end of Argent Lane) is available for viewing, if you would like to see an example of a finished home
Please contact us 0274990075.
Sensation Developments 100% kiwi owned & operated.
Proud build partners to Fulton Hogan (the Milldale/Millwater developers) for over 24 years!
Buy direct from the developer - contact us on 0800 99 00 75 or 0274 99 0075
This is a fixed price house & land package including all groundworks & an extensive landscaping package - there is no more to pay on top of fixed price.
PRICING NOT YET SET - TALK TO US BUYER ENQUIRY GUIDE OVER $1.5m+
10% deposit, then balance payable upon completion - settlement early 2023
16 Karapapa Road, Milldale (lot 205) - centrally located  in brand new stage 4D - close to shops and school!
Built to exceed building code standards
-4 double bedrooms - walk in robe to master.
-Double garaging & 2 car  offstreet parking space
-Gerard Texture tile roof
-Midland or Huntly Claybricks (one and a half or double size brick) brick & KLC (high grade) weatherboard cladding - colour to be confirmed
-Beautiful custom designed kitchen, double ovens, double bowls, double fridge space & quartz Caesarstone bench tops.
-Open plan kitchen with attached walk in pantry/store area (very good size to this area) - it even has a second access back into the garage!
-Separate formal lounge, then open plan family, kitchen & dining areas
-Alarm system, airconditioning, under tile heating, central vacuum, stairs to space above garage, insulated garage door, carpet to garage area.
-designated laundry space, offset between hall/garage area
-Really great section - site has wide street frontage with lovely rear garden space
-Fully landscaped, fenced, planted as part of the package
-10 Year Master Builder Guarantee
Please phone on  0800 99 00 75 or email us if you would like to know more about this upcoming package
Photos shown from some of our recent homes in the area
"""
        )
