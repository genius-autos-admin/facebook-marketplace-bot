# Remove and then publish each listing
def update_listings(listings, type, scraper):
    # If listings are empty stop the function
    if not listings:
        return

    # Check if listing is already listed and remove it then publish it like a new one
    for listing in listings:
        # Remove listing if it is already published
        remove_listing(listing, type, scraper)

        # Publish the listing in marketplace
        publish_listing(listing, type, scraper)


def remove_listing(data, listing_type, scraper):
    title = generate_title_for_listing_type(data, listing_type)
    listing_title = find_listing_by_title(title, scraper)

    # Listing not found so stop the function
    if not listing_title:
        return

    listing_title.click()

    # Click on the delete listing button
    scraper.element_click(
        'div:not([role="gridcell"]) > div[aria-label="Delete"][tabindex="0"]'
    )

    # Click on confirm button to delete
    confirm_delete_selector = (
        'div[aria-label="Delete listing"] div[aria-label="Delete"][tabindex="0"]'
    )
    if scraper.find_element(confirm_delete_selector, False, 3):
        scraper.element_click(confirm_delete_selector)
    else:
        confirm_delete_selector = (
            'div[aria-label="Delete Listing"] div[aria-label="Delete"][tabindex="0"]'
        )
        if scraper.find_element(confirm_delete_selector, True, 3):
            scraper.element_click(confirm_delete_selector)

    # Wait until the popup is closed
    scraper.element_wait_to_be_invisible('div[aria-label="Your Listing"]')


def publish_listing(data, listing_type, scraper):
    # Click on create new listing button
    scraper.element_click(
        'div[aria-label="Marketplace sidebar"] a[aria-label="Create new listing"]'
    )
    # Choose listing type
    scraper.element_click('a[href="/marketplace/create/' + listing_type + '/"]')

    # Create string that contains all of the image paths separeted by \n
    images_path = generate_multiple_images_path(
        data["Photos Folder"], data["Photos Names"]
    )
    # Add images to the the listing
    scraper.input_file_add_files(
        'input[accept="image/*,image/heif,image/heic"]', images_path
    )

    # Add specific fields based on the listing_type
    function_name = "add_fields_for_" + listing_type
    # Call function by name dynamically
    globals()[function_name](data, scraper)

    scraper.element_send_keys('label[aria-label="Price"] input', data["Price"])
    scraper.element_send_keys(
        'label[aria-label="Description"] textarea', data["Description"]
    )
    scraper.element_send_keys('label[aria-label="Location"] input', data["Location"])
    scraper.element_click('ul[role="listbox"] li:first-child > div')

    next_button_selector = 'div [aria-label="Next"] > div'
    next_button = scraper.find_element(next_button_selector, False, 3)
    if next_button:
        # Go to the next step
        scraper.element_click(next_button_selector)
        # Add listing to multiple groups
        add_listing_to_multiple_groups(data, scraper)

    # Publish the listing
    scraper.element_click('div[aria-label="Publish"]:not([aria-disabled])')

    # Wait until the listing is published and we are on the listings page where there is a search input
    scraper.find_element('input[placeholder="Search your listings"]', False)

    # if not next_button:
    post_listing_to_multiple_groups(data, listing_type, scraper)


def generate_multiple_images_path(path, images):
    # Last character must be '/' because after that we are adding the name of the image
    if path[-1] != "/":
        path += "/"

    images_path = ""

    # Split image names into array by this symbol ";"
    image_names = images.split(";")

    # Create string that contains all of the image paths separeted by \n
    if image_names:
        for image_name in image_names:
            # Remove whitespace before and after the string
            image_name = image_name.strip()

            # Add "\n" for indicating new file
            if images_path != "":
                images_path += "\n"

            images_path += path + image_name

    return images_path


def add_fields_for_vehicle(data, scraper):
    try:
        # Step 1: Select Vehicle Type
        print("Selecting vehicle type...")
        scraper.scroll_to_element('label[aria-label="Vehicle type"]')
        scraper.element_click('label[aria-label="Vehicle type"]')
        vehicle_type_xpath = f'//span[contains(text(), "{data["Vehicle Type"]}")]'
        scraper.element_click_by_xpath(vehicle_type_xpath)
        print(f"Vehicle type {data['Vehicle Type']} selected.")

        # Step 2: Select Year
        print("Selecting year...")
        scraper.scroll_to_element('label[aria-label="Year"]')
        scraper.element_click('label[aria-label="Year"]')
        year_xpath = f'//span[contains(text(), "{data["Year"]}")]'
        scraper.element_click_by_xpath(year_xpath)
        print(f"Year {data['Year']} selected.")

        # Step 3: Select Make
        print("Selecting make...")
        scraper.scroll_to_element('label[aria-label="Make"]')
        scraper.element_click('label[aria-label="Make"]')
        make_input_xpath = f'//span[contains(text(), "{data["Make"]}")]'
        scraper.element_click_by_xpath(make_input_xpath)
        print(f"Make {data['Make']} selected.")

        # Step 4: Enter Model
        print("Entering model...")
        scraper.scroll_to_element('label[aria-label="Model"] input')
        scraper.element_send_keys('label[aria-label="Model"] input', data["Model"])
        print(f"Model {data['Model']} entered.")

        # Step 5: Enter Mileage
        print("Entering mileage...")
        scraper.scroll_to_element('label[aria-label="Mileage"] input')
        scraper.element_send_keys('label[aria-label="Mileage"] input', data["Mileage"])
        print(f"Mileage {data['Mileage']} entered.")

        # Step 6: Select Fuel Type
        print("Selecting fuel type...")
        scraper.scroll_to_element('label[aria-label="Fuel type"]')
        scraper.element_click('label[aria-label="Fuel type"]')
        fuel_type_xpath = f'//span[contains(text(), "{data["Fuel Type"]}")]'
        scraper.element_click_by_xpath(fuel_type_xpath)
        print(f"Fuel type {data['Fuel Type']} selected.")

        # Step 7: Select Body Style
        print("Selecting body style...")
        scraper.scroll_to_element('label[aria-label="Body style"]')
        scraper.element_click('label[aria-label="Body style"]')
        body_style_xpath = f'//span[contains(text(), "{data["Body Style"]}")]'
        scraper.element_click_by_xpath(body_style_xpath)
        print(f"Body style {data['Body Style']} selected.")

        # Step 8: Select Exterior Colour
        print("Selecting exterior colour...")
        scraper.scroll_to_element('label[aria-label="Exterior colour"]')
        scraper.element_click('label[aria-label="Exterior colour"]')
        exterior_colour_xpath = f'//span[contains(text(), "{data["Exterior Colour"]}")]'
        scraper.element_click_by_xpath(exterior_colour_xpath)
        print(f"Exterior colour {data['Exterior Colour']} selected.")

        # Step 8: Select Interior Colour
        print("Selecting interior colour...")
        scraper.scroll_to_element('label[aria-label="Interior colour"]')
        scraper.element_click('label[aria-label="Interior colour"]')
        interior_colour_xpath = f'//span[contains(text(), "{data["Interior Colour"]}")]'
        scraper.element_click_by_xpath(interior_colour_xpath)
        print(f"Interior colour {data['Interior Colour']} selected.")

    except Exception as e:
        print(f"Error while inserting fields: {str(e)}")


