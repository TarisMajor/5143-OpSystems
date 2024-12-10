import keyboard
import time

# This function will be called to display the key pressed
def on_key_event(event):
    # Only react to keydown events (key press), not keyup events
    if event.event_type == keyboard.KEY_DOWN:
        print(f"Key pressed: {event.name}")

def main():
    print("Press any key to trigger on_key_event. Press 'esc' to stop the program.")
    
    # Start listening for key events
    keyboard.hook(on_key_event)

    # While loop that runs the program until 'esc' is pressed
    running = True
    while running:
        print("Top")

        # Check for the 'esc' key to stop the loop
        if keyboard.is_pressed('esc'):
            running = False
            print("Exiting the loop.")
        
        time.sleep(0.1)  # Slow down the loop to make it readable and prevent CPU overload

if __name__ == "__main__":
    main()
