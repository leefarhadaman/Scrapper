import requests
from bs4 import BeautifulSoup
import time
import turtle
import csv
import json

# Function to perform web scraping
def scrape_website(url, tags, save_format="txt"):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        extracted_data = {}
        # Extract specified tags
        for tag in tags:
            extracted_data[tag] = soup.find_all(tag)

        # Display and save the extracted tags
        if extracted_data:
            for tag, elements in extracted_data.items():
                if elements:
                    screen.clear()
                    screen.update()
                    screen.bgcolor("lightblue")
                    write_to_screen(f"\nExtracted <{tag}> Tags:", -250, 200)
                    for idx, element in enumerate(elements, start=1):
                        write_to_screen(f"{idx}: {element.text.strip()}", -250, 150 - 30 * idx)

                    # Optionally save the tags to a file in different formats
                    if save_format == "txt":
                        with open(f"{tag}_tags.txt", "w") as file:
                            for element in elements:
                                file.write(element.text.strip() + "\n")
                        write_to_screen(f"\n<{tag}> tags saved to '{tag}_tags.txt'.", -250, -100)
                    elif save_format == "csv":
                        with open(f"{tag}_tags.csv", "w", newline='', encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([f"<{tag}> Text"])
                            for element in elements:
                                writer.writerow([element.text.strip()])
                        write_to_screen(f"\n<{tag}> tags saved to '{tag}_tags.csv'.", -250, -100)
                    elif save_format == "json":
                        with open(f"{tag}_tags.json", "w", encoding="utf-8") as jsonfile:
                            json_data = [element.text.strip() for element in elements]
                            json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)
                        write_to_screen(f"\n<{tag}> tags saved to '{tag}_tags.json'.", -250, -100)
                else:
                    write_to_screen(f"\nNo <{tag}> tags found on this page.", -250, 100)
        else:
            write_to_screen("\nNo tags found on this page.", -250, 100)

    except requests.exceptions.RequestException as e:
        write_to_screen(f"An error occurred: {e}", -250, 100)
        # Log the error to a file
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Error scraping {url}: {e}\n")

def write_to_screen(message, x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.write(message, font=("Arial", 12, "normal"))

# Main entry point for the script
if __name__ == "__main__":
    # Set up the screen for Turtle
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.title("Web Scraper with Turtle Interface")
    turtle.speed(0)  # Fastest drawing

    # Clear the screen for first use
    turtle.clear()
    
    # Ask user to input the URL using Turtle
    url = turtle.textinput("Input", "Enter a website URL to scrape:")
    
    # Ask user for tags
    tags_input = turtle.textinput("Input", "Enter the tags to scrape (comma-separated, e.g., h1,p,a):")
    tags = [tag.strip() for tag in tags_input.split(",")]
    
    # Ask user for save format
    save_format = turtle.textinput("Input", "Enter the output format (txt, csv, json):").lower()

    # Display scraping progress
    write_to_screen("Scraping in Progress...", -250, 250)
    
    # Call the function to scrape the website
    scrape_website(url, tags, save_format)

    # Close the Turtle screen when clicked
    screen.exitonclick()
