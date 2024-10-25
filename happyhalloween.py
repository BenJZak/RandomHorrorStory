import praw
import tkinter as tk
import requests
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
from io import BytesIO
import random

def get_random_unsplash_image(access_key):
    url = 'https://api.unsplash.com/photos/random/?horror'
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']  # You can also use 'full', 'small', etc.
        return image_url
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Replace 'YOUR_ACCESS_KEY' with your actual Unsplash API access key
access_key = 'YOUR_ACCESS_KEY'
random_image_url = get_random_unsplash_image(access_key)

# Set up Reddit API credentials
reddit = praw.Reddit(
    #Replace with your own information. User_agent can be anything.
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="project name by /u/yourusername"
)

# Get two random posts from the subreddit
subreddit = reddit.subreddit("TwoSentenceHorror")
random_post1 = subreddit.random().selftext
random_post2 = subreddit.random().selftext

# Download a random scary image from the internet
response = requests.get(random_image_url)
image = Image.open(BytesIO(response.content))

# Apply a "scary" filter to the image
image = image.filter(ImageFilter.GaussianBlur(3))  # Add a slight blur
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(5)  # Increase contrast for intensity

# Set up Tkinter window
root = tk.Tk()
root.geometry("800x600")

# Convert PIL image to a format Tkinter can display
bg_image = ImageTk.PhotoImage(image)

# Create a Canvas to display the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Define text positions and box sizes
text1_pos = (400, 200)
text2_pos = (400, 400)
text_box_padding = 10

#Create black rectangles (boxes) behind the text
canvas.create_rectangle(
    text1_pos[0] - 350, text1_pos[1] - 20,
    text1_pos[0] + 350, text1_pos[1] + 20,
    fill="white", outline=""
)

canvas.create_rectangle(
    text2_pos[0] - 350, text2_pos[1] - 20,
    text2_pos[0] + 350, text2_pos[1] + 20,
    fill="white", outline=""
)

# Add text labels over the black boxes
canvas.create_text(text1_pos, text=random_post1, fill="black", font=("Arial", 20), width=700)
canvas.create_text(text2_pos, text=random_post2, fill="black", font=("Arial", 20), width=700)

# Run the Tkinter main loop
root.mainloop()
