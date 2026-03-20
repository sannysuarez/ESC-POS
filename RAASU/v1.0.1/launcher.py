import os

# Force Kivy to use ANGLE (DirectX instead of OpenGL)
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
os.environ["KIVY_NO_ARGS"] = "1"

# Run the main program
import main
