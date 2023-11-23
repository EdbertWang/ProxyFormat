
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import utils
import requests
from time import sleep

# Take and parse command line input, then store in a dictonary
'''
Ex.
3 Black Lotus
3x Island
''' 
def parseInput(log) -> dict:
    cards = {} # Tuples of type name, number
    print("Enter Cards: (type 'End' to stop):")
    
    while True:
        user_input = input().lower()

        if (user_input == "end"):
            break
        
        user_input = user_input.split(" ")
        if len(user_input) < 2 or user_input[0] == "" or user_input[1] == "":
            log[0] += "Unrecognised input: " + str(user_input) + "\n"
            continue
    
        user_input = user_input[:2]

        if user_input[0][-1] == 'x':
           user_input[0] = user_input[0][:-1]

        cards[user_input[1].lower()] = int(user_input[0])

    log[0] += "Cards Entered: " + str(cards) + "\n"
    
    return cards


# Grab images scryfall, Example api search
# https://api.scryfall.com/cards/search?q=name=%22black%20lotus%22
def grabImages(cardsDict, log) -> dict:
    print("Retrieving Images from Scryfall")
    search_base = "https://api.scryfall.com/cards/search?q=name=\"{}\""
    fileNames = {}
    for i in cardsDict.items():
        response = requests.get(search_base.format(i[0]))
        if response.status_code == 200:
            # Parse the JSON content of the response
            json_data = response.json()

            if 'card_faces' in json_data['data'][0]: # Check if dual faced card
                # Download Frontside
                try:
                    large_image_url = json_data['data'][0]['card_faces'][0]['image_uris']['large']
                except:
                    log += "Error Reading JSON for " + i[0] + "\n"
                    continue
                
                response = requests.get(large_image_url)
                
                if response.status_code == 200:
                    with open('images/' + i[0].replace(" ", "_").lower() + '_f.jpg', 'wb') as f:
                        f.write(response.content)
                    fileNames[i[0].replace(" ", "_") + '_f'] = i[1]
                else:
                    log[0] += f"Failed to download image for front of {i}.\n"
                
                # Download Backside
                try:
                    large_image_url = json_data['data'][0]['card_faces'][1]['image_uris']['large']
                except:
                    log += "Error Reading JSON for " + i[0] + "\n"
                    continue
                
                response = requests.get(large_image_url)
                
                if response.status_code == 200:
                    with open('images/' + i[0].replace(" ", "_") + '_b.jpg', 'wb') as f:
                        f.write(response.content)
                    fileNames[i[0].replace(" ", "_") + "_b"] = i[1]
                else:
                    log[0] += f"Failed to download image for back of {i}.\n"

            else:
                large_image_url = json_data['data'][0]['image_uris']['large']
                response = requests.get(large_image_url)
                
                if response.status_code == 200:
                    with open('images/' + i[0].replace(" ", "_") + '_n.jpg', 'wb') as f:
                        f.write(response.content)
                    fileNames[i[0].replace(" ", "_")  + '_n'] = i[1]
                else:
                    log[0] += f"Failed to download image for {i}.\n"

            sleep(0.05) # 50~100 ms wait query as specified in API Documentation
        else:
            log[0] += f"Failed to access Scryfall for {i}.\n"

    log[0] += "Cards Found: " + str(fileNames) + "\n"
    return fileNames



# Format a PDF
def add_image_to_pdf(pdf_canvas, image_path, x, y, width, height):
    image = utils.ImageReader("images/" + image_path + ".jpg")

    if y < 150: # Images need to be rotated before they can fit
        pdf_canvas.saveState()
        # Rotate the canvas by the specified angle
        pdf_canvas.rotate(90)
        # The math for the new location is beyond me
        # The numbers choosen were the result of lots of trial and error
        temp = x
        x = y
        y = height - temp 
        # Draw the rotated image
        pdf_canvas.drawImage(image, x, y, width, height, preserveAspectRatio=True, anchor='c')
        # Restore the original state of the canvas
        pdf_canvas.restoreState()
    else:
        pdf_canvas.drawImage(image, x, y, width, height, preserveAspectRatio=True, anchor='c')


def create_pdf(images, output_file):
    print("Generating PDF")
    locations = [(25,504),(216, 504),(410, 504),(25, 234),(216, 234),(410, 234),(550,40),(830,40)] # Enumerate the 8 possible places that we can place an image
    images_per_page = len(locations)
    
    # Set the dimensions for the images (2.5 x 3.5 inches)
    image_width = 2.5 * inch
    image_height = 3.5 * inch
    current_page = 1
    i = 0

    pdf_canvas = canvas.Canvas(output_file, pagesize=letter)
    pdf_canvas.setPageSize((8.5 * inch, 11 * inch))

    for cardTuple in images.items():
        name = cardTuple[0]
        for copy in range(cardTuple[1]):
            add_image_to_pdf(pdf_canvas, name, locations[i % images_per_page][0], locations[i % images_per_page][1], image_width, image_height)
            i += 1
            # If the current page is filled with images, start a new page
            if i % images_per_page == 0:
                pdf_canvas.showPage()
                current_page += 1

    # Save the PDF
    pdf_canvas.save()

if __name__ == "__main__":
    log = [""]
    cards = parseInput(log)
    cards = grabImages(cards,log)

    create_pdf(cards, 'output.pdf')

    with open("ErrorLog.txt","w") as f:
        f.write(log[0])

    
    print("PDF created")
    print("Errors saved to ErrorLog.txt")