# Add specific fields for listing from type item
def add_fields_for_item(data, scraper):
    scraper.element_send_keys('label[aria-label="Title"] input', data["Title"])

    # Scroll to "Category" select field
    scraper.scroll_to_element('label[aria-label="Category"]')
    # Expand category select
    scraper.element_click('label[aria-label="Category"]')
    # Select category
    scraper.element_click_by_xpath('//span[text()="' + data["Category"] + '"]')

    # Expand category select
    scraper.element_click('label[aria-label="Condition"]')
    # Select category
    scraper.element_click_by_xpath(
        '//span[@dir="auto"][text()="' + data["Condition"] + '"]'
    )

    if data["Category"] == "Sports & Outdoors":
        scraper.element_send_keys('label[aria-label="Brand"] input', data["Brand"])


def generate_title_for_listing_type(data, listing_type):
    title = ""

    if listing_type == "item":
        title = data["Title"]

    if listing_type == "vehicle":
        title = data["Year"] + " " + data["Make"] + " " + data["Model"]

    return title


def add_listing_to_multiple_groups(data, scraper):
    # Create an array for group names by spliting the string by this symbol ";"
    group_names = data["Groups"].split(";")

    # If the groups are empty do not do nothing
    if not group_names:
        return

    # Post in different groups
    for group_name in group_names:
        # Remove whitespace before and after the name
        group_name = group_name.strip()

        scraper.element_click_by_xpath('//span[text()="' + group_name + '"]')


def post_listing_to_multiple_groups(data, listing_type, scraper):
    title = generate_title_for_listing_type(data, listing_type)
    title_element = find_listing_by_title(title, scraper)

    # If there is no add with this title do not do nothing
    if not title_element:
        return

    # Create an array for group names by spliting the string by this symbol ";"
    group_names = data["Groups"].split(";")

    # If the groups are empty do not do nothing
    if not group_names:
        return

    search_input_selector = '[aria-label="Search for groups"]'

    # Post in different groups
    for group_name in group_names:
        # Click on the Share button to the listing that we want to share
        scraper.element_click('[aria-label="' + title + '"] + div [aria-label="Share"]')

        # Click on the Share to a group button
        scraper.element_click_by_xpath('//span[text()="Group"]')

        # Remove whitespace before and after the name
        group_name = group_name.strip()

        # Remove current text from this input
        scraper.element_delete_text(search_input_selector)
        # Enter the title of the group in the input for search
        scraper.element_send_keys(search_input_selector, group_name[:51])

        scraper.element_click_by_xpath('//span[text()="' + group_name + '"]')

        if scraper.find_element('[aria-label="Create a public post…"]', False, 3):
            scraper.element_send_keys(
                '[aria-label="Create a public post…"]', data["Description"]
            )
        elif scraper.find_element('[aria-label="Write something..."]', False, 3):
            scraper.element_send_keys(
                '[aria-label="Write something..."]', data["Description"]
            )

        scraper.element_click('[aria-label="Post"]:not([aria-disabled])')
        # Wait till the post is posted successfully
        scraper.element_wait_to_be_invisible('[role="dialog"]')
        scraper.element_wait_to_be_invisible('[aria-label="Loading...]"')
        scraper.find_element_by_xpath(
            '//span[text()="Shared to your group."]', False, 10
        )


def find_listing_by_title(title, scraper):
    searchInput = scraper.find_element(
        'input[placeholder="Search your listings"]', False
    )
    # Search input field is not existing
    if not searchInput:
        return False

    # Clear input field for searching listings before entering title
    scraper.element_delete_text('input[placeholder="Search your listings"]')
    # Enter the title of the listing in the input for search
    scraper.element_send_keys('input[placeholder="Search your listings"]', title)

    return scraper.find_element_by_xpath('//span[text()="' + title + '"]', False, 10)
