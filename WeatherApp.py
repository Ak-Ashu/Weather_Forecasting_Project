import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.configure(bg="#57adff")
root.resizable(False, False)

# Function to get the weather information
def getWeather(event = None):
    city = textfield.get()

    geolocator = Nominatim(user_agent="weatherData")
    location = geolocator.geocode(city)

    if location is None:
        messagebox.showerror("Error", "City not found")
        return

    # Get the timezone for the city
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude,4)}°N,{round(location.longitude,4)}°E")
    
    # Get current local time in that timezone
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    current_date = local_time.strftime("%Y-%m-%d")
   
    clock.config(text=f"{current_time} \n{current_date} ")
   
    
    # OpenWeatherMap API request for current and daily weather
    api = "https://api.openweathermap.org/data/2.5/weather?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&units=metric&exclude=hourly&appid=b51a5938137efefab7c3104593b68596"
    try:
        json_data = requests.get(api).json()
        if json_data.get("cod") != 200:
            messagebox.showerror("Error", "Failed to retrieve weather data")
            return
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return

    # Current weather data
    current = json_data['weather']
    temp = json_data['main']['temp']
    humidity = json_data['main']['humidity']
    pressure = json_data['main']['pressure']
    wind = json_data['wind']['speed']
    description = current[0]['description']
    

    t.config(text=(temp,"°C"))
    h.config(text=(humidity,"%"))
    p.config(text=(pressure,"hPa"))
    w.config(text=(wind,"m/s"))
    d.config(text=description)

    
    # Load the weather icon
    dayimage = json_data['weather'][0]['icon']
    img=(Image.open(f"icon/{dayimage}@2x.png"))
    resized_image= img.resize((200,200))
    weather_icon = ImageTk.PhotoImage(resized_image)

    # Display the icon in a label
    icon_label.config(image=weather_icon)
    icon_label.image = weather_icon
    icon_label.place(x=380, y=175)

# Add a label to display the weather icon
icon_label = tk.Label(root, bg="#57adff")
icon_label.place(x=30, y=100)

# Search Box
Search_image = ImageTk.PhotoImage(file="Images/rrr.png")
myimage = tk.Label(image=Search_image, bg="#57adff")
myimage.place(x=305, y=120)

# Search Box Logo Image
weat_image = ImageTk.PhotoImage(file="Images/layar7.png")
weatherimage = tk.Label(root, image=weat_image, bg="#203243")
weatherimage.place(x=307, y=122)

# Text Entry Box
textfield = tk.Entry(root, justify='center', font=('poppins', 22, 'bold'), bg="#203243", border=0, fg="white")
textfield.place(x=345, y=122)
textfield.focus()
textfield.bind("<Return>",getWeather)

# Search Icon
Search_icon = ImageTk.PhotoImage(file="Images/Layer6.png")
myimage_icon = tk.Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
myimage_icon.place(x=663, y=122)


# Logo Icon
image_icon = ImageTk.PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

# Bottom Box
frame=tk.Frame(root,width=900,height=80,bg="#0ACED9")
frame.pack(padx=5,pady=5,side=tk.BOTTOM)


# Clock Time and Date
clock = tk.Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=30, y=20)


# TimeZone and Coordinates
timezone = tk.Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone.place(x=650, y=20)
long_lat = tk.Label(root, font=("Helvetica", 10), fg="white", bg="#57adff")
long_lat.place(x=700, y=55)

# Labels for weather data
label1 = tk.Label(root, text="Temperature", font=('Helvetica', 14, 'bold'), fg="white", bg="#0ACED9")
label1.place(x=60, y=420)

label2 = tk.Label(root, text="Humidity", font=('Helvetica', 14, 'bold'), fg="white", bg="#0ACED9")
label2.place(x=240, y=420)

label3 = tk.Label(root, text="Pressure", font=('Helvetica', 14, 'bold'), fg="white", bg="#0ACED9")
label3.place(x=390, y=420)

label4 = tk.Label(root, text="Wind Speed", font=('Helvetica', 14, 'bold'), fg="white", bg="#0ACED9")
label4.place(x=550, y=420)

label5 = tk.Label(root, text="Description", font=('Helvetica', 14, 'bold'), fg="white", bg="#0ACED9")
label5.place(x=730, y=420)

# Labels for weather data
t = tk.Label(text="...", font=("Helvetica", 14, 'bold'), fg="white", bg="#0ACED9")
t.place(x=70, y=450)
h = tk.Label(text="...", font=("Helvetica", 14, 'bold'), fg="white", bg="#0ACED9")
h.place(x=250, y=450)
p = tk.Label(text="...", font=("Helvetica", 14, 'bold'), fg="white", bg="#0ACED9")
p.place(x=400, y=450)
w = tk.Label(text="...", font=("Helvetica", 14, 'bold'), fg="white", bg="#0ACED9")
w.place(x=560, y=450)
d = tk.Label(text="...", font=("Helvetica", 14, 'bold'), fg="white", bg="#0ACED9")
d.place(x=740, y=450)

root.mainloop()
