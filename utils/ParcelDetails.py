class ParcelDetails:
    def __init__(self, apn="", owner_name="", address="", city="", zip_code="", state="", size="", tax="", date="", zoning=""):
        self.apn = apn
        self.owner_name = owner_name
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.state = state
        self.size = size
        self.tax = tax
        self.date = date
        self.zoning = zoning

    def __repr__(self):
        return (f"ParcelDetails(apn={self.apn}, owner_name={self.owner_name}, address={self.address}, "
                f"city={self.city}, zip_code={self.zip_code}, state={self.state}, size={self.size}, "
                f"tax={self.tax}, date={self.date}, zoning={self.zoning})")

    def display_details(self):
        """Method to display the details of the parcel in a readable format."""
        print(f"APN: {self.apn}")
        print(f"Owner Name: {self.owner_name}")
        print(f"Address: {self.address}")
        print(f"City: {self.city}")
        print(f"ZIP Code: {self.zip_code}")
        print(f"State: {self.state}")
        print(f"Size: {self.size} sqft")
        print(f"Tax: ${self.tax}")
        print(f"Date: {self.date}")
        print(f"Zoning: {self.zoning}")

