
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Room:
    def __init__(self, room_number, price, image_path):
        self.room_number = room_number
        self.price = price
        self.image_path = image_path
        self.reservations = []

    def is_available(self, date):
        for reservation_date in self.reservations:
            if reservation_date == date:
                return False
        return True

    def reserve(self, date):
        if self.is_available(date):
            self.reservations.append(date)
            return True
        else:
            return False

    def cancel_reservation(self, date):
        if date in self.reservations:
            self.reservations.remove(date)
            return True
        else:
            return False

class Hotel:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_number] = room

    def make_reservation(self, room_number, date):
        room = self.rooms.get(room_number)
        if room:
            if room.reserve(date):
                return room.price
        return None

    def cancel_reservation(self, room_number, date):
        room = self.rooms.get(room_number)
        if room:
            return room.cancel_reservation(date)
        return False

    def get_reservations(self):
        reservations = []
        for room in self.rooms.values():
            for date in room.reservations:
                reservations.append({'room_number': room.room_number, 'date': date})
        return reservations

class HotelReservationApp:
    def __init__(self, master):
        self.master = master
        self.hotel = Hotel()
        self.hotel.add_room(Room(101, 10000, "images/single_room.jpg"))
        self.hotel.add_room(Room(102, 12000, "images/single_room.jpg"))
        self.hotel.add_room(Room(201, 15000, "images/double_room.jpg"))

        self.label = tk.Label(master, text="Welcome to Hotel Reservation System", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.list_rooms_button = tk.Button(master, text="List Rooms", command=self.list_rooms, font=("Helvetica", 12), bg="orange", fg="white")
        self.list_rooms_button.pack(pady=5)

        self.book_now_button = tk.Button(master, text="Book Now", command=self.book_now, font=("Helvetica", 12), bg="green", fg="white")
        self.book_now_button.pack(pady=5)

        self.make_reservation_button = tk.Button(master, text="Make Reservation", command=self.make_reservation, font=("Helvetica", 12), bg="green", fg="white")
        self.make_reservation_button.pack(pady=5)

        self.cancel_reservation_button = tk.Button(master, text="Cancel Reservation", command=self.cancel_reservation, font=("Helvetica", 12), bg="red", fg="white")
        self.cancel_reservation_button.pack(pady=5)

        self.list_reservations_button = tk.Button(master, text="List Reservations", command=self.list_reservations, font=("Helvetica", 12), bg="blue", fg="white")
        self.list_reservations_button.pack(pady=5)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit, font=("Helvetica", 14))
        self.exit_button.pack(pady=5)

    def list_rooms(self):
        top = tk.Toplevel()
        top.title("Available Rooms")

        for room_number, room in self.hotel.rooms.items():
            room_info = f"Room Number: {room_number}\nPrice: {room.price}Ft/night\n "
            tk.Label(top, text=room_info, font=("Helvetica", 14)).pack()

            # Display room image (you need to have Pillow installed)
            try:
                from PIL import Image, ImageTk
                image = Image.open(room.image_path)
                image = image.resize((150, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(top, image=photo)
                label.image = photo
                label.pack()
            except:
                tk.Label(top, text="Image not available", font=("Helvetica", 14)).pack()

            tk.Label(top, text="-------------------------", font=("Helvetica", 14)).pack()


    def book_now(self):
        top = tk.Toplevel()
        top.title("Book Now")

        tk.Label(top, text="Enter Room Number:", font=("Helvetica", 14)).pack()
        self.room_number_entry = tk.Entry(top, font=("Helvetica", 14))
        self.room_number_entry.pack()

        tk.Label(top, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14)).pack()
        self.date_entry = tk.Entry(top, font=("Helvetica", 14))
        self.date_entry.pack()

        self.submit_button = tk.Button(top, text="Submit", command=self.submit_booking, font=("Helvetica", 14), bg="green", fg="white")
        self.submit_button.pack(pady=10)

    def submit_booking(self):
        room_number = int(self.room_number_entry.get())
        date_str = self.date_entry.get()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        price = self.hotel.make_reservation(room_number, date)
        if price:
            messagebox.showinfo("Success", f"Reservation made successfully! Price: {price}")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Room is not available on this date.")

    def clear_entries(self):
        self.room_number_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def make_reservation(self):
        top = tk.Toplevel()
        top.title("Make Reservation")

        tk.Label(top, text="Enter Room Number:", font=("Helvetica", 14)).pack()
        self.room_number_entry = tk.Entry(top, font=("Helvetica", 14))
        self.room_number_entry.pack()

        tk.Label(top, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14)).pack()
        self.date_entry = tk.Entry(top, font=("Helvetica", 14))
        self.date_entry.pack()

        self.submit_button = tk.Button(top, text="Submit", command=self.submit_reservation, font=("Helvetica", 14), bg="green", fg="white")
        self.submit_button.pack(pady=10)

    def submit_reservation(self):
        room_number = int(self.room_number_entry.get())
        date_str = self.date_entry.get()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        price = self.hotel.make_reservation(room_number, date)
        if price:
            messagebox.showinfo("Success", f"Reservation made successfully! Price: {price}")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Room is not available on this date.")

    def cancel_reservation(self):
        top = tk.Toplevel()
        top.title("Cancel Reservation")

        tk.Label(top, text="Enter Room Number:", font=("Helvetica", 14)).pack(pady=(10, 0))
        self.room_number_entry = tk.Entry(top, font=("Helvetica", 14))
        self.room_number_entry.pack(pady=(5, 0))

        tk.Label(top, text="Enter Date (YYYY-MM-DD):", font=("Helvetica", 14)).pack(pady=(10, 0))
        self.date_entry = tk.Entry(top, font=("Helvetica", 14))
        self.date_entry.pack(pady=(5, 0))

        self.submit_button = tk.Button(top, text="Submit", command=lambda: self.cancel_reservation_impl(top, int(self.room_number_entry.get()), self.date_entry.get()), font=("Helvetica", 14), bg="green", fg="white")
        self.submit_button.pack(pady=10)

    def cancel_reservation_impl(self, top, room_number, date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        result = self.hotel.cancel_reservation(room_number, date)
        if result:
            messagebox.showinfo("Success", f"Reservation cancelled successfully!")
            top.destroy()
        else:
            messagebox.showerror("Error", "No reservation found for this room and date.")

    def list_reservations(self):
        top = tk.Toplevel()
        top.title("List Reservations")

        reservations_list = tk.Listbox(top, font=("Helvetica", 14))
        reservations_list.pack(fill=tk.BOTH, expand=True)

        for reservation in self.hotel.get_reservations():
            room_number = reservation['room_number']
            date_str = reservation['date'].strftime("%Y-%m-%d")
            reservations_list.insert(tk.END, f"{room_number} - {date_str}")

        top.grab_set()

root = tk.Tk()
app = HotelReservationApp(root)
root.mainloop()
