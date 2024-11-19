from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont

# Declare department choices as a constant
DEPARTMENT_CHOICES = [
    ('Ushering', 'Ushering'), ('Sanctuary', 'Sanctuary'),
    ('Spirit and Truth', 'Spirit and Truth'), ('Technical', 'Technical'),
    ('Light and Power', 'Light and Power'), ('Labour Room', 'Labour Room'),
    ('New Wine Media', 'New Wine Media'), ('Decoration', 'Decoration'),
    ('Welfare', 'Welfare'), ('Pastoral Care', 'Pastoral Care')
]

class Worker(models.Model):
    worker_id = models.CharField(max_length=4, unique=True, blank=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default='')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='New Wine Media')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.department}"

    def save(self, *args, **kwargs):
        # Generate worker ID if not already set
        if not self.worker_id:
            self.worker_id = f'{Worker.objects.count() + 1:04}'  # Example logic for ID generation

        # Generate QR code if not already set
        if not self.qr_code:
            qr_content = f'{self.first_name} {self.last_name} - {self.department}'
            qr_img = qrcode.make(qr_content)
            qr_io = BytesIO()
            qr_img.save(qr_io, 'PNG')
            qr_io.seek(0)
            self.qr_code.save(f'{self.first_name}_{self.last_name}_qr.png', File(qr_io), save=False)

        super().save(*args, **kwargs)

class WorkerCard(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, unique=True)  # Unique card number
    card_image = models.ImageField(upload_to='worker_cards/', blank=True, null=True)  # Image of the card

    def __str__(self):
        return f"Card for {self.worker.first_name} {self.worker.last_name} - {self.card_number}"

    def generate_card_image(self):
        # This function will generate a card image (profile pic, name, QR code, etc.)
        card_width, card_height = 600, 400
        card_image = Image.new('RGB', (card_width, card_height), color=(0, 0, 0))

        # Load a font for text (make sure to have the font in the right path)
        font = ImageFont.load_default()

        # Draw on the image
        draw = ImageDraw.Draw(card_image)

        # Add worker's name to the card
        draw.text((20, 20), f"Name: {self.worker.first_name} {self.worker.last_name}", fill=(255, 255, 255), font=font)

        # Add department to the card
        draw.text((20, 60), f"Department: {self.worker.department}", fill=(255, 255, 255), font=font)

        # Add the QR code image to the card
        if self.worker.qr_code:
            qr_code = Image.open(self.worker.qr_code.path)
            qr_code = qr_code.resize((100, 100))  # Resize QR code for fitting into the card
            card_image.paste(qr_code, (20, 100))

        # Optionally, add the profile picture
        if self.worker.profile_picture:
            profile_picture = Image.open(self.worker.profile_picture.path)
            profile_picture = profile_picture.resize((100, 100))  # Resize profile picture
            card_image.paste(profile_picture, (400, 100))

        # Save the generated image to a file-like object
        card_io = BytesIO()
        card_image.save(card_io, 'PNG')
        card_io.seek(0)

        # Save the image file to the model
        self.card_image.save(f"{self.worker.worker_id}_card.png", File(card_io), save=False)
        self.save()

    def save(self, *args, **kwargs):
        # Automatically generate a card number if not set
        if not self.card_number:
            self.card_number = f'CARD{self.worker.worker_id}'  # Example logic for card number

        # Generate the card image if not already set
        if not self.card_image:
            self.generate_card_image()

        super().save(*args, **kwargs)

class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)  # Use lowercase for field names
    scanned_at = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.worker.first_name} {self.worker.last_name} - {self.event_name} ({self.scanned_at})"
