from sqlmodel import SQLModel, Field

class Equipments(SQLModel, table = True):
    
    __tablename__ = "equipments"
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(unique=True,index=True)
    description : str



computer_lab_equipment = [
    {"name": "Desktop Computer", "description": "A stationary computer for general use."},
    {"name": "Laptop", "description": "A portable computer suitable for mobile use."},
    {"name": "Monitor", "description": "A display screen for computers."},
    {"name": "Keyboard", "description": "An input device used for typing."},
    {"name": "Mouse", "description": "A pointing device used to interact with the computer."},
    {"name": "Printer", "description": "A device that produces a hard copy of digital documents."},
    {"name": "Scanner", "description": "A device that converts physical documents into digital format."},
    {"name": "Projector", "description": "A device that projects images or videos onto a screen."},
    {"name": "Router", "description": "A networking device that forwards data packets between computer networks."},
    {"name": "Switch", "description": "A networking device that connects devices together on a computer network."},
    {"name": "Server", "description": "A computer or system that provides resources, data, or services to other computers."},
    {"name": "Headphones", "description": "A pair of small speakers worn on or around the head over the ears."},
    {"name": "Webcam", "description": "A video camera that feeds or streams images in real time to a computer."},
    {"name": "USB Flash Drive", "description": "A portable storage device that uses flash memory."},
    {"name": "Graphics Tablet", "description": "An input device that allows hand-drawing images or graphics."},
    {"name": "Speakers", "description": "Output devices that produce sound from the computer."},
    {"name": "Microphone", "description": "An input device that captures audio."}
]